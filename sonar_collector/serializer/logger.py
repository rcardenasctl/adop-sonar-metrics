import os, json, datetime

def writeLogs(data, path):

    # Check first path does not exists
    if not os.path.exists(path):
        os.makedirs(path)
    
    logs_path = os.path.join(path, datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.json')
    print(logs_path)
    print(data)
    with open(logs_path, "a+") as log_file:
        log_file.write(json.dumps(data))
        # add an extra line in order to avoid issues with Logstash
        log_file.write("\n")
        log_file.close()