#!/usr/bin/python
from time import sleep, strftime, time
import pi_pact
import board
import busio
import adafruit_bme280
import statistics

i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
bme280.sea_level_pressure = 1012.8689
bme280.mode = adafruit_bme280.MODE_NORMAL
bme280.standby_period = adafruit_bme280.STANDBY_TC_500
bme280.iir_filter = adafruit_bme280.IIR_FILTER_X16
bme280.overscan_pressure = adafruit_bme280.OVERSCAN_X16
bme280.overscan_humidity = adafruit_bme280.OVERSCAN_X1
bme280.overscan_temperature = adafruit_bme280.OVERSCAN_X2

sleep(1)

# scanner = pi_pact.Scanner_Blank(control_file_name="scanner_control")

while(True):
    temps = list()
    hums = list()
    pres = list()
    for i in range(20):
        temps.append(bme280.temperature)
        hums.append(bme280.humidity)
        pres.append(bme280.pressure)
    
    avg_temps = sum(temps) / len(temps)
    avg_hums = sum(hums) / len(hums)
    avg_pres = sum(pres) / len(pres)

    print("Temperature: " + str(avg_temps))
    print("Humidity: " + str(avg_hums))
    print("Pressure: " + str(avg_pres))
