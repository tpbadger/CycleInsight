import sys
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class cycleInsight(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'CycleInsight'
        self.width = 1000
        self.height = 600
        self.left = 10
        self.top = 10
        self.initUI()

    def initUI(self ,time_interval = 600, distance_interval = 10000, cadence_interval = 120):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top , self.width, self.height)

        # start_btn = QPushButton('Start', self)
        # start_btn.resize(start_btn.sizeHint()) start_btn.move(200, 100) #
        # stop_btn = QPushButton('Stop', self)
        # stop_btn.resize(stop_btn.sizeHint()) stop_btn.move(200, 130) #
        # save_btn = QPushButton('Save', self)
        # save_btn.resize(save_btn.sizeHint()) save_btn.move(200, 160)

        self.fig = Figure(figsize=(2,2), dpi = 100)
        self.canvas = FigureCanvas(self.fig)

        self.distance_graph = self.fig.add_subplot(2,1,1)
        self.distance_graph.set_xlabel('Elapsed time (s)')
        self.distance_graph.set_ylabel('Distance (m)')
        self.distance_graph.set_xlim(0,time_interval)
        self.distance_graph.set_ylim(0, distance_interval)

        self.cadence_graph = self.fig.add_subplot(2,1,2)
        self.cadence_graph.set_xlabel('Elapsed time (s)')
        self.cadence_graph.set_ylabel('Cadence')
        self.cadence_graph.set_xlim(0,time_interval)
        self.cadence_graph.set_ylim(0,cadence_interval)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.canvas.draw()


    # def initGraphs(self):
    #
    #     distance_data = []
    #     cadence_data = []
    #     time_data = []
    #     time_interval = 600
    #     distance_interval = 1000
    #     cadence_interval = 130
    #     intervals = (time_interval, distance_interval, cadence_interval)
    #
    #     self.fig = plt.figure()
    #     self.canvas = FigureCanvas(self.fig)
    #
    #     self.distance_graph = self.fig.add_subplot(2,1,1)
    #     self.distance_graph.set_xlabel('Elapsed time (s)')
    #     self.distance_graph.set_ylabel('Distance (m)')
    #     self.distance_graph.set_xlim(0,time_interval)
    #     self.distance_graph.set_ylim(0, distance_interval)
    #
    #     self.cadence_graph = self.fig.add_subplot(2,1,2)
    #     self.cadence_graph.set_xlabel('Elapsed time (s)')
    #     self.cadence_graph.set_ylabel('Cadence')
    #     self.cadence_graph.set_xlim(0,time_interval)
    #     self.cadence_graph.set_ylim(0,cadence_interval)
    #
    #     distance_plot, = self.distance_graph.plot(time_data, distance_data)
    #     cadence_plot, = self.cadence_graph.plot(time_data, cadence_data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = cycleInsight()
    sys.exit(app.exec_())
