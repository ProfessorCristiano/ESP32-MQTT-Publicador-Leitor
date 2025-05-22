# Professor Cristiano Teixeira
# Mudanças do original Sob Licença Apache 2.0
# Baseado no original de: Copyright (C) 2022, Uri Shaked
# https://wokwi.com/arduino/projects/322577683855704658

'''
Este projeto trabalha em conjunto com outro
MicroPython MQTT ESP32 Leitor [Prof.Cristiano]
Em:
https://wokwi.com/projects/431601424527252481

Os dois tem que estar executando ao mesmo tempo.

Para visualizar os dados sem o outro projeto:
1. Vá para http://www.hivemq.com/demos/websocket-client/
2. Clique em "Connect"
3. Em "Subscriptions", clique em "Add New Topic Subscription"
4. No campo Tópico, digite "wokiwi77" e clique em "Subscribe"
Agora clique no sensor HC-SR04 na simulação,
altere a distância e você verá
a mensagem aparece no MQTT Broker, no painel "Mensagens".
'''

import network
import machine
import time
from machine import Pin
import ujson
from umqtt.simple import MQTTClient
frequency = 5000

#Função que calcula a distância com ultrassom
def distancia():
    echo_timeout = echo_timeout=500*2*30
    trigger = Pin(02, Pin.OUT, pull=None)
    echo = Pin(04, Pin.IN, pull=None)
    trigger.value(0) 
    # Aguarda 5 milisegundos.
    time.sleep_us(5)
    trigger.value(1)
    # Aguarda 10 milisegundos.
    time.sleep_us(10)
    trigger.value(0)
    try:
        pulse_time = machine.time_pulse_us(echo, 1, echo_timeout)
    except OSError as ex:
        if ex.args[0] == 110: # 110 = ETIMEDOUT
            raise OSError('Fora de Alcance')
        raise ex  
  
    cms = (pulse_time / 2) / 29.1
    print ("Distância: ",cms, "cms")
    return cms

#As Instruções abaixo são somente para conectar a internet no wokwi. Remova esssas linhas no projeto físico
def conectando_wifi():
    print("Conectando no WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('Wokwi-GUEST', '')
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.1)
    print(" Conectado no Wi-Fi com Sucesso!")
#Fim da conexão Wi-fi do wokwi

# Chamamos a conexão
conectando_wifi()

# MQTT Server Parameters
MQTT_CLIENT_ID = "micropython-weather-demo"
MQTT_BROKER    = "broker.mqttdashboard.com"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = "wokwi77"

def conectando_mqtt():
    print("Conectando no MQTT server... ", end="")
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
    client.connect()
    print("Conectado no MQTT com sucesso!")
    return client

# fazemos a conexão inicial no MQTT
client = conectando_mqtt()

distancia_anterior = 0
while True:
    #acrescentado um try... except pois dava muito erro de conexão com o MQTT na versão física
    try:
        print("Medindo distância... ", end="")
        distancia_atual= distancia() 
        message = ujson.dumps({
            "Distancia:": str(distancia_atual),
        })
        if distancia_atual != distancia_anterior:
            print("Atualizando Informações")
            print("Publicando no Tópico do MQTT {}: {}".format(MQTT_TOPIC, message))
            client.publish(MQTT_TOPIC, message)
            distancia_anterior = distancia_atual
        else:
            print("Sem Mudaças")
        time.sleep(5)
    except OSError as e:
        print("Erro de conexão, tentando reconectar...")
        client = conectando_mqtt()
  
