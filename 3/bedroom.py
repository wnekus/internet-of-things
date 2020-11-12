from common_functions import *
from VirtualCopernicusNG import TkCircuit
from gpiozero import LED, Button
import paho.mqtt.client as mqtt

# initialize the circuit

circuit = TkCircuit(set_copernicus_settings("Bedroom"))


@circuit.run
def main():
    led1 = LED(21)
    led2 = LED(22)
    lamps = [["Bedroom lamp 1", "lamp", 1, False, led1],
             ["Bedroom lamp 2", "lamp", 2, False, led2]]

    def switch_bedroom_lamp1():
        change_lamp_state(lamps[0])

    def switch_bedroom_lamp2():
        change_lamp_state(lamps[1])

    button1 = Button(11)
    button1.when_pressed = switch_bedroom_lamp1

    button2 = Button(12)
    button2.when_pressed = switch_bedroom_lamp2

    def on_connect(client, userdata, flags, rc):
        mqttc.subscribe("kamils_home/zone2")
        mqttc.publish("kamils_home/server", "Bedroom connected!", 0, False)

    def on_message(client, userdata, msg):
        process_command(str(msg.payload), lamps)

    mqttc = mqtt.Client("kamils_home_bedroom")
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.will_set("kamils_home/server", "Bedroom disconnected!")

    mqttc.connect("test.mosquitto.org", 1883, 60)

    mqttc.loop_forever()