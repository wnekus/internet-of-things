import time
import paho.mqtt.client as mqtt


def main():
    def on_connect(client, userdata, flags, rc):
        mqttc.subscribe("kamils_home/server")

    def on_message(client, userdata, msg):
        print(str(msg.payload))

    mqttc = mqtt.Client("kamils_home_server")
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect

    mqttc.connect("test.mosquitto.org", 1883, 60)

    mqttc.loop_forever()


main()