#!/usr/bin/env python
import os
import sys
import yaml
import requests
from requests.auth import HTTPBasicAuth


#  TODO: Method to configure the source and destination properties of the predefined DataStage ingestion job
#  Need to find out which DataStage method can be used for this configuration
def configureDSJob(urlConfigure, credential):
    print("\nConfiguring the DataStage Job: ")

    # Read config map values from volume mount
    with open('/datastage/confDataStage.yaml', 'r') as stream:
        content = yaml.safe_load(stream)
        for key, val in content.items():
            if "data" in key:
                data = val[0]
                connectionName = data["connection.name"]
                connectionFormat = data["format"]
                vault = data["vault_credentials"]
                s3Bucket = data["s3.bucket"]
                s3Endpoint = data["s3.endpoint"]

#  Method to compile the DataStage job
def compileDSJob(urlCompile, username, password):
    print("\nCompiling the DataStage: ")

    response = requests.request("GET", str(urlCompile).replace("{{action}}", "compileDSJob"),
                                verify=False, auth=HTTPBasicAuth(username, password))

    print(response.text)


#  Method to run the DataStage job
def runDSJob(urlRun, username, password):
    print("\nRunning the DataStage Job: ")

    response = requests.request("GET", str(urlRun).replace("{{action}}", "runDSJob"), verify=False,
                                auth=HTTPBasicAuth(username, password))

    print(response.text)


#  Method to get the DataStage job status
def getDSJobStatus(urlJobStatus, username, password):
    print("\nGetting the DataStage Job status: ")

    response = requests.request("GET", str(urlJobStatus).replace("{{action}}", "getDSJobStatus"), verify=False,
                                auth=HTTPBasicAuth(username, password))
    print(response.text)


def main():
    print("\nETL Engine Module!")

    # Read config map values from volume mount
    with open('confDataStage.yaml', 'r') as stream:
        content = yaml.safe_load(stream)
        for key, val in content.items():
            if "data" in key:
                data = val[0]
                connectionUrlDataStage = data["connection.dataStage.url"]
                connectionUsername = data["connection.dataStage.username"]
                connectionPassword = data["connection.dataStage.password"]

    compileDSJob(connectionUrlDataStage, connectionUsername, connectionPassword)
    runDSJob(connectionUrlDataStage, connectionUsername, connectionPassword)
    getDSJobStatus(connectionUrlDataStage, connectionUsername, connectionPassword)

    sys.exit(os.EX_OK)

if __name__ == "__main__":
    main()