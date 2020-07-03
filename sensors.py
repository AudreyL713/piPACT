#!/usr/bin/python
from time import sleep, strftime, time
import pi_pact
import board
import dht
import bmp
import statistics

# Initial the dht device, with data pin connected to:
hSensor = dht.DHT11(board.D18)
pSensor = bmp.BMP085()
scanner = pi_pact.Scanner

humidityList = list()
temperatureList = list()
pressureList = list()

def write_data(val1, val2, val3):
    with open("/home/pi/Documents/log.csv", "a") as log:
        log.write("{0},{1},{2},{3}\n".format(strftime("%Y-%m-%d %H:%M:%S"), str(val1), str(val2), str(val3)))

while True:
    for i in range(10):
        humidityList.append(hSensor.humidity())
        temperatureList.append(pSensor.read_temperature())
        pressureList.append(pSensor.read_pressure())
        print(temperatureList)
        print(humidityList)
        print(pressureList)
        print()
        sleep(2.0)
    humidity = statistics.mean(humidityList)
    temperature = statistics.mean(temperatureList)
    pressure = statistics.mean(pressureList)

    write_data(temperature, humidity, pressure)

    humidityList.clear()
    temperatureList.clear()
    pressureList.clear()

    sleep(30.0)
