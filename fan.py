from IAmAFan.Fan import Fan

port = "/dev/ttyACM0"
baud = 38400

fan = Fan(port=port, baudrate=baud)

fan.start()
