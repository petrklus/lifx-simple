#!/usr/bin/env python

"""
Simple implementation of colour-sending functionality, 
without the ACK/retry functionality. Send only, no listen.

Author: Petr Klus
"""
RETRIES  = 5
DELAY    = 0.05
UDP_PORT = 56700


import socket
import time
import sys
import random

from tools import gen_packet

SEQ_NUM = random.randint(0, 255)

def set_HSBK(bulb_ip, hue, sat, bri, kel=3500):
    print hue, sat, bri, kel    
    for _ in range(RETRIES):
        sock.sendto(gen_packet(hue, sat, bri,kel,SEQ_NUM), (bulb_ip, UDP_PORT))
        time.sleep(DELAY)

if __name__ == "__main__":
    print sys.argv
        
    # different for each execution
    
    print "Using sequence number:", SEQ_NUM
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP    
    
    bulb_ip = sys.argv[1]
    
    if len(sys.argv) == 2:
        # demo        
        print "Testing H"
        for x in range(80):
            set_HSBK(bulb_ip, 360/80*x, 100, 100)        
            time.sleep(0.1)

        print "Testing S"
        for x in range(21):
            set_HSBK(bulb_ip, 120, x*5, 100)
            time.sleep(0.1)

        print "Testing B"
        for x in range(11):
            set_HSBK(bulb_ip, 360, 100, x*10)
            time.sleep(0.1)

        print "Testing K"
        for x in range(10):
            set_HSBK(bulb_ip, 360, 0, 100, 6500/10*x+2500)
            time.sleep(0.3)
    else:
        bulb_ip            = sys.argv[1]
        hue, sat, bri, kel = map(int, sys.argv[2:])
        
        set_HSBK(bulb_ip, hue, sat, bri, kel)
    
    
