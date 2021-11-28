#!/usr/bin/env python

import sys

def main():

    if len(sys.argv) >1:
        inputfile  = sys.argv[1]

    else:
        print("\nTransforms a sequence of 0s and 1s into text")
        print("\nUsage:")
        print("> python3 bin2text.py <inputfile>\n")
        quit()

    with open(inputfile) as f:
        contents = f.read()
        arrC = list(contents)
        sym = list(map(lambda a: ord(a), arrC))
        sbi = list(map(lambda a: '{:08b}'.format(a), sym))
        #print(*arrC,sep = ",")
        #print(*sym, sep = ",")
        print(*sbi, sep = "") 

    f.close()


if __name__ == '__main__':

    main()
