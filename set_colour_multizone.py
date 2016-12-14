#!/usr/bin/env python

"""
Simple implementation of colour-sending functionality,
without the ACK/retry functionality. Send only, no listen.

Author: Petr Klus
"""
import socket
import time
import sys
import random
import tools

from tools import gen_packet, get_colour_zones_packet

RETRIES = 2
DELAY = 0.05
UDP_PORT = 56700
SEQ_NUM = random.randint(0, 255)


def set_colour_zones(bulb_ip, start_index, end_index,
    hue, sat, bri, kel, apply_changes, retries=RETRIES):

    print(start_index, end_index, hue, sat, bri, kel, apply_changes)
    for _ in range(retries):

        sock.sendto(get_colour_zones_packet(start_index, end_index,
                hue, sat, bri, kel, apply_changes, SEQ_NUM),
                (bulb_ip, UDP_PORT))

        time.sleep(DELAY)


if __name__ == "__main__":
    print(sys.argv)

    # different for each execution

    print("Using sequence number:", SEQ_NUM)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP

    bulb_ip = sys.argv[1]

    if len(sys.argv) == 2:
        # demo
        set_colour_zones(bulb_ip, 0, 255, 60, 100, 100, 3500, tools.APPLY)
        time.sleep(1)
        for i in range(15):
            set_colour_zones(bulb_ip, i, i, 30 if i%2 == 0 else 120, 100, 100, 3500, tools.NO_APPLY, 1)

        set_colour_zones(bulb_ip, 15, 15, 60, 100, 100, 3500, tools.NO_APPLY)
        set_colour_zones(bulb_ip, 14, 14, 60, 0, 100, 6000, tools.APPLY_ONLY)

        time.sleep(1)

        # moving cursor

        def draw_thingy(position):
            # solid colour
            set_colour_zones(bulb_ip, 0, 255, 10, 100, 60, 3500, tools.NO_APPLY)
            # "cursor"
            set_colour_zones(bulb_ip, position, position, 242, 100, 100, 3500, tools.APPLY)

        for i in range(16):
            draw_thingy(i)
            time.sleep(0.05)

        for i in range(16):
            draw_thingy(15-i)
            time.sleep(0.05)

    else:
        bulb_ip = sys.argv[1]
        start_index, end_index, hue, sat, bri, kel, apply_changes = map(int, sys.argv[2:])

        set_colour_zones(bulb_ip, start_index, end_index, hue, sat, bri, kel, apply_changes)
