#!/usr/bin/python
from time import sleep, strftime, time
import pi_pact
import board
import dht
import bmp
import statistics

scanner = pi_pact.Scanner_Blank(control_file="scanner_control")

print(scanner.return_RSSI())