from sonar_monitor import SonarMonitor


class SonarComponentMonitor:

    COMPONENTS_SEARCH_ENDPOINT = '/api/components/search'

    def __init__(self, sonar_monitor):
        self._sonar_monitor = sonar_monitor

    def get_components(self, query_param=None, qualifiers=None):

        # query string definition
        params = {}
        if query_param:
            params['q'] = query_param

        if qualifiers:
            if not isinstance(qualifiers, str):
                qualifiers = ','.join(qualifiers)
            params['qualifiers'] = qualifiers.upper()

        page_index = 1
        page_size = 1
        page_total = 2

        params['p'] = page_index
        params['ps'] = page_size

        url = self._sonar_monitor.build_url(self.COMPONENTS_SEARCH_ENDPOINT)

        # Looping all the pages looking for components
        while page_index * page_size < page_total:
            # Update paging information for calculation
            res = self._sonar_monitor.get_response_by_params(
                'get', url, **params).json()
            page_index = res['paging']['pageIndex']
            page_size = res['paging']['pageSize']
            page_total = res['paging']['total']

            # Update page number (next) in queryset
            params['p'] = page_index + 1

            # Yield rules
            for component in res['components']:
                yield component
