import serial

from .CommandInterface import CommandInterface, TerminalInput



class CantDoThatError(Exception):
    pass


class Fan(serial.Serial):
    def __init__(
        self,
        controller: CommandInterface=TerminalInput(), 
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
        self.cur_speed = 0
        self._controller = controller

    def start(self):
        print("I Am A Fan!")
        print("Initializing controller...")
        self._controller.start()
        try:
            while True:
                speed = self._controller.get_fan_speed()
                self.check_speed(speed)
                print(f"Received speed: {speed}")
                try:
                    self.set_speed(speed)
                except CantDoThatError as e:
                    print(e)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"Something happened: {e}")
            raise e
        finally:
            self.stop()

    def stop(self):
        self.write(str(self.min_speed).encode())
        self._controller.stop()
        self.cur_speed = self.min_speed

    def set_speed(self, speed):
        self.write(str(speed).encode())
        self.cur_speed = speed

    def check_speed(self, num):
        try:
            num = int(num)
        except ValueError:
            raise CantDoThatError(f"{num} is not an integer.")
        if num > self.max_speed:
            raise CantDoThatError(f"{num} is greater than max speed ({self.fan.max_speed}).")
        elif num < self.min_speed:
            raise CantDoThatError(f"Int is less than min speed ({self.fan.min_speed}).")
