import sys
import socket

from struct import error as struct_error, pack, unpack

ARTNET_HEADER = b"Art-Net\x00"
ARTNET_DMX_OPCODE = 0x5000

def make_artnet_packet(raw_data):
    header, opcode = unpack("!8sH", raw_data[:10])

    # Convert opcode to little-endian and check both header and opcode
    opcode = opcode if opcode == ARTNET_DMX_OPCODE else unpack("<H", pack(">H", opcode))[0]
    if header != ARTNET_HEADER or opcode != ARTNET_DMX_OPCODE:
        return None
    
    return ArtnetPacket(raw_data)

class ArtnetPacket:
    def __init__(self, raw_data):
        try:
            (
                self.opcode,
                self.ver,
                self.sequence,
                self.physical,
                self.universe,
                self.length,
            ) = unpack("!HHBBHH", raw_data[8:18])
            self.universe = unpack("<H", pack(">H", self.universe))[0]

            self.data = unpack(
                "{0}s".format(int(self.length)), raw_data[18 : 18 + int(self.length)]
            )[0]
        except struct_error:
            raise ValueError("Invalid Art-Net DMX packet format or data length.")

    def __str__(self):
        return (
            "ArtNet packet:\n - opcode: {0}\n - version: {1}\n - "
            "sequence: {2}\n - physical: {3}\n - universe: {4}\n - "
            "length: {5}\n - data : {6}"
        ).format(
            self.opcode,
            self.ver,
            self.sequence,
            self.physical,
            self.universe,
            self.length,
            self.data,
        )


class ArtNetReceiver:
    IP = "127.0.0.1"
    PORT = 6454

    def __init__(self, port=PORT, ip=IP, timeout=None):
        self._socket = None
        self.port = port
        self.ip = ip
        self.timeout = timeout

    @property
    def socket(self):
        if self._socket is None:
            self._socket = socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
            )
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.bind((self.ip, self.port))
            if self.timeout is not None:  # Set the timeout if it's specified
                self._socket.settimeout(self.timeout)
        return self._socket

    def receive(self):
        try:
            data, addr = self.socket.recvfrom(1024)
            return make_artnet_packet(data)
        except socket.timeout:
            return None

if __name__ == "__main__":
    print("artnet listner")
    artnet = ArtNetReceiver(ip="0.0.0.0")
    u_c = {}
    while True:
        packet = artnet.receive()
        if packet:
            if len(u_c.keys()) < 3:
                print(packet)
            else:
                print(u_c.keys())
                sys.exit()
            u_c[packet.universe] = True