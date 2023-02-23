import serial.tools.list_ports
import serial
import time


class GkSerial:
    def __init__(self, portname_in):
        self.connectionPort = portname_in
        self.connectionBaud = 115200
        try:
            self.connection = serial.Serial(self.connectionPort, self.connectionBaud, timeout=1)
        except serial.SerialException as e:
            self.connection = None
            print(e)

    def open(self):
        if not self.connection.is_open:
            try:
                self.connection.open()
            except serial.SerialException as e:
                print(e)
            except Exception as e:
                print(e)

    def commandsend(self, command_in):
        command_in = command_in + "\n"
        if self.connection:
            if not self.connection.is_open:
                self.open()
            if self.connection.is_open:
                self.connection.write(command_in.encode('ascii'))
                line = []
                time.sleep(0.025)   # 25ms delay to allow serial to flow
                while self.connection.in_waiting > 0:
                    line.append(self.connection.readline().decode('ascii').rstrip())
                self.connection.reset_input_buffer()
                self.connection.close()
                if line:
                    return line
        else:
            return None
