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

class Component(object):
    """
    Components send and receive messages.

    Remember to call __init__() from your constructor!
    """
    def __init__(self):
        """
        """
        pass

class Bus(Component):
    """
    Busses broadcast/route messages between components.

    Remember to call __init__() from your constructor!
    """
    def __init__(self):
        """
        """
        pass

def test():
    pass

if __name__ == "__main__":
    test()
