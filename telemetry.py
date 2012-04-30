import threading
from time import sleep
import boto
from boto.s3.bucket import Bucket
from boto.s3.key import Key
from boto.cloudfront import CloudFrontConnection
import json, datetime, signal


class Telemetry(threading.Thread):
    def __init__(self, ergometer=None, session=None):
        threading.Thread.__init__(self)
        self.ergometer = ergometer
        self.session = session
        self.running = True

        self.connection = boto.connect_s3()
        self.bucket = Bucket(self.connection, 'ergometria.async.fi')
        self.k = Key(self.bucket)
        self.k.key = 'live/latest.json'

    def write_data(self, timestamp=datetime.datetime.utcnow, pulse=0, target_pulse=0, power=0, rpm=0):
        data = {
            'timestamp': timestamp.strftime('%Y-%m-%dT%H:%M:%S+0000'),
            'pulse': pulse,
            'target_pulse': target_pulse,
            'power': power,
            'rpm': rpm
            }
        print data
        f = open('www/' + self.k.key, 'w')
        f.write(json.dumps(data))
        f.close()
        self.k.set_contents_from_filename('www/' + self.k.key, headers={'Cache-Control': 'max-age=0'})
        
        
    def run(self):
        
        while True:
            self.write_data(timestamp = datetime.datetime.utcnow(),
                            pulse = self.ergometer.device.pulse,
                            target_pulse = self.session.step(self.ergometer.pc)['pulse'],
                            power = self.ergometer.device.power,
                            rpm = self.ergometer.device.rpm)
            
            sleep(0.5)
            
            if not self.running:
                self.k.delete()
                return
