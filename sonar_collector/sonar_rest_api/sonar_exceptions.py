

class MissingMeasuretKey(Exception):
    pass

class MissingMeasureMetric(Exception):
    pass

class UnknowMeasureMetric(Exception):
    def __init__(self, unknown_metric):
        self.message = "Unknown metric [{}]".format(unknown_metric)