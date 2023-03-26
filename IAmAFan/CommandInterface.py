# Interface for controlling fans
import serial

class CantDoThatError(Exception):
    pass

def _is_8_bit(num: int):
    if num > 255:
        raise CantDoThatError(f"Int is too big for 8 bits: {num}")
    elif num < 0:
        raise CantDoThatError(f"Int is less than 0: {num}")
    return num


class CommandInterface:
    def __init__(self, fan: serial.Serial):
        self.fan = fan
    
    def set_fan_speed(self, speed: _is_8_bit):
        print(f"setting speed to {speed}")
        self.fan.write(str(speed).encode())

    def get_fan_speed(self) -> int:
        raise NotImplementedError("OVERRIDE ME")

    def _loop(self):
        print("Waiting to set the fan speed")
        try:
            while True:
                speed = self.get_fan_speed()
                self.set_fan_speed(speed)
        except KeyboardInterrupt:
            pass
    
    def start(self):
        self._loop()


class TerminalInput(CommandInterface):
    def get_fan_speed(self) -> int:
        speed = int(input("Set me a speed: "))
        return speed
