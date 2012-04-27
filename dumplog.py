#!/usr/bin/env python

import json, sys, datetime

try:
    log = json.loads(open(sys.argv[1]).read())
except:
    print 'usage, it goes here'
    exit()

t = datetime.datetime.strptime(log['begin'], '%Y-%m-%dT%H:%M:%S')

print '%s,%s,%s,%s,%s' % ('Time', 'Power (W)', 'Rpm', 'Pulse', 'Target pulse')

for step in log['steps']:
    print '%s,%d,%d,%d,%d' % (t.strftime('%Y-%m-%dT%H:%M:%S'), int(step['power']), int(step['rpm']), int(step['pulse']), int(step['target_pulse']))
    t += datetime.timedelta(0, 1)
