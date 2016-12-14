from struct import pack, unpack
import logging

logger = logging.getLogger("lifx_packet_tools")

"""
LiFX packet generator

Author: Petr Klus
"""

MESSAGE_SET_COLOR = 102
MESSAGE_SET_POWER = 117

MESSAGE_SET_COLOR_ZONES = 501

DURATION = 100
NO_APPLY = 0
APPLY = 1
APPLY_ONLY = 2

def gen_packet_universal(seq_num, message_type, payload):
    # size
    #packet = b"\x31\x00"

    # binary field
    packet = b"\x00\x34"

    # source
    packet += b"\x00\x00\x00\x00"

    # frame address
    packet += b"\x00\x00\x00\x00\x00\x00\x00\x00"

    # reserved section
    packet += b"\x00\x00\x00\x00\x00\x00"  # NOQA

    # we actually want 6 bits of padding and 2 bits of 1s,
    # res_required and ack_required
    packet += pack(">B", 3)

    packet += pack("<B", seq_num)  # sequence number

    # protocol header
    packet += b"\x00\x00\x00\x00\x00\x00\x00\x00" # padding
    packet += pack("<H", message_type)   # type
    packet += b"\x00\x00"   # padding

    # payload
    packet += payload

    # finally, calculate size adjusting for the size information itself
    packet = pack("<H", len(packet)+2) + packet + b"\x00"

    return packet


def gen_packet(hue, sat, bri, kel, seq_num):
    if hue < 0 or hue > 360:
        raise Exception("Invalid hue: 0-360")
    if sat < 0 or sat > 100:
        raise Exception("Invalid sat: 0-100")
    if bri < 0 or bri > 100:
        raise Exception("Invalid bri: 0-100")
    if kel < 2500 or kel > 9000:
        raise Exception("Invalid kel: 2500-9000")

    def calc_hue(hue):
        return int(hue / 360.0 * 65535)  # degrees

    def calc_sat(sat):
        return int(sat / 100.0 * 65535)  # percentage

    def calc_bri(bri):
        return int(bri / 100.0 * 65535)  # percentage

    payload = b"\x00"
    payload += pack("<H", calc_hue(hue))
    payload += pack("<H", calc_sat(sat))
    payload += pack("<H", calc_bri(bri))
    payload += pack("<H", int(kel))

    transition_time = pack("<L", DURATION)
    payload += transition_time

    return gen_packet_universal(seq_num, MESSAGE_SET_COLOR, payload)


def get_power_packet(seq_num, power_state):
    if type(power_state) != type(True):
        raise Exception("Invalid power state")

    if power_state:
        payload = pack(">H", 65535) # 1 - switched on
    else:
        payload = pack(">H", 0)     # 0 - switched off

    payload += pack("<L", DURATION)      # duration

    return gen_packet_universal(seq_num, MESSAGE_SET_POWER, payload)



def get_colour_zones_packet(start_index, end_index,
    hue, sat, bri, kel, apply_changes, seq_num):

    if start_index < 0 or start_index > 255:
        raise Exception("Invalid start_index: 0-255")
    if end_index < 0 or end_index > 255:
        raise Exception("Invalid end_index: 0-255")
    if start_index > end_index:
        raise Exception("Invalid end_index: needs to be < start_index")
    if hue < 0 or hue > 360:
        raise Exception("Invalid hue: 0-360")
    if sat < 0 or sat > 100:
        raise Exception("Invalid sat: 0-100")
    if bri < 0 or bri > 100:
        raise Exception("Invalid bri: 0-100")
    if kel < 2500 or kel > 9000:
        raise Exception("Invalid kel: 2500-9000")
    if apply_changes not in [0, 1, 2]:
        raise Exception("Invalid apply_changes, allowed: 0, 1 or 2")

    def calc_hue(hue):
        return int(hue / 360.0 * 65535)  # degrees

    def calc_sat(sat):
        return int(sat / 100.0 * 65535)  # percentage

    def calc_bri(bri):
        return int(bri / 100.0 * 65535)  # percentage

    payload = pack("<B", start_index)
    payload += pack("<B", end_index)

    payload += pack("<H", calc_hue(hue))
    payload += pack("<H", calc_sat(sat))
    payload += pack("<H", calc_bri(bri))
    payload += pack("<H", int(kel))

    payload += pack("<L", DURATION)      # duration
    payload += pack("<B", apply_changes) # apply_changes

    logger.debug("test")
    return gen_packet_universal(seq_num, MESSAGE_SET_COLOR_ZONES, payload)
