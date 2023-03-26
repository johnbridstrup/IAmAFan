from IAmAFan.CommandInterface import TerminalInput
from IAmAFan.Fan import Fan

port = "/dev/ttyACM0"
baud = 38400


fan = Fan(port, baud)
term = TerminalInput(fan)
term.start()
