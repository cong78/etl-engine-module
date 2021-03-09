#!/usr/bin/env python

import os
import yaml


def main():
    print("\nHello World Module!")

    # Read config map values from volume mount
    with open('/hw-module/conf.yaml', 'r') as stream:
        content = yaml.safe_load(stream)
        for key,val in content.items():
            if "data" in key:
                data = val[0]
                connectionName = data["connection.name"]
                connectionFormat = data["connection.format"]
                connectionCred = data["connection.credentialLocation"]
                s3Bucket = data["s3.bucket"]
                s3Endpoint = data["s3.endpoint"]

    print("\nConnection name is " + connectionName)
    print("\nConnection format is " + connectionFormat)
    print("\nConnection credential location is " + connectionCred)
    print("\nS3 bucket is " + s3Bucket)
    print("\nS3 endpoint is " + s3Endpoint)
    print ("\nCOPY SUCCEEDED")


if __name__ == "__main__":
    main()