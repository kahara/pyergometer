import tempfile, shutil, os, sys, signal, datetime, time


class Ergometer:
    def __init__(self, device=None, session=None, log=None):
        self.device = device
        self.session = session
        if log:
            self.logtemp = tempfile.NamedTemporaryFile(mode='w', delete=False)
            self.log = log            
        else:
            self.logtemp = None
            self.log = None
    
    def run(self):
        self.pc = 0
        def handler(signum, frame):
            
            self.device.status()
            if self.device.rpm < 20 or self.device.pulse < 20:
                sys.stderr.write('On hold...\n')
                return
            
            step = self.session.step(self.pc)
            sys.stderr.write('%d/%d bpm\t%d W\t%d rpm\n' % (int(self.device.pulse), int(step['pulse']), int(self.device.power), self.device.rpm))            
            self.pc += 1
            
            if step['power'] > 0.0:
                self.device.set_power(absolute=step['power'])
            elif step['pulse'] > 0.0:
                r = (step['pulse']-self.device.pulse)/200.0
                self.device.set_power(relative=r)
                
        sys.stderr.write('Waiting for session to start')
        while True:
            self.device.status()
            if self.device.rpm < 20 or self.device.pulse < 20:
                sys.stderr.write('.')
                time.sleep(1.0)
            else:
                sys.stderr.write('..ok\n')
                self.begin = datetime.datetime.utcnow()
                break

        
        signal.signal(signal.SIGALRM, handler)
        signal.setitimer(signal.ITIMER_REAL, 1, 1)
        
        # loop here until session is finished
        while (datetime.datetime.utcnow() - self.begin).seconds < self.session.duration:
            time.sleep(0.01)
        
        self.end = datetime.datetime.utcnow()
        self.finish()
        
    def finish(self):
        if self.log:
            self.logtemp.close()
            shutil.copyfile(self.logtemp.name, self.log)
            os.remove(self.logtemp.name)
        sys.stderr.write('\nstart: ' + str(self.begin) + ' end: ' + str(self.end) + ' delta: ' + str((self.end-self.begin).seconds) + ' seconds\n')
