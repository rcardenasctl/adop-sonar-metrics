import json


class IssueClient:

    ISSUES_ENDPOINT = "/api/issues/search"

    SEVERITIES_COLLECTION = (
        'MAJOR', 'CRITICAL', 'BLOCKER'
    )

    def __init__(self, controller_client):
        self._controller_client = controller_client

    def get_critical_severity(self, component_keys_param=None):

        SEVERITY = ('CRITICAL')
        response = self.get_issues_by_severities(
            component_keys_param, severities_param=SEVERITY)

        total = response['paging']['total']
        return total

    def get_blocker_severity(self, component_keys_param=None):

        SEVERITY = ('BLOCKER')
        response = self.get_issues_by_severities(
            component_keys_param, severities_param=SEVERITY)

        total = response['paging']['total']
        return total

    def get_major_severity(self, component_keys_param=None):

        SEVERITY = ('MAJOR')
        response = self.get_issues_by_severities(
            component_keys_param, severities_param=SEVERITY)

        total = response['paging']['total']
        return total

    def get_issues_by_severities(self, component_keys_param=None, severities_param=None):

        # query string definition
        params = {}
        if component_keys_param:
            params['componentKeys'] = component_keys_param
        else:
            raise MissingComponentParam()

        if severities_param:
            if not isinstance(severities_param, str):
                severities_param = ','.join(severities_param)
        else:
            severities_param = ','.join(self.SEVERITIES_COLLECTION)

        params['severities'] = severities_param

        url = self._controller_client.build_url(self.ISSUES_ENDPOINT)

        res = self._controller_client.get_response_by_params(
            'get', url, **params)

        response_data = json.loads(res.text)

        return response_data
