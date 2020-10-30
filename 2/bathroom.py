from common_functions import *
from VirtualCopernicusNG import TkCircuit
from gpiozero import LED, Button

# set udp controller

set_receiver_settings()

# initialize the circuit

circuit = TkCircuit(set_copernicus_settings("Bathroom"))


@circuit.run
def main():
    led1 = LED(21)
    led2 = LED(22)
    lamps = [["Bathroom main lamp", "lamp", 1, False, led1],
             ["Bathroom mirror lamp", "lamp", 2, False, led2]]

    def switch_bathroom_lamp():
        change_lamp_state(lamps[0])

    def switch_bathroom_mirror_lamp():
        change_lamp_state(lamps[1])

    button1 = Button(11)
    button1.when_pressed = switch_bathroom_lamp

    button2 = Button(12)
    button2.when_pressed = switch_bathroom_mirror_lamp

    while True:
        command = sock.recv(10240)
        command = command.decode("utf-8")
        if perform_command(command.split(';'), "f1", "bathroom"):
            process_command(command.split(';'), lamps)
