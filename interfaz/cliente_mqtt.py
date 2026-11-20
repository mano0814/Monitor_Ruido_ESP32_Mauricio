import paho.mqtt.client as mqtt

class ControladorMQTT:
    def __init__(self, topico_suscripcion, callback_recepcion):
        self.broker = "broker.hivemq.com"
        self.topico_suscripcion = topico_suscripcion
        self.callback_recepcion = callback_recepcion
        self.cliente = mqtt.Client()
        self.cliente.on_connect = self.al_conectar
        self.cliente.on_message = self.al_recibir

    def al_conectar(self, client, userdata, flags, rc):
        print("Conectado a MQTT. Escuchando lecturas...")
        self.cliente.subscribe(self.topico_suscripcion)

    def al_recibir(self, client, userdata, msg):
        try:
            valor = float(msg.payload.decode())
            self.callback_recepcion(valor)
        except ValueError:
            pass

    def iniciar(self):
        self.cliente.connect(self.broker, 1883, 60)
        self.cliente.loop_start()

    def publicar(self, topico, mensaje):
        self.cliente.publish(topico, mensaje)