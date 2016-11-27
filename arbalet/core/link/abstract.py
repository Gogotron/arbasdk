"""
    Arbalet - ARduino-BAsed LEd Table
    AbstractLink - Abstract class for hardware LED controllers

    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
from __future__ import print_function  # py2 stderr
from threading import Thread
from serial import SerialException
from struct import error
from time import sleep
from ..rate import Rate

__all__ = ['AbstractLink']


class AbstractLink(Thread):
    def __init__(self, arbalet, diminution=1):
        """
        Create a thread in charge of the serial connection to hardware
        :param arbalet: The reference to arbalet controller (its touch interface can be modified)
        :param diminution: Brightness of the table from 0.0 to 1.0
        """
        Thread.__init__(self)
        self.setDaemon(True)
        self._current_device = 0
        self._diminution = diminution
        self._running = True
        self._arbalet = arbalet
        self._rate = Rate(self._arbalet.config['refresh_rate'])


    def connect(self):
        raise NotImplementedError()

    def connect_forever(self):
        success = False
        while not success:
            success = self.connect()
            if success:
                break
            sleep(0.5)
        return success

    def is_connected(self):
        raise NotImplementedError()

    def close(self):
        self._running = False

    def read_touch_frame(self):
        raise NotImplementedError()

    def write_led_frame(self, end_model):
        raise NotImplementedError()

    def run(self):
        while (self._running):
            if self.is_connected():
                try:
                    data_follows = self.write_led_frame(self._arbalet.end_model)
                    if data_follows:
                        self.read_touch_frame()
                except (SerialException, OSError, error) as e:
                    self._connected = False
                self._rate.sleep()
            else:
                self.connect_forever()
        self.close()
