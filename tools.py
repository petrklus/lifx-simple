from struct import pack, unpack

"""
LiFX packet generator

Author: Petr Klus
"""

MESSAGE_SET_COLOR = 102
MESSAGE_SET_POWER = 117


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

    transition_time = pack("<L", 200)
    payload += transition_time

    return gen_packet_universal(seq_num, MESSAGE_SET_COLOR, payload)


def get_power_packet(seq_num, power_state):
    if type(power_state) != type(True):
        raise Exception("Invalid power state")

    if power_state:
        payload = pack(">H", 65535) # level - either 1 or 0
    else:
        payload = pack(">H", 0) # level - either 1 or 0

    payload += pack("<L", 200) # duration

    return gen_packet_universal(seq_num, MESSAGE_SET_POWER, payload)
