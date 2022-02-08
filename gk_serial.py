import serial.tools.list_ports
import serial
import time


class GkSerial:
    def __init__(self, portname_in):
        self.connection = serial.Serial()
        self.connectionState = 0
        self.connectionPort = portname_in
        self.connectionBaud = 115200

    def connect(self):
        self.connection.close()
        self.connection = serial.Serial(self.connectionPort, self.connectionBaud, timeout=1)
        self.connection.write("deviceinfo\n".encode('ascii'))
        time.sleep(0.010)   # 10ms delay to allow serial to flow
        line = self.connection.readline().decode('ascii').rstrip()
        if line == 'gameKey':
            print('gameKey connected on port', self.connectionPort)
            self.connectionPort = 1
            return self.connectionPort
        else:
            print('gameKey connection failure on port', self.connectionPort)
            return None

    def scangk(self):
        comports = list(serial.tools.list_ports.comports())
        for x in comports:
            print('Attempting to check device', x.device, ':', x.hwid)
            try:
                ser = serial.Serial(x.device, self.connectionBaud, timeout=1)
                ser.write("deviceinfo\n".encode('ascii'))
                time.sleep(0.010)   # 10ms
                line = ser.readline().decode('ascii').rstrip()
                ser.close()
                if line == 'gameKey':
                    print('gameKey detected on port', x.device)
                    fdeviceport = x.device
                    return fdeviceport
                else:
                    print('no device detected on', x.device)
            except serial.SerialException as e:
                print(e)
