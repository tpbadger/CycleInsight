import sys
import serial.tools.list_ports
import time

from utils import parse_data, update_data

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QLabel, QComboBox
from PyQt5.QtGui import QIcon, QPixmap


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
        self.text = ""

    def initUI(self):
        self.setWindowTitle(self.title) # Set title of the GUI
        self.setGeometry(self.left, self.top, self.width, self.height) # Size the GUI from specified parameters

        m = PlotCanvas(self, width = 10, height=7.2) # Plot the canvas where width = x represents x00 pixels e.g 8 = 800 pixels
        # m.whatever is how to call stuff from canvas class in initUI
        m.move(0,0) # Move the canvas to the top corner of the GUI

        start_btn = QPushButton('Start', self)
        start_btn.setToolTip('Click to start session')
        start_btn.move(975,375)
        start_btn.resize(250,75)
        start_btn.setStyleSheet("background-color: green")
        start_btn.clicked.connect(self.start_clicked)

        stop_btn = QPushButton('Stop', self)
        stop_btn.setToolTip('Click to stop session')
        stop_btn.move(975, 475)
        stop_btn.resize(250,75)
        stop_btn.setStyleSheet("background-color: red")
        stop_btn.clicked.connect(self.stop_clicked)


        save_btn = QPushButton('Save', self)
        save_btn.setToolTip('Click to save session data')
        save_btn.move(975, 575)
        save_btn.resize(250,75)
        save_btn.setStyleSheet("background-color: blue")
        save_btn.clicked.connect(self.save_clicked)

        self.port_lbl = QLabel("Select port:", self)
        self.port_lbl.move(975, 270)

        port_dd = QComboBox(self)
        port_dd.setToolTip('Select port that arduio.resize(pixmap.width(), pixmap.height())no is connected to. If nothing shows then restart CI after plugging in USB')
        ports = self.get_ports()
        port_dd.addItem("Select")
        for port in range(0,len(ports)):
            port_dd.addItem(ports[port].device)
        port_dd.activated[str].connect(self.on_selected)
        port_dd.move(975, 300)

        logo = QLabel(self)
        pixmap = QPixmap('logo.png')
        logo.setPixmap(pixmap)
        logo.move(975, 80)
        logo.resize(pixmap.width(), pixmap.height())

        self.show()

    def get_ports(self):
        ports = list(serial.tools.list_ports.comports())
        return ports

    def on_selected(self, text):
        self.text = text

    def start_clicked(self):
        global ser
        ser = serial.Serial(self.text, baudrate = 115200, timeout = 1)
        data = "go"
        data += "\r\n"
        time.sleep(2)
        ser.write(data.encode())
        # TODO: m.update_graphs

    def stop_clicked(self):
        global ser
        ser.close()
        # TODO: m.stop_updating graphs

    def save_clicked(self):
        print("save")

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=10, height=7.2, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.test = "test"

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
