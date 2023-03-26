import serial


class Fan(serial.Serial):
    def __init__(
        self, 
        port=None, 
        baudrate=9600, 
        max_speed=255, 
        min_speed=0, 
        bytesize=serial.EIGHTBITS, 
        parity=serial.PARITY_NONE, 
        stopbits=serial.STOPBITS_ONE, 
        timeout=None, 
        xonxoff=False, 
        rtscts=False, 
        write_timeout=None, 
        dsrdtr=False, 
        inter_byte_timeout=None, 
        exclusive=None, 
        **kwargs
    ):
    
        super().__init__(port, baudrate, bytesize, parity, stopbits, timeout, xonxoff, rtscts, write_timeout, dsrdtr, inter_byte_timeout, exclusive, **kwargs)
        self.max_speed = max_speed
        self.min_speed = min_speed
