import logging
import os

from pad.db.db_util import DbWrapper
from pad.common.shared_types import Server
from pad.storage.purchase import Purchase
from pad.raw_processor import crossed_data

logger = logging.getLogger('processor')

class PurchaseProcessor(object):
    def __init__(self, data: crossed_data.CrossServerDatabase):
        self.purchase_data = {
            Server.jp: data.jp_purchase,
            Server.na: data.na_purchase,
            Server.kr: data.kr_purchase,
        }

    def process(self, db: DbWrapper):
        for server, purchase_map in self.purchase_data.items():
            logger.debug('Process {} purchases'.format(server.name.upper()))
            for raw in purchase_map:
                logger.debug('Creating purchase: %s', raw)
                item = Purchase.from_raw_purchase(raw)
                db.insert_or_update(item)
