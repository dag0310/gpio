#!/usr/bin/python3

import configparser
import os
from time import sleep
import requests
import RPi.GPIO as GPIO
import display_74hc595

def main():
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

    CO2_CONFIG_FILEPATH = config['general']['CO2_CONFIG_FILEPATH']
    GPIO_BUTTON_RED = int(config['buttons']['GPIO_BUTTON_RED'])
    GPIO_BUTTON_DOWN = int(config['buttons']['GPIO_BUTTON_DOWN'])
    GPIO_BUTTON_UP = int(config['buttons']['GPIO_BUTTON_UP'])
    API_URL = config['buttons']['API_URL']
    DISPLAY_CO2_SECONDS = int(config['buttons']['DISPLAY_CO2_SECONDS'])
    DISPLAY_TIME_SECONDS = int(config['buttons']['DISPLAY_TIME_SECONDS'])

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(GPIO_BUTTON_RED, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(GPIO_BUTTON_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(GPIO_BUTTON_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    co2_config = configparser.ConfigParser()
    co2_config.read(CO2_CONFIG_FILEPATH)
    co2_filepath = co2_config['co2']['co2_filepath']

    try:
        print("Receiving button state ...")
        while True:
            try:
                if GPIO.input(GPIO_BUTTON_RED) == GPIO.LOW:
                    print("\nButton RED pressed.")
                    try:
                        with open(co2_filepath, 'r') as reader:
                            co2 = int(reader.read())
                            display_74hc595.display_integer(co2, DISPLAY_CO2_SECONDS)
                    except Exception:
                        display_74hc595.display_invalid(DISPLAY_CO2_SECONDS)
                    display_74hc595.display_time(DISPLAY_TIME_SECONDS, "%H.%M")
                    display_74hc595.display_time(DISPLAY_TIME_SECONDS, "%S")
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
