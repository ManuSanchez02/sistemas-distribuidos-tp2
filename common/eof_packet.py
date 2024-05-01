from common.packet import Packet
from common.packet_type import PacketType


class EOFPacket(Packet):
    def __init__(self):
        pass

    @property
    def packet_type(self):
        return PacketType.EOF

    @property
    def payload(self):
        return []

    @staticmethod
    def decode(fields: list[str]):
        return EOFPacket()

    def __str__(self):
        return self.encode()