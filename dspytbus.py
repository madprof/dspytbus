"""
dspytbus.py - the Desperately Silly PYthon Threaded message BUS

Copyright (c) 2010 by |ALPHA| Mad Professor <alpha.mad.professor@gmail.com>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
                if isinstance(msg, intr):
                    com.receive_message(msg)
            if self._bus is not None and self._connected.is_set():
                self.send_message(msg)

    def start_bus(self, message):
        self.start()
        with self._lock:
            for c in self._components:
                c.start()
        self._queue.put(message)
        signal.pause()

def attach(bus, component, interest):
    bus.connect_component(component, interest)
    component.connect_bus(bus)
