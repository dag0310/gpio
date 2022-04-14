#!/usr/bin/python3

import time
import requests
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO_BUTTON_UP = 2
GPIO_BUTTON_DOWN = 3

GPIO.setup(GPIO_BUTTON_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(GPIO_BUTTON_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

API_URL = 'http://retropie:3000/udp?command='

try:
    print("Receiving button state ...\n")
    while True:
        if GPIO.input(GPIO_BUTTON_UP) == GPIO.LOW:
            requests.post(f"{API_URL}shutters_up")
            print("Button UP pressed.")
            time.sleep(1)
        if GPIO.input(GPIO_BUTTON_DOWN) == GPIO.LOW:
            requests.post(f"{API_URL}shutters_down")
            print("Button DOWN pressed.")
            time.sleep(1)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\Script stopped by user.")
    GPIO.cleanup()
