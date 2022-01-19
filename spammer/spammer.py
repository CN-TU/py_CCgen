#!/usr/bin/python3

import configparser
import random
import time
import socket
import sys

METHODS = {'tcp': socket.SOCK_STREAM, 'udp': socket.SOCK_DGRAM}

config = configparser.ConfigParser()
cfg = ['spammer.ini']
if len(sys.argv) == 2:
    cfg = sys.argv[1:2]
config.read(cfg)

def isFloat(x):
    try:
        float(x)
        return True
    except:
        return False

def rangeOrInt(x):
    if '-' not in x:
        return int(x)
    a, b = x.split('-')
    return random.randrange(int(a), int(b))

try:
    section = config.sections()[-1]
    instructions = [x for x in config.get(section, 'send').split() if x]
except:
    print('Could not load configuration.', file=sys.stderr)
    sys.exit(-2)
dest = config.get(section, 'target')

print('Started')
sys.stdout.flush()

restart = True
while restart:
    restart = False
    # handle instructions line by line
    for instruction in instructions:
        # send instruction
        if ',' in instruction:
            comm, pattern, repeat, packets = instruction.split(',')
            packets = rangeOrInt(packets)
            if pattern.startswith('0x'):
                pattern = pattern[2:].decode('hex')
            m, sourcehost, sourceport, destination = comm.split(':')
            destination = (dest, int(destination))
            method = METHODS[m.lower()]

            try:
                s = socket.socket(socket.AF_INET, method)
                if sourceport == '':
                    sourceport = 0
                else:
                    sourceport = int(sourceport)
                if sourcehost or sourceport:
                    s.bind((sourcehost, sourceport))
                if method == socket.SOCK_STREAM:
                    s.connect(destination)
                    # set TCP_NODELAY to disable nagle so packets don't get merged
                    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    for i in range(packets):
                        s.sendall(pattern*rangeOrInt(repeat))
                        time.sleep(0.1)
                if method == socket.SOCK_DGRAM:
                    for i in range(packets):
                        s.sendto(pattern*rangeOrInt(repeat), destination)
                        time.sleep(0.01)
                s.close()
            except socket.error:
                print("Connection failure ({} {} -> {}). Is the listener running?".format(m, (sourcehost, sourceport), destination), file=sys.stderr)
                sys.exit(-1)
        elif instruction == 'restart':
            restart = True
            continue
        elif isFloat(instruction):
            time.sleep(float(instruction))
        elif '-' in instruction:
            a, b = instruction.split('-')
            time.sleep(random.uniform(float(a), float(b)))
