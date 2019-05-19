"""
This script implements an interface with the One Bus Away API to pull and 
parse data from an OBA GTFS real-time feed, This class also implements
parsers to return all retrieved data as useful pandas DataFrames
"""

from google.transit import gtfs_realtime_pb2
import pandas as pd
import requests
import sys

class OBA:
    """
    This class implements methods to retrieve One Bus Away API data and
    parse it into pandas DataFrames
    """
    def __init__(self, conf_path):
        """
        Takes a path to a config file with 2 urls for trip updates and system 
        alerts as well as a 3rd line for an API key and test-queries the feed.

            conf_path (str): Path to a config file with format as 
                                described above

            returns: None
        """
        self.conf_path = conf_path
        self.trip_update_url = ""
        self.system_alert_url = ""
        self.api_key = ""

        self.load_config()

    """
    Load Config
    """

    def load_config(self):
        """
        Populates the URL fields and API key field

            returns: None
        """
        conflines = [line.strip('\n') 
                        for line in open(self.conf_path).readlines()]
        self.trip_update_url = conflines[0]
        self.system_alert_url = conflines[1]
        self.api_key = conflines[2]

    """
    Query Feed
    """

    def query(self, qrtype, qrtes):
        """
        Issues queries to the three realtime update feeds and returns
        three DataFrames with the resulting data

            returns ((pd.DataFrame, pd.DataFrame, pd.DataFrame)): Parsed data
        """
        trip_updates_pb = self.query_trip_update()
        #alert_pb = self.query_system_alert()

        trip_updates_df = self.parse_trip_updates(trip_updates_pb)
        #alerts_df = self.parse_system_alerts(alert_pb)
      
        trip_updates_df['veh_id'] = trip_updates_df['veh_id'].astype(int)
        trip_updates_df['rte_id'] = trip_updates_df['rte_id'].astype(int)
        print(trip_updates_df[trip_updates_df[qrtype].isin(qrtes)].sort_values(by="veh_id"))  #Debug
        #print(trip_updates_df[trip_updates_df['delay']>0])
        sys.exit(1)  #Debug

        return trip_updates_df, vehicle_pos_df, alerts_df

    def query_trip_update(self):
        """
        Returns the Python representation of the GTFS feed for trip updates

            returns (gtfs_realtime_pb2.FeedMessage): Python repr of pb data
        """
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get(self.trip_update_url+"?key="+self.api_key)
        feed.ParseFromString(response.content)
        return feed

    """
    Parsing Functions
    """

    def parse_trip_updates(self, tu_feed):
        """
        This function converts the protocol buffer data from trip updates into
        a useful pandas DataFrame

            tu_feed (gtfs_realtime_pb2.FeedMessage): Python repr of pb data

            returns (pd.DataFrame): Pandas representation of pb data
        """
        tu_d = {
            "trip_id": [], "rte_id": [], "ns_id": [],
            "ns_depart": [], "veh_id": [], "delay": [],
            "ts": []
        }
        for e in tu_feed.entity:
            tu_d['trip_id'].append(e.trip_update.trip.trip_id)
            tu_d['rte_id'].append(e.trip_update.trip.route_id)
            tu_d['ns_id'].append(e.trip_update.stop_time_update[0].stop_id)
            tu_d['ns_depart'].append(e.trip_update.stop_time_update[0].departure.time)
            tu_d['veh_id'].append(e.trip_update.vehicle.id)
            tu_d['delay'].append(e.trip_update.delay)#/60.0)
            tu_d['ts'].append(e.trip_update.timestamp)
        return pd.DataFrame(tu_d).set_index('trip_id')


if __name__ == "__main__":
    print("OBA.py")
    qrtype = sys.argv[1]
    qrtes = sys.argv[2].split(',')
    if len(qrtes) > 1 or "-" in qrtes[0]:
        for qr in qrtes:
            if type(qr) == int:
                continue
            elif str(qr)[-1] == "-":
                qrtes += list(range(int(qr[:-1]+"00"), int(qr[:-1]+"99")))
            else:
                qrtes += int(qr)
    oba = OBA("private_conf.txt")
    oba.query(qrtype, qrtes)
