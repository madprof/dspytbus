# dspytbus.py - the Desperately Silly PYthon Threaded message BUS
# See files README and COPYING for copyright and licensing details.

import logging
from dspytbus import Component

LOGGER = logging.getLogger('dspytbus.BusLogger')

class BusLogger(Component):
    """
    Simple bus logger.

    Log all messages of interest across the bus.
    """
    def handle_message(self, message):
        LOGGER.info(message)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    BusLogger().start()
