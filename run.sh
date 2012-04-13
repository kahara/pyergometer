#!/bin/sh
./pyergometer.py --session session.xml --device /dev/tty.usbserial-FTUKKECU --log ./log/`date +'%Y-%m-%dT%H:%M:%S'`.log
