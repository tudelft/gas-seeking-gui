from PyQt5 import QtGui,QtCore  # (the example applies equally well to PySide2)
from czf_client import *
import pyqtgraph as pg
import numpy as np
from cflib.crazyflie.log import LogConfig


# MAX ONE CAN BE TRUE
#######################
flash_led = False
green_led = False
#######################

take_off = True


goal = [0,0] # goal wp, starts at origin
n = 5
cflib.crtp.init_drivers(enable_debug_driver=False)
dummy_1 = ParamExample('radio://0/80/2M/E7E7E7E7E0')
dummy_2 = ParamExample('radio://1/80/2M/E7E7E7E7E1')

if green_led:
    dummy_1.green_leds()
    time.sleep(0.1)
    dummy_2.green_leds()

elif flash_led:
    dummy_1._flash_leds()
    time.sleep(0.1)
    dummy_2._flash_leds()

if take_off:
    dummy_1._dummy_to()
    time.sleep(0.1)
    dummy_2._dummy_to()

else:
    dummy_1.dummy_land()
    time.sleep(0.1)
    dummy_2.dummy_land()

