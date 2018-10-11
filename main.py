from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import time

from pymetawear.client import MetaWearClient
from pymetawear.exceptions import PyMetaWearException, PyMetaWearDownloadTimeout
from mbientlab.metawear import MetaWear, libmetawear
from mbientlab.metawear.cbindings import *
from time import sleep
from threading import Event
import pandas as pd
# import matplotlib.pyplot as plt
# address = select_device()

address = "D9:05:CD:93:E5:FC" #select_device()

def blink_10():


    c = MetaWearClient(str(address), debug=True)
    print("New client created: {0}".format(c))

    print("Blinking 10 times with green LED...")
    pattern = c.led.load_preset_pattern('blink', repeat_count=10)
    c.led.write_pattern(pattern, 'g')
    c.led.play()

    time.sleep(5.0)

    c.disconnect()

def log():
    client = MetaWearClient(str(address), debug=False)
    print("New client created: {0}".format(client))

    settings = client.accelerometer.get_possible_settings()
    print("Possible accelerometer settings of client:")
    for k, v in settings.items():
        print(k, v)

    print("Write accelerometer settings...")
    client.accelerometer.set_settings(data_rate=400, data_range=4.0)

    settings = client.accelerometer.get_current_settings()
    print("Accelerometer settings of client: {0}".format(settings))

    client.accelerometer.high_frequency_stream = False
    client.accelerometer.start_logging()
    print("Logging accelerometer data...")

    for i in range(5):
        time.sleep(1.0)
        print(i)

    client.accelerometer.stop_logging()
    print("Logging stopped.")

    print("Downloading data...")
    download_done = False
    n = 0
    data = None
    while (not download_done) and n < 3:
        try:
            data = client.accelerometer.download_log()
            download_done = True
        except PyMetaWearDownloadTimeout:
            print("Download of log interrupted. Trying to reconnect...")
            client.disconnect()
            client.connect()
            n += 1
    if data is None:
        raise PyMetaWearException("Download of logging data failed.")

    print("Disconnecting...")
    client.disconnect()

    with open('data.txt','w') as f:
        for d in data:
            f.write(str(d) +"\n")


if __name__ == '__main__':
    log()