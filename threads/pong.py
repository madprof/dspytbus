# dspytbus.py - the Desperately Silly PYthon Threaded message BUS
# See files README and COPYING for copyright and licensing details.

from dspytbus import Message, Component, Bus, attach

class Ping(Message):
    pass
class Pong(Message):
    pass

class Maddy(Component):
    def handle_message(self, message):
        print "Maddy got", message
        self.send_message(Pong())

class Mission(Component):
    def handle_message(self, message):
        print "Mission got", message
        self.send_message(Ping())

bus = Bus()
madprof = Maddy()
comish = Mission()

attach(bus, madprof, Ping)
attach(bus, comish, Pong)
bus.start_bus(Ping())
