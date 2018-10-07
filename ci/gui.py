import sys
import serial.tools.list_ports
import time

from utils import parse_data, update_data

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QLabel, QComboBox
from PyQt5.QtGui import QIcon, QPixmap


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import random

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.left = 10 # Changes where gui opens up
        self.top = 10
        self.title = 'CycleInsight' # Title of GUI
        self.width = 1280 # Width of GUI window
        self.height = 720 # Height of GUI window
        self.port = "" # Set port attribute to empty string initially

        self.initUI()
        self.setStyleSheet("background-color: white;")


    def initUI(self):
        self.setWindowTitle(self.title) # Set title of the GUI
        self.setGeometry(self.left, self.top, self.width, self.height) # Size the GUI from specified parameters

        self.m = PlotCanvas(self, width = 10, height=7.2) # Plot the canvas where width = x represents x00 pixels e.g 8 = 800 pixels
        # m.whatever is how to call stuff from canvas class in initUI
        self.m.move(0,0) # Move the canvas to the top corner of the GUI

        # Start button
        start_btn = QPushButton('Start', self)
        start_btn.setToolTip('Click to start session')
        start_btn.move(975,375)
        start_btn.resize(250,75)
        start_btn.setStyleSheet("background-color: green")
        start_btn.clicked.connect(self.start_clicked)

        # Stop button
        stop_btn = QPushButton('Stop', self)
        stop_btn.setToolTip('Click to stop session')
        stop_btn.move(975, 475)
        stop_btn.resize(250,75)
        stop_btn.setStyleSheet("background-color: red")
        stop_btn.clicked.connect(self.stop_clicked)

        # Save button
        save_btn = QPushButton('Save', self)
        save_btn.setToolTip('Click to save session data')
        save_btn.move(975, 575)
        save_btn.resize(250,75)
        save_btn.setStyleSheet("background-color: blue")
        save_btn.clicked.connect(self.save_clicked)

        # Port selection
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

        # Logo
        logo = QLabel(self)
        pixmap = QPixmap('logo.png')
        logo.setPixmap(pixmap)
        logo.move(975, 80)
        logo.resize(pixmap.width(), pixmap.height())

        # Draw gui
        self.show()

    @staticmethod
    def get_ports():
        '''Get list of active serial ports

        Returns:
        ports -- List of active serial ports
        '''
        ports = list(serial.tools.list_ports.comports())
        return ports

    def on_selected(self, port):
        '''Set port attribute to port selected from drop down menu
        '''
        self.port = port

    def start_clicked(self):
        '''Tell arduio to start sending data
        '''
        global ser
        ser = serial.Serial(self.port, baudrate = 115200, timeout = 1)
        data = "go"
        data += "\r\n"
        time.sleep(2)
        ser.write(data.encode())
        self.m.plot_data()

    @staticmethod
    def stop_clicked():
        '''Close the serial port and reset the arduino
        '''
        global ser
        ser.close()
        # TODO: m.stop_updating graphs

    def save_clicked(self):
        '''Save session data into Excel sheet
        '''
        print("save")

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=10, height=7.2, dpi=100):
        global fig
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

        global distance_data, cadence_data, time_data, intervals, distance_plot, cadence_plot

        distance_graph = self.figure.add_subplot(2,1,1)
        distance_graph.set_xlabel('Elapsed time (s)')
        distance_graph.set_ylabel('Distance (m)')
        distance_graph.set_xlim(0,intervals[0])
        distance_graph.set_ylim(0, intervals[1])

        cadence_graph = self.figure.add_subplot(2,1,2)
        cadence_graph.set_xlabel('Elapsed time (s)')
        cadence_graph.set_ylabel('Cadence (rpm)')
        cadence_graph.set_xlim(0,intervals[0])
        cadence_graph.set_ylim(0,intervals[2])

        distance_plot, = distance_graph.plot(time_data, distance_data)
        cadence_plot, = cadence_graph.plot(time_data, cadence_data)


    def update_graphs(self,i):
        '''Update plotted graphs

        Keyword arguements:
        i -- mandatory arguement that is current frame in animation

        Returns
        (distance_plot, cadence_plot) -- tuple of plot objects
        '''
        global ser, distance_data, cadence_data, time_data, intervals, distance_plot, cadence_plot
        data = ser.readline()
        parsed_data = parse_data(data)
        updated_data = update_data(parsed_data[0], parsed_data[1], parsed_data[2], distance_data, cadence_data, time_data)

        distance_plot.set_data(time_data, distance_data)
        cadence_plot.set_data(time_data, cadence_data)

        if time_data[-1] >= intervals[0]:
            distance_plot.axes.set_xlim(time_data[-1], 2*intervals[0])
            cadence_plot.axes.set_xlim(time_data[-1], 2*intervals[0])

        if distance_data[-1] >= intervals[1]:
            distance_plot.axes.set_ylim(distance_data[-1], 2*intervals[1])

        if cadence_data[-1] >= intervals[2]:
            cadence_plot.axes.set_ylim(cadence_data[-1], 2*intervals[2])
        else:
            cadence_plot.axes.set_ylim(0, intervals[2])

        return (distance_plot, cadence_plot)

    def plot_data(self):
        global fig
        self.ani = animation.FuncAnimation(fig, self.update_graphs, frames = 200, interval = 20, repeat = False)
        self.draw()

    @staticmethod
    def parse_data(data):
        ''' Parse data read from serial into seperate distance and cadence data.

        Keyword arguements:
        data -- string containing distance and cadence data e.g 0.00,0

        Returns:
        (distance, cadence, elapsed_time) -- tuple with parsed distance, cadence and elapsed_time data as float, int and int
        '''
        data = data.decode("UTF-8").rstrip()
        if data == '':
            distance = 0.0
            cadence = 0
            elapsed_time = 0
        else:
            distance = float(data.split(",")[0])
            cadence = int(data.split(",")[1])
            elapsed_time = int(data.split(",")[2])
        return (distance, cadence, elapsed_time)


    @staticmethod
    def update_data(distance, cadence, elapsed_time, distance_data, cadence_data, time_data):
        ''' Updates distance, cadence and time data that will be plotted with new parsed data and elapsed time

        Keyword arguements:
        distance -- float of parsed distance data in meters
        cadence -- int of parsed cadence data
        elapsed_time -- int of parsed elapsed time data
        distance_data -- list containing existing distance data that will be appended to
        cadence_data -- list containing existing cadence data that will be appended to
        time_data -- list containing exisiting time data that will be appended to

        Returns:
        (distance_data, cadence_data, time_data) -- tuple of lists with new data appended
        '''
        distance_data.append(distance)
        cadence_data.append(cadence)
        time_data.append(elapsed_time)
        return (distance_data, cadence_data, time_data)





if __name__ == '__main__':

    distance_data = []
    cadence_data = []
    time_data = []

    time_interval = 600
    distance_interval = 1000
    cadence_interval = 130
    intervals = (time_interval, distance_interval, cadence_interval)

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
