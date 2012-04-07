#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Control and logging program for Kettler ergometers"""

__appname__ = "pyergometer"
__author__  = "Joni Kähärä (kahara)"
__version__ = "0.0pre0"
__license__ = "GNU GPL 3.0 or later"

import logging
log = logging.getLogger(__name__)


import time, argparse
from kettler import Kettler
from session import Session
#from simulator import Simulator

        
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description=__doc__, version="v%s" % __version__)
    
    parser.add_argument('-d', '--device', action='store', dest='device', default=None, help='Serial device')
    parser.add_argument('-s', '--session', action='store', dest='session', default=None, help='Use this session file (jErgometer-like XML format)')
    parser.add_argument('-l', '--log', action='store', dest='log', default=None, help='Record session stats to this log file')
    parser.add_argument('-x', '--simulate', action='store', dest='simulate', default=0.5, type=float, help='Run session file against a simulated human with pulse reaction factor SIMULATE (0.0...1.0)')
    
    args  = parser.parse_args()
    
    if args.simulate:
        session = Session(session=args.session)
        #simulator = Simulator(factor=args.factor)
    
    #bike = Kettler(device=args.device)    
    # for power in range(25, 100, 5):
    #     print 'req power %d' % (power, )
    #     bike.power(power)   
    #     for i in range(0, 10):
    #         bike.status()
    #         print '%d bpm\t%d rpm\t%d/%d W' % (bike.pulse, bike.rpm, bike.set_power, bike.actual_power)
    #         time.sleep(1)
