#!/usr/bin/env python

import bme680
import argparse
import sys

def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="reads bme688 sensor data and outputs prometheus-format metrics to file")
    parser.add_argument("-o", "--output", help="metrics output file path")
    options = parser.parse_args(args)
    return options

options = getOptions(sys.argv[1:])

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

if sensor.get_sensor_data():
    output = 'temprature_celsius {0:.2f}\npressure_hectopascals {1:.2f}\nhumidity_percent_relative_humidity {2:.3f}'.format(
        sensor.data.temperature,
        sensor.data.pressure,
        sensor.data.humidity)
    with open(options.output, "w") as text_file:
        print(output, file=text_file)
    