from common_functions import *
from VirtualCopernicusNG import TkCircuit
from gpiozero import LED, Button

# set udp controller

set_receiver_settings()

# initialize the circuit

circuit = TkCircuit(set_copernicus_settings("Living room"))


@circuit.run
def main():
    led = LED(21)
    lamps = [["Livin room lamp", "lamp", 1, False, led]]

    def switch_living_room_lamp():
        change_lamp_state(lamps[0])

    def switch_kitchen_lamp():
        line = "f1;kitchen;lamp;1;change"
        sock.sendto(line.encode('utf-8'), (MCAST_GRP, MCAST_PORT))

    button1 = Button(11)
    button1.when_pressed = switch_living_room_lamp

    button2 = Button(12)
    button2.when_pressed = switch_kitchen_lamp

    while True:
        command = sock.recv(10240)
        command = command.decode("utf-8")
        if perform_command(command.split(';'), "f1", "living_room"):
            process_command(command.split(';'), lamps)
