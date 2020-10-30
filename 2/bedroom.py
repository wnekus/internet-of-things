from common_functions import *
from VirtualCopernicusNG import TkCircuit
from gpiozero import LED, Button

# set udp controller

set_receiver_settings()

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

    while True:
        command = sock.recv(10240)
        command = command.decode("utf-8")
        if perform_command(command.split(';'), "f1", "bedroom"):
            process_command(command.split(';'), lamps)