from common_functions import *
from VirtualCopernicusNG import TkCircuit
from gpiozero import LED, Button

# set udp controller

set_controller_settings()
set_receiver_settings()

# initialize the circuit inside the

circuit = TkCircuit(set_copernicus_settings("Lobby"))

global_switch_state = False

@circuit.run
def main():
    led = LED(21)
    lamps = [["Lobby lamp", "lamp", 1, False, led]]

    def button1_pressed():
        change_lamp_state(lamps[0])

    def button2_pressed():
        global global_switch_state
        if global_switch_state:
            line = "*;*;*;*;off"
        else:
            line = "*;*;*;*;on"
        global_switch_state = not global_switch_state
        print("Lobby global switch pressed!")
        sock.sendto(line.encode('utf-8'), (MCAST_GRP, MCAST_PORT))

    button1 = Button(11)
    button1.when_pressed = button1_pressed

    button2 = Button(12)
    button2.when_pressed = button2_pressed

    while True:
        command = sock.recv(10240)
        command = command.decode("utf-8")
        if perform_command(command.split(';'), "f1", "lobby"):
            process_command(command.split(';'), lamps)
