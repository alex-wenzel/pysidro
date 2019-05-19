"""
Simulation management and data conversion utilities
"""

"""
Functions to convert from clock time to timestamp and reverse
"""

def time2timestamp(time):
    """
    Converts a time in the format HH:MM:SS to an integer timestamp
    where 0 indicates midnight on the start of the service day and
    > 86399 indicates times extending into the next calendar day (i.e.,
    service running past midnight)

        time (str): Time in format HH:MM:SS

        returns (int): Timestamp
    """
    hour, minute, second = list(map(int, time.split(':')))
    return (3600*hour) + (60*minute) + second

def timestamp2time(timestamp):
    """
    Converts an integer timstamp to a string giving the time in
    the format "HH:MM:SS". See time2timestamp() docstring for specifics
    on time format and what happens when you feed buses after midnight
    """
    hour, remainder = divmod(timestamp, 3600)
    minute, second = divmod(remainder, 60)
    return "{:02d}:{:02d}:{:02d}".format(hour, minute, second)

if __name__ == "__main__":
    print(time2timestamp("24:00:01") == 86401)
    print(timestamp2time(86401) == "24:00:01")

"""
Logging functions
"""

def log(message, timestamp=None):
    """
    Prints a logging message with an optional simulation time timestamp

        message (str): message to print
        timestamp (int|str|None): Simulation time - if passed as an int,
                                timestamp2time() will be called

        returns: None
    """
    if timestamp is None:
        timestamp = "--:--:--"
    if type(timestamp) is int:
        timestamp = timestamp2time(timestamp)
    print("[{}]: {}".format(timestamp, message))
