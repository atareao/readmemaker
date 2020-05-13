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
    gi.require_version('Pango', '1.0')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Gtk
from gi.repository import Pango
from config import _


class BoxDependencies(Gtk.Grid):

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

        label = Gtk.Label.new(_('Dependencies:'))
        label.set_halign(Gtk.Align.START)
        label.set_margin_end(10)
        self.attach(label, 0, 0, 1, 1)

        scrollbar = Gtk.ScrolledWindow.new(None, None)
        scrollbar.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
        scrollbar.set_size_request(500, 300)
        self.attach(scrollbar, 0, 1, 1, 1)

        self.dependencies = Gtk.TextView.new()
        self.dependencies.set_margin_bottom(10)
        self.dependencies.set_margin_start(10)
        self.dependencies.set_margin_end(10)
        self.dependencies.set_margin_top(10)
        font_desc = Pango.FontDescription.from_string("monospace")
        if font_desc:
            self.dependencies.modify_font(font_desc)
        scrollbar.add(self.dependencies)

    def get_description(self):
        """Get the project description
        :returns: the name of the project

        """
        return self.project_name.get_text()
