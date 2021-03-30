#!/usr/bin/env python
import os
import sys
import yaml
import requests
import json
from requests.auth import HTTPBasicAuth


def getM4DDatasetCredentials(url, role, secretName):
    params = {'role': role,
              'secret_name': secretName}
    response = requests.request("GET", url, params=params)
    return response.json()


#  TODO: Method to configure the source and destination properties from m4dapplication.yaml
def configureDSJobParameters(payload):
    print("\nConfiguring the DataStage Job source and destination properties from M4D Application instructs: ")
    str(payload)

    # Read config map values from volume mount
    with open('/etl-engine-module/files/conf.yaml', 'r') as stream:
        content = yaml.safe_load(stream)
        for key, val in content.items():
            if "source" in key:
                source = val[0]

                # Source data credential from vault
                sourceVaultPath = source["vault_credentials.address"] + source["authPath"]
                paramsSourceVault = {'role': source["vault_credentials.role"],
                                     'secret_name': source["vault_credentials.secretPath"]}
                responseSourceVault = requests.request("GET", sourceVaultPath, params=paramsSourceVault)

                # Configure source COS properties
                sourceAccessKey = responseSourceVault.get('access_key')
                sourceSecretKey = responseSourceVault.get('secret_key')
                sourceEndpoint = source["s3.endpoint"]
                sourceBucket = source["s3.bucket"]
                sourceObject = source["s3.object"]

                # Replace Data Stage API payload parameters from source
                payload.replace("SourceCosUrlValue", sourceEndpoint)
                payload.replace("SourceCosBucketNameValue", sourceBucket)
                payload.replace("SourceCosFileNameValue", sourceObject)
                payload.replace("SourceCosAccessKeyValue", sourceAccessKey)
                payload.replace("SourceCosSecretKeyValue", sourceSecretKey)

            if "destination" in key:
                destination = val[0]
                # Destination data credential from vault
                destinationVaultPath = source["vault_credentials.address"] + source["authPath"]
                paramsDestinationVault = {'role': source["vault_credentials.role"],
                                          'secret_name': source["vault_credentials.secretPath"]}
                responseDestinationVault = requests.request("GET", destinationVaultPath, params=paramsDestinationVault)

                # Configure destination COS properties
                sourceAccessKey = responseDestinationVault.get('access_key')
                sourceSecretKey = responseDestinationVault.get('secret_key')
                destinationEndpoint = destination["s3.endpoint"]
                destinationBucket = destination["s3.bucket"]
                destinationObject = destination["s3.object"]

                # Replace Data Stage API payload parameters from destination
                payload.replace("DestinationCosUrlValue", destinationEndpoint)
                payload.replace("DestinationCosBucketNameValue", destinationBucket)
                payload.replace("DestinationCosFileNameValue", destinationObject)
                payload.replace("DestinationCosAccessKey", sourceAccessKey)
                payload.replace("DestinationCosAccessKeyValue", sourceSecretKey)

    return payload


#  Method to compile the DataStage job
def compileDSJob(urlCompile, username, password):
    print("\nCompiling the DataStage: ")

    response = requests.request("GET", str(urlCompile).replace("{{action}}", "compileDSJob"), verify=False,
                                auth=HTTPBasicAuth(username, password))
    print(response.text)


#  Method to run the DataStage job
def runDSJob(urlRun, username, password):
    print("\nRunning the DataStage Job: ")

    with open('parameters.json') as f:
        payload = json.load(f)

    configureDSJobParameters(payload)
    response = requests.request("POST", str(urlRun).replace("{{action}}", "runDSJob"), verify=False,
                                auth=HTTPBasicAuth(username, password), data=payload)
    print(response.text)


#  Method to get the DataStage job status
def getDSJobStatus(urlJobStatus, username, password):
    print("\nGetting the DataStage Job status: ")

    response = requests.request("GET", str(urlJobStatus).replace("{{action}}", "getDSJobStatus"), verify=False,
                                auth=HTTPBasicAuth(username, password))
    print(response.text)


def main():
    print("\nRunning a ETL Engine Module of Mesh for Data!")

    # Read Data Stage configuration values
    with open('confDataStage.yaml', 'r') as stream:
        content = yaml.safe_load(stream)
        for key, val in content.items():
            if "data" in key:
                data = val[0]
                connectionUrlDataStage = data["connection.dataStage.url"]
                connectionUsername = data["connection.dataStage.username"]
                connectionPassword = data["connection.dataStage.password"]

    # compileDSJob(connectionUrlDataStage, connectionUsername, connectionPassword)
    runDSJob(connectionUrlDataStage, connectionUsername, connectionPassword)
    getDSJobStatus(connectionUrlDataStage, connectionUsername, connectionPassword)


if __name__ == "__main__":
    main()
    sys.exit(os.EX_OK)
