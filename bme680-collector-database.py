#!/usr/bin/env python3

import bme680
import time
import datetime
import mysql.connector

print("STARTED BME680 Collector DB version!")


# VARIABLES
host = 'HOSTNAME_HERE'
interval = 15
mydb = mysql.connector.connect(
	host="localhost",
	user="USERNAME",
	password="PASSWORD",
	database="DBNAME"
)
cursor = mydb.cursor()

# beginning of script
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

			cursor.execute("INSERT INTO data (dt, host, temperature, pressure, humidity, gas_resistance) VALUES (%(dt)s,%(host)s,%(temperature)s,%(pressure)s,%(humidity)s,%(gas_resistance)s)", sensor_data)
			mydb.commit()
			# print("inserted")

		time.sleep(interval)

except KeyboardInterrupt:
	pass