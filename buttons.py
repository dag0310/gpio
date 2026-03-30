#!/usr/bin/python3

from time import sleep
import requests
import RPi.GPIO as GPIO

GPIO_BUTTON_RED = 2
GPIO_BUTTON_DOWN = 3
GPIO_BUTTON_UP = 4
API_URL = 'http://localhost:3000/udp?command='

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(GPIO_BUTTON_RED, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(GPIO_BUTTON_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(GPIO_BUTTON_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    try:
        print("Receiving button state ...\n")
        while True:
            try:
                if GPIO.input(GPIO_BUTTON_RED) == GPIO.LOW:
                    print("Button RED pressed.")
                    sleep(1)
                if GPIO.input(GPIO_BUTTON_UP) == GPIO.LOW:
                    requests.post(f"{API_URL}shutters_up")
                    print("Button UP pressed.")
                    sleep(1)
                if GPIO.input(GPIO_BUTTON_DOWN) == GPIO.LOW:
                    requests.post(f"{API_URL}shutters_down")
                    print("Button DOWN pressed.")
                    sleep(1)
            except Exception as e:
                print(f"An error occurred: {e}")
                sleep(1)
            sleep(0.1)
    except KeyboardInterrupt:
        print("\nScript stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
