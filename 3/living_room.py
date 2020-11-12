from common_functions import *
from VirtualCopernicusNG import TkCircuit
from gpiozero import LED, Button
import paho.mqtt.client as mqtt

# initialize the circuit

circuit = TkCircuit(set_copernicus_settings("Living room"))


@circuit.run
def main():
    led = LED(21)
    lamps = [["Livin room lamp", "lamp", 1, False, led]]

    def switch_living_room_lamp():
        change_lamp_state(lamps[0])

    def switch_zone1():
        mqttc.publish("kamils_home/zone1", "off", 0, False)

    button1 = Button(11)
    button1.when_pressed = switch_living_room_lamp

    button2 = Button(12)
    button2.when_pressed = switch_zone1

    def on_connect(client, userdata, flags, rc):
        mqttc.subscribe("kamils_home/zone1")
        mqttc.subscribe("kamils_home/zone2")
        mqttc.publish("kamils_home/server", "Living room connected!", 0, False)

    def on_message(client, userdata, msg):
        process_command(str(msg.payload), lamps)

    mqttc = mqtt.Client("kamils_home_living_room")
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.will_set("kamils_home/server", "Living room disconnected!")

    mqttc.connect("test.mosquitto.org", 1883, 60)

    mqttc.loop_forever()