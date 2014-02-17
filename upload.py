#!/usr/bin/env python

import boto
from boto.s3.bucket import Bucket
from boto.s3.key import Key
import os, json


def dirwalk(dir):
    for f in os.listdir(dir):
        fullpath = os.path.join(dir,f)
        if os.path.isdir(fullpath) and not os.path.islink(fullpath):
            for x in dirwalk(fullpath):
                yield x
        else:
            yield fullpath


bucketname = 'ergometria.async.fi'

connection = boto.connect_s3()
bucket = Bucket(connection, bucketname)
keynames = [key.name for key in bucket.get_all_keys(prefix='data/')]

datafile_uploaded = False
for filename in dirwalk('data/'):
    if not filename in keynames and not filename.endswith('.json'):
        datafile_uploaded = True
        print 'uploading', filename
        k = Key(bucket)
        k.key = filename
        k.set_contents_from_filename(filename)
        
        
if True: #datafile_uploaded:
    k = Key(bucket)
    k.key = 'data/index.json'
    sessions = []
    for key in bucket.get_all_keys(prefix='data/'):
        if key.name.endswith('.csv'):
            sessions.append(key.name)
    data = {
        'sessions': sessions,
        'overview': 'Time,Avg power (W),Total power (Wh),Avg rpm,Avg pulse,Avg target pulse\n'
        }
    
    for filename in dirwalk('data/'):
        if not filename.endswith('.json'):

            try:
                time = filename.split('/')[1].split('.')[0]
                nlines = 0
                power = 0
                rpm = 0
                pulse = 0
                target = 0
                for index, line in enumerate(open(filename).read().split('\n')):
                    if index > 0 and len(line) > 0:
                        nlines += 1
                        parts = line.split(',')
                        power += int(parts[1])
                        rpm += int(parts[2])
                        pulse += int(parts[3])
                        target += int(parts[4])
                total = power/3600
                power = power/nlines
                rpm = rpm/nlines
                pulse = pulse/nlines
                target = target/nlines

                data['overview'] += '%s,%d,%d,%d,%d,%d\n' % (time.split('T')[0], power, total, rpm, pulse, target)

            except:
                pass

    print 'uploading index', k.key
    k.set_contents_from_string(json.dumps(data), headers={'Content-Type': 'application/json'})
        
for filename in dirwalk('www/'):
    if filename in keynames or 'index.json' == filename or filename.endswith('.csv') or filename.startswith('www/.') or filename.startswith('www/#') or filename.endswith('~') or filename.startswith('www/data'):
        continue

    print 'uploading', filename, filename[4:]
    k = Key(bucket)
    k.key = filename[4:] #filename.split('/')[1]
    k.set_contents_from_filename(filename)

