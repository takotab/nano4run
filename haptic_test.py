import numpy as np
import time
from pymetawear.client import MetaWearClient


address = "D9:05:CD:93:E5:FC" #select_device()

def extract_data(value_str):
    value_str = str(value_str)
    return [float(a.split(":")[1][1:]) for a in value_str.replace("}","").split(",")]


def haptic():
    c = MetaWearClient(str(address), debug=True)
    print("New client created: {0}".format(c))
    # time.sleep(1)
    # c.led.load_preset_pattern('blink', repeat_count=10)
    time.sleep(1)
    c.haptic.start_buzzer(100)
    c.accelerometer.set_settings(data_rate=50, data_range=8)

    def acc_callback(c, data):
        """Handle a (epoch, (x,y,z)) accelerometer tuple."""

        com = sum(extract_data(data['value']))

        if com > 3:
            c.haptic.start_motor(100, 1000)
            print("\n\n\n\n\n\n")
            print("com", com)
            print("\n\n\n\n\n\n")

        elif np.random.random() > 0.9:
            print("com", com)

    c.accelerometer.notifications(lambda x:acc_callback(c,x))

    time.sleep(60)
    c.led.load_preset_pattern('blink', repeat_count = 10)



    c.haptic.start_buzzer(100)

    time.sleep(2)

    c.disconnect()

if __name__ == '__main__':
    haptic()