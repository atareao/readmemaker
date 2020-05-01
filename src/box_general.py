#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of readmemaker
#
# Copyright (c) 2020 Lorenzo Carbonell Cerezo <a.k.a. atareao>
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
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Gtk
from config import _
from utils import select_in_combo, get_selected_in_combo


class BoxGeneral(Gtk.Grid):

    """Docstring for AddContextDialog. """

    def __init__(self):
        """TODO: to be defined. """
        Gtk.Grid.__init__(self)

        self.set_row_spacing(10)
        self.set_column_spacing(10)
        self.set_margin_bottom(10)
        self.set_margin_start(10)
        self.set_margin_end(10)
        self.set_margin_top(10)

        label = Gtk.Label.new(_('Project name:'))
        label.set_halign(Gtk.Align.START)
        label.set_margin_end(10)
        self.attach(label, 0, 0, 1, 1)

        self.project_name = Gtk.Entry.new()
        self.attach(self.project_name, 1, 0, 1, 1)

        label = Gtk.Label.new(_('Package name:'))
        label.set_halign(Gtk.Align.START)
        label.set_margin_end(10)
        self.attach(label, 0, 1, 1, 1)

        self.package_name = Gtk.Entry.new()
        self.attach(self.package_name, 1, 1, 1, 1)

        label = Gtk.Label.new(_('GitHub project'))
        label.set_halign(Gtk.Align.START)
        label.set_margin_end(10)
        self.attach(label, 0, 2, 1, 1)

        self.github_project = Gtk.Entry.new()
        self.attach(self.github_project, 1, 2, 1, 1)

        label = Gtk.Label.new(_('License:'))
        label.set_halign(Gtk.Align.START)
        label.set_margin_end(10)
        self.attach(label, 0, 3, 1, 1) 

        license_store = Gtk.ListStore(str, str)
        license_store.append([_('MIT'), 'MIT'])
        license_store.append([_('GPL'), 'GPL'])
        self.license = Gtk.ComboBox.new()
        self.license.set_model(license_store)
        cell1 = Gtk.CellRendererText()
        self.license.pack_start(cell1, True)
        self.license.add_attribute(cell1, 'text', 0)
        self.attach(self.license, 1, 3, 1, 1)

        select_in_combo(self.license, 'MIT')

        label = Gtk.Label.new(_('Icon:'))
        label.set_halign(Gtk.Align.START)
        label.set_margin_end(10)
        self.attach(label, 0, 4, 1, 1)

        iconfilter = Gtk.FileFilter.new()
        iconfilter.add_pattern('*.svg')
        iconfilter.add_mime_type('image/svg+xml')
        iconfilter.add_pattern('*.png')
        iconfilter.add_mime_type('image/png')

        self.icon = Gtk.FileChooserButton.new(_('Icon'),
                                              Gtk.FileChooserAction.OPEN)
        self.icon.add_filter(iconfilter)
        self.attach(self.icon, 1, 4, 1, 1)

        label = Gtk.Label.new(_('Homepage:'))
        label.set_halign(Gtk.Align.START)
        label.set_margin_end(10)
        self.attach(label, 0, 5, 1, 1)

        self.homepage = Gtk.Entry.new()
        self.attach(self.homepage, 1, 5, 1, 1)

    def get_project_name(self):
        """Get the name of the project
        :returns: the name of the project

        """
        return self.project_name.get_text()

    def get_license(self):
        """Get license
        :returns: TODO

        """
        selected_license = get_selected_in_combo(self.license)
        license = 'https://img.shields.io/badge/{}-{}-green'.format(
                _('License'), selected_license)
        return license

