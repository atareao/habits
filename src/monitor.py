#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of habits
#
# Copyright (c) 2019 Lorenzo Carbonell Cerezo <a.k.a. atareao>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Gtk, Gdk
import sys
import os
import time
import math

from Xlib import X, XK, display
from Xlib.ext import record
from Xlib.protocol import rq
from configurator import Configuration
from threading import Thread


class Monitor(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self._running = False
        self.local_dpy = display.Display()
        self.record_dpy = display.Display()
        self.display = Gdk.Display.get_default()
        self.data = {}
        day = time.strftime('%Y-%m-%d', time.localtime())
        configuration = Configuration()
        stats = configuration.get('stats')
        if day in stats:
            self.data[day] = stats[day]

        # Check if the extension is present
        if not self.record_dpy.has_extension("RECORD"):
            print("RECORD extension not found")
            sys.exit(1)
        r = self.record_dpy.record_get_version(0, 0)
        print("RECORD extension version {}.{}".format(r.major_version,
                                                      r.minor_version))
        self.ctx = self.record_dpy.record_create_context(
                0,
                [record.AllClients],
                [{
                        'core_requests': (0, 0),
                        'core_replies': (0, 0),
                        'ext_requests': (0, 0, 0, 0),
                        'ext_replies': (0, 0, 0, 0),
                        'delivered_events': (0, 0),
                        'device_events': (X.KeyPress, X.MotionNotify),
                        'errors': (0, 0),
                        'client_started': False,
                        'client_died': False,
                }])
        default_seat = self.display.get_default_seat()
        _, self.x2, self.y2 = default_seat.get_pointer().get_position()

    def run(self):
        self._running = True
        self.record_dpy.record_enable_context(self.ctx, self.record_callback)

    def stop(self):
        self.local_dpy.record_disable_context(self.ctx)
        self.local_dpy.flush()
        self.record_dpy.record_free_context(self.ctx)
        self._running = False

    def save(self):
        configuration = Configuration()
        stats = configuration.get('stats')
        for day in self.data:
            stats[day] = self.data[day]
        configuration.set('stats', stats)
        configuration.save()

    def lookup_keysym(self, keysym):
        for name in dir(XK):
            if name[:3] == "XK_" and getattr(XK, name) == keysym:
                return name[3:]
        return "[%d]" % keysym

    def record_callback(self, reply):
        if reply.category != record.FromServer:
            return
        if reply.client_swapped:
            print("* received swapped protocol data, cowardly ignored")
            return
        if not len(reply.data) or reply.data[0] < 2:
            return
        data = reply.data
        while len(data):
            event, data = rq.EventField(None).parse_binary_value(
                data, self.record_dpy.display, None, None)
            if event.type == X.KeyPress:
                keysym = self.local_dpy.keycode_to_keysym(event.detail, 0)
                if keysym:
                    # self.inc_data(self.lookup_keysym(keysym), 1)
                    self.inc_data('keys', 1)
            elif event.type == X.ButtonPress:
                # self.inc_data('Button-{}'.format(event.detail), 1)
                self.inc_data('clics', 1)
            elif event.type == X.MotionNotify:
                x1 = self.x2
                y1 = self.y2
                self.x2 = event.root_x
                self.y2 = event.root_y
                monitor2 = self.display.get_monitor_at_point(self.x2, self.y2)
                dx = (self.x2 - x1) * (
                    monitor2.get_width_mm() / monitor2.get_geometry().width)
                dy = (self.y2 - y1) * (
                    monitor2.get_height_mm() / monitor2.get_geometry().height)
                distance = int(math.sqrt(math.pow(dx, 2) + math.pow(dy, 2)))
                self.inc_data('distance', distance)

    def set_data(self, key, value):
        day = time.strftime('%Y-%m-%d', time.localtime())
        if day not in self.data:
            self.data.keys = {}
        self.data[day][key] = value

    def inc_data(self, key, value):
        day = time.strftime('%Y-%m-%d', time.localtime())
        if day not in self.data:
            self.data[day] = {}
        if key not in self.data[day]:
            self.data[day][key] = 0
        self.data[day][key] += value

    def get_data(self, key):
        day = time.strftime('%Y-%m-%d', time.localtime())
        if day in self.data:
            if key in self.data[day].keys:
                return self.data[day][key]
        return 0

    def is_running(self):
        return self._running


if __name__ == '__main__':
    try:
        monitor = Monitor()
        monitor.start()
        Gtk.main()
    except KeyboardInterrupt as e:
        monitor.stop()
        monitor.save()
        print(e)
