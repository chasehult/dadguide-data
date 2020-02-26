"""
Parses monster purchase data.
"""

import json
import os
from typing import List

from pad.common import pad_util
from pad.common.pad_util import Printable
from pad.common.shared_types import Server

FILE_NAME = 'shop_item.json'

class Purchase(Printable):
    """Buyable monsters."""

    def __new__(cls, raw, server, tbegin, tend):
        if str(raw[0]) != "P": # Either P (point purchase) or T (time interval)
            return raw[1], raw[2]
        return super(Purchase, cls).__new__(cls)

    def __init__(self, raw: List[str], server: Server, tbegin, tend):
        self.server = server
        self.start_time_str = tbegin
        self.start_timestamp = pad_util.gh_to_timestamp_2(self.start_time_str, server)
        self.end_time_str = tend
        self.end_timestamp = pad_util.gh_to_timestamp_2(self.end_time_str, server)
        self.type = str(raw[0])   # Should be P

        # Trade monster ID
        self.monster_id = int(raw[1])

        # Cost of the monster in MP
        self.cost = int(raw[2])

        # Probably amount.  Always 1
        self.amount = int(raw[3])

        # A None and two 0s
        self.unknown = raw[4:]

    def __str__(self):
        return 'Purchase({} {} - {})'.format(self.server, self.monster_id, self.cost)

    def __eq__(self, other):
        return self.monster_id == other.monster_id

    def __hash__(self):
        return self.monster_id * 90237433

    def sterilize(self):
        return "{},{},{}".format(self.server.value, self.monster_id, self.cost)

    @staticmethod
    def unsterilize(sterilized):
        sterilized=[int(val) for val in sterilized.split(',')]
        return Purchase(['P', sterilized[1], sterilized[2], 1, None, 0, 0], Server(sterilized[0]))


def load_data(server: Server, data_dir: str = None, json_file: str = None) -> List[Purchase]:
    """Load Card objects from PAD JSON file."""
    data_json = pad_util.load_raw_json(data_dir, json_file, FILE_NAME)
    tdata = None, None
    mpbuys = []
    for item in filter(None, data_json['d'].split('\n')):
        p = Purchase(item.split(','), server, *tdata)
        if isinstance(p, tuple):
            tdata = p
        else:
            mpbuys.append(p)
    return list(set(mpbuys))
