from struct import pack

"""
LiFX packet generator

Author: Petr Klus
"""


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

    packet = b"\x31\x00\x00\x34\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"  # NOQA

    # we actually want 6 bits of padding and 2 bits of 1s,
    # not to encode in little endian
    packet += pack(">B", 3)

    packet += pack("<B", seq_num)  # sequence number
    packet += b"\x00\x00\x00\x00\x00\x00\x00\x00\x66\x00\x00\x00\x00"
    packet += pack("<H", calc_hue(hue))
    packet += pack("<H", calc_sat(sat))
    packet += pack("<H", calc_bri(bri))
    packet += pack("<H", int(kel))

    transition_time = pack("<L", 200)
    packet += transition_time+b"\x00"

    return packet
