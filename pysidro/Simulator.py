"""
Class for managing the simulation based on GTFS input
"""

from GTFS import GTFS
from Utils import log, time2timestamp, timestamp2time

class Simulator:
    def __init__(self, gtfs_dir_path):
        log("Loading GTFS...")
        self.gtfs = GTFS(gtfs_dir_path)
        log("Loaded GTFS successfully")
