import xml.etree.ElementTree as ET
from exceptions import *


class SvgBadgesClient:

    BADGES_MEASURE_ENDPOINT = "/api/badges/measure"

    MEASURE_COLLECTION = (
        "lines",
        "ncloc",
        "coverage",
        "it_coverage",
        "overall_coverage",
        "blocker_violations",
        "critical_violations",
        "vulnerabilities",
        "new_vulnerabilities",
        "sqale_debt_ratio")

    # M"apping the relation between sonar category number (index) and category letter value.",
    MEASURE_CATEGORY_MAP = {1.0: 'A', 2.0: 'B',
                            3.0: 'C', 4.0: 'D', 5.0: 'E', -1.0: "N/A"}

    def __init__(self, controller_client):
        self._controller_client = controller_client

    def get_measure(self, key_param=None, metric_param=None):

        # query string definition
        params = {}
        if key_param:
            params['key'] = key_param
        else:
            raise MissingMeasureKey()

        if metric_param:
            if metric_param not in self.MEASURE_COLLECTION:
                raise UnknowMeasureMetric(metric_param)
            else:
                params['metric'] = metric_param
        else:
            raise MissingMeasureMetric()

        url = self._controller_client.build_url(self.BADGES_MEASURE_ENDPOINT)
        res = self._controller_client.get_response_by_params(
            'get', url, **params)

        measure_value = self.get_measure_value(res.text)
        return {
            metric_param: measure_value
        }

    def get_all_measures(self, key_param=None):
        # query string definition
        params = {}
        if key_param:
            params['key'] = key_param
        else:
            raise MissingMeasureKey()

        url = self._controller_client.build_url(self.BADGES_MEASURE_ENDPOINT)

        for measure in self.MEASURE_COLLECTION:
            params['metric'] = measure
            res = self._controller_client.get_response_by_params(
                'get', url, **params)
            measure_value = self.get_measure_value(res.text)
            measure_category = self.get_measure_category(measure_value)
            if measure_category is None:
                yield {
                    measure: measure_value
                }
            else:
                yield {
                    measure: measure_value,
                    "{}_category".format(measure): measure_category
                }

    def get_measure_category(self, value):
        if value in self.MEASURE_CATEGORY_MAP:
            return self.MEASURE_CATEGORY_MAP[value]

    def get_measure_value(self, xml):
        xml_data = ET.fromstring(xml)
        value = xml_data[3][2].text
        if value == "N/A":
            return -1.0
        if '%' in value:
            value = value.split('%')[0]
        return float(value)
