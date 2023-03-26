import re
import socket

from IAmAFan.Fan import Fan

class CantDoThatError(Exception):
    pass


class CommandInterface:
    def __init__(self, fan: Fan):
        self.fan = fan

    def check_speed(self, num):
        try:
            num = int(num)
        except ValueError:
            raise CantDoThatError(f"{num} is not an integer.")
        if num > self.fan.max_speed:
            raise CantDoThatError(f"{num} is greater than max speed ({self.fan.max_speed}).")
        elif num < self.fan.min_speed:
            raise CantDoThatError(f"Int is less than min speed ({self.fan.min_speed}).")
    
    def set_fan_speed(self, speed: int):
        self.check_speed(speed)
        print(f"setting speed to {speed}")
        self.fan.write(str(speed).encode())
        self.fan.cur_speed = speed

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
        except Exception as e:
            print(f"Something happened: {e}")
        finally:
            self.stop()
    
    def start(self):
        self._loop()

    def stop(self):
        pass


class TerminalInput(CommandInterface):
    def get_fan_speed(self) -> int:
        speed = int(input("Set me a speed: "))
        return speed


class NetworkController(CommandInterface):
    def __init__(self, fan: Fan, host, port):
        super().__init__(fan)
        self.port = port
        self.host = host
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind()
        self.listen()

    def get_fan_speed(self) -> int:
        conn, _ = self._socket.accept()
        data = conn.recv(512).decode()
        headers, body = data.split('\r\n\r\n')
        num = body.strip()
        try:
            # attempt to convert the received data to an integer
            num = int(num)
            print(f"Received integer: {num}.")
            return num
        except ValueError:
            print("Invalid input received.")
            return self.fan.cur_speed or 0

    def stop(self):
        self._socket.close()
        print("Connection closed.")

    def bind(self):
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((self.host, self.port))
        print(f"Bound to {self.host}:{self.port}.")

    def listen(self):
        self._socket.listen(1)
        print(f"Listening on port {self.port}...")
