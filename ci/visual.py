# Sort imports
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

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

def update_graphs(i):
    '''Update plotted graphs

    Keyword arguements:
    i -- mandatory arguement that is current frame in animation

    Returns
    (distance_plot, cadence_plot) -- tuple of plot objects
    '''    
    global ser, distance_data, cadence_data, time_data, intervals
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


if __name__ == '__main__':

    ser = serial.Serial('/dev/ttyUSB0', baudrate = 115200, timeout = 1)
    distance_data = []
    cadence_data = []
    time_data = []

    time_interval = 600
    distance_interval = 1000
    cadence_interval = 130

    intervals = (time_interval, distance_interval, cadence_interval)

    fig = plt.figure()

    distance_graph = fig.add_subplot(2,1,1)
    distance_graph.set_xlabel('Elapsed time (s)')
    distance_graph.set_ylabel('Distance (m)')
    distance_graph.set_xlim(0,time_interval)
    distance_graph.set_ylim(0, distance_interval)

    cadence_graph = fig.add_subplot(2,1,2)
    cadence_graph.set_xlabel('Elapsed time (s)')
    cadence_graph.set_ylabel('Cadence')
    cadence_graph.set_xlim(0,time_interval)
    cadence_graph.set_ylim(0,cadence_interval)

    distance_plot, = distance_graph.plot(time_data, distance_data)
    cadence_plot, = cadence_graph.plot(time_data, cadence_data)

    ani = animation.FuncAnimation(fig, update_graphs, blit = False, frames = 200, interval = 20, repeat = False)
    plt.show()
