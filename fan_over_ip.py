from IAmAFan.CommandInterface import NetworkController
from IAmAFan.Fan import Fan

dev_port = "/dev/ttyACM0"
baud = 38400
port = 5000
host = 'localhost'

FoIP = NetworkController(host, port)
fan = Fan(FoIP, dev_port, baud)

fan.start()