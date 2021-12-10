#!/usr/bin/env python

import argparse
import logging
from os import system
import sys

from scapy.all import PcapReader
from scapy.utils import PcapWriter
from scapy.layers.inet import IP, TCP, ICMP, UDP

import util
import util.config
import util.iptables


def _process_online(config, callback):
    import socket
    import nfqueue

    iprule = util.iptables.get_iprule(config)

    #REMOVE iptables rule just in case
    system('iptables -w -F ' + config.iptables_chain)
    #APPLY iptables rule
    system(iprule)

    socket.SO_RCVBUFFORCE = 2*1024*1024

    conn = nfqueue.Connection()

    q = conn.bind(config.iptables_queue)
    q.set_mode(0xffff, nfqueue.COPY_PACKET)

    try:
        for packet in conn:
            scapypkt = IP(packet.payload)
            callback(scapypkt)
            packet.payload = bytes(scapypkt)
            packet.mangle()
    finally:
        system('iptables -w -F ' + config.iptables_chain)
        conn.close()

def process_summary(modus, config, frames):
    print("\n[Modus]", modus[1])
    if modus[0] == 3:
        required_pkts = config.message.necessary_packets()    
        if required_pkts == frames:
            print("  SUCCEEDED!!")
        else:
            print("  FAILED!!")
        print("  Required packets: ", required_pkts)    
        print("  Modified packets: ", frames)    
    elif modus[0] == 4:
        print("  Inspected packets: ", frames)
        print("  Check obtained message in the 'message_file'!!")        

def process_online_send(config):
    def callback(pkt):
        datagram = config.message.getdatagram()
        mappedvalue = config.mapping.getmapping(datagram)
        # check if there is a value to map otherwise skip packet
        if mappedvalue:
            config.technique.modify(pkt, mappedvalue)

            del pkt[IP].chksum  #recalculate checksum
            if pkt.haslayer(TCP):
                del pkt[TCP].chksum
            if pkt.haslayer(ICMP):
                del pkt[ICMP].chksum
        else:
            pass

    _process_online(config, callback)


def process_online_receive(config):
    outputfile = open(config.message_file, 'w')

    def callback(pkt):
        received = config.technique.extract(pkt)
        for i in received:
            data = config.mapping.getdata(str(i))
            print(data)
            outputfile.write(data)
            outputfile.flush()

    _process_online(config, callback)


def process_offline_send(config):
    modified_frames = 0
    params = config.mapping.getparams()
    with PcapWriter(config.output_file) as outfile:
        for frame in PcapReader(config.input_file):
            if not util.should_filter_frame(config, frame):
                # Add covert channel
                datagram = config.message.getdatagram()
                mappedvalue = config.mapping.getmapping(datagram)
                # if there is a message, insert it in the technique. Otherwise, do not do anything
                if mappedvalue is not None:
                    modified_frames = modified_frames + 1
                    if config.layer == 'IP' and not 'pIAT' in params:
                        config.technique.modify(frame[IP], mappedvalue, params)
                    #elif config.layer == 'PCAP':
                    else:
                        config.technique.modify(frame, mappedvalue, params)

                    # Recalculate checksums
                    if frame.haslayer(TCP):
                        del frame[TCP].chksum
                    if frame.haslayer(UDP):
                        del frame[UDP].chksum
                    if frame.haslayer(ICMP):
                        del frame[ICMP].chksum
                    del frame[IP].chksum
            outfile.write(frame)
    return modified_frames


def process_offline_receive(config):
    checked_frames = 0
    params = config.mapping.getparams()
    with open(config.message_file, 'w') as outfile:
        for frame in PcapReader(config.input_file):
            if not util.should_filter_frame(config, frame):
                checked_frames = checked_frames + 1
                if config.layer == 'IP' and not 'pIAT' in params:
                    mappedvalue = config.technique.extract(frame[IP],params)
                #elif config.layer == 'PCAP':
                else:
                    mappedvalue = config.technique.extract(frame,params)
                if mappedvalue is None:
                    continue
                if isinstance(mappedvalue, list):
                    for i in mappedvalue:
                        data = config.mapping.getdata(str(i))
                        outfile.write(data)
                else:
                    try:
                        data = config.mapping.getdata(str(mappedvalue))
                        outfile.write(data)
                    except:
                        pass
    return checked_frames

def main():
    # let the controller know that we're there
    print("\nTUW-CCgen.v2...")
    sys.stdout.flush()

    logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

    argparser = argparse.ArgumentParser(description='covert channel generator')
    argparser.add_argument('network', type=str, choices=[util.config.NETWORK_ONLINE, util.config.NETWORK_OFFLINE])
    argparser.add_argument('direction', type=str, choices=[util.config.DIRECTION_SEND, util.config.DIRECTION_RECEIVE])
    argparser.add_argument('configfile', type=argparse.FileType('r'))
    argparser.add_argument('--queue', type=int)
    args = argparser.parse_args()

    config = util.config.parse_config(args.configfile, args.network, args.direction, args.queue)
    
    frames = 0
    if args.network == util.config.NETWORK_ONLINE:
        if args.direction == util.config.DIRECTION_SEND:
            process_online_send(config)
            modus = (1,'ONLINE INJECTION...')
        elif args.direction == util.config.DIRECTION_RECEIVE:
            process_online_receive(config)
            modus = (2,'ONLINE EXTRACTION...')
    elif args.network == util.config.NETWORK_OFFLINE:
        if args.direction == util.config.DIRECTION_SEND:
            frames = process_offline_send(config)
            modus = (3,'OFFLINE INJECTION...')
        elif args.direction == util.config.DIRECTION_RECEIVE:
            frames = process_offline_receive(config)
            modus = (4,'OFFLINE EXTRACTION...')

    process_summary(modus, config, frames)


if __name__ == '__main__':
    main()
