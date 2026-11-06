from machine import Pin, ADC
import time
import math

mic = ADC(Pin(34))
mic.atten(ADC.ATTN_11DB)

led_verde = Pin(13, Pin.OUT)
led_amarillo = Pin(12, Pin.OUT)
led_rojo = Pin(14, Pin.OUT)
buzzer = Pin(27, Pin.OUT)

UMBRAL_ADVERTENCIA = 15000
UMBRAL_CLIPPING = 25000
MUESTRAS_RMS = 100


def calcular_rms():
    suma_cuadrados = 0
    offset_dc = 32768

    for _ in range(MUESTRAS_RMS):
        lectura = mic.read_u16()
        onda_pura = lectura - offset_dc
        suma_cuadrados += (onda_pura * onda_pura)

    media = suma_cuadrados / MUESTRAS_RMS
    return math.sqrt(media)