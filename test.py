#!/usr/bin/env python

from struct import pack
import socket
import time
import sys

bulb_ips = ["192.168.2.219",
            "192.168.2.220",
            "192.168.2.221",
            "192.168.2.222",
            "192.168.2.223"]
RETRIES = 5
DELAY = 0.05
UDP_PORT = 56700


def gen_packet(hue, sat, bri, kel):
    if hue < 0 or hue > 360:
        raise Exception("Invalid hue")
    if sat < 0 or sat > 100:
        raise Exception("Invalid sat")
    if bri < 0 or bri > 100:
        raise Exception("Invalid bri")
    if bri < 0 or bri > 100:
        raise Exception("Invalid bri")

    def calc_hue(hue):
        return int(hue / 360.0 * 65535)  # degrees

    def calc_sat(sat):
        return int(sat / 100.0 * 65535)  # percentage

    def calc_bri(bri):
        return int(bri / 100.0 * 65535)  # percentage

    packet = b"\x31\x00\x00\x34\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x66\x00\x00\x00\x00"  # NOQA
    packet += pack("<H", calc_hue(hue))
    packet += pack("<H", calc_sat(sat))
    packet += pack("<H", calc_bri(bri))
    packet += pack("<H", int(kel))

    transition_time = pack("<L", 100)
    packet += transition_time+b"\x00"

    return packet


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP


def set_HSBK(bulb_ip, hue, sat, bri, kel=3500):
    # make it a bit more reliable..
    print(hue, sat, bri, kel)
    for _ in range(RETRIES):
        sock.sendto(gen_packet(hue, sat, bri, kel), (bulb_ip, UDP_PORT))
        time.sleep(DELAY)

if __name__ == "__main__":
    print(sys.argv)

    if len(sys.argv) == 1:
        bulb_ip = "192.168.2.222"
        print("Testing H")
        for x in range(80):
            set_HSBK(bulb_ip, 360/80*x, 100, 100)
            time.sleep(0.1)

        print("Testing S")
        for x in range(21):
            set_HSBK(bulb_ip, 120, x*5, 100)
            time.sleep(0.1)

        print("Testing B")
        for x in range(11):
            set_HSBK(bulb_ip, 360, 100, x*10)
            time.sleep(0.1)

        print("Testing K")
        for x in range(10):
            set_HSBK(bulb_ip, 360, 0, 100, 6500/10*x+2500)
            # sock.sendto(gen_packet(360, 0, 100,6500/10*x+2500),
            # (bulb_ip, UDP_PORT))
            time.sleep(0.3)
    else:
        bulb_ip = sys.argv[1]
        hue, sat, bri, kel = map(int, sys.argv[2:])

        set_HSBK(bulb_ip, hue, sat, bri, kel)
