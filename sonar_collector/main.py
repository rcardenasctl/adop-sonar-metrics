from rest_api.controller_client import ControllerClient
from rest_api.component_client import ComponentClient
from rest_api.svg_badges_client import SvgBadgesClient
from rest_api.measure_client import MeasureClient
from rest_api.issue_client import IssueClient

from controllers.component import Component
from controllers.svg_badges import SvGBadges
from controllers.measure import Measure
from controllers.issue import Issue

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
    logger.info("Starting sonar metrics collection")

    controller_client = ControllerClient(
        sonar_host=SONAR_HOST, sonar_base_path="/sonar", username=SONAR_USERNAME, password=SONAR_PASSWORD)

    component_client = ComponentClient(controller_client)
    component_controller = Component(component_client)

    measure_client = MeasureClient(controller_client)
    measure_controller = Measure(measure_client)

    issue_client = IssueClient(controller_client)
    issue_controller = Issue(issue_client)

    sonar_data_result = {}

    try:
        components = component_controller.get_all_components()

        components_collection = [component for component in components]

        measure_results = measure_controller.get_all_measure_by_components(
            components_collection)

        issues_results = issue_controller.get_all_issue_severity_per_component(
            components_collection)

        sonar_data_result.update(measure_results)
        sonar_data_result.update(issues_results)

        serializer.logger.write(sonar_data_result, SONAR_DATA_LOGS)

    except AuthenticationError as error:
        logger.error("Authentication Error. Verify credentials provided")
    except NotFoundError as error:
        logger.error("Resource Not Found. Check query url and query executed")
    except ClientError as error:
        logger.error("Client error related with 4xx")
    except ServerError as error:
        logger.error("Server error related with 5xx")

    logger.info("Successfull metrics collection")
    return 0


if __name__ == "__main__":
    main()
