from sonar_rest_api.sonar_monitor import SonarMonitor
from sonar_rest_api.sonar_components_monitor import SonarComponentMonitor
from sonar_rest_api.sonar_project_measure import SonarProjectMeasure
from sonar_rest_api.sonar_exceptions import UnknowMeasureMetric
from serializer import logger
import os

def main():

    SONAR_HOST = os.environ.get('SONAR_HOST')
    SONAR_TOKEN = os.environ.get('SONAR_TOKEN')
    SONAR_LOGS_PATH = os.environ.get('SONAR_LOGS_PATH')
    monitor = SonarMonitor(sonar_host=SONAR_HOST, sonar_base_path="/sonar", sonar_token=SONAR_TOKEN)
    components = SonarComponentMonitor(monitor)
    project_measures = SonarProjectMeasure(monitor)

    COMPONENTS_QUALIFIERS = ('TRK')
    components = components.get_components(qualifiers=COMPONENTS_QUALIFIERS)

    for component in components:
        try:
            all_measures = project_measures.get_all_measures(key_param=component['key'])
            for measure in all_measures:
                component.update(measure)

        except UnknowMeasureMetric as missing_metric:
            print(missing_metric.message)
        
        logger.writeLogs(component, SONAR_LOGS_PATH)
        

if __name__ == "__main__":
    main()