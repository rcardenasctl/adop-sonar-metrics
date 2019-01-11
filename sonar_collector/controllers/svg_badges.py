

class SvGBadges:
    def __init__(self, client):
        self.client = client

    def get_all_measure_by_components(self, components):
        for component in components:
            all_measures = self.client.get_all_measures(
                key_param=component['key'])

            for measure in all_measures:
                component.update(measure)
            yield component
