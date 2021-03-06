#!/usr/bin/env python3

import bme680
import time
import requests
import datetime
import csv
import sys
import os

print("STARTED BME680 Collector POST request version!")


# VARIABLES
host = 'HOSTNAME_HERE'
interval = 15
url = 'http://127.0.0.1/receiver.php'
use_csv = False

# dont touch
script_path = sys.path[0]
datafile = os.path.join(script_path, "data.csv")


# functions
def prep_sensor_data(sensor):
	sensor_data = {
		'dt': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
		'host': host,
		'temperature': '{0:.2f}'.format(sensor.data.temperature),
		'pressure': '{0:.2f}'.format(sensor.data.pressure),
		'humidity': '{0:.2f}'.format(sensor.data.humidity),
		'gas_resistance': None
	}
	if sensor.data.heat_stable:
		sensor_data['gas_resistance'] = '{0:.2f}'.format(sensor.data.gas_resistance)
	return sensor_data

def send_sensor_data(sensor_data):
	try:
		r = requests.post(url, data=sensor_data, timeout=5)
		# failed reqs AND 4xx/5xx are handled as exceptions
		r.raise_for_status()
		data_sent = 1
	except:
		data_sent = 0
	return data_sent

def send_csv_data():
	try:
		with open(datafile) as csvfile:
			r = requests.post(url, data={'csvdata': csvfile.read()})
		r.raise_for_status()
		csv_sent = 1
	except:
		csv_sent = 0

	return csv_sent



def write_to_csv(sensor_data):
	# dont write to csv if bigger than 1mb
	if os.path.isfile(datafile) and os.stat(datafile).st_size > 1048576:
		return

	with open(datafile, "a") as csvfile:
		fnames = sensor_data.keys()
		writer = csv.DictWriter(csvfile, fieldnames=fnames, delimiter=';')
		writer.writerow(sensor_data)


# beginning of script
print('URL: {}, Host: {}, interval: {}, use_csv: {}'.format(url, host, interval, use_csv))
try:
	sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
	sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

try:
	while True:
		if sensor.get_sensor_data():
			sensor_data = prep_sensor_data(sensor)
			data_sent = send_sensor_data(sensor_data)

			#only check and write to csv if functionality is enabled!
			if use_csv:
				if data_sent:
					print("it sent! trying to send csv if exists")
					csv_sent = send_csv_data()
					if csv_sent:
						print('csv sent! deleting csv')
						os.remove(datafile)
					else:
						print('did not send csv!')
				else:
					print("data not sent! writing to csv")
					write_to_csv(sensor_data)

		time.sleep(interval)

except KeyboardInterrupt:
	pass