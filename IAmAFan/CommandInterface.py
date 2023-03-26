from IAmAFan.Fan import Fan

class CantDoThatError(Exception):
    pass


class CommandInterface:
    def __init__(self, fan: Fan):
        self.fan = fan

    def check_speed(self, num):
        if num > self.fan.max_speed:
            raise CantDoThatError(f"{num} is greater than max speed ({self.fan.max_speed})")
        elif num < self.fan.min_speed:
            raise CantDoThatError(f"Int is less than min speed ({self.fan.min_speed})")
    
    def set_fan_speed(self, speed: int):
        self.check_speed(speed)
        print(f"setting speed to {speed}")
        self.fan.write(str(speed).encode())

    def get_fan_speed(self) -> int:
        raise NotImplementedError("OVERRIDE ME")

    def _loop(self):
        print("Controlling the fan.")
        try:
            while True:
                speed = self.get_fan_speed()
                try:
                    self.set_fan_speed(speed)
                except CantDoThatError as e:
                    print(e)
        except KeyboardInterrupt:
            pass
    
    def start(self):
        self._loop()


class TerminalInput(CommandInterface):
    def get_fan_speed(self) -> int:
        speed = int(input("Set me a speed: "))
        return speed
