import re


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


def process_command(command, lamps):
    for lamp in lamps:
        if re.search(".*on.*", command):
            turn_on_lamp(lamp)
        elif re.search(".*off.*", command):
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
