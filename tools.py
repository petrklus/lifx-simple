from struct import pack


def gen_packet(hue, sat, bri, kel, seq_num):
    if hue < 0 or hue > 360:
        raise Exception("Invalid hue")
    if sat < 0 or sat > 100:
        raise Exception("Invalid sat")
    if bri < 0 or bri > 100:
        raise Exception("Invalid bri")
    if bri < 0 or bri > 100:
        raise Exception("Invalid bri")        
    
    calc_hue = lambda hue: int(hue / 360.0 * 65535) #degrees
    calc_sat = lambda sat: int(sat / 100.0 * 65535) #percentage
    calc_bri = lambda bri: int(bri / 100.0 * 65535) #percentage
    
    packet = "\x31\x00\x00\x34\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    
    packet += pack(">B",3) # we actually want 6 bits of padding and 2 bits of 1s, not to encode in little endian
    
    packet += pack("<B",seq_num) #sequence number
    packet += "\x00\x00\x00\x00\x00\x00\x00\x00\x66\x00\x00\x00\x00"
    packet += pack("<H",calc_hue(hue))
    packet += pack("<H",calc_sat(sat))
    packet += pack("<H",calc_bri(bri))
    packet += pack("<H",int(kel))

    transition_time = pack("<L", 100)
    packet += transition_time+"\x00"
    
    return packet
