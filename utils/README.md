# Extraction of Flow Statistics from Captures (GFkeyext)

- *Nov 2021, FIV*


## Steps

1. Use "GFkeyext" to obtain a go-flow configuration file according to the desired flow-key and timeout. For instance:

        > python3 GFkeyext.py 300 2 > config.json

2. Run go-flows with the obtained configuration file. Example:

        > ./go-flows run features config.json export csv stats.csv source libpcap example.pcap 
