# this "simulator" if for basic testing of the system (so as not to
# annoy the test subject too much with non-functional software and
# hence repeated re-runs)


class Simulator:
    def __init__(self, pulse=135.0):
        self.pulse = pulse
        self.rpm = 50
        self.power = 0
        self.xpower = float(self.power)
        
    def status(self):
        pass
    
    def set_power(self, absolute=0.0, relative=0.0):
        if relative != 0.0:
            self.xpower += relative
        elif absolute > 0.0:
            self.xpower = absolute
        
        self.power = int(self.xpower)
