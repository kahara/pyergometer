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
    keynames = []
    for key in bucket.get_all_keys(prefix='data/'):
        print key.name
        if key.name.endswith('.csv'):
            keynames.append(key.name)
    print 'uploading index', k.key
    k.set_contents_from_string(json.dumps(keynames), headers={'Content-Type': 'application/json'})
    
    
for filename in dirwalk('www/'):
    if filename in keynames or 'index.json' == filename or filename.endswith('.csv') or filename.startswith('www/.') or filename.startswith('www/#') or filename.endswith('~') or filename.endswith('-combined.js') or filename.endswith('-min.js'):
        continue

    print 'uploading', filename
    k = Key(bucket)
    k.key = filename.split('/')[1]
    k.set_contents_from_filename(filename)
