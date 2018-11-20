import requests
import default
from status_codes import *
from http_exceptions import *


class SonarMonitor:
    
    def __init__(self, sonar_host=None, sonar_port=None, sonar_base_path=None, sonar_token=None):

        self._sonar_host = sonar_host or default.SONAR_HOST
        self._sonar_port = sonar_port or default.SONAR_PORT
        self._sonar_base_path = sonar_base_path or default.SONAR_BASE_PATH
        self._session = requests.Session()

        if sonar_token:
            self._session.auth = sonar_token, ''

    def build_url(self, endpoint):
        if self._sonar_port:
            return '{}:{}{}{}'.format(self._sonar_host, self._sonar_port, self._sonar_base_path, endpoint)
        return '{}{}{}'.format(self._sonar_host, self._sonar_base_path, endpoint)
    
    def get_response_by_params(self, method, url, **params):
        # Get method and make the call
        call = getattr(self._session, method.lower())
        self._session.params = params
        res = call(url)

        if res.status_code < HTTP_300:
            # OK, return http response
            return res
        elif res.status_code in (HTTP_401, HTTP_403):
            # Authentication error. Need to verify username/password or token
            raise AuthenticationError(res.reason)
        elif res.status_code == HTTP_404:
            # Need to check the endpoint provided
            raise NotFoundError(res.reason)
        elif res.status_code < HTTP_500:
            # Any other 4xx, it is reported as a generic client error
            print(res.status_code)
            raise ClientError(res.reason)
        else:
            # 5xx is server error
            raise ServerError(res.reason)