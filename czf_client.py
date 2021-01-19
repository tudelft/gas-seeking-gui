import logging
import random
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig

import sys

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

class ParamExample:

    def __init__(self, link_uri):
        """ Initialize and run the example with the specified link_uri """

        self.x = 0.0
        self.y = 0.0
        self._cf = Crazyflie(rw_cache='./cache')

        # Connect some callbacks from the Crazyflie API
        self._cf.connected.add_callback(self._connected)
        self._cf.disconnected.add_callback(self._disconnected)
        self._cf.connection_failed.add_callback(self._connection_failed)
        self._cf.connection_lost.add_callback(self._connection_lost)
        self.is_connected = False

        print('Connecting to %s' % link_uri)

        # Try to connect to the Crazyflie
        self._cf.open_link(link_uri)

        # Variable used to keep main loop occupied until disconnect
        

        self._param_check_list = []
        self._param_groups = []

        random.seed()

    def _take_off(self):
        self._cf.param.set_value('relative_ctrl.keepFlying', '1')
    
    def _land(self):
        self._cf.param.set_value('relative_ctrl.keepFlying', '0')

    def _connected(self, link_uri):
        """ This callback is called form the Crazyflie API when a Crazyflie
        has been connected and the TOCs have been downloaded."""
        print('Connected to %s' % link_uri)
        self.is_connected = True
        # The definition of the logconfig can be made before connecting
        self._lg_stab = LogConfig(name='State', period_in_ms=10)
        self._lg_stab.add_variable('kalman.stateX', 'float')
        self._lg_stab.add_variable('kalman.stateY', 'float')

        # Adding the configuration cannot be done until a Crazyflie is
        # connected, since we need to check that the variables we
        # would like to log are in the TOC.
        self._cf.log.add_config(self._lg_stab)
        # This callback will receive the data
        self._lg_stab.data_received_cb.add_callback(self._stab_log_data)
        # This callback will be called on errors
        # self._lg_stab.error_cb.add_callback(self._stab_log_error)
        # Start the logging
        self._lg_stab.start()       
    
    def _stab_log_data(self, timestamp, data, logconf):
        """Callback from a the log API when data arrives"""
        self.x = data['kalman.stateX']
        self.y = data['kalman.stateY']

    def _a_pitch_kd_callback(self, name, value):
        """Callback for pid_attitude.pitch_kd"""
        print('Readback: {0}={1}'.format(name, value))

        # End the example by closing the link (will cause the app to quit)
        self._cf.close_link()

    def _connection_failed(self, link_uri, msg):
        """Callback when connection initial connection fails (i.e no Crazyflie
        at the specified address)"""
        print('Connection to %s failed: %s' % (link_uri, msg))
        self.is_connected = False

    def _connection_lost(self, link_uri, msg):
        """Callback when disconnected after a connection has been made (i.e
        Crazyflie moves out of range)"""
        print('Connection to %s lost: %s' % (link_uri, msg))

    def _disconnected(self, link_uri):
        """Callback when the Crazyflie is disconnected (called in all cases)"""
        print('Disconnected from %s' % link_uri)
        self.is_connected = False

if __name__ == '__main__':
    cflib.crtp.init_drivers(enable_debug_driver=False)
    pe = ParamExample('radio://0/50/2M/E7E7E7E7E5')
    while not pe.is_connected:
        time.sleep(0.1)
    

