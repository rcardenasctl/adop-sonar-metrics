import xml.etree.ElementTree as ET
from sonar_exceptions import *

class SonarProjectMeasure:

    BADGES_MEASURE_ENDPOINT = "/api/badges/measure"

    MEASURE_COLLECTION = (
        "reliability_rating", 
        "security_rating", 
        "sqale_rating",
        "lines",
        "ncloc",
        "comment_lines_density",
        "function_complexity",
        "test_errors",
        "test_failures",
        "skipped_tests",
        "test_success_density",
        "coverage",
        "new_coverage",
        "it_coverage",
        "new_it_coverage",
        "overall_coverage",
        "new_overall_coverage",
        "duplicated_lines_density",
        "new_duplicated_lines_density",
        "blocker_violations",
        "critical_violations",
        "new_blocker_violations",
        "new_critical_violations",
        "code_smells",
        "new_code_smells",
        "bugs",
        "new_bugs",
        "vulnerabilities",
        "new_vulnerabilities",
        "sqale_debt_ratio",
        "new_sqale_debt_ratio",
        "new_maintainability_rating",
        "new_reliability_rating",
        "new_security_rating")

    # M"apping the relation between sonar category number (index) and category letter value.",
    MEASURE_CATEGORY_MAP = { 1.0:'A', 2.0:'B', 3.0:'C', 4.0:'D', 5.0:'E', -1.0: "N/A" }

    def __init__(self, sonar_monitor):
        self._sonar_monitor = sonar_monitor

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
        
        url = self._sonar_monitor.build_url(self.BADGES_MEASURE_ENDPOINT)
        res = self._sonar_monitor.get_response_by_params('get', url, **params)

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
        
        url = self._sonar_monitor.build_url(self.BADGES_MEASURE_ENDPOINT)
        
        for measure in self.MEASURE_COLLECTION:
            params['metric'] = measure
            res = self._sonar_monitor.get_response_by_params('get', url, **params)
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