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

        self.x_1 = 0.0
        self.y_1 = 0.0
        self.x_2 = 0.0
        self.y_2 = 0.0
        self.yaw_1 = 0.0
        self.yaw_2 = 0.0

        self._cf = Crazyflie(rw_cache='./cache')
        self.forcing_wp = False

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
        time.sleep(4)

    def _take_off(self):
        self._cf.param.set_value('relative_ctrl.keepFlying', '1')
    
    def _land(self):
        self._cf.param.set_value('relative_ctrl.keepFlying', '0')

    def _force_wp(self,goal):
        self._cf.param.set_value('relative_ctrl.force_wp', '1')
        self._cf.param.set_value('relative_ctrl.forced_wp_x', str(goal[0]))
        self._cf.param.set_value('relative_ctrl.forced_wp_y', str(goal[1]))
        self.forcing_wp = True
    
    def _release_wp(self):
        self._cf.param.set_value('relative_ctrl.force_wp', '0')
        self.forcing_wp = False
    
    def _release_leds(self):
        self._cf.param.set_value('led_f405.block_leds', '0')
        time.sleep(0.1)
        self._cf.param.set_value('relative_ctrl.flash_leds', '0')
        time.sleep(2)
    
    def _flash_leds(self):
        self._cf.param.set_value('led_f405.block_leds', '1')
        time.sleep(0.1)
        self._cf.param.set_value('relative_ctrl.flash_leds', '1')
        time.sleep(2)

    def _connected(self, link_uri):
        """ This callback is called form the Crazyflie API when a Crazyflie
        has been connected and the TOCs have been downloaded."""
        print('Connected to %s' % link_uri)
        self.is_connected = True
        # The definition of the logconfig can be made before connecting
        self._lg_stab = LogConfig(name='State', period_in_ms=10)
        self._lg_stab.add_variable('kalman.stateX', 'float')
        self._lg_stab.add_variable('kalman.stateY', 'float')
        self._lg_stab.add_variable('relative_pos.rlX1','float')
        self._lg_stab.add_variable('relative_pos.rlY1','float')
        self._lg_stab.add_variable('relative_pos.rlX2','float')
        self._lg_stab.add_variable('relative_pos.rlY2','float')

        self._lg_stab_2 = LogConfig(name='State_2', period_in_ms=10)
        self._lg_stab_2.add_variable('relative_pos.rlYaw1','float')
        self._lg_stab_2.add_variable('relative_pos.rlYaw2','float')

        # self._lg_stab.add_variable('relative_pos.rlYaw2','float') 
        # Adding the configuration cannot be done until a Crazyflie is
        # connected, since we need to check that the variables we
        # would like to log are in the TOC.
        self._cf.log.add_config(self._lg_stab)
        self._cf.log.add_config(self._lg_stab_2)
        # This callback will receive the data
        self._lg_stab.data_received_cb.add_callback(self._stab_log_data)
        self._lg_stab_2.data_received_cb.add_callback(self._stab_log_data_2)
        # This callback will be called on errors
        # self._lg_stab.error_cb.add_callback(self._stab_log_error)
        # Start the logging
        self._lg_stab.start()   
        self._lg_stab_2.start()    
    
    def _stab_log_data(self, timestamp, data, logconf):
        """Callback from a the log API when data arrives"""
        self.x = data['kalman.stateX']
        self.y = data['kalman.stateY']
        self.x_1 = data['relative_pos.rlX1']
        self.y_1 = data['relative_pos.rlY1']
        self.x_2 = data['relative_pos.rlX2']
        self.y_2 = data['relative_pos.rlY2']
    
    def _stab_log_data_2(self,timestamp,data,logconf):
        self.yaw_1 = data['relative_pos.rlYaw1']
        self.yaw_2 = data['relative_pos.rlYaw2']
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
    

