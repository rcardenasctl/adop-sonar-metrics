import requests
from status_codes import *
from http_exceptions import *
from exceptions import InvalidAuthentication
import logging

logger = logging.getLogger('sonar-logs')


class ControllerClient:

    def __init__(self, sonar_host=None, sonar_port=None, sonar_base_path=None, username=None, password=None):

        self._sonar_host = sonar_host
        self._sonar_port = sonar_port
        self._sonar_base_path = sonar_base_path
        self._session = requests.Session()

        logger.info("Create client controller for sonar server: {}{}".format(
            self._sonar_host, self._sonar_base_path))

        if username != None:
            # password is empty when username works as token id.
            # So credentials works like:
            #       self._session.auth = token, '' where token is username
            self._session.auth = username, password
            logger.info(
                "Creating credentials with username/password")
        else:
            raise InvalidAuthentication()

    def build_url(self, endpoint):
        new_url = None
        if self._sonar_port:
            new_url = '{}:{}{}{}'.format(
                self._sonar_host, self._sonar_port, self._sonar_base_path, endpoint)
        else:
            new_url = '{}{}{}'.format(
                self._sonar_host, self._sonar_base_path, endpoint)
        return new_url

    def get_response_by_params(self, method, url, **params):
        # Get method and make the call
        call = getattr(self._session, method.lower())
        self._session.params = params

        logger.info("Calling endpoint: {url} with params {params}" .format(
            url=url, params=params))
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
