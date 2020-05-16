#!/usr/bin/env python
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
from basedialog import BaseDialog
from utils import select_in_combo, get_selected_in_combo
from contributor import Contributor
import requests


class ContributorDialog(BaseDialog):
    """Docstring for AddTodoDialog. """

    def __init__(self, contributor=None):
        """TODO: to be defined. """
        BaseDialog.__init__(self, _('Add task'), None, ok_button=True,
                            cancel_button=True)
        self.contributor = contributor
        if contributor:
            self.nickname.set_text(self.contributor.get_nickname())
            self.name.set_text(self.contributor.get_name())
            self.url.set_text(self.contributor.get_url())
            self.avatar_url.set_text(self.contributor.get_avatar_url())
            select_in_combo(self.role, self.contributor.get_role())
        else:
            select_in_combo(self.role, -1)

    def init_ui(self):
        BaseDialog.init_ui(self)

        label = Gtk.Label.new(_('Nick name:'))
        label.set_property('halign', Gtk.Align.START)
        self.grid.attach(label, 0, 0, 1, 1)

        self.nickname = Gtk.Entry.new()
        self.grid.attach(self.nickname, 1, 0, 1, 1)

        button_import = Gtk.Button.new_with_label(_('Import from GitHub'))
        button_import.connect('clicked', self.on_button_import_clicked)
        self.grid.attach(button_import, 0, 1, 2, 1)

        label = Gtk.Label.new(_('Name:'))
        label.set_property('halign', Gtk.Align.START)
        self.grid.attach(label, 0, 2, 1, 1)

        self.name = Gtk.Entry.new()
        self.grid.attach(self.name, 1, 2, 1, 1)

        label = Gtk.Label.new(_('Url:'))
        label.set_property('halign', Gtk.Align.START)
        self.grid.attach(label, 0, 3, 1, 1)

        self.url = Gtk.Entry.new()
        self.grid.attach(self.url, 1, 3, 1, 1)

        label = Gtk.Label.new(_('Avatar url:'))
        label.set_property('halign', Gtk.Align.START)
        self.grid.attach(label, 0, 4, 1, 1)

        self.avatar_url = Gtk.Entry.new()
        self.grid.attach(self.avatar_url, 1, 4, 1, 1)

        label = Gtk.Label.new(_('Role'))
        label.set_property('halign', Gtk.Align.START)
        self.grid.attach(label, 0, 5, 1, 1)

        role_store = Gtk.ListStore(str, str)
        role_store.append(['🐛 - {}'.format(_('Bug')), '🐛'])
        role_store.append(['💻 - {}'.format(_('Code')), '💻'])
        role_store.append(['🎨 - {}'.format(_('Design')), '🎨'])
        role_store.append(['📖 - {}'.format(_('Documentation')), '📖'])
        role_store.append(['🤔 - {}'.format(_('Ideas')), '🤔'])
        role_store.append(['🌍 - {}'.format(_('Translation')), '🌍'])
        self.role = Gtk.ComboBox.new()
        self.role.set_model(role_store)
        cell1 = Gtk.CellRendererText()
        self.role.pack_start(cell1, True)
        self.role.add_attribute(cell1, 'text', 0)
        self.grid.attach(self.role, 1, 5, 1, 1)

    def on_button_import_clicked(self, widget):
        nickname = self.nickname.get_text()
        if nickname != '':
            url = 'https://api.github.com/users/{}'.format(nickname)
            content = requests.get(url)
            if content.status_code == 200:
                data = content.json()
                if 'name' in data and data['name']:
                    self.name.set_text(data['name'])
                else:
                    self.name.set_text(nickname)
                self.url.set_text(data['html_url'])
                self.avatar_url.set_text(data['avatar_url'])

    def get_contributor(self):
        """Return contributor
        :returns: TODO

        """
        nickname = self.nickname.get_text()
        name = self.name.get_text()
        url = self.url.get_text()
        avatar_url = self.avatar_url.get_text()
        role = get_selected_in_combo(self.role)
        contributor = Contributor(nickname, name, role, avatar_url, url)
        return contributor

if __name__ == '__main__':
    contributorDialog = ContributorDialog()
    if contributorDialog.run() == Gtk.ResponseType.ACCEPT:
        contributor = contributorDialog.get_contributor()
        print(contributor)
    contributorDialog.destroy()
