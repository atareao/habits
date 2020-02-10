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
except ValueError as e:
    print(e)
    exit(1)
from gi.repository import Gtk
from gi.repository import Gdk
import os
import config
import shutil
from config import _
from configurator import Configuration
from basedialog import BaseDialog


def convert_rgb2hex(color):
    red = int(color.red * 255)
    green = int(color.green * 255)
    blue = int(color.blue * 255)
    return '#%02x%02x%02x' % (red, green, blue)


def select_value_in_combo(combo, value):
    model = combo.get_model()
    for i, item in enumerate(model):
        if value == item[1]:
            combo.set_active(i)
            return
    combo.set_active(0)


def get_selected_value_in_combo(combo):
    model = combo.get_model()
    return model.get_value(combo.get_active_iter(), 1)


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

        self.grid.attach(Gtk.Separator(), 0, 3, 2, 1)

        label = Gtk.Label(_('Units'))
        label.set_alignment(0, 0.5)
        self.grid.attach(label, 0, 4, 1, 1)

        units_store = Gtk.ListStore(str, str)
        units_store.append([_('meters'), 'meters'])
        units_store.append([_('feets'), 'feets'])

        self.units = Gtk.ComboBox.new()
        self.units.set_model(units_store)
        cell1 = Gtk.CellRendererText()
        self.units.pack_start(cell1, True)
        self.units.add_attribute(cell1, 'text', 0)
        self.grid.attach(self.units, 1, 4, 1, 1)

        self.grid.attach(Gtk.Separator(), 0, 5, 2, 1)

        self.grid.attach(Gtk.Label.new(_('Colors')), 0, 6, 2, 1)
        self.grid.attach(Gtk.Label.new(_('Distance')), 0, 7, 1, 1)
        color = Gdk.RGBA()
        color.parse('#445c3c')
        self.distance_color = Gtk.ColorButton()
        self.grid.attach(self.distance_color, 1, 7, 1, 1)
        self.grid.attach(Gtk.Label.new(_('Clicks')), 0, 8, 1, 1)
        color.parse('#445c3c')
        self.clics_color = Gtk.ColorButton.new_with_rgba(color)
        self.grid.attach(self.clics_color, 1, 8, 1, 1)
        self.grid.attach(Gtk.Label.new(_('Keys')), 0, 9, 1, 1)
        color.parse('#445c3c')
        self.keys_color = Gtk.ColorButton()
        self.keys_color.set_rgba(color)
        self.grid.attach(self.keys_color, 1, 9, 1, 1)

    def load(self):
        configuration = Configuration()
        preferences = configuration.get('preferences')
        self.theme_light.set_active(preferences.get('theme-light'))
        self.start_actived.set_active(preferences.get('start-actived'))
        select_value_in_combo(self.units, preferences.get('units'))

        color = Gdk.RGBA()
        color.parse(preferences['distance-color'])
        self.distance_color.set_rgba(color)
        color.parse(preferences['clics-color'])
        self.clics_color.set_rgba(color)
        color.parse(preferences['keys-color'])
        self.keys_color.set_rgba(color)

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
        preferences['units'] = get_selected_value_in_combo(self.units)

        preferences['distance-color'] = convert_rgb2hex(
            self.distance_color.get_rgba())
        preferences['clics-color'] = convert_rgb2hex(
            self.clics_color.get_rgba())
        preferences['keys-color'] = convert_rgb2hex(
            self.keys_color.get_rgba())

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
