#!/usr/bin/env python

import bottle as btl
import threading
import socket
import time
import tools
import receive
import Queue
# seqnum generator

def get_seq_num_fun():     
    # workaround for nested function scoping for python 2.7    
    state = {
        "seq_lock" : threading.Lock(),
        "seq_num"  : 0
    }
    
    def _get_seq_num():
        with state["seq_lock"]:
            state["seq_num"] = (state["seq_num"] + 1) % 256
            return state["seq_num"]
    return _get_seq_num

@btl.route('/<bulb_ip>/<hue>/<sat>/<bri>/<kel>')
def set_colour(**kwargs):
    
    print kwargs["bulb_ip"]
    
    for key in ["hue", "sat", "bri", "kel"]:
        kwargs[key] = float(kwargs[key])
        print key, kwargs[key]
    
    command_q.put(kwargs)
    
    return "ENQUEUED"


@btl.route('/hello')
def hello():
    return "HELLO"


RETRIES       = 10
DELAY         = 0.1
UDP_PORT      = 56700
UDP_IP        = "0.0.0.0"   # where to listen
NO_OF_SENDERS = 3
MAX_ACK_AGE   = 1           # maximum ACK age


ACKS = [0.0 for _ in xrange(256)]

def packet_listener():        
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes        
        try:
            response = receive.process_incoming_data(data, addr)
            print response
            if response["packet_id"] == 45:                
                ACKS[response["seqnum"]] = time.time()
            
        except Exception, e:
            print "Unable to process packet from: {}, (error {})".format(addr, e)


def command_sender():

    while True:
        try:
            kwargs = command_q.get()
            seq_num = get_seq_num() 
            print "seq num", seq_num
               
            for _ in range(RETRIES):
                with send_lock:
                    sock.sendto(
                        tools.gen_packet(kwargs["hue"], kwargs["sat"], kwargs["bri"], kwargs["kel"], seq_num), 
                        (kwargs["bulb_ip"], UDP_PORT))
        
                # wait...
                time.sleep(DELAY)
        
                # do we have ACK?
                if time.time() - ACKS[seq_num] < MAX_ACK_AGE:
                    print "ACK confirmed, no more retries needed"
                    break
    
        except Exception, e:
            print "Unable to process command: {}".format(e)
    

if __name__ == "__main__":

    # testing http://192.168.2.212:8888/192.168.2.222/120/100/100/3500

    # UDP functionality
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP    
    get_seq_num = get_seq_num_fun() # initialise sequence number
    
    # listen for lifx packets
    sock.bind((UDP_IP, UDP_PORT))
    
    
    # coordination objects - lock and command queue
    send_lock = threading.Lock()
    command_q = Queue.Queue(maxsize=5)
    
    
    t = threading.Thread(target=packet_listener)
    t.daemon = True
    t.start()
    
    # spawn command sending thread
    for _ in xrange(NO_OF_SENDERS):    
        t = threading.Thread(target=command_sender)
        t.daemon = True
        t.start()
    
    
    btl.run(host='0.0.0.0', port=8888)