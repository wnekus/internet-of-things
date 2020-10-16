from VirtualCopernicusNG import TkCircuit
from pyowm.owm import OWM


# initialize the circuit inside the

configuration = {
    "name": "CopernicusNG Weather Forecast",
    "sheet": "sheet_forecast.png",
    "width": 343,
    "height": 267,

    "servos": [
        {"x": 170, "y": 150, "length": 90, "name": "Servo 1", "pin": 17}
    ],
    "buttons": [
        {"x": 295, "y": 200, "name": "Button 1", "pin": 11},
        {"x": 295, "y": 170, "name": "Button 2", "pin": 12},
    ]
}

circuit = TkCircuit(configuration)

cities = ["Krakow,PL", "Istanbul,TR", "Stockholm,SE"]
iterator = 0


def get_weather(city):
    owm = OWM('4526d487f12ef78b82b7a7d113faea64')
    manager = owm.weather_manager()
    weather = manager.weather_at_place(city).weather
    dictionary = weather.to_dict()

    return dictionary.get("status")


def get_angle(weather_status):
    return {
        'Rain': 50,
        'Thunderstorm': 60,
        'Drizzle': 30,
        'Snow': 55,
        'Clear': -70,
        'Clouds': -30
    }.get(weather_status, -90)


@circuit.run
def main():
    # now just write the code you would use on a real Raspberry Pi

    from time import sleep
    from gpiozero import AngularServo, Button

    servo1 = AngularServo(17, min_angle=-90, max_angle=90)

    servo1.angle = -90

    def set_city(city):
        print("Status in city: " + city)
        servo1.angle = get_angle(get_weather(city))

    def set_cracow_status():
        set_city("Krakow,PL")

    def button1_pressed():
        global iterator
        iterator = (iterator + 1) % 3
        set_city(cities[iterator])

    def button2_pressed():
        global iterator
        iterator = (iterator + 2) % 3
        set_city(cities[iterator])

    button1 = Button(11)
    button1.when_pressed = button1_pressed

    button2 = Button(12)
    button2.when_pressed = button2_pressed

    set_cracow_status()

    while True:
        sleep(0.1)
