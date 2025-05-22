# ESP32-MQTT-Publicador-Leitor
Este projeto via demonstrar a utilização do ESP32 se comunicando com um MQTT aberto e de fácil utilização. Tanto agindo como Publicador, como Leitor. 

Apesar de fazerem referência ao simulador do Wokwi esse projeto, funciona em dispositivos reais desde que sejam mudados os parâmetros de conecção para uma rede Wi-Fi que tenha acesso a internet.


# Notas da versão Publicador

Baseado no original de: Copyright (C) 2022, Uri Shaked

https://wokwi.com/arduino/projects/322577683855704658

Mudanças do original Sob Licença Apache 2.0

Este projeto trabalha em conjunto com outro
MicroPython MQTT ESP32 Leitor [Prof.Cristiano]
Em:
# https://wokwi.com/projects/431601424527252481

Os dois tem que estar executando ao mesmo tempo.

Para visualizar os dados sem o outro projeto:
1. Vá para http://www.hivemq.com/demos/websocket-client/
2. Clique em "Connect"
3. Em "Subscriptions", clique em "Add New Topic Subscription"
4. No campo Tópico, digite "wokiwi77" e clique em "Subscribe"
Agora clique no sensor HC-SR04 na simulação,
altere a distância e você verá
a mensagem aparece no MQTT Broker, no painel "Mensagens".


# Notas da Versão Leitor

Baseado no original de Copyright (C) 2022, Uri Shaked

https://wokwi.com/arduino/projects/315787266233467457

Mudanças do original Sob Licença Apache 2.0

Este projeto trabalha em conjunto com outro
MicroPython MQTT ESP32 Publicador [Prof.Cristiano]
Em:
# https://wokwi.com/projects/431601399598404609
Os dois tem que estar executando ao mesmo tempo.

Para testar isolado sem o outro projeto
Abra o site:
1. http://www.hivemq.com/demos/websocket-client/
2. Click em "Connect"
3. No campo Publish, deixe o Topic como "wokwi77"
4. Escreva alguma mensagem, por exemplo: {"Mensagem" : "Oi"} 
5. click em "Publish"

OBS: A versão do Leitor para trabalhar com o i2c LCD precisará também dos arquivos "i2c_lcd.py" e lcd_api.py"
