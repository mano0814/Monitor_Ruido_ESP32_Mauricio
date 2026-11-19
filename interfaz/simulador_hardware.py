import paho.mqtt.client as mqtt
import time
import random
import math

cliente = mqtt.Client()
# Nos conectamos al mismo servidor público
cliente.connect("broker.hivemq.com", 1883, 60)

print("Simulador de hardware iniciado. Enviando datos MQTT...")

try:
    while True:
        # Generamos un valor RMS falso simulando que alguien habla por el micrófono
        # Oscila entre 5000 (silencio/verde) y 28000 (grito/rojo)
        valor_rms = random.uniform(5000, 28000)

        cliente.publish("estudio/monitor/gain", str(valor_rms))
        print(f"Dato enviado a Tkinter: {int(valor_rms)}")

        time.sleep(0.5)  # Envía medio segundo
except KeyboardInterrupt:
    print("Simulador detenido.")