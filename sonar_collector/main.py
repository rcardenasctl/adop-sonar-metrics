from rest_api.controller_client import ControllerClient
from rest_api.component_client import ComponentClient
from rest_api.svg_badges_client import SvgBadgesClient
from rest_api.exceptions import UnknowMeasureMetric
from rest_api.http_exceptions import *
import serializer.logger
import watcher.logger
import logging
import os


def main():

    SONAR_HOST = os.environ.get('SONAR_HOST')
    SONAR_USERNAME = os.environ.get('SONAR_USERNAME')
    SONAR_PASSWORD = os.environ.get('SONAR_PASSWORD')
    SONAR_LOGS_PATH = os.environ.get('SONAR_LOGS_PATH')
    SONAR_DATA_LOGS = os.environ.get('SONAR_DATA_LOGS')

    watcher.logger.init(SONAR_LOGS_PATH)
    logger = logging.getLogger('sonar-logs')

    controller_client = ControllerClient(
        sonar_host=SONAR_HOST, sonar_base_path="/sonar", username=SONAR_USERNAME, password=SONAR_PASSWORD)

    component_client = ComponentClient(controller_client)
    svg_measures_client = SvgBadgesClient(controller_client)

    COMPONENTS_QUALIFIERS = ('TRK')

    try:
        components = component_client.get_components(
            qualifiers=COMPONENTS_QUALIFIERS)

        for component in components:
            try:
                all_measures = svg_measures_client.get_all_measures(
                    key_param=component['key'])
                for measure in all_measures:
                    component.update(measure)

            except UnknowMeasureMetric as missing_metric:
                logger.error(missing_metric.message)

            serializer.logger.write(component, SONAR_DATA_LOGS)

    except AuthenticationError as error:
        logger.error("Authentication Error. Verify credentials provided")
    except NotFoundError as error:
        logger.error("Resource Not Found. Check query url and query executed")
    except ClientError as error:
        logger.error("Client error related with 4xx")
    except ServerError as error:
        logger.error("Server error related with 5xx")


if __name__ == "__main__":
    main()
