import serial, time


class Kettler():
    def __init__(self, device=None):
        self.device = device
        
        self.pulse = 0
        self.rpm = 0
        self.power = 0
        self.xpower = float(self.power)
        
        self.serialport = serial.Serial(self.device, 9600, timeout=0.1)

        if not self.device:
            raise NameError, 'Serial port not specified'
        
        if not self.serialport.isOpen():
            raise IOError, 'Serial port could not be opened'
        
        time.sleep(1)

        self.serialport.write('RS\r\n')
        time.sleep(5)
        if not self.serialport.readline().startswith('ACK'):
            raise IOError, 'Could not connect to bike'

        self.serialport.write('CM\r\n')
        time.sleep(1)
        if not self.serialport.readline().startswith('ACK'):
            raise IOError, 'Could not connect to bike'
        
    def status(self):
        self.serialport.write('ST\r\n')
        parts = self.serialport.readline().rstrip('\r\n').split('\t')
        self.pulse = int(parts[0], 10)
        self.rpm = int(parts[1], 10)
        
    def set_power(self, absolute=0.0, relative=0.0):        
        if relative != 0.0:
            self.xpower += relative
        elif absolute > 0.0:
            self.xpower = absolute
        
        self.power = int(self.xpower)

        watts = self.power
        if watts < 25:
            watts = 25
        if watts > 400:
            watts = 400

        self.serialport.write('PW ' + str(int(watts)) + '\r\n')
