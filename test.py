#!/usr/bin/python
from time import sleep, strftime, time
import pi_pact
import board
import busio
import adafruit_bme280
import statistics

i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# scanner = pi_pact.Scanner_Blank(control_file_name="scanner_control")

print(bme280.temperature)