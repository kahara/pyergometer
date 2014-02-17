#!/bin/sh

FILENAME=`date +'%Y-%m-%dT%H:%M:%S'`
./pyergometer.py --session session-test.xml --device /dev/ttyUSB0 --log ./data-test/$FILENAME.json
#./dumplog.py ./data/$FILENAME.json >./data/$FILENAME.csv
#./upload.py
