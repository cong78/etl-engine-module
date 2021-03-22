#!/usr/bin/env python

import os
import yaml
import requests

cookies = 'IIS-LtpaToken2=SR96ltj4LNdJquhsa/l6qRXfu5OoyPO6CueGZZ3zdihWgFThKLrwh16envRmxoU5MQztPOxd9hnE8AnOvhEXEfj2M4yYMl37Rx+vSptbk/CK+LXbnp2IrbHnPojjSoCLDVpl74u4LJS/Cjln9JL9GOozfwzLza4pexGP5zzj+Kqw759tSpNTG6YY6rJ0uV+lFIKTkQuuUtTDSOT6jwMr1H6dIBmg+opUmiSlUm+DzJeTllrJRYuMupTRHrJ1u4c3wjazK33cgNPAAQQ3/U+++8jlQ4F+Y2Wsc2XNz4jUs8pj+4GtolY5iYy/LSORarht; IIS-JSESSIONID=000018TEJHSeoFcZubJ01dtQIGU:b067e1c0-574f-4898-865d-71ec4164d741; X-IBM-IISSessionId={issvr2048:isf}6Ja9o_pvm_4oXeW3C9VNYffavDsSA5xyfGNecqBVbGJaYDGUh2GUE8TIpJAQPxGHZTiZKy5YtRBHKhp097WFMAd--FS32FCOm65LL4r44eTMlNj4vVjtBffyvNtYDHT4YD7m3MCBuZg5qyvGbLH4qweqW9EnyCGldjAH1ImRwQFr8A-uajkxa6JPtbJf0RA89pSD9eQK_RD-1wFCUGEjNEXd7o-I3kN6ESqRnUsXU_knjXFVogO5TAZQ4Uy0g--oD6CiInle7Zo9KMW-hisEK8aoysJx8nGG40lB6e6RN3uDpFt9wGn1gnKSluQVLt6zdX_uSVzWiKd1AUUiKlI1BA..'
def getDSJobStatus(urlStatus, credential):
    print("\nGetting the DataStage Job status from: " + urlStatus)
    payload={}
    headers = {
      'Authorization': credential,
      'Cookie': cookies
    }

    response = requests.request("GET", urlStatus, headers=headers, data=payload)
    print(response.text)

def runDSJob(urlRun, credential):
    print("\nRunning the DataStage Job from: " + urlRun)
    payload={}
    headers = {
      'Authorization': credential,
      'Cookie': cookies
    }

    response = requests.request("GET", urlRun, headers=headers, data=payload)

    print(response.text)


def compileDSJob(urlCompile, credential):

    print("\nCompiling the DataStage Job from: " + urlCompile)
    payload={}
    headers = {
      'Authorization': credential,
      'Cookie': cookies
    }

    response = requests.request("GET", urlCompile, headers=headers, data=payload)

    print(response.text)

def main():
    print("\nETL Engine Module!")

    # Read config map values from volume mount
    with open('etl-engine-module/files/conf.yaml', 'r') as stream:
        content = yaml.safe_load(stream)
        for key,val in content.items():
            if "data" in key:
                data = val[0]
                connectionUrlRunDSJob = data["connection.url.runDSJob"]
                connectionUrlCompileDSJob = data["connection.url.compileDSJob"]
                connectionUrlGetDSJobStatus = data["connection.url.getDSJobStatus"]
                connectionCredential = data["connection.credential"]

    compileDSJob(connectionUrlCompileDSJob, connectionCredential)
    runDSJob(connectionUrlRunDSJob, connectionCredential)
    getDSJobStatus(connectionUrlGetDSJobStatus, connectionCredential)


if __name__ == "__main__":
    main()