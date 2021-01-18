from PyQt5 import QtGui  # (the example applies equally well to PySide2)
from czf_client import *
import pyqtgraph as pg
import numpy as np

goal = [0,0] # goal wp, starts at origin
n = 5
cflib.crtp.init_drivers(enable_debug_driver=False)
pe = ParamExample('radio://0/50/2M/E7E7E7E7E5')

## Always start by initializing Qt (only once per application)
app = QtGui.QApplication([])

## Define a top-level widget to hold everything
w = QtGui.QWidget()

plot = pg.PlotWidget()
plot.plot([1,2,3],[1,2,4])


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
    pos = mouseClickEvent.pos()
    x = plot.plotItem.vb.mapSceneToView(pos).x()
    y = plot.plotItem.vb.mapSceneToView(pos).y()
    print([x,y])

plot.scene().sigMouseClicked.connect(set_goal)


## Create some widgets to be placed inside
connect = QtGui.QPushButton('Connect Drone')
take_off = QtGui.QPushButton('Take off')
land = QtGui.QPushButton('Land')
led = QtGui.QPushButton('LED')

listw = QtGui.QListWidget()

scatter = pg.ScatterPlotItem(pen=pg.mkPen(width=5, color='r'), symbol='o', size=1)
plot.addItem(scatter)

data = np.random.normal(size=(2, n))
pos = [{'pos': data[:, i]} for i in range(n)]
scatter.setData(pos)


take_off.clicked.connect(take_off_func)
connect.clicked.connect(connect_drone)
land.clicked.connect(land_func)
# led.clicked.connect(czf_LED)

## Create a grid layout to manage the widgets size and position
layout = QtGui.QGridLayout()
w.setLayout(layout)

## Add widgets to the layout in their proper positions
layout.addWidget(connect, 0, 0)   # button goes in upper-left
layout.addWidget(take_off, 1, 0)   # button goes in upper-left
layout.addWidget(land, 2, 0)   # text edit goes in middle-left
layout.addWidget(led, 3, 0)   # text edit goes in middle-left
layout.addWidget(listw, 4, 0)  # list widget goes in bottom-left
layout.addWidget(plot, 0, 1, 5, 1)  # plot goes on right side, spanning 3 rows

## Display the widget as a new window
w.show()

## Start the Qt event loop
app.exec_()