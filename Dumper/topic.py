
class Topic:
    def __init__(self,t_name,ofset,timestamp):
        self.t_name = t_name
        self.ofset = ofset
        self.ar = None
        self.timestamp = timestamp
    
    def calc_ar(self, latest_ofset, latest_timestamp):
        time_sec = (latest_timestamp - self.timestamp).total_seconds()
        ofset_diff = latest_ofset - self.ofset
        self.ar = ofset_diff/time_sec

    def __str__(self):
        pass