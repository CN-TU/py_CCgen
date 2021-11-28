#!/usr/bin/env python

import sys

def chunkstring(string, length):
    chunks = [string[i:i+length] for i in range(0, len(string), length)]
    return chunks 

def main():

    if len(sys.argv) >1:
        inputfile  = sys.argv[1]

    else:
        print("\nTransforms text into a sequence of 0s and 1s")
        print("\nUsage:")
        print("> python3 text2bin.py <inputfile>\n")
        quit()

    csize = 8
    with open(inputfile) as f:
        contents = f.read().strip()
        binc = chunkstring(contents, csize)
        text = list(map(lambda a: chr(int(a,2)), binc))
        #print(*binc, sep = ",")
        print(*text, sep = "") 

    f.close()


if __name__ == '__main__':
    main()
