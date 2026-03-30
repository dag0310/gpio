#!/usr/bin/python3

from time import sleep
import requests
import RPi.GPIO as GPIO
import display_74hc595

GPIO_BUTTON_RED = 2
GPIO_BUTTON_DOWN = 3
GPIO_BUTTON_UP = 4
API_URL = 'http://localhost:3000/udp?command='
CO2_FILEPATH = '/ram-dir/co2.txt'
DISPLAY_CO2_SECONDS = 1
DISPLAY_TIME_SECONDS = 1

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(GPIO_BUTTON_RED, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(GPIO_BUTTON_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(GPIO_BUTTON_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    try:
        print("Receiving button state ...")
        while True:
            try:
                if GPIO.input(GPIO_BUTTON_RED) == GPIO.LOW:
                    print("\nButton RED pressed.")
                    try:
                        with open(CO2_FILEPATH, 'r') as reader:
                            co2 = int(reader.read())
                            display_74hc595.display_integer(co2, DISPLAY_CO2_SECONDS)
                    except Exception:
                        display_74hc595.display_invalid(DISPLAY_CO2_SECONDS)
                    display_74hc595.display_time(DISPLAY_TIME_SECONDS)
                if GPIO.input(GPIO_BUTTON_UP) == GPIO.LOW:
                    print("\nButton UP pressed.")
                    requests.post(f"{API_URL}shutters_up")
                    sleep(1)
                if GPIO.input(GPIO_BUTTON_DOWN) == GPIO.LOW:
                    print("\nButton DOWN pressed.")
                    requests.post(f"{API_URL}shutters_down")
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
