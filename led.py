#!/usr/bin/python3

import configparser
import os
from time import sleep, time
import RPi.GPIO as GPIO

GPIO_LED = None
led_is_on = False

def set_led_status(_led_is_on):
    global led_is_on
    global GPIO_LED
    if _led_is_on == led_is_on:
        return
    led_is_on = _led_is_on
    if led_is_on:
        print('LED on ...')
        GPIO.output(GPIO_LED, GPIO.HIGH)
    else:
        print('LED off ...')
        GPIO.output(GPIO_LED, GPIO.LOW)

def flash_led():
    set_led_status(True)
    sleep(0.3)
    set_led_status(False)
    sleep(0.3)

def main():
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

    CO2_CONFIG_FILEPATH = config['general']['CO2_CONFIG_FILEPATH']
    global GPIO_LED
    GPIO_LED = int(config['led']['GPIO_LED'])
    POLL_SECONDS = int(config['led']['POLL_SECONDS'])
    THRESHOLD_ON_PPM_CO2 = int(config['led']['THRESHOLD_ON_PPM_CO2'])
    THRESHOLD_OFF_PPM_CO2 = int(config['led']['THRESHOLD_OFF_PPM_CO2'])
    ERROR_FEEDBACK_AFTER_X_MINUTES = int(config['led']['ERROR_FEEDBACK_AFTER_X_MINUTES'])

    script_start_timestamp = time()

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(GPIO_LED, GPIO.OUT)

    GPIO.output(GPIO_LED, GPIO.LOW)

    co2_config = configparser.ConfigParser()
    co2_config.read(CO2_CONFIG_FILEPATH)
    co2_filepath = co2_config['co2']['co2_filepath']

    try:
        print(f"Polling interval: {POLL_SECONDS}s")
        print(f"CO2 threshold until LED ON: {THRESHOLD_ON_PPM_CO2} ppm")
        print(f"CO2 threshold until LED OFF: {THRESHOLD_OFF_PPM_CO2} ppm")
        print(f"CO2 filepath: {co2_filepath}")
        while True:
            try:
                with open(co2_filepath, 'r') as reader:
                    co2 = int(reader.read())
                    # print(f"CO2: {co2} ppm")
                    if co2 < THRESHOLD_OFF_PPM_CO2:
                        set_led_status(False)
                    elif co2 >= THRESHOLD_ON_PPM_CO2:
                        set_led_status(True)
            except Exception as e:
                print(e)
                set_led_status(False)
                show_error_feedback = (time() - script_start_timestamp) > (ERROR_FEEDBACK_AFTER_X_MINUTES * 60)
                print(f"Show error feedback: {show_error_feedback}")
                if show_error_feedback:
                    sleep(0.1)
                    flash_led()
                    flash_led()
                    flash_led()

            sleep(POLL_SECONDS)
    except KeyboardInterrupt:
        print("\nScript stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
