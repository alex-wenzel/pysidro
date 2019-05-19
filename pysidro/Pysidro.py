"""
Driver script for the simulation
"""

from GTFS import GTFS
from Utils import timestamp2time, time2timestamp, log

log("Loading GTFS...")
gtfs = GTFS("../data/sample-feed/")
log("Loaded GTFS successfully")
