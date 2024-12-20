import csv

from common.packet_type import PacketType
from common.packet import Packet


class Review(Packet):
    def __init__(self,
                 book_title: str,
                 score: float,
                 text: str,
                 client_id: int,
                 packet_id: int):
        super().__init__(client_id, packet_id)
        self.book_title = book_title
        self.score = score
        self.text = text

    @property
    def packet_type(self):
        return PacketType.REVIEW

    @property
    def payload(self):
        return [self.book_title, self.score, self.text]

    @staticmethod
    def from_csv_row(csv_row: str, client_id: int, packet_id: int) -> 'Review':
        # Id,Title,Price,User_id,profileName,review/helpfulness,review/score,review/time,review/summary,review/text
        fields = list(csv.reader([csv_row]))[0]
        title = fields[1].strip()
        score = float(fields[6].strip())
        text = fields[9].strip()

        return Review(title, score, text, client_id, packet_id)

    @staticmethod
    def decode(fields: list[str], client_id: int, packet_id: int) -> 'Review':
        title = fields[0]
        score = fields[1]
        text = fields[2]

        return Review(title, score, text, client_id, packet_id)

    def __str__(self):
        return self.encode()
