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
from list_box_contributors import ListBoxContributors
from contributor_dialog import ContributorDialog


class BoxContributors(Gtk.Grid):

    """Docstring for AddContextDialog. """

    def __init__(self, title, source_code=False):
        """TODO: to be defined. """
        Gtk.Grid.__init__(self)

        self.set_row_spacing(10)
        self.set_column_spacing(10)
        self.set_margin_bottom(10)
        self.set_margin_start(10)
        self.set_margin_end(10)
        self.set_margin_top(10)

        label = Gtk.Label.new(title)
        label.set_halign(Gtk.Align.START)
        label.set_margin_end(10)
        self.attach(label, 0, 0, 2, 1)

        scrollbar = Gtk.ScrolledWindow.new(None, None)
        scrollbar.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
        scrollbar.set_size_request(800, 150)
        self.attach(scrollbar, 0, 1, 2, 1)

        self.content = Gtk.TextView.new()
        self.content.set_margin_bottom(10)
        self.content.set_margin_start(10)
        self.content.set_margin_end(10)
        self.content.set_margin_top(10)
        if source_code:
            font_desc = Pango.FontDescription.from_string('monospace')
            if font_desc:
                self.content.modify_font(font_desc)
        scrollbar.add(self.content)

        self.attach(Gtk.Separator(), 0, 2, 2, 1)

        self.contributors = ListBoxContributors()
        self.contributors.set_size_request(500, 150)
        self.attach(self.contributors, 0, 3, 1, 1)
        
        box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
        self.attach(box, 1, 3, 1, 1)

        button_add = Gtk.Button.new_with_label(_('Add contributor'))
        button_add.connect('clicked', self.on_button_add_clicked)
        box.add(button_add)

        button_edit = Gtk.Button.new_with_label(_('Edit contributor'))
        button_edit.connect('clicked', self.on_button_edit_clicked)
        box.add(button_edit)

        button_remove = Gtk.Button.new_with_label(_('Remove contributor'))
        button_remove.connect('clicked', self.on_button_remove_clicked)
        box.add(button_remove)

        button_clear = Gtk.Button.new_with_label(_('Clear contributors'))
        button_clear.connect('clicked', self.on_button_clear_clicked)
        box.add(button_clear)

    def on_button_remove_clicked(self, widget):
        selected = self.contributors.get_selected()
        if selected:
            self.contributors.remove_item(selected)

    def on_button_clear_clicked(self, widget):
        self.contributors.clear()

    def on_button_add_clicked(self, widget):
        contributorDialog = ContributorDialog()
        if contributorDialog.run() == Gtk.ResponseType.ACCEPT:
            contributor = contributorDialog.get_contributor()
            self.contributors.add_item(contributor)
        contributorDialog.destroy()

    def on_button_edit_clicked(self, widget):
        selected = self.contributors.get_selected()
        if selected:
            contributorDialog = ContributorDialog(selected.get_contributor())
            if contributorDialog.run() == Gtk.ResponseType.ACCEPT:
                contributor = contributorDialog.get_contributor()
                self.contributors.add_item(contributor)
            contributorDialog.destroy()


    def get_content(self):
        """Get the content
        :returns: the content

        """
        buffer = self.content.get_buffer()
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_end_iter()
        return  buffer.get_text(start_iter, end_iter, True) 

    def set_content(self, content):
        """Set the content
        :content: The content

        """
        self.content.get_buffer().set_text(content)

    def get_contributors(self):
        """TODO: Docstring for get_contributors.
        :returns: TODO

        """
        return self.contributors.get_items()

    def set_contributors(self, contributors):
        """TODO: Docstring for set_contributors.

        :contributors: TODO
        :returns: TODO

        """
        self.contributors.add_all(contributors)

    def get_table_contributors(self, github_project=''):
        table = '\n<table id="contributors">'
        table += '\n\t<tr id="info_avatar">'
        for contributor in self.contributors.get_contributors():
            #contributor = row_contributor.get_contributor()
            print(contributor)
            table += '\n\t\t<td id="{}" align="center">'.format(
                    contributor.get_nickname())
            table += '\n\t\t\t<a href="{}">'.format(
                    contributor.get_url())
            table += '\n\t\t\t\t<img src="{}" width="100px"/>'.format(
                    contributor.get_avatar_url())
            table += '\n\t\t\t</a>'
            table += '\n\t\t</td>'
        table += '\n\t</tr>'
        table += '\n\t<tr id="info_name">'
        for contributor in self.contributors.get_contributors():
            table += '\n\t\t<td id="{}" align="center">'.format(
                    contributor.get_nickname())
            table += '\n\t\t\t<a href="{}">'.format(
                    contributor.get_url())
            table += '\n\t\t\t\t<strong>{}</strong>'.format(
                    contributor.get_name())
            table += '\n\t\t\t</a>'
            table += '\n\t\t</td>'
        table += '\n\t</tr>'
        table += '\n\t<tr id="info_commit">'
        for contributor in self.contributors.get_contributors():
            table += '\n\t\t<td id="{}" align="center">'.format(
                    contributor.get_nickname())
            table += '\n\t\t\t<a href="{}/commits?author={}">'.format(
                    github_project, contributor.get_nickname())
            table += '\n\t\t\t\t<span id="role">{}</span>'.format(
                    contributor.get_role())
            table += '\n\t\t\t</a>'
            table += '\n\t\t</td>'
        table += '\n\t</tr>'
        table += '\n</table>'
        return table

