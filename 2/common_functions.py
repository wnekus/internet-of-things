import socket
import struct

MCAST_GRP = '236.0.0.0'
MCAST_PORT = 3456
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)


def set_receiver_settings():
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


def set_controller_settings():
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)


def set_copernicus_settings(room):
    return {
        "name": room + " - SmartHouse",
        "sheet": "sheet_smarthouse.png",
        "width": 332,
        "height": 300,
        "leds": [
            {"x": 112, "y": 70, "name": "LED 1", "pin": 21},
            {"x": 71, "y": 141, "name": "LED 2", "pin": 22}
        ],
        "buttons": [
            {"x": 242, "y": 146, "name": "Button 1", "pin": 11},
            {"x": 200, "y": 217, "name": "Button 2", "pin": 12},
        ],
        "buzzers": [
            {"x": 277, "y": 9, "name": "Buzzer", "pin": 16, "frequency": 440},
        ]
    }


def perform_command(command, floor, room):
    if command[0] == floor or command[0] == "*":
        if command[1] == room or command[1] == "*":
            return True
    return False


def process_command(command, lamps):
    for lamp in lamps:
        if (command[2] == lamp[1] or command[2] == "*") and (command[3] == "*" or int(command[3]) == lamp[2]):
            if command[4] == "on":
                turn_on_lamp(lamp)
            elif command[4] == "off":
                turn_off_lamp(lamp)
            else:
                change_lamp_state(lamp)


def change_lamp_state(lamp):
    if lamp[3]:
        print(lamp[0] + " turn off!")
        lamp[3] = not lamp[3]
    else:
        print(lamp[0] + " turn on!")
        lamp[3] = not lamp[3]
    lamp[4].toggle()


def turn_on_lamp(lamp):
    if not lamp[3]:
        print(lamp[0] + " turn on!")
        lamp[3] = not lamp[3]
        lamp[4].toggle()
    else:
        return


def turn_off_lamp(lamp):
    if lamp[3]:
        print(lamp[0] + " turn off!")
        lamp[3] = not lamp[3]
        lamp[4].toggle()
    else:
        return
