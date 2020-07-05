#!/usr/bin/python
from time import sleep, strftime, time
import pi_pact
import board
import busio
import adafruit_bme280
import statistics

scanner = pi_pact.Scanner_Blank(control_file_name="scanner_control")

print(scanner.return_RSSI())