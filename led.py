#!/usr/bin/python3

from time import sleep, time
import RPi.GPIO as GPIO

CO2_FILEPATH = '/ram-dir/co2.txt'
GPIO_LED = 10
POLL_SECONDS = 5
CO2_THRESHOLD_PPM = 800
ERROR_FEEDBACK_AFTER_X_MINUTES = 60

led_is_on = False

def set_led_status(_led_is_on):
    global led_is_on
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
    script_start_timestamp = time()

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(GPIO_LED, GPIO.OUT)

    GPIO.output(GPIO_LED, GPIO.LOW)

    try:
        print(f"Polling interval: {POLL_SECONDS}s")
        print(f"CO2 threshold until LED lights up: {CO2_THRESHOLD_PPM} ppm")
        print(f"CO2 filepath: {CO2_FILEPATH}")
        while True:
            try:
                with open(CO2_FILEPATH, 'r') as reader:
                    co2 = int(reader.read())
                    # print(f"CO2: {co2} ppm")
                    set_led_status(co2 >= CO2_THRESHOLD_PPM)
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
