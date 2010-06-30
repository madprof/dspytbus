# dspytbus.py - the Desperately Silly PYthon Threaded message BUS
# See files README and COPYING for copyright and licensing details.

"""
dspytbus.py - the Desperately Silly PYthon Threaded message BUS

First off, this is probably a really bad idea... Now that *that's*
out of the way, what is it?

I got frustrated with the complexity of the otherwise excellent
circuits framework by my pal prologic. I love his stuff, but it's
just so full of implicit assumptions that it's hard to get one's
head around starting out. I appreciate how well it all works in
his hands, but it sure doesn't in mine, at least not yet.

All my frustration lead me to think about alternative ways to
structure a component framework, and one way I couldn't get out
of my head was based on lots of threads. That's what dspytbus is.
And yes, it's pronounced "despite-bus" because I was frustrated.
Did I say that already?

In dspytbus, every component is a thread. Components get attached
to busses which are also threads. Busses can be attached to other
busses, so they are really also components at the same time. The
components communicate through messages, and when you attach them
to a bus, you can define what types of messages that component is
interested in.

That's pretty much it. Note that this is a quick prototype that I
wrote to get this darn idea out of my head, not a framework ready
for production use. I think it *could* be developed into something
useful eventually, but I doubt it'll be me who does that. Please
feel free to fork and make things better, that's why I threw it
on github.com after all.
"""

from threading import Thread, Lock, Event
from Queue import Queue
import signal

class Message(object):
    """
    Messages shuffle data between components through busses.

    You can do whatever you want with subclasses of Message.
    Actually, you don't have to use the class at all. Note,
    however, that the framework will force __origin__ into
    message objects, so you better don't use that identifier
    yourself.
    """
    pass

class Component(Thread):
    """
    Components send and receive messages.

    Remember to call __init__() from your constructor! Subclass
    this and implement handle_message() to actually do stuff.
    Don't override anything but __init__() and handle()!
    """
    def __init__(self):
        super(Component, self).__init__()
        self.daemon = True
        self._connected = Event()
        self._bus = None
        self._queue = Queue()

    def connect_bus(self, bus):
        assert isinstance(bus, Bus)
        assert bus is not self
        assert self._bus is None
        self._bus = bus
        self._connected.set()

    def send_message(self, message):
        if self._bus is None:
            self._connected.wait()
        message.__origin__ = self
        self._bus.receive_message(message)

    def receive_message(self, message):
        self._queue.put(message)

    def handle_message(self, _message):
        assert False, "override this"

    def run(self):
        while True:
            msg = self._queue.get()
            self.handle_message(msg)

class Bus(Component):
    """
    Busses broadcast/route messages between components.

    Don't subclass this. Just use it.
    """
    def __init__(self):
        super(Bus, self).__init__()
        self._lock = Lock()
        self._components = []
        self._interests = []

    def connect_component(self, component, interest):
        assert component is not self
        with self._lock:
            self._components.append(component)
            self._interests.append(interest)

    def run(self):
        while True:
            msg = self._queue.get()
            with self._lock:
                components = self._components[:]
                interests = self._interests[:]
            for com, intr in zip(components, interests):
                if isinstance(msg, intr) and msg.__origin__ is not com:
                    com.receive_message(msg)
            if self._bus is not None and self._connected.is_set():
                msg.__origin__ = self # relabel across busses
                self.send_message(msg)

    def start_bus(self, message):
        self.start()
        with self._lock:
            for c in self._components:
                c.start()
        message.__origin__ = self
        self._queue.put(message)
        signal.pause()

def attach(bus, component, interest):
    bus.connect_component(component, interest)
    component.connect_bus(bus)
