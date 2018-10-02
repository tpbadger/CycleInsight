# Sort imports
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time

def parse_data(data):
    ''' Parse data read from serial into seperate distance and cadence data.

    Keyword arguements:
    data -- string containing distance and cadence data e.g 0.00,0

    Returns:
    (distance, cadence) -- tuple with parsed distance and cadence data as float and int
    '''
    data = data.decode("UTF-8").rstrip()
    distance = float(data.split(",")[0])
    cadence = int(data.split(",")[1])
    return (distance, cadence)

def update_data(distance, cadence, elapsed_time, distance_data, cadence_data, time_data):
    elapsed_time += 1
    distance_data.append(distance)
    cadence_data.append(cadence)
    time_data.append(elapsed_time)
    return(distance_data, cadence_data, time_data, elapsed_time)

def update_graphs(distance_data, cadence_data, time_data):
    distance_graph.clear()
    distance_graph.plot(time_data, distance_data)
    cadence_graph.clear()
    cadence_graph.plot(time_data, cadence_data)

if __name__ == "__main__":
    # Create serial object
    ser = serial.Serial('/dev/ttyUSB4', baudrate = 115200, timeout = 1)

    # Create arrays to hold data
    distance_data = []
    cadence_data = []
    time_data = []

    # Create graphs
    fig = plt.figure()
    distance_graph = fig.add_subplot(211)
    cadence_graph = fig.add_subplot(212)

    elapsed_time = 0
    plt.show()
    
    while 1:
        data = ser.readline()
        parsed_data = parse_data(data)
        updated_data = update_data(parsed_data[0], parsed_data[1], elapsed_time, distance_data, cadence_data, time_data)
        elapsed_time = updated_data[3]
        print("fuck")
        update_graphs(updated_data[0], updated_data[1], updated_data[2])


# Sort out imports and create serial object
# Read in the data and parse it appropriately i.e into distance and cadence
# Create a data structure that the parsed data can be added to along with the elapsed time
# Generate plots for the data
# Write a function that can be called to update the graphs dynamically
# Style the graphs appropriately
# Export the data structures to an excel sheet with CI_data_{date}.xlsx as the file name

# Set up a template excel sheet with space allocated for data
# make a macro button that when you click generates tables for inserted data
