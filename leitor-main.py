# Professor Cristiano Teixeira
# Mudanças do Original Sob Licença Apache 2.0
# Baseado no original de Copyright (C) 2022, Uri Shaked
# https://wokwi.com/arduino/projects/315787266233467457


'''
Este projeto trabalha em conjunto com outro
MicroPython MQTT ESP32 Publicador [Prof.Cristiano]
Em:
https://wokwi.com/projects/431601399598404609
Os dois tem que estar executando ao mesmo tempo.

Para testar isolado sem o outro projeto
Abra o site:
1. http://www.hivemq.com/demos/websocket-client/
2. Click em "Connect"
3. No campo Publish, deixe o Topic como "wokwi77"
4. Escreva alguma mensagem, por exemplo: {"Mensagem" : "Oi"} 
5. click em "Publish"
'''

import network
import ujson
from machine import Pin
from time import sleep
from umqtt.simple import MQTTClient

from machine import Pin, SoftI2C
import machine
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

''' Declaro informações o I2C'''
I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)
lcd.move_to(0,0)
lcd.putstr("Ligando...")
sleep(0.5)
lcd.clear()

def mqtt_message(topic, msg):
  print("Recebendo mensagem:", msg)
  
  lcd.clear()
  try:
    msg = ujson.loads(msg)
    lcd.move_to(0,0)
    lcd.putstr(str(msg))
  except Exception as e:
    print("Erro:", e)

def conectando_wifi():
    print("Conectando no WiFi...", end="")
    import network
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect("Wokwi-GUEST", "")
    while not wifi.isconnected():
        sleep(0.5)
        print(".", end="")
    print("Concectado no Wi-Fi com Sucesso!")

def conectando_mqtt():
    print("Conectando no MQTT...")
    client = MQTTClient("wokwi1", "broker.hivemq.com")
    client.set_callback(mqtt_message)
    client.connect()
    client.subscribe("wokwi77")
    print("Conectado no MQTT com Sucesso!")
    return client

conectando_wifi()
client = conectando_mqtt()

while True:
    #acrescentado um try... except pois dava muito erro de conexão com o MQTT na versão física
    try:
        client.wait_msg()
    except OSError as e:
        print("Erro de conexão, tentando reconectar...")
        client = conectando_mqtt()
