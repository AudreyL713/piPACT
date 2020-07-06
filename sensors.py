#!/usr/bin/python3
from time import sleep, localtime, strftime, time
from csv import writer
import pi_pact
import board
import dht
import bmp
import statistics

# Initial the dht device, with data pin connected to:
hSensor = dht.DHT11(board.D18)
pSensor = bmp.BMP085()
scanner = pi_pact.Scanner_Blank(control_file_name="scanner_control")

rssiList = list()
humidityList = list()
temperatureList = list()
pressureList = list()

def write_data(data_list):
    with open("/home/pi/Documents/data.csv", "a+", newline='') as log:
    # with open("/home/aud2pact/piPACT/pact_scans/log.csv", "a+", newline='') as log:
        csv_writer = writer(log)
        csv_writer.writerow(data_list)


def log_raw(rssi_list, temp_list, humidity_list, pressure_list):
    with open("/home/pi/Documents/rssi.csv", "a+", newline='') as log:
        csv_writer = writer(log)
        csv_writer.writerow([strftime("%Y-%m-%d %H:%M:%S")] + rssi_list)

    with open("/home/pi/Documents/temp.csv", "a+", newline='') as log:
        csv_writer = writer(log)
        csv_writer.writerow([strftime("%Y-%m-%d %H:%M:%S")] + temp_list)

    with open("/home/pi/Documents/humidity.csv", "a+", newline='') as log:
        csv_writer = writer(log)
        csv_writer.writerow([strftime("%Y-%m-%d %H:%M:%S")] + humidity_list)

    with open("/home/pi/Documents/pressure.csv", "a+", newline='') as log:
        csv_writer = writer(log)
        csv_writer.writerow([strftime("%Y-%m-%d %H:%M:%S")] + pressure_list)


try :
    sleep(2.0)
    for i in range(20):
        rssiList.append(scanner.return_RSSI())
        humidityList.append(hSensor.humidity())
        temperatureList.append(pSensor.read_temperature())
        pressureList.append(pSensor.read_pressure())
        # print(rssiList)
        # print(humidityList)
        # print(temperatureList)
        # print(pressureList)
        # print()
        sleep(1.0)
except RuntimeError as error:
    print(error.args[0])
    with open("/home/pi/Documents/err.log", "a+") as log:
        log.write(error.args[0])


data_list = list()
data_list.append(strftime("%Y-%m-%d %H:%M:%S"))
data_list.append(statistics.mean(rssiList))
data_list.append(statistics.mean(humidityList))
data_list.append(statistics.mean(temperatureList))
data_list.append(statistics.mean(pressureList))
write_data(data_list)
log_raw(rssiList, temperatureList, humidityList, pressureList)
sleep(5.0)
