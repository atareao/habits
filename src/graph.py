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
    gi.require_version('WebKit2', '4.0')
except ValueError as e:
    print(e)
    exit(1)
from gi.repository import Gtk
from gi.repository import WebKit2
import config
from basedialog import BaseDialog
from configurator import Configuration


class Graph(BaseDialog):
    def __init__(self, title='', subtitle='', days='', distance='', clics='',
                 keys=''):
        self.title = title
        self.subtitle = subtitle
        self.days = days
        self.distance = distance
        self.clics = clics
        self.keys = keys
        BaseDialog.__init__(self, title, None, ok_button=False,
                            cancel_button=False)

    def init_ui(self):
        BaseDialog.init_ui(self)

        self.scrolledwindow1 = Gtk.ScrolledWindow()
        self.scrolledwindow1.set_policy(Gtk.PolicyType.AUTOMATIC,
                                        Gtk.PolicyType.AUTOMATIC)
        self.grid.attach(self.scrolledwindow1, 0, 0, 1, 1)

        self.viewer = WebKit2.WebView()
        self.scrolledwindow1.add(self.viewer)
        self.scrolledwindow1.set_size_request(900, 600)
        self.viewer.load_uri('file://' + config.HTML_GRAPH)
        self.viewer.connect('load-changed', self.load_changed)
        self.set_focus(self.viewer)

    def update(self):
        configuration = Configuration()
        preferences = configuration.get('preferences')
        units = preferences['units']
        distance = []
        if units == 'feets':
            for i in self.distance:
                distance.append(i/3.28084)
        else:
            distance = self.distance

        self.web_send('title="{}";subtitle="{}";days={};distance={};\
            clics={};keys={};draw_graph(title,subtitle,days,distance,\
                clics, keys);'.format(self.title, self.subtitle, self.days,
                                      distance, self.clics, self.keys))

    def load_changed(self, widget, load_event):
        if load_event == WebKit2.LoadEvent.FINISHED:
            self.update()
            configuration = Configuration()
            preferences = configuration.get('preferences')
            distance_color = preferences['distance-color']
            clics_color = preferences['clics-color']
            keys_color = preferences['keys-color']
            units = preferences['units']
            self.web_send('set_colors("{}", "{}", "{}");'.format(
                distance_color, clics_color, keys_color
            ))
            self.web_send('set_units("{}");'.format(units))
            while Gtk.events_pending():
                Gtk.main_iteration()

    def web_send(self, msg):
        self.viewer.run_javascript(msg, None, None, None)


if __name__ == '__main__':
    title = 'Titulo'
    subtitle = 'Subtitulo'
    days = ['2019-12-25', '2019-12-26', '2019-12-27', 10]
    distance = [25, 30, 35]
    clics = [50, 60, 70]
    keys = [1230, 2550, 2600]
    graph = Graph(title, subtitle, days, distance, clics, keys)
    graph.run()
