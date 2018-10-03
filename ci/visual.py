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
    return(distance_data, cadence_data, time_data)

def update_graphs(distance_data, cadence_data, time_data):
    ''' Updates graphs with new data
    '''
    distance_graph.clear()
    cadence_graph.clear()
    distance_graph.plot(time_data, distance_data)
    cadence_graph.plot(time_data, cadence_data)

def run(ser):
    ''' Wrapper function called by matplotlib animation
    '''
    global distance_data, cadence_data, time_data
    data = ser.readline()
    parse_data = parse_data(data)
    updated_data = update_data(parsed_data[0], parsed_data[1], parsed_data[2], distance_data, cadence_data, time_data)
    update_graphs(updated_data[0], updated_data[1], updated_data[2])


if __name__ == "__main__":
    # Create serial object
    ser = serial.Serial('/dev/ttyUSB0', baudrate = 115200, timeout = 1)

    # Create global arrays to hold data
    distance_data = []
    cadence_data = []
    time_data = []

    # Create graphs
    fig = plt.figure()
    distance_graph = fig.add_subplot(211)
    cadence_graph = fig.add_subplot(212)
    # cadence_graph = fig.add_subplot()

    ani = animation.FuncAnimation(fig, run, ser)
    plt.show()

# Sort out imports and create serial object
# Read in the data and parse it appropriately i.e into distance and cadence
# Create a data structure that the parsed data can be added to along with the elapsed time
# Generate plots for the data
# Write a function that can be called to update the graphs dynamically
# Style the graphs appropriately
# Export the data structures to an excel sheet with CI_data_{date}.xlsx as the file name

# Set up a template excel sheet with space allocated for data
# make a macro button that when you click generates tables for inserted data
