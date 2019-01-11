class Issue:
    def __init__(self, client):
        self.client = client
        self.issues_results = {
            'violation_critical': 0,
            'violation_major': 0,
            'violation_blocker': 0
        }

    def get_all_issue_severity_per_component(self, components):

        for component in components:
            critical = self.client.get_critical_severity(
                component_keys_param=component['key'])

            major = self.client.get_major_severity(
                component_keys_param=component['key'])

            blocker = self.client.get_blocker_severity(
                component_keys_param=component['key'])

            self._update_issues('violation_critical', critical)
            self._update_issues('violation_major', major)
            self._update_issues('violation_blocker', blocker)

        return self.issues_results

    def _update_issues(self, violation_index, violation_value):
        self.issues_results[violation_index] = self.issues_results[violation_index] + \
            int(violation_value)
