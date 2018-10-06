import sys
import serial.tools.list_ports


from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QLabel, QComboBox
from PyQt5.QtGui import QIcon


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.left = 10 # Changes where gui opens up
        self.top = 10
        self.title = 'CycleInsight' # Title of GUI
        self.width = 1280 # Width of GUI window
        self.height = 720 # Height of GUI window
        self.initUI()
        self.setStyleSheet("background-color: white;")

    def initUI(self):
        self.setWindowTitle(self.title) # Set title of the GUI
        self.setGeometry(self.left, self.top, self.width, self.height) # Size the GUI from specified parameters

        m = PlotCanvas(self, width = 10, height=7.2) # Plot the canvas where width = x represents x00 pixels e.g 8 = 800 pixels
        m.move(0,0) # Move the canvas to the top corner of the GUI

        start_btn = QPushButton('Start', self)
        start_btn.setToolTip('Click to start session')
        start_btn.move(975,310)
        start_btn.resize(250,100)
        start_btn.setStyleSheet("background-color: green");

        stop_btn = QPushButton('Stop', self)
        stop_btn.setToolTip('Click to stop session')
        stop_btn.move(975, 430)
        stop_btn.resize(250,100)
        stop_btn.setStyleSheet("background-color: red");


        save_btn = QPushButton('Save', self)
        save_btn.setToolTip('Click to save session data')
        save_btn.move(975, 550)
        save_btn.resize(250,100)
        save_btn.setStyleSheet("background-color: blue");

        self.port_lbl = QLabel("Select port:", self)
        self.port_lbl.move(975, 200)

        port_dd = QComboBox(self)
        port_dd.setToolTip('Select port that arduino is connected to. If nothing shows then restart CI after plugging in USB')
        ports = self.get_ports()
        for port in range(0,len(ports)):
            port_dd.addItem(ports[port].device)
        port_dd.move(975, 250)

        # TODO: add a cool logo for CI
        self.ci_lbl = QLabel("CycleInsight", self)
        self.ci_lbl.move(975, 150)

        self.show()

    def get_ports(self):
        ports = list(serial.tools.list_ports.comports())
        return ports

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=10, height=7.2, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.init_plot()


    def init_plot(self):

        global distance_data, cadence_data, time_data, intervals

        distance_graph = self.figure.add_subplot(2,1,1)
        distance_graph.set_xlabel('Elapsed time (s)')
        distance_graph.set_ylabel('Distance (m)')
        distance_graph.set_xlim(0,time_interval)
        distance_graph.set_ylim(0, distance_interval)

        cadence_graph = self.figure.add_subplot(2,1,2)
        cadence_graph.set_xlabel('Elapsed time (s)')
        cadence_graph.set_ylabel('Cadence (rpm)')
        cadence_graph.set_xlim(0,time_interval)
        cadence_graph.set_ylim(0,cadence_interval)

        distance_plot, = distance_graph.plot(time_data, distance_data)
        cadence_plot, = cadence_graph.plot(time_data, cadence_data)

if __name__ == '__main__':

    distance_data = []
    cadence_data = []
    time_data = []

    time_interval = 600
    distance_interval = 1000
    cadence_interval = 130

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
