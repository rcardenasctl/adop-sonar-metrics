class MissingMeasuretKey(Exception):
    pass


class MissingMeasureMetric(Exception):
    pass


class MissingComponentParam(Exception):
    pass


class MissingMetricKeysParam(Exception):
    pass


class UnknowMeasureMetric(Exception):
    def __init__(self, unknown_metric):
        self.message = "Unknown metric [{}]".format(unknown_metric)


class InvalidAuthentication(Exception):
    def __init__(self):
        self.message = "Need to provide authentication credentials: Username/Password or Token"
