#!/usr/bin/python
from time import sleep, strftime, time
from csv import writer
import pi_pact
# import board
import dht
import bmp
import statistics

# Initial the dht device, with data pin connected to:
# hSensor = dht.DHT11(board.D18)
# pSensor = bmp.BMP085()
scanner = pi_pact.Scanner_Blank(control_file_name="scanner_control")

rssiList = list()
# humidityList = list()
# temperatureList = list()
# pressureList = list()

def write_data(data_list):
    # with open("/home/pi/Documents/log.csv", "a+" newline='') as log:
    with open("/home/aud2pact/piPACT/pact_scans/log.csv", "a+", newline='') as log:
        csv_writer = writer(log)
        csv_writer.writerow(data_list)
        # log.write("{0},{1},{2},{3}\n".format(strftime("%Y-%m-%d %H:%M:%S"), str(val1), str(val2), str(val3)))

while True:
    for i in range(10):
        rssiList.append(scanner.return_RSSI())
        # humidityList.append(hSensor.humidity())
        # temperatureList.append(pSensor.read_temperature())
        # pressureList.append(pSensor.read_pressure())
        print(rssiList)
        # print(humidityList)
        # print(temperatureList)
        # print(pressureList)
        print()
        sleep(2.0)
    # rssi = statistics.mean(rssiList)
    # humidity = statistics.mean(humidityList)
    # temperature = statistics.mean(temperatureList)
    # pressure = statistics.mean(pressureList)

    data_list = list()
    data_list.append(statistics.mean(rssiList))
    # data_list.append(statistics.mean(humidityList))
    # data_list.append(statistics.mean(temperatureList))
    # data_list.append(statistics.mean(pressureList))

    write_data(data_list)

    rssiList.clear()
    # humidityList.clear()
    # temperatureList.clear()
    # pressureList.clear()

    sleep(30.0)
