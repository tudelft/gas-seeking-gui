from PyQt5 import QtGui,QtCore  # (the example applies equally well to PySide2)
from czf_client import *
import pyqtgraph as pg
import numpy as np
from cflib.crazyflie.log import LogConfig

led_on = False
goal = [0,0] # goal wp, starts at origin
n = 5
cflib.crtp.init_drivers(enable_debug_driver=False)
pe = ParamExample('radio://0/50/2M/E7E7E7E7E5')
pe_2 = ParamExample('radio://1/60/2M/E7E7E7E7E6')
pe_3 = ParamExample('radio://2/70/2M/E7E7E7E7E7')
dummy_1 = ParamExample('radio://3/80/2M/E7E7E7E7E8')
dummy_2 = ParamExample('radio://4/90/2M/E7E7E7E7E9')

goal_mouse = [0,0]

x_arr = []
y_arr = []

x_scatter = []
y_scatter = []
    
## Always start by initializing Qt (only once per application)
app = QtGui.QApplication([])


## Define a top-level widget to hold everything
w = QtGui.QWidget()

plot = pg.PlotWidget()
# line = plot.plot([0.0],[0.0])

scatter = pg.ScatterPlotItem(pen=pg.mkPen(width=5, color='r'), symbol='o', size=1)
plot.addItem(scatter)

goal_text = pg.TextItem('goal_wp')

arrow_1 = pg.ArrowItem(angle=90)
agent_1_text = pg.TextItem('E5')

arrow_2 = pg.ArrowItem(angle=90)
agent_2_text = pg.TextItem('E6')

arrow_3 = pg.ArrowItem(angle=90)
agent_3_text = pg.TextItem('E7')

def update_plot_data():
    if pe.is_connected:
        x_arr.append(-pe.y)
        y_arr.append(pe.x)

        # line.setData(x_arr,y_arr)
        x_scatter = [x_arr[-1]]
        y_scatter = [y_arr[-1]]

        plot.addItem(arrow_1)
        plot.addItem(agent_1_text)
        plot.addItem(arrow_2)
        plot.addItem(agent_2_text)
        plot.addItem(arrow_3)
        plot.addItem(agent_3_text)

        arrow_1.setPos(x_scatter[0],y_scatter[0])     
        agent_1_text.setPos(x_scatter[0],y_scatter[0]) 

        arrow_2.setPos(x_scatter[0] - pe.y_1, y_scatter[0] + pe.x_1)
        agent_2_text.setPos(x_scatter[0] - pe.y_1, y_scatter[0] + pe.x_1)

        arrow_3.setPos(x_scatter[0] - pe.y_2, y_scatter[0] + pe.x_2)
        agent_3_text.setPos(x_scatter[0] - pe.y_2, y_scatter[0] + pe.x_2)

        arrow_2.setStyle(angle=90-(np.rad2deg(pe.yaw_1)))
        arrow_2.setStyle(angle=90-(np.rad2deg(pe.yaw_2)))

        if (pe.forcing_wp):
            x_scatter.append(goal_mouse[0])
            y_scatter.append(goal_mouse[1])
            goal_text.setPos(goal_mouse[0],goal_mouse[1])
            plot.addItem(goal_text)
        scatter.setData(x_scatter,y_scatter)
        

def connect_drone():
    global pe,pe_2,pe_3
    pe = ParamExample('radio://0/50/2M/E7E7E7E7E5')
    pe_2 = ParamExample('radio://0/60/2M/E7E7E7E7E6')
    pe_3 = ParamExample('radio://0/70/2M/E7E7E7E7E7')

def take_off_func():
    while not pe.is_connected:
        time.sleep(0.1)
    pe._take_off()

def land_func():
    while not pe.is_connected:
        time.sleep(0.1)
    pe._land()

def set_goal(mouseClickEvent):
    global goal_mouse
    pos = mouseClickEvent.pos()
    x = plot.plotItem.vb.mapSceneToView(pos).x()
    y = plot.plotItem.vb.mapSceneToView(pos).y()
    pe._force_wp([y,-x])
    goal_mouse = [x,y]

def set_led_1(state):
    if (state == 2 ):
        pe._flash_leds()
    else:
        pe._release_leds()

def set_led_2(state):
    if (state == 2 ):
        pe_2._flash_leds()
    else:
        pe_2._release_leds()

def set_led_3(state):
    if (state == 2 ):
        pe_3._flash_leds()
    else:
        pe_3._release_leds()

def set_led_1_green(state):
    if (state == 2 ):
        pe.green_leds()
    else:
        pe._release_leds()

def set_led_2_green(state):
    if (state == 2 ):
        pe_2.green_leds()
    else:
        pe_2._release_leds()

def set_led_3_green(state):
    if (state == 2 ):
        pe_3.green_leds()
    else:
        pe_3._release_leds()

plot.scene().sigMouseClicked.connect(set_goal)


## Create some widgets to be placed inside
connect = QtGui.QPushButton('Connect Drone')
take_off = QtGui.QPushButton('Take off')
land = QtGui.QPushButton('Land')
led_1 = QtGui.QCheckBox('LED 1 flash')
led_2 = QtGui.QCheckBox('LED 2 flash')
led_3 = QtGui.QCheckBox('LED 3 flash')

led_1_green = QtGui.QCheckBox('LED 1 green')
led_2_green = QtGui.QCheckBox('LED 2 green')
led_3_green = QtGui.QCheckBox('LED 3 green')
listw = QtGui.QListWidget()

take_off.clicked.connect(take_off_func)
connect.clicked.connect(connect_drone)
land.clicked.connect(land_func)

led_1.stateChanged.connect(set_led_1)
led_2.stateChanged.connect(set_led_2)
led_3.stateChanged.connect(set_led_3)

led_1_green.stateChanged.connect(set_led_1_green)
led_2_green.stateChanged.connect(set_led_2_green)
led_3_green.stateChanged.connect(set_led_3_green)

## Create a grid layout to manage the widgets size and position
layout = QtGui.QGridLayout()
w.setLayout(layout)

## Add timer
timer = QtCore.QTimer()
timer.setInterval(50)
timer.timeout.connect(update_plot_data)
timer.start()

## Add widgets to the layout in their proper positions
layout.addWidget(connect, 0, 0)   # button goes in upper-left
layout.addWidget(take_off, 1, 0)   # button goes in upper-left
layout.addWidget(land, 2, 0)   # text edit goes in middle-left
layout.addWidget(led_1, 3, 0)   # text edit goes in middle-left
layout.addWidget(led_2, 4, 0)   # text edit goes in middle-left
layout.addWidget(led_3, 5, 0)   # text edit goes in middle-left
layout.addWidget(led_1_green, 6, 0)   # text edit goes in middle-left
layout.addWidget(led_2_green, 7, 0)   # text edit goes in middle-left
layout.addWidget(led_3_green, 8, 0)   # text edit goes in middle-left
layout.addWidget(listw, 9, 0)  # list widget goes in bottom-left
layout.addWidget(plot, 0, 1, 10, 1)  # plot goes on right side, spanning 3 rows

## Display the widget as a new window
w.show()

## Start the Qt event loop
app.exec_()