import network
import time
import math
from machine import Pin, ADC
from umqtt.simple import MQTTClient

print("Iniciando sistema...")

mic = ADC(Pin(34))
mic.atten(ADC.ATTN_11DB)

led_verde = Pin(13, Pin.OUT)
led_amarillo = Pin(12, Pin.OUT)
led_rojo = Pin(14, Pin.OUT)
buzzer = Pin(27, Pin.OUT)

UMBRAL_ADVERTENCIA = 15000
UMBRAL_CLIPPING = 25000
MUESTRAS_RMS = 100

print("Conectando al WiFi simulado...")
red = network.WLAN(network.STA_IF)
red.active(True)
red.connect('Wokwi-GUEST', '')

while not red.isconnected():
    time.sleep(0.1)
print("¡WiFi Conectado!")

print("Conectando al servidor MQTT...")
cliente = MQTTClient("esp32_sim_audio", "broker.hivemq.com")
cliente.connect()
print("¡MQTT Conectado! Empezando a leer el micrófono...")


def calcular_rms():
    suma_cuadrados = 0
    offset_dc = 32768

    for _ in range(MUESTRAS_RMS):
        lectura = mic.read_u16()
        onda_pura = lectura - offset_dc
        suma_cuadrados += (onda_pura * onda_pura)

    media = suma_cuadrados / MUESTRAS_RMS
    return math.sqrt(media)


def actualizar_estado(valor_rms):
    if valor_rms >= UMBRAL_CLIPPING:
        led_verde.value(0)
        led_amarillo.value(0)
        led_rojo.value(1)
        buzzer.value(1)
    elif valor_rms >= UMBRAL_ADVERTENCIA:
        led_verde.value(0)
        led_amarillo.value(1)
        led_rojo.value(0)
        buzzer.value(0)
    else:
        led_verde.value(1)
        led_amarillo.value(0)
        led_rojo.value(0)
        buzzer.value(0)


while True:
    nivel_rms = calcular_rms()
    actualizar_estado(nivel_rms)

    print(f"RMS: {int(nivel_rms)} - Enviando a Python...")

    cliente.publish("estudio/monitor/gain", str(nivel_rms))

    time.sleep(0.1)