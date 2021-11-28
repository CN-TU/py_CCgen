#!/usr/bin/env python

import sys
import glob
import os


def main():

    if len(sys.argv) >1:
        inpath  = sys.argv[1]

    else:
        print("\Extracts a collection of CCs in a given pcap(s)")
        print("\nUsage:")
        print("> python3 ccgen_wrapper_ext.py [path-to-ccgen-config-files]")
        print("> (config-files must have .ini extension)")
        quit()

    for idf, filename in enumerate(sorted(glob.glob(os.path.join(inpath, '*.ini')))):
        print("\n----", idf, " Configuration file (.ini): ", filename)
        #python3 ccgen/ccgen.py offline extract wrapper/gcc_config/ccflow_1_1e.ini
        str_to_run = "python3 ccgen/ccgen.py offline extract "+filename
        os.system(str_to_run)

    inpath = ""
    for idf, filename in enumerate(sorted(glob.glob(os.path.join(inpath, '*.txt')))):
        print("----", idf, " Binary message file (.txt):", filename)
        str_to_run = "python3 utils/bin2text.py "+filename
        os.system(str_to_run)

if __name__ == '__main__':
    main()
