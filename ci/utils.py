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
