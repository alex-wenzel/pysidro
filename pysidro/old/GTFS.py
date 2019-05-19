"""
A pandas-based GTFS parser and query engine
"""

import pandas as pd
import sys

class GTFS:
    """
    A pandas-based GTFS parser and query engine
    """
    def __init__(self, dirpath):
        """
        Loads GTFS files into a DataFrame

            dirpath (str): Path containing GTFS files

            returns: None
        """
        self.dirpath = dirpath

        self.routes = self.load_gtfs_file(self.dirpath+"routes.txt", "route_id")

        self.stop_times = self.load_gtfs_file(self.dirpath+"stop_times.txt", None)
        
        self.stops = self.load_gtfs_file(self.dirpath+"stops.txt", "stop_id")

        self.trips = self.load_gtfs_file(self.dirpath+"trips.txt", "trip_id")

        self.calendar_dates = self.load_gtfs_file(self.dirpath+"calendar_dates.txt", None)
        self.calendar_dates['date'] = self.calendar_dates['date'].astype(str)

    def load_gtfs_file(self, filepath, index):
        """
        Returns a DataFrame of the GTFS file at fpath
        with indx_col set as the index

            filepath (str): Path to a GTFS csv
            index (str): Name of the column to set as the index
        """
        df = pd.read_csv(filepath)
        if index != None:
            return df.set_index(index)
        else:
            return df

    """
    Get all trips for a day
    """

    def get_trips_day(self, day):
        """
        Gets all of the trips that are scheduled to be run
        on a specific day

            day (str): A date in the format YYYMMDD

            returns (pd.DataFrame): The trips scheduled for that day
        """
        service_ids = self.calendar_dates[self.calendar_dates['date']==day]['service_id']
        return self.trips[self.trips['service_id'].isin(service_ids)]

    """
    Get list of blocks covering a group of trips
    """

    def get_blocks_from_trips(self, trips):
        """
        Gets a list of the block ids covering a group of trips

            trips (pd.DataFrame): Some subset of self.trips

            returns ([str]): List of block IDs in these trips
        """
        return list(set(trips['block_id']))

    def get_block_trips(self, trips, block_id):
        """
        Gets a list of trips from a block_id

            block_id (str): ID for a block

            returns (pd.DataFrame): Subset of trips
        """
        return trips[trips['block_id']==block_id]

    def get_stop_times_from_trips(self, trips):
        """
        Gets a subset of self.stop_times for given trip_ids

            trips (pd.DataFrame): Some subset of self.trips

            returns (pd.DataFrame): Subset of stop_times
        """
        st = self.stop_times[self.stop_times['trip_id'].isin(set(trips.index))]
        return st.sort_values(by="departure_time")

    def get_terminal_times_from_stop_times(self, stop_times):
        """
        Retrieves the stop times that occur at route terminals from a 
        DataFrame of stop times sorted by time
        """
        terminal_indices = []
        for trip_id in set(stop_times['trip_id']):
            trip_stops = stop_times[stop_times['trip_id']==trip_id]
            terminal_indices.append(trip_stops.iloc[0,:].name)
            terminal_indices.append(trip_stops.iloc[-1,:].name)
        return stop_times.loc[terminal_indices,:].sort_values(by='departure_time')

if __name__ == "__main__":
    gtfs = GTFS("../sdmts_gtfs/sdmts_gtfs_WI2019/")

    #todays_trips = gtfs.get_trips_day("20190307")
    #todays_202s = todays_trips[todays_trips['route_id']=="202"]
    #todays_202_blocks = gtfs.get_blocks_from_trips(todays_202s)
    #some_202_blocks_trips = gtfs.get_block_trips(todays_202_blocks[5])
    #this_202s_stop_times = gtfs.get_stop_times_from_trips(some_202_blocks_trips)
    #print(this_202s_stop_times)

    trip_id = sys.argv[1]
    todays_trips = gtfs.get_trips_day("20190424")
    block_id = gtfs.get_blocks_from_trips(todays_trips.loc[[trip_id],:])[0]
    block_trips = gtfs.get_block_trips(todays_trips, block_id)
    block_stop_times = gtfs.get_stop_times_from_trips(block_trips)
    block_term_times = gtfs.get_terminal_times_from_stop_times(block_stop_times)
    trip_rte_d = todays_trips['route_id'].to_dict()
    block_term_times['route_id'] = block_term_times['trip_id'].map(trip_rte_d)
    print(block_term_times)