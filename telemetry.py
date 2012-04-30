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
        
    def run(self):
        connection = boto.connect_s3()
        bucket = Bucket(connection, 'ergometria.async.fi')
        k = Key(bucket)
        k.key = 'live/latest.json'
        
        while True:
            if not self.running:
                return
            
            data = {
                'timestamp': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+0000'),
                'pulse': self.ergometer.device.pulse,
                'target_pulse': self.session.step(self.ergometer.pc)['pulse'],
                'power': self.ergometer.device.power,
                'rpm': self.ergometer.device.rpm,
                }
            f = open('www/' + k.key, 'w')
            f.write(json.dumps(data))
            f.close()
            k.set_contents_from_filename('www/' + k.key, headers={'Cache-Control': 'max-age=0'})
            sleep(1)
