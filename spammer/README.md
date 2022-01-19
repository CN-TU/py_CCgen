# Generate Artificial Traffic for the Online Covert Channel

This guide presents a small example on how to generate TCP and UDP packets with random content. The packets are tend to be sent to the machine crafting the packets to inject the covert message using the online modus of the CCgen.

We rocomment that you create two Virutal Machines (VMs): a CC machine, doing the injection and a Spammer machine, generating traffic and receiving and discarting the replies (in case of TCP for example).

In short, you should modify spammer.ini and listener.ini based on your destination (in this case the IP address of CC). See bellow for more details about how to modify those. Then you should run `python3 spammer.py` and `python3 listener.py` on the Spammer VM. On the CC VM you should run the CCgen tool as follows:
```
> python3 ../ccgen.py online send cc.cfg <queue-number-e.g.:0>
```
Of course, the configuration in `cc.cfg`, `spammer.ini` and `listener.ini` should match

Te short explaination is that the Spammer generates semi-random packets, sends them to CC where they are crafted and sent to their final destination. THe replies are then received by the Spammer and get discarded.

#Listener

listener is a simple script, that handles incomming tcp/udp connections. Application data within the connections is dropped. This script does not reply in any way. TCP connections are teared gracefully.

##configuration
-------------

listener.ini (or the specified configuration file) needs to contain at least a section with the key listen (Actually the listen key of the last section is used). The value needs to contain a port list with one port per line. A port needs to be specified with METHOD:port. All entries are not case sensitive.

##Example:

-------->8-------->8-------->8-------->8-------->8-------->8-------->8--------<br>
[Stuff]<br>
Listen=TCP:1234<br>
    UDP:4321<br>
-------->8-------->8-------->8-------->8-------->8-------->8-------->8--------<br>


#Spammer

spammer is a simple script for sending TCP/UDP data streams to a target. The
streams are sent consecutively. A connection causes the script to exit with
a return value of -1.

##configuration
-------------
listener.ini (or the specified configuration file) needs to contain at least
a section with the keys target and send (Actually the listen key of the last
section is used). Target is the IP address of the target and send needs to be
a list of instructions with one instruction per line.<br>

An instruction can be:
  -  floating point number: Pause for this number of seconds
  -  float-float: Pause for a random number of seconds chosen from this interval
  -  restart: start from the beginning
  -  CONN,PATTERN,REPEAT,PACKETS: Send this stream

1. CONN: Connection specification in the format METHOD:SRCHOST:SRCPORT:DSTPORT
-  METHOD: TCP or UDP
-  SRCHOST: source IP; if unspecified the OS choses an apropriate one
-  SRCPORT: source port; if unspecified the OS choses an apropriate one
-  DSTPORT: destination port
2. PATTERN: Pattern that will be sent per packet.
  Can be a hexadecimal number starting with 0x or text.
3. REPEAT: How often to repeate the pattern
  Can be number or start-stop, where the latter chooses a random number between start and stop. If the resulting pattern is to long the OS or the net might fragment the packets.
4. PACKETS: Number of packets to send
  Can be number or start-stop, where the latter chooses a random number between start and stop.

##Example:
  
-------->8-------->8-------->8-------->8-------->8-------->8-------->8--------<br>
[ClientA]<br>
Target = 10.1.0.2<br>
Send =<br>
    TCP:10.1.0.1::1234,0xAA,10-100,50-60<br>
    3-5<br>
    UDP:10.1.0.1:4321:1234,0xBB,30,10<br>
    2<br>
    restart<br>
-------->8-------->8-------->8-------->8-------->8-------->8-------->8--------<br>