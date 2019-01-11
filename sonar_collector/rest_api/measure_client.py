from exceptions import MissingComponentParam
from exceptions import MissingMetricKeysParam
import json


class MeasureClient:

    MEASURE_ENDPOINT = "/api/measures/component"

    MEASURE_COLLECTION = (
        'ncloc',  # Lines of code
        'sqale_index'  # technical debts
    )

    def __init__(self, client):
        self._client = client

    def get_all_measures(self, component_param=None, metric_keys_param=None):

        # query string definition
        params = {}
        if component_param:
            params['component'] = component_param
        else:
            raise MissingComponentParam()

        if metric_keys_param:
            if not isinstance(metric_keys_param, str):
                metric_keys_param = ','.join(metric_keys_param)
        else:
            metric_keys_param = ','.join(self.MEASURE_COLLECTION)

        params['metricKeys'] = metric_keys_param

        url = self._client.build_url(self.MEASURE_ENDPOINT)

        res = self._client.get_response_by_params(
            'get', url, **params)

        response_data = json.loads(res.text)

        for measure in response_data['component']['measures']:
            metric = measure['metric']
            value = measure['value']
            yield {
                metric: value
            }
