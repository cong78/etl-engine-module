#!/usr/bin/env python

import os
import yaml


def main():
    print("\nHello World Module!")

    # Read config map values from volume mount
    with open('/hw-module/conf.yaml', 'r') as stream:
        content = yaml.load(stream)
        for key,val in content.items():
            if "data" in key:
                x = val[0]
                for k,v in x.items():
                    if "connection.name" in k:
                        connectionName = v
                    if "connection.format" in k:
                        connectionFormat = v
                    if "connection.credentialLocation" in k:
                        connectionCred = v
                    if "s3.bucket" in k:
                        s3Bucket = v
                    if "s3.endpoint" in k:
                        s3Endpoint = v

    print("\nConnection name is " + connectionName)
    print("\nConnection format is " + connectionFormat)
    print("\nConnection credential location is " + connectionCred)
    print("\nS3 bucket is " + s3Bucket)
    print("\nS3 endpoint is " + s3Endpoint)
    print ("\nCOPY SUCCEEDED")


if __name__ == "__main__":
    main()