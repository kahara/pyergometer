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
from session import Session
from kettler import Kettler
from simulator import Simulator
from ergometer import Ergometer

        
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description=__doc__, version="v%s" % __version__)
    
    parser.add_argument('-s', '--session', action='store', dest='session', default=None, required=True, help='Use session file SESSION (jErgometer-like XML format)')
    parser.add_argument('-d', '--device', action='store', dest='device', default=None, help='Use serial device DEVICE')
    parser.add_argument('-l', '--log', action='store', dest='log', default=None, help='Record session stats to log file LOG')
    parser.add_argument('-x', '--simulate', action='store_true', dest='simulate', default=None, help='Run session file against a simulation')
    
    args  = parser.parse_args()
    
    if not args.session:
        parser.print_help()
        exit()
    
    session = Session(session=args.session)
    
    if args.simulate:
        simulator = Simulator()
        ergometer = Ergometer(device=simulator, session=session, log=args.log)
    elif args.device:
        kettler = Kettler(device=args.device)
        ergometer = Ergometer(device=kettler, session=session, log=args.log)
    else:
        parser.print_help()
        exit()

    ergometer.run()
