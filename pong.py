from dspytbus import Message, Component, Bus, attach

class Ping(Message):
    pass
class Pong(Message):
    pass

class Maddy(Component):
    def handle_message(self, message):
        print "Maddy GOT", message
        self.send_message(Pong())

class Mission(Component):
    def handle_message(self, message):
        print "Mission GOT", message
        self.send_message(Ping())

bus = Bus()
madprof = Maddy()
comish = Mission()

attach(bus, madprof, Ping)
attach(bus, comish, Pong)
bus.start_bus(Ping())
