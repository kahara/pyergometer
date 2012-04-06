#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Control and logging program for Kettler ergometers"""

__appname__ = "pyergometer"
__author__  = "Joni Kähärä (kahara)"
__version__ = "0.0pre0"
__license__ = "GNU GPL 3.0 or later"

import logging
log = logging.getLogger(__name__)


import time
from kettler import Kettler

        
if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(description=__doc__, version="%%prog v%s" % __version__)
    parser.add_option('-d', '--device', action="store", dest="device",
        default='', help="Serial device.")
    parser.add_option('-v', '--verbose', action="count", dest="verbose",
        default=2, help="Increase the verbosity. Can be used twice for extra effect.")
    parser.add_option('-q', '--quiet', action="count", dest="quiet",
        default=0, help="Decrease the verbosity. Can be used twice for extra effect.")    
    
    opts, args  = parser.parse_args()
    
    bike = Kettler(device=opts.device)
    
    for power in range(25, 100, 5):
        print 'req power %d' % (power, )
        bike.power(power)
        
        for i in range(0, 10):
            bike.status()
            
            print '%d bpm\t%d rpm\t%d/%d W' % (bike.pulse, bike.rpm, bike.set_power, bike.actual_power)
            
            time.sleep(1)
