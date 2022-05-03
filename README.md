## Development

- `sudo apt update`
- `sudo apt install python3-pip`
- `pip3 install RPi.GPIO`
- `chmod +x gpio.py`
- `./gpio.py`

## Auto-start the script on startup

[Five Ways To Run a Program On Your Raspberry Pi At Startup](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/)

/etc/rc.local:
```
sudo python3 /var/www/gpio/gpio.py &

exit 0
```