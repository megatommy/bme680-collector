# BME680 Collector

**DISCLAIMER: These scripts are not tested well and might contain bugs. Use at your own risk.**

![Service Running](img/service-screenshot.png?raw=true "Service Running")

This repository contains the necessary files to make the raspberry store sensor information obtained by a connected BME680 sensor in a MySQL database.

The python scripts are **modified versions** of the [examples provided by the Pimoroni BME680 library](https://github.com/pimoroni/bme680-python).

The files:
 - `bme680-collector.service`: The service file, to tell the Raspberry to run the wanted script at boot time
 - `bme680.sql`: SQL file which creates the database and the necessary table and columns
 - `bme680-collector-database.py`: This script reads the data (every 15 seconds by default) and stores it in a local MySQL database
 - `bme680-collector-postrequest.py`: Reads the data and sends a POST request containing the data to a given URL.
   **Entirely up to you how you choose to handle the data**

## Why?

The reason I wanted to save the data in a MySQL database, is because this way I could install Grafana on the Pi aswell and use the database as a data source. 

*To install Grafana on the Raspberry Pi, I recommend this tutorial: [Install Grafana on Raspberry Pi](https://grafana.com/tutorials/install-grafana-on-raspberry-pi/)*

Hooking up and configuring Grafana with the database gave me the following result:
![Grafana Dashboard](img/grafana-dashboard.png?raw=true "Grafana Dashboard")

## Installation & Configuration

Before installing, these are the prerequisites:

Hardware:
 - A Raspberry Pi
 - BME680 connected to the Pi *To connect the BME680 to the Raspberry Pi, I recommend this article: [Getting Started with BME680 Breakout](https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-bme680-breakout)*

Software (on the Pi):
 - MySQL
 - Python package `bme680-python` provided by Pimoroni. **Test the examples provided**

When the necessary is installed, proceed:


```bash
# clone the reporitory and enter the directory:
git clone XXX
cd bme680-collector

# edit the python script with the credentials of MySQL:
nano bme680-collector-database.py

# execute the SQL provided in the `bme680.sql` file

# open the bme680-collector.service file and edit the line starting with "ExecStart="
# to match the path of the python file you want to use:
nano bme680-collector.service

# copy the bme680-collector.service file to /usr/lib/systemd/system
sudo cp bme680-collector.service /usr/lib/systemd/system

# reload the systemctl daemon
sudo systemctl daemon-reload

# start and enable the service to start on boot
sudo systemctl start bme680-collector
sudo systemctl enable bme680-collector
```

That's it! If you want to install Grafana, please follow the link I provided earlier

Maybe someday i'll make a foolproof tutorial, but for now this is enough info provided to get started