import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())

for port in range(0,len(ports)):
    print(ports[port].device)
