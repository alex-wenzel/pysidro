"""
Parent class for GTFS files, loads the file as a pandas DataFrame
"""

from pandas import read_csv

class GTFSFile:
    def __init__(self, file_path):
        """
        Read data as a DataFrame
        """
        self.data = read_csv(file_path)
