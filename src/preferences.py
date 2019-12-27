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
except ValueError as e:
    print(e)
    exit(1)
from gi.repository import Gtk
import os
import config
import shutil
from config import _
from configurator import Configuration
from basedialog import BaseDialog


class Preferences(BaseDialog):
    def __init__(self):
        BaseDialog.__init__(self, _('Preferences'), None, ok_button=True,
                            cancel_button=True)
        self.load()

    def init_ui(self):
        BaseDialog.init_ui(self)
        self.grid.attach(Gtk.Label.new(_('Theme light:')), 0, 0, 1, 1)
        self.theme_light = Gtk.Switch.new()
        self.grid.attach(self.theme_light, 1, 0, 1, 1)
        self.grid.attach(Gtk.Label.new(_('Start actived:')), 0, 1, 1, 1)
        self.start_actived = Gtk.Switch.new()
        self.grid.attach(self.start_actived, 1, 1, 1, 1)
        self.grid.attach(Gtk.Label.new(_('Autostart:')), 0, 2, 1, 1)
        self.autostart = Gtk.Switch.new()
        self.grid.attach(self.autostart, 1, 2, 1, 1)

    def load(self):
        configuration = Configuration()
        preferences = configuration.get('preferences')
        self.theme_light.set_active(preferences['theme-light'])
        self.start_actived.set_active(preferences['start-actived'])
        autostart_file = 'habits-autostart.desktop'
        if os.path.exists(os.path.join(
                os.getenv('HOME'), '.config/autostart', autostart_file)):
            self.autostart.set_active(True)
        else:
            self.autostart.set_active(False)

    def save(self):
        configuration = Configuration()
        preferences = configuration.get('preferences')
        preferences['theme-light'] = self.theme_light.get_active()
        preferences['start-actived'] = self.start_actived.get_active()
        configuration.set('preferences', preferences)
        configuration.save()
        autostart_file = 'habits-autostart.desktop'
        autostart_file = os.path.join(
            os.getenv('HOME'), '.config/autostart', autostart_file)
        if self.autostart.get_active():
            if not os.path.exists(os.path.dirname(autostart_file)):
                os.makedirs(os.path.dirname(autostart_file))
            shutil.copyfile(config.AUTOSTART, autostart_file)
        else:
            if os.path.exists(autostart_file):
                os.remove(autostart_file)


if __name__ == '__main__':
    preferences = Preferences()
    response = preferences.run()
    if response == Gtk.ResponseType.ACCEPT:
        preferences.save()
    preferences.destroy()
