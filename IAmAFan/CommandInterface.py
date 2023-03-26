import socket


class CommandInterface:
    def get_fan_speed(self) -> int:
        raise NotImplementedError("OVERRIDE ME")

    def stop(self):
        pass

    def start(self):
        pass


class TerminalInput(CommandInterface):
    def get_fan_speed(self) -> int:
        speed = int(input("Set me a speed: "))
        return speed


class NetworkController(CommandInterface):
    def __init__(self, host, port):
        print(0)
        self.port = port
        self.host = host
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def start(self):
        self._bind()
        self._listen()

    def stop(self):
        self._socket.close()
        print("Connection closed.")

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

    def _bind(self):
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((self.host, self.port))
        print(f"Bound to {self.host}:{self.port}.")

    def _listen(self):
        self._socket.listen(1)
        print(f"Listening on port {self.port}...")
