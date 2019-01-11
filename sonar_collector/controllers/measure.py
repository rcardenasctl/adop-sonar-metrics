
class Measure:

    def __init__(self, client):
        self.client = client

    def get_all_measure_by_components(self, components):
        measure_results = {
            'ncloc': 0,
            'sqale_index': 0
        }

        for component in components:
            all_measures = self.client.get_all_measures(
                component_param=component['key'])

            for measure in all_measures:
                for key, value in measure.iteritems():
                    if key in measure_results:
                        measure_results[key] = measure_results[key] + \
                            int(measure[key])

        return measure_results
