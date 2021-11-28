#!/usr/bin/env python

import sys
import pandas as pd
import numpy as np

def main():

    timeout = 300
    flowkey = 2
    if len(sys.argv) >1:
        timeout  = int(sys.argv[1])
        if len(sys.argv) >2:
            flowkey = int(sys.argv[2])
    else:
        print("\nUsage:")
        print("> python3 GFkeyext.py <timeout> <flowkey_option>")
        print(" - timeout: int (seconds)" )
        print(" - flowkey_option: 1 (one-tuple: srcIP)" )
        print("                   2 (two-tuple: scrIP,dstIP)" )
        print("                   3 (three-tuple: scrIP,dstIP,Prot)" )
        print("                   4 (three-tuple: scrIP,dstIP,srcPort,dstPort)" )
        print("               other (five-tuple: scrIP,dstIP,Prot,srcPort,dstPort)" )
        quit()

    print(" { ") 
    print("	\"version\": \"v2\", ") 
    print("	\"preprocessing\": {  ")  
    print("		\"flows\": [{ ") 
    print("			\"active_timeout\":", timeout, ", ") 
    print("			\"idle_timeout\":", timeout, ", ") 
    print("			\"features\": [ ") 
    print("				\"flowStartMilliseconds\", ") 
    print("				\"flowDurationMilliseconds\", ") 
    if flowkey==1:
        print("				\"sourceIPAddress\", ") 
    elif flowkey==2:
        print("				\"sourceIPAddress\", ") 
        print("				\"destinationIPAddress\", ") 
    elif flowkey==3:
        print("				\"sourceIPAddress\", ") 
        print("				\"destinationIPAddress\", ") 
        print("				\"protocolIdentifier\", ") 
    elif flowkey==4:
        print("				\"sourceIPAddress\", ") 
        print("				\"destinationIPAddress\", ") 
        print("				\"sourceTransportPort\", ") 
        print("				\"destinationTransportPort\", ") 
    else:
        print("				\"sourceIPAddress\", ") 
        print("				\"destinationIPAddress\", ") 
        print("				\"protocolIdentifier\", ") 
        print("				\"sourceTransportPort\", ") 
        print("				\"destinationTransportPort\", ") 
    print("				\"packetTotalCount\" ") 
    print("			], ") 
    print("			\"bidirectional\": false, ") 
    print("			\"key_features\": [ ") 
    if flowkey==1:
        print("				\"sourceIPAddress\" ") 
    elif flowkey==2:
        print("				\"sourceIPAddress\", ") 
        print("				\"destinationIPAddress\" ") 
    elif flowkey==3:
        print("				\"sourceIPAddress\", ") 
        print("				\"destinationIPAddress\", ") 
        print("				\"protocolIdentifier\" ") 
    elif flowkey==4:
        print("				\"sourceIPAddress\", ") 
        print("				\"destinationIPAddress\", ") 
        print("				\"sourceTransportPort\", ") 
        print("				\"destinationTransportPort\" ") 
    else:
        print("				\"sourceIPAddress\", ") 
        print("				\"destinationIPAddress\", ") 
        print("				\"protocolIdentifier\", ") 
        print("				\"sourceTransportPort\", ") 
        print("				\"destinationTransportPort\" ") 
    print("			] ") 
    print("		}] ") 
    print("	} ") 
    print("} ")


if __name__ == '__main__':
    main()
