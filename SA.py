
# importing Qt widgets 
from PyQt5.QtWidgets import *
  
# importing system 
import sys 
  
# importing numpy as np 
import numpy as np 
  
# importing pyqtgraph as pg 
import pyqtgraph as pg 
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot
clicks = []
class Window(QMainWindow): 
  
    def __init__(self): 
        super().__init__() 
  
        # setting title 
        self.setWindowTitle("PyQtGraph") 
  
        # setting geometry 
        self.setGeometry(100, 100, 600, 500) 
  
        # icon 
        icon = QIcon("skin.png") 
  
        # setting icon to the window 
        self.setWindowIcon(icon) 
  
        # calling method 
        self.UiComponents() 
  
        # showing all the widgets 
        self.initUI()
  
    # method for components 
    def UiComponents(self): 
  
        # creating a widget object 
        widget = QWidget() 
  
        # creating a label 
        label = QLabel("Geeksforgeeks Scatter Plot") 
  
        # making label do word wrap 
        label.setWordWrap(True) 
  
        # creating a plot window 
        plot = pg.plot() 
  
        # number of points 
        n = 300
  
        # creating a scatter plot item 
        # of size = 10 
        # using brush to enlarge the of white color with transparency is 50% 
        scatter = pg.ScatterPlotItem( 
            size=10, brush=pg.mkBrush(255, 255, 255, 120)) 
  
        plot.scene().sigMouseClicked.connect(self.onClick)
        # getting random position 
        pos = np.random.normal(size=(2, n), scale=1e-5) 
        # creating spots using the random position 
        spots = [{'pos': pos[:, i], 'data': 1} 
                 for i in range(n)] + [{'pos': [0, 0], 'data': 1}] 
  
        # adding points to the scatter plot 
        scatter.addPoints(spots) 
  
        # add item to plot window 
        # adding scatter plot item to the plot window 
        plot.addItem(scatter) 
  
        # Creating a grid layout 
        layout = QGridLayout() 
  
        # minimum width value of the label 
        label.setMinimumWidth(130) 
  
        # setting this layout to the widget 
        widget.setLayout(layout) 
  
        # adding label in the layout 
        layout.addWidget(label, 1, 0) 
  
        # plot window goes on right side, spanning 3 rows 
        layout.addWidget(plot, 0, 1, 3, 1) 
  
        # setting this widget as central widget of the main widow 
        self.setCentralWidget(widget) 
      
    def initUI(self):
        # self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        
        button = QPushButton('PyQt5 button', self)
        button.setToolTip('This is an example button')
        button.move(200,200)
        button.clicked.connect(self.on_click)
        self.show() 
        # self.show()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')
  

    def onClick(ev):
        global clicks
        x = ev.pos().x()
        y = ev.pos().y()
        print(x,y)

# create pyqt5 app 
App = QApplication(sys.argv) 
  
# create the instance of our Window 
window = Window() 



# start the app 
sys.exit(App.exec()) 
