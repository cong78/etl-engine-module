#!/usr/bin/env python

import os

def main():
    print("\nHello World Module!")
    #Read config map values from environment variables
    print("\nData format is " + os.environ['FORMAT'])
    print("Data asset name is " + os.environ['NAME'])
    print("Path to data is " + os.environ['DATAPATH'])
    
    print ("\nCOPY SUCCEEDED")


if __name__ == "__main__":
    main()