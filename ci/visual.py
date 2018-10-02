# Sort imports
import serial
import matplotlib

# Create serial object
ser = serial.Serial('/dev/ttyUSB4', baudrate = 115200, timeout = 1)

# Create lists to hold distance and cadence data
distance_data = []
cadence_data = []

while 1:
    data = ser.readline()
    print(data)

def parse_data(data):
    pass



# Sort out imports and create serial object
# Read in the data and parse it appropriately i.e into distance and cadence
# Create a data structure that the parsed data can be added to along with the elapsed time
# Generate plots for the data
# Write a function that can be called to update the graphs dynamically
# Style the graphs appropriately
# Export the data structures to an excel sheet with CI_data_{date}.xlsx as the file name

# Set up a template excel sheet with space allocated for data
# make a macro button that when you click generates tables for inserted data
