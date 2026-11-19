import paho.mqtt.client as mqtt

class ControladorMQTT:
    def __init__(self, topic, callback):
        self.topic = topic
        self.callback = callback
        self.cliente = mqtt.Client()
        self.cliente.on_connect = self.al_conectar
        self.cliente.on_message = self.al_recibir

    def iniciar(self):
        self.cliente.connect("broker.hivemq.com", 1883, 60)
        self.cliente.loop_start()

    def al_conectar(self, client, userdata, flags, rc):
        client.subscribe(self.topic)

    def al_recibir(self, client, userdata, msg):
        try:
            valor = float(msg.payload.decode())
            self.callback(valor)
        except ValueError:
            pass