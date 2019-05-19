"""
Python representation of the GTFS stop_times.txt file
"""

from GTFSFile import GTFSFile

class StopTimes(GTFSFile):
    def __init__(self, file_path):
        """
        Instantiate stop_times representation
        """
        GTFSFile.__init__(self, file_path)
