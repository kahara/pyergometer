class Simulator:
    def __init__(self, factor=None):
        self.pulse = 0
        self.rpm = 0
        self.set_power = 0
        self.actual_power = 0
        
        # xxx set up the simulation part
        
    def status(self):
        # xxx
        self.pulse = 0
        self.rpm = 0
        self.set_power = 0
        self.actual_power = 0
        
    def power(self, watts):
        if watts < 25:
            watts = 25
        if watts > 400:
            watts = 400
        
        # xxx
