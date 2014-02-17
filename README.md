pyergometer
===========

This program connects to a Kettler ergometer (tested with model E3)
through a serial connection and, following a user-specified program, controls the
ergometer power setting to keep the subject's heart rate at a desired level (which
may or may not vary during the program run).

The program can also run in "fixed" mode, i.e. setting power levels at
set times given in the user program.

Pulse, power and pedaling rpm are optionally recorded to a log file
that can be used to e.g. visualize the run afterwards.

Motivation
----------

I could not get [jErgometer](https://github.com/xylo/JErgometer) to work in
Mac OS X 10.6. That is, the program basically worked ok but the Java serial comms
(RXTXserial) tended to be too unstable.
