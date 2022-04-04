# gas-seeking-gui
Groundstation GUI for the gas-seeking/swarm-exploration demo 

# Gas Seeking Demo (Manual V1.0, April 2022)

Please notify the MAVLab Crazyflie Responsible in case of any problems with this Demo

The Gas Seeking Demo is based on the Sniffy Bug Swarm by Bart Duisterhof. It consists of three drones cooperating to find a gas source. The code can also be used without a gas source to demonstrate swarm exploration in an unknown environment. This instruction assumes you are running Ubuntu 20.04 with Python 3.7.

Reference: *B. P. Duisterhof, S. Li, J. Burgués, V. J. Reddi and G. C. H. E. de Croon, "Sniffy Bug: A Fully Autonomous Swarm of Gas-Seeking Nano Quadcopters in Cluttered Environments," 2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2021, pp. 9099-9106, doi: 10.1109/IROS51168.2021.9636217.*

**Preparation**
- Clone and install the Crazyflie Client (https://github.com/bitcraze/crazyflie-clients-python)
- Clone the gas-seeking-gui (https://github.com/tudelft/gas-seeking-gui)
- Charge the Batteries
- Prepare the environment. This could mean adding some obstacles and walls in the Cyberzoo and making sure that the drones can’t “escape” the testing area
- If running the Demo in the Cyberzoo, make sure the stationary UWB beacons are switched off.
- If you want to localize a gas source, get some Isopropyl Alcohol (ask in the Aircraft Hall). There should be a becher with attached fan on the same shelf as the Demo Box. Then place the Becher somewhere in the Environment.
 
**Execution**
- Connect the Crazyradio Dongles to your computer
- Install the batteries on the crazyflies
- Place the crazyflie facing approximately the same direction and with about 1m in between.
- Run the “MA.py” file of the gas-seeking-gui and press the take-off button
- The drones should now take-off, initialize around their starting location and then start flying around.
- Try landing the drones using the “land” button. This actually often doesn’t work properly, in that case simply block the drones propeller with you leg to make them crash (not ideal but the best we have atm)

**Common Problems**
- *Can’t connect to the drones:* Debug the connection using bitcraze resources (www.bitcraze.io) and the crazyflie client. The drone’s addresses are 0xE7E7E7E7EX, where X is the number on the drone’s white marker (5, 6 or 7).
- *Connections drop frequently:* As long as you can connect to drone number 5 and take off, it doesn’t matter. The take-off command is only received by drone 5 and then shared via UWB. Once the drone’s are flying, the Demo doesn’t need the connection.
- *Only drone 5 takes off:* There is an issue with UWB connection dropping sometimes. This can be determined with the blue lights on the gas deck. If all 4 blink, the connection is fine. Sometimes however, all but 1 light stop blinking. In that case simply restart drone number 5 and try again (annoyingly, this can happen during the connection process).
- *The drones crash (at the start or later):* Shit happens, just try again
- *One of the drones breaks and can’t be used anymore:* The demo still works with 2 drones. If drone 5 breaks, reassign it’s address to one of the other drones (cfclient>connect>configure 2.X). For small issues, you can probably fix the drone yourself, there are spare-parts and decks in the box and you can find instructions on www.bitcraze.io. Notify the MAVLab Crazyflie Responsible if you need help with repairs or you used the last spare.
- *Drones struggle taking off:* Because the setup is quite heavy, it only works with good batteries. Try a new battery (contact CF responsible if you need new ones).
- *Ubuntu 18.04:* Ubuntu 18.04’s Terminal does not seem to work with Python 3.7. As a workaround, install Python 3.7 alongside Python 3.6 or 3.5 and use the command ‘python3.7’ when running the script or the client (e.g. ‘python3.7 MA.py’ or ‘python3.7 -m cfclient.gui’)
- *Other:* Restarting the drone and wiggling the decks a bit can often help

**In-Depth (For Demo Maintenance)**
- The firmware for the demo can be found on https://github.com/tudelft/crazyflie-firmware on the ‘gas-seeking-demo’ branch.

*Box contains:*
  3x Crazyflie 2.X
  4x Flow Deck V2
  4x Multi-Ranger Deck
  5x Custom Gas Deck
  3x Crazyradio Dongle
  3x Micro-USB Cable
  1x USB Hub
  9x Batteries with single battery charger
  1x Multi-Battery Charger
  Assorted spare parts
