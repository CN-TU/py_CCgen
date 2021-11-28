#!/usr/bin/env python

import sys
import numpy as np
import pandas as pd
from os.path import exists
import os
import glob

PATH_TO_GOFLOWS = "wrapper/go-flows-master"
GCC_CONF_INJ_FOLDER = "wrapper/ccgen_inj_config"
GCC_CONF_EXT_FOLDER = "wrapper/ccgen_ext_config"
WRP_TEMP_FOLDER = "wrapper/temp"

def DropInLists(sel,dfst1,dfst2,dfst3,dfst4,dfst5):
    fields = ['sourceIPAddress','destinationIPAddress','protocolIdentifier','sourceTransportPort','destinationTransportPort']
    key = len([element for element in sel.columns if element in fields])
    #print(len(dfst1),len(dfst2),len(dfst3),len(dfst4),len(dfst5))
    if key == 1:
        val1 = sel.iloc[0]['sourceIPAddress']
        dfst1 = dfst1[dfst1['sourceIPAddress'] != val1]
        dfst2 = dfst2[dfst2['sourceIPAddress'] != val1]
        dfst3 = dfst3[dfst3['sourceIPAddress'] != val1]
        dfst4 = dfst4[dfst4['sourceIPAddress'] != val1]
        dfst5 = dfst5[dfst5['sourceIPAddress'] != val1]
    elif key == 2:
        val1 = sel.iloc[0]['sourceIPAddress']
        val2 = sel.iloc[0]['destinationIPAddress']
        dfst1 = dfst1[dfst1['sourceIPAddress'] != val1]
        dfst2 = dfst2[(dfst2['sourceIPAddress'] != val1) & (dfst2['destinationIPAddress'] != val2)]
        dfst3 = dfst3[(dfst3['sourceIPAddress'] != val1) & (dfst3['destinationIPAddress'] != val2)]
        dfst4 = dfst4[(dfst4['sourceIPAddress'] != val1) & (dfst4['destinationIPAddress'] != val2)]
        dfst5 = dfst5[(dfst5['sourceIPAddress'] != val1) & (dfst5['destinationIPAddress'] != val2)]
    elif key == 3:
        val1 = sel.iloc[0]['sourceIPAddress']
        val2 = sel.iloc[0]['destinationIPAddress']
        val3 = sel.iloc[0]['protocolIdentifier']
        dfst1 = dfst1[dfst1['sourceIPAddress'] != val1]
        dfst2 = dfst2[(dfst2['sourceIPAddress'] != val1) & (dfst2['destinationIPAddress'] != val2)]
        dfst3 = dfst3[(dfst3['sourceIPAddress'] != val1) & (dfst3['destinationIPAddress'] != val2) & 
            (dfst3['protocolIdentifier'] != val3)]
        dfst4 = dfst4[(dfst4['sourceIPAddress'] != val1) & (dfst4['destinationIPAddress'] != val2) ]
        dfst5 = dfst5[(dfst5['sourceIPAddress'] != val1) & (dfst5['destinationIPAddress'] != val2) & 
            (dfst5['protocolIdentifier'] != val3)]
    elif key == 4:
        val1 = sel.iloc[0]['sourceIPAddress']
        val2 = sel.iloc[0]['destinationIPAddress']
        val4 = sel.iloc[0]['sourceTransportPort']
        val5 = sel.iloc[0]['destinationTransportPort']
        dfst1 = dfst1[dfst1['sourceIPAddress'] != val1]
        dfst2 = dfst2[(dfst2['sourceIPAddress'] != val1) & (dfst2['destinationIPAddress'] != val2)]
        dfst3 = dfst3[(dfst3['sourceIPAddress'] != val1) & (dfst3['destinationIPAddress'] != val2)]
        dfst4 = dfst4[(dfst4['sourceIPAddress'] != val1) & (dfst4['destinationIPAddress'] != val2) & 
            (dfst4['sourceTransportPort'] != val4) & (dfst4['destinationTransportPort'] != val5)]
        dfst5 = dfst5[(dfst5['sourceIPAddress'] != val1) & (dfst5['destinationIPAddress'] != val2) & 
            (dfst5['sourceTransportPort'] != val4) & (dfst5['destinationTransportPort'] != val5)]
    elif key == 5:
        val1 = sel.iloc[0]['sourceIPAddress']
        val2 = sel.iloc[0]['destinationIPAddress']
        val3 = sel.iloc[0]['protocolIdentifier']
        val4 = sel.iloc[0]['sourceTransportPort']
        val5 = sel.iloc[0]['destinationTransportPort']
        dfst1 = dfst1[dfst1['sourceIPAddress'] != val1]
        dfst2 = dfst2[(dfst2['sourceIPAddress'] != val1) & (dfst2['destinationIPAddress'] != val2)]
        dfst3 = dfst3[(dfst3['sourceIPAddress'] != val1) & (dfst3['destinationIPAddress'] != val2) & 
            (dfst3['protocolIdentifier'] != val3)]
        dfst4 = dfst4[(dfst4['sourceIPAddress'] != val1) & (dfst4['destinationIPAddress'] != val2) & 
            (dfst4['sourceTransportPort'] != val4) & (dfst4['destinationTransportPort'] != val5)]
        dfst5 = dfst5[(dfst5['sourceIPAddress'] != val1) & (dfst5['destinationIPAddress'] != val2) & 
            (dfst5['sourceTransportPort'] != val4) & (dfst5['destinationTransportPort'] != val5) & (dfst5['protocolIdentifier'] != val3)]
    #print(len(dfst1),len(dfst2),len(dfst3),len(dfst4),len(dfst5))
    return dfst1,dfst2,dfst3,dfst4,dfst5

#df = df[(df.col1 > 8) & (df.col2 != 'A')]

def WriteInjConfigFile(configfile, cfg_data, flowkey):

    with open(configfile, 'w') as f:
        f.write('[Files]\n')
        f.write('input: '+str(cfg_data['inpcap'])+'\n')
        f.write('output: '+str(cfg_data['outpcap'])+'\n')
        f.write('message: '+str(cfg_data['message'])+'\n')
        f.write('mapping: '+str(cfg_data['mapping'])+'\n')
        f.write('\n')
        f.write('[Filter]\n')
        f.write('src_ip: '+str(cfg_data['src_ip'][0])+'\n')
        if flowkey != "1tup":
            f.write('dst_ip: '+str(cfg_data['dst_ip'][0])+'\n')
            if flowkey == "3tup":
                f.write('proto: '+str(cfg_data['proto'][0])+'\n')
            elif flowkey == "4tup":
                f.write('src_port: '+str(cfg_data['src_port'][0])+'\n')
                f.write('dst_port: '+str(cfg_data['dst_port'][0])+'\n')
            elif flowkey == "5tup":
                f.write('proto: '+str(cfg_data['proto'][0])+'\n')
                f.write('src_port: '+str(cfg_data['src_port'][0])+'\n')
                f.write('dst_port: '+str(cfg_data['dst_port'][0])+'\n')
        f.write('\n')
        f.write('[Channel]\n')
        f.write('technique: '+str(cfg_data['technique'])+'\n')
        f.write('bits: '+str(cfg_data['bits'])+'\n')
        f.write('layer: IP')

def WriteExtConfigFile(configfile, cfg_data, flowkey, msgfile):

    with open(configfile, 'w') as f:
        f.write('[Files]\n')
        f.write('input: '+str(cfg_data['inpcap'])+'\n')
        f.write('message: '+msgfile+'\n')
        f.write('mapping: '+str(cfg_data['mapping'])+'\n')
        f.write('\n')
        f.write('[Filter]\n')
        f.write('src_ip: '+str(cfg_data['src_ip'][0])+'\n')
        if flowkey != "1tup":
            f.write('dst_ip: '+str(cfg_data['dst_ip'][0])+'\n')
            if flowkey == "3tup":
                f.write('proto: '+str(cfg_data['proto'][0])+'\n')
            elif flowkey == "4tup":
                f.write('src_port: '+str(cfg_data['src_port'][0])+'\n')
                f.write('dst_port: '+str(cfg_data['dst_port'][0])+'\n')
            elif flowkey == "5tup":
                f.write('proto: '+str(cfg_data['proto'][0])+'\n')
                f.write('src_port: '+str(cfg_data['src_port'][0])+'\n')
                f.write('dst_port: '+str(cfg_data['dst_port'][0])+'\n')
        f.write('\n')
        f.write('[Channel]\n')
        f.write('technique: '+str(cfg_data['technique'])+'\n')
        f.write('bits: '+str(cfg_data['bits'])+'\n')
        f.write('layer: IP')

def check_input_files(args):
    file_exists = exists(args[1])
    if file_exists==0:
        print("ERROR! I can't find ", args[1])
        quit()
    file_exists = exists(args[2])
    if file_exists==0:
        print("ERROR! I can't find ", args[2])
        quit()
    file_exists = exists(PATH_TO_GOFLOWS)
    if file_exists==0:
        print("ERROR! I can't find go-flows")
        quit()

def extract_stats(inpcap):
    #./go-flows run features cfg.json export csv output.csv source libpcap input.pcap
    goflows = "./"+PATH_TO_GOFLOWS+"/go-flows"
    str_to_run = goflows+" run features "+WRP_TEMP_FOLDER+"/1tup.json export csv "+WRP_TEMP_FOLDER+"/1tup.csv source libpcap "+inpcap
    os.system(str_to_run)
    str_to_run = goflows+" run features "+WRP_TEMP_FOLDER+"/2tup.json export csv "+WRP_TEMP_FOLDER+"/2tup.csv source libpcap "+inpcap
    os.system(str_to_run)
    str_to_run = goflows+" run features "+WRP_TEMP_FOLDER+"/3tup.json export csv "+WRP_TEMP_FOLDER+"/3tup.csv source libpcap "+inpcap
    os.system(str_to_run)
    str_to_run = goflows+" run features "+WRP_TEMP_FOLDER+"/4tup.json export csv "+WRP_TEMP_FOLDER+"/4tup.csv source libpcap "+inpcap
    os.system(str_to_run)
    str_to_run = goflows+" run features "+WRP_TEMP_FOLDER+"/5tup.json export csv "+WRP_TEMP_FOLDER+"/5tup.csv source libpcap "+inpcap
    os.system(str_to_run)
    d1 = pd.read_csv(WRP_TEMP_FOLDER+"/1tup.csv") 
    d2 = pd.read_csv(WRP_TEMP_FOLDER+"/2tup.csv") 
    d3 = pd.read_csv(WRP_TEMP_FOLDER+"/3tup.csv") 
    d4 = pd.read_csv(WRP_TEMP_FOLDER+"/4tup.csv") 
    d5 = pd.read_csv(WRP_TEMP_FOLDER+"/5tup.csv") 
    return d1,d2,d3,d4,d5

def main():

    cfg_data = {'inpcap':"i.pcap", 'outpcap':"o.pcap", 'src_ip':"0.0.0.0", 'dst_ip':"1.1.1.1", 'proto':"1", 'src_port':"10", 'dst_port':"80", 
        'technique':"ttl", 'bits':1, 'mapping':'mp.txt', 'message':'mg.txt'} 

    verbose = 0
    if len(sys.argv) >1:
        check_input_files(sys.argv)
        configfile  = sys.argv[1]
        inpcap  = sys.argv[2]
        outpcap  = sys.argv[3]
        if len(sys.argv) >4:
            verbose = 1
    else:
        print("\n-- genCCconfigs.py --")
        print("Generate configuration files for the ccgen tool")
        print("\nUsage:")
        print("> python3 genCCconfigs.py <configfile> <inpcap> <outpcap> (-v)\n")
        quit()

    dfst1,dfst2,dfst3,dfst4,dfst5 = extract_stats(inpcap) 
    dfcg = pd.read_csv(configfile)

    cfg_data['inpcap'] = inpcap
    cfg_data['outpcap'] = outpcap
    auxpcapA = outpcap.split(".")[0]+"_auxA.pcap"
    auxpcapB = outpcap.split(".")[0]+"_auxB.pcap"

    files = glob.glob(GCC_CONF_INJ_FOLDER+'/*')
    for f in files:
        os.remove(f)
    files = glob.glob(GCC_CONF_EXT_FOLDER+'/*')
    for f in files:
        os.remove(f)

    for index, row in dfcg.iterrows(): 
        file = open(row['message_file'], "r")
        bits = file.read()
        bits = bits[:-1]
        nbits = len(bits)
        cfg_data['bits'] = int(row['bitspkt'])
        cfg_data['mapping'] = row['mapping']
        cfg_data['technique'] = row['technique']
        cfg_data['message'] = row['message_file']
        rep = int(row['rep'])
        flowkey = row['key']
        req_pkts = int(nbits/cfg_data['bits'])

        if flowkey == "1tup":
            dfst = dfst1
        elif flowkey == "2tup":
            dfst = dfst2
        elif flowkey == "3tup":
            dfst = dfst3
        elif flowkey == "4tup":
            dfst = dfst4
        else:
            dfst = dfst5

        for i in range(rep):
            sindex = "%03d" %index
            si = "%03d" %i
            dfst_small = dfst[(dfst['packetTotalCount'] > req_pkts)] # required packets + 1 (taking into account ctc)
            if len(dfst_small) > 0:
                sel = dfst_small.sample()
                print("- Found matching flow!! in ", i+1, "of", rep, "for...", *row.tolist()[:-1], sep=" ")
                if verbose:
                    print(sel.iloc[0])
                dfst.drop(index=sel.index, inplace=True)
                #dfst1,dfst2,dfst3,dfst4,dfst5 = DropInLists(sel,dfst1,dfst2,dfst3,dfst4,dfst5)
                cfg_data['src_ip'] = sel['sourceIPAddress'].to_numpy()
                if flowkey != "1tup":
                    cfg_data['dst_ip'] = sel['destinationIPAddress'].to_numpy() 
                    if flowkey == "3tup":
                        cfg_data['proto'] = sel['protocolIdentifier'].to_numpy()
                    elif flowkey == "4tup":
                        cfg_data['src_port'] = sel['sourceTransportPort'].to_numpy() 
                        cfg_data['dst_port'] = sel['destinationTransportPort'].to_numpy()      
                    elif flowkey == "5tup":
                        cfg_data['proto'] = sel['protocolIdentifier'].to_numpy()              
                        cfg_data['src_port'] = sel['sourceTransportPort'].to_numpy()    
                        cfg_data['dst_port'] = sel['destinationTransportPort'].to_numpy()

                configfile = GCC_CONF_INJ_FOLDER+"/ccflow_"+str(sindex)+"_"+str(si)+".ini"

                if index == len(dfcg) - 1 and i == rep - 1:
                    cfg_data['inpcap'] = lastpcap
                    cfg_data['outpcap'] = outpcap
                elif index == 0 and i == 0:
                    lastpcap = auxpcapA
                    cfg_data['inpcap'] = inpcap
                    cfg_data['outpcap'] = lastpcap
                else:
                    if lastpcap == auxpcapA:
                        cfg_data['inpcap'] = auxpcapA
                        cfg_data['outpcap'] = auxpcapB
                        lastpcap = auxpcapB
                    else:
                        cfg_data['inpcap'] = auxpcapB
                        cfg_data['outpcap'] = auxpcapA
                        lastpcap = auxpcapA

                WriteInjConfigFile(configfile, cfg_data, flowkey)
                configfile = GCC_CONF_EXT_FOLDER+"/ccflow_"+str(sindex)+"_"+str(si)+".ini"
                cfg_data['inpcap'] = outpcap
                msgfile = "msg"+str(sindex)+"_"+str(si)+".txt"
                WriteExtConfigFile(configfile, cfg_data, flowkey, msgfile)

            else:
                print("- Condition not possible!! in ", i+1, "of", rep, "for...", *row.tolist()[:-1], sep=" ")

if __name__ == '__main__':
    main()
    print("\nConfig files for injecting CCs with gencc saved in: ", GCC_CONF_INJ_FOLDER)
    print("Config files for extracting CCs with gencc saved in: ", GCC_CONF_EXT_FOLDER, "\n")
