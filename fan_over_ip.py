from IAmAFan.CommandInterface import NetworkController
from IAmAFan.Fan import Fan

dev_port = "/dev/ttyACM0"
baud = 38400
port = 5000
host = 'localhost'


fan = Fan(dev_port, baud)
term = NetworkController(fan, host, port)
term.start()