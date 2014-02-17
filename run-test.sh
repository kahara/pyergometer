#!/bin/sh

FILENAME=`date +'%Y-%m-%dT%H:%M:%S'`
./pyergometer.py --session session-test.xml --device /dev/ttyUSB0 --log ./data-test/$FILENAME.json
./dumplog.py ./data-test/$FILENAME.json >./data-test/$FILENAME.csv
#./upload.py
