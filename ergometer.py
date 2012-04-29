import tempfile, shutil, os, sys, signal, datetime, time, json


class Ergometer:
    def __init__(self, device=None, session=None, log=None):
        self.device = device
        self.session = session
        self.pc = 0
        
        if log:
            self.logtemp = tempfile.NamedTemporaryFile(mode='w', delete=False)
            self.log = log            
            
        else:
            self.logtemp = None
            self.log = None
    
    def run(self):
        def handler(signum, frame):
            
            self.device.status()
            if self.device.rpm < 20 or self.device.pulse < 20:
                sys.stderr.write('.')
                return
            
            step = self.session.step(self.pc)
            sys.stderr.write('\n%d/%d bpm\t%d W\t%d rpm' % (int(self.device.pulse), int(step['pulse']), int(self.device.power), self.device.rpm))
            
            self.logtemp.write('%d %d %d %d\n' % (int(self.device.pulse), int(step['pulse']), int(self.device.power), int(self.device.rpm)))
            self.logtemp.flush()
            
            self.pc += 1
            if step['power'] > 0.0:
                self.device.set_power(absolute=step['power'])
            elif step['pulse'] > 0.0:
                
                diff  = step['pulse'] - self.device.pulse
                if diff <= 0 and diff >= -5.0:
                    return
                
                absdiff = abs(diff)
                
                if absdiff > 10.0:
                    r = 0.25
                elif absdiff > 5.0:
                    r = 0.125
                elif absdiff > 0.0:
                    r = 0.025
                else:
                    r = 0.0
                
                self.device.set_power(relative = r if diff > 0 else -r)
                
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
        print '\nfinishing...'
        
        self.device.pulse = 0
        self.session.step(self.pc)['pulse'] = 0
        self.device.power = 0
        self.device.rpm = 0
        
        if self.log:
            self.logtemp.close()
            
            fmt = '%Y-%m-%dT%H:%M:%S'
            
            data = {
                'begin': self.begin.strftime(fmt),
                'end': self.end.strftime(fmt),
                'duration': self.session.duration,
                'name': self.session.name,
                'steps': []
                }
            for line in open(self.logtemp.name).read().split('\n'):
                if len(line) < 1:
                    continue
                
                parts = line.split(' ')
                step = {
                    'pulse': parts[0],
                    'target_pulse': parts[1],
                    'power': parts[2],
                    'rpm': parts[3]
                    }
                data['steps'].append(step)
            
            open(self.log, 'w').write(json.dumps(data))                
            os.remove(self.logtemp.name)
        
        exit()
