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
line = plot.plot([0.0],[0.0])

scatter = pg.ScatterPlotItem(pen=pg.mkPen(width=5, color='r'), symbol='o', size=1)
plot.addItem(scatter)

goal_text = pg.TextItem('goal_wp')
arrow_1 = pg.ArrowItem(angle=90)
agent_1_text = pg.TextItem('E5')

def update_plot_data():
    if pe.is_connected:
        x_arr.append(-pe.y)
        y_arr.append(pe.x)

        line.setData(x_arr,y_arr)
        x_scatter = [x_arr[-1]]
        y_scatter = [y_arr[-1]]

        plot.addItem(arrow_1)
        plot.addItem(agent_1_text)

        arrow_1.setPos(x_scatter[0],y_scatter[0])     
        agent_1_text.setPos(x_scatter[0],y_scatter[0]) 

        if (pe.forcing_wp):
            x_scatter.append(goal_mouse[0])
            y_scatter.append(goal_mouse[1])
            goal_text.setPos(goal_mouse[0],goal_mouse[1])
            plot.addItem(goal_text)
        scatter.setData(x_scatter,y_scatter)
        

def connect_drone():
    global pe
    pe = ParamExample('radio://0/50/2M/E7E7E7E7E5')

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

def set_led(state):
    if (state == 2 ):
        pe._flash_leds()
    else:
        pe._release_leds()

def set_led_green(state):
    if (state == 2 ):
        pe.green_leds()
    else:
        pe._release_leds()

plot.scene().sigMouseClicked.connect(set_goal)


## Create some widgets to be placed inside
connect = QtGui.QPushButton('Connect Drone')
take_off = QtGui.QPushButton('Take off')
land = QtGui.QPushButton('Land')
led = QtGui.QCheckBox('LED Flash ')
led_green = QtGui.QCheckBox('LED Green ')


listw = QtGui.QListWidget()


take_off.clicked.connect(take_off_func)
connect.clicked.connect(connect_drone)
land.clicked.connect(land_func)
led.stateChanged.connect(set_led)
led_green.stateChanged.connect(set_led_green)

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
layout.addWidget(led, 3, 0)   # text edit goes in middle-left
layout.addWidget(led_green, 4, 0)   # text edit goes in middle-left
layout.addWidget(listw, 5, 0)  # list widget goes in bottom-left
layout.addWidget(plot, 0, 1, 6, 1)  # plot goes on right side, spanning 3 rows

## Display the widget as a new window
w.show()

## Start the Qt event loop
app.exec_()