#!/usr/bin/env python

import os

def main():
    print("\nHello World Module!")

    # Read config map values from volume mount
    f = open("/hw-module/connection.name", "r")
    connectionName = f.read()
    f.close()
    print("\nConnection name is " + connectionName)

    f = open("/hw-module/connection.format", "r")
    connectionFormat  = f.read()
    f.close()
    print("\nConnection format is " + connectionFormat)

    f = open("/hw-module/connection.credentialLocation", "r")
    connectionCred  = f.read()
    f.close()
    print("\nConnection credential location is " + connectionCred)

    f = open("/hw-module/s3.bucket", "r")
    s3Bucket  = f.read()
    f.close()
    print("\nS3 bucket is " + s3Bucket)

    f = open("/hw-module/s3.endpoint", "r")
    s3Endpoint  = f.read()
    f.close()
    print("\nS3 endpoint is " + s3Endpoint)

    print ("\nCOPY SUCCEEDED")


if __name__ == "__main__":
    main()