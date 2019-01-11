import os
import json
import datetime
import logging

logger = logging.getLogger('sonar-logs')


def write(data, path):

    # Check first path does not exists
    if not os.path.exists(path):
        logger.info("The path [{}] does not exists".format(path))
        os.makedirs(path)
        logger.info("Created path {}".format(path))

    logs_path = os.path.join(
        path, datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.json')
    with open(logs_path, "a+") as log_file:
        log_file.write(json.dumps(data))
        # add an extra line in order to avoid issues with Logstash
        log_file.write("\n")
        log_file.close()
        logger.info("Writing data logs into file {}".format(logs_path))
