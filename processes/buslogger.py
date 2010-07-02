# dspytbus.py - the Desperately Silly PYthon Threaded message BUS
# See files README and COPYING for copyright and licensing details.

from dspytbus import Component
from datetime import datetime

class BusLogger(Component):
    """
    Simple bus logger.

    This will simply print all the messages going across the bus.
    """
    def handle_message(self, message):
        print datetime.now(), "=====", message, "====="

if __name__ == "__main__":
    BusLogger().start()
