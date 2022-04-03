from configparser import ConfigParser
from collections import namedtuple
from os import path, getcwd
import re
import sys
import logging

from util.handle_csv import Mapping
from util.handle_message import Message


NETWORK_OFFLINE = 'offline'
NETWORK_ONLINE = 'online'

DIRECTION_SEND = 'inject'
DIRECTION_RECEIVE = 'extract'


Config = namedtuple('Config',
    [
        'network',
        'direction',
        'input_file',
        'output_file',
        'message_file',
        'src_ip',
        'dst_ip',
        'src_port',
        'dst_port',
        'proto',
        'mapping',
        'layer',
        'message',
        'technique',
        'iptables_chain',
        'iptables_queue',
    ]
)


def parse_config(configfile, network, direction, arg_queue=None):
    #Parse config file
    cfg = ConfigParser()
    cfg.readfp(configfile)

    #read files from cfg
    if network == NETWORK_OFFLINE:
        input_file = cfg.get('Files', 'input')
        if not path.dirname(input_file):
            input_file = path.join(getcwd(), input_file)

        if direction == DIRECTION_SEND:
            output_file = cfg.get('Files', 'output')
            if not path.dirname(output_file):
                output_file = path.join(getcwd(), output_file)
        else:
            output_file = None
    else:
        input_file = None
        output_file = None

    message_file = cfg.get('Files', 'message')
    mapping_file = cfg.get('Files', 'mapping')

    print("\n[FILES]")
    print("  input_file: ", input_file)
    print("  output_file: ", output_file)
    print("  message_file: ", message_file)
    print("  mapping_file: ", mapping_file)

    #read filter from cfg
    src_ip = None
    dst_ip = None
    src_port = None
    dst_port = None
    proto = None

    print("\n[FILTER]")
    try:
        src_ip = cfg.get('Filter', 'src_ip')
        print("  src_ip: ", src_ip)
    except:
        print("  src_ip: ANY")

    try:
        dst_ip = cfg.get('Filter', 'dst_ip')
        print("  dst_ip: ", dst_ip)
    except:
        print("  dst_ip: ANY")

    try:
        src_port = int(cfg.get('Filter', 'src_port'))
        assert src_port in range(0, 65536), 'Invalid value for source port: %d' % src_port
        print("  src_port: ", src_port)
    except:
        src_port = None
        print("  src_port: ANY")

    try:
        dst_port = int(cfg.get('Filter', 'dst_port'))
        assert dst_port in range(0, 65536), 'Invalid value for destination port: %d' % dst_port
        print("  dst_port: ", dst_port)
    except:
        dst_port = None
        print("  dst_port: ANY")

    try:
        proto = int(cfg.get('Filter', 'proto'))
        assert proto in range(0, 255), 'Invalid value for IP protocol: %d' % proto
        print("  proto: ", proto)
    except:
        proto = None
        print("  proto: ANY")

    if network == NETWORK_ONLINE:
        try:
            iptables_chain = cfg.get('Iptables', 'chain')
        except:
            #iptables_chain = 'OUTPUT' if direction == DIRECTION_SEND else 'INPUT'
            iptables_chain = dst_ip
            print("No iptables chain given, using %s, based on dst_ip" % iptables_chain)

        logging.error("Configuring iptables_queue")
        if arg_queue is not None:
            logging.error("arg_queue: {}".format(arg_queue))
            iptables_queue = arg_queue
        else:
            try:
                iptables_queue = int(cfg.get('Iptables', 'queue'))
                logging.error("Exception did not happen")
            except:
                iptables_queue = int(dst_ip.split('.')[-1])
                print("No iptables queue given, using %s, based on dst_ip" % iptables_queue)
        # added by astra, just use fixed queue id
        iptables_queue = int(dst_ip.split('.')[-1])
    else:
        iptables_chain = None
        iptables_queue = None

    technique = cfg.get('Channel', 'technique')
    assert re.match('^[_a-zA-Z0-9]+$', technique), 'Invalid name for technique %s' % technique

    bits = cfg.getint('Channel', 'bits')

    layer = cfg.get('Channel', 'layer')
    assert layer in ('IP', 'PCAP', 'TLS'), 'Invalid layer'

    #Import modular covert channel technique
    technique = "%s/../techniques/%s.py" % (path.dirname(path.abspath(__file__)), technique)
    if not path.exists(technique):
        sys.stderr.write("ERROR: Technique file '%s' does not exist!\n" % technique)
        sys.exit(2)
    #execfile(technique, globals())
    exec(compile(open(technique, "rb").read(), technique, 'exec'), globals())

    return Config(
        network=network,
        direction=direction,
        input_file=input_file,
        output_file=output_file,
        message_file=message_file,
        src_ip=src_ip,
        dst_ip=dst_ip,
        src_port=src_port,
        dst_port=dst_port,
        proto=proto,
        mapping=Mapping(mapping_file, bits),
        layer=layer,
        message=Message(message_file, bits) if direction == DIRECTION_SEND else None,
        technique=CovertChannel(0 if network == NETWORK_OFFLINE else 1, cfg, Message(message_file, bits).message if direction == DIRECTION_SEND else None),
        iptables_chain=iptables_chain,
        iptables_queue=iptables_queue)
