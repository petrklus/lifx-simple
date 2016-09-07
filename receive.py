import socket
import io
import struct

"""
LiFX test receiver

Author: Petr Klus
"""

def process_incoming_data(data, addr):
    sio = io.BytesIO(data)

    size, = struct.unpack("<H", sio.read(2))
    sec_part, = struct.unpack("<H",sio.read(2))

    protocol = sec_part % 4096

    if protocol != 1024:
        print("Not LiFX packet")
        return {
            "packet_id" : "-1",
            "message"   : "Not LiFX protocol"
        }

    source, = struct.unpack("<I",sio.read(4))

    # skip over frame address except sequence number
    sio.read(15)
    seqnum,  = struct.unpack("<B",sio.read(1))

    res, payloadtype, res2 = struct.unpack("<QHH",sio.read(12))

    if payloadtype == 45:
        # ACK
        print("Packet with seqnum", seqnum, "ACKed")
        return {
            "packet_id" : payloadtype,
            "seqnum"    : seqnum,
        }

    elif payloadtype == 107:
        print("Light state received with seqnum", seqnum)
        print("MSG:",size, protocol, payloadtype)
        return {
            "packet_id" : payloadtype,
            "seqnum"    : seqnum,
        }

    # fallback for not currently processed packets
    return {
        "packet_id" : "-1",
        "message"   : "Payloadtype: {} not currently supported".format(payloadtype)
    }


if __name__ == "__main__":

    # standalone demo
    UDP_IP = "0.0.0.0"
    UDP_PORT = 56700
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        process_incoming_data(data, addr)
