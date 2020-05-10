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

        label = Gtk.Label.new(_('Project title:'))
        label.set_halign(Gtk.Align.START)
        label.set_margin_end(10)
        self.attach(label, 0, 0, 1, 1)

        self.project_title = Gtk.Entry.new()
        self.attach(self.project_title, 1, 0, 1, 1)

        label = Gtk.Label.new(_('GitHub project'))
        label.set_halign(Gtk.Align.START)
        label.set_margin_end(10)
        self.attach(label, 0, 1, 1, 1)

        self.github_project = Gtk.Entry.new()
        self.attach(self.github_project, 1, 1, 1, 1)

        label = Gtk.Label.new(_('License:'))
        label.set_halign(Gtk.Align.START)
        label.set_margin_end(10)
        self.attach(label, 0, 2, 1, 1) 

        license_store = Gtk.ListStore(str, str)
        license_store.append([_('MIT'), 'MIT'])
        license_store.append([_('GPL'), 'GPL'])
        self.license = Gtk.ComboBox.new()
        self.license.set_model(license_store)
        cell1 = Gtk.CellRendererText()
        self.license.pack_start(cell1, True)
        self.license.add_attribute(cell1, 'text', 0)
        self.attach(self.license, 1, 2, 1, 1)

        select_in_combo(self.license, 'MIT')

        label = Gtk.Label.new(_('Icon:'))
        label.set_halign(Gtk.Align.START)
        label.set_margin_end(10)
        self.attach(label, 0, 3, 1, 1)

        iconfilter = Gtk.FileFilter.new()
        iconfilter.add_pattern('*.svg')
        iconfilter.add_mime_type('image/svg+xml')
        iconfilter.add_pattern('*.png')
        iconfilter.add_mime_type('image/png')

        self.icon = Gtk.FileChooserButton.new(_('Icon'),
                                              Gtk.FileChooserAction.OPEN)
        self.icon.add_filter(iconfilter)
        self.attach(self.icon, 1, 3, 1, 1)

        label = Gtk.Label.new(_('Homepage:'))
        label.set_halign(Gtk.Align.START)
        label.set_margin_end(10)
        self.attach(label, 0, 4, 1, 1)

        self.homepage = Gtk.Entry.new()
        self.homepage.set_width_chars(50)
        self.attach(self.homepage, 1, 4, 1, 1)

        label = Gtk.Label.new(_('License badge:'))
        label.set_halign(Gtk.Align.START)
        label.set_margin_end(10)
        self.attach(label, 0, 5, 1, 1)

        self.licencia_badge = Gtk.Switch.new()
        self.licencia_badge.set_halign(Gtk.Align.START)
        self.attach(self.licencia_badge, 1, 5, 1, 1)

        label = Gtk.Label.new(_('Contributors badge:'))
        label.set_halign(Gtk.Align.START)
        label.set_margin_end(10)
        self.attach(label, 0, 6, 1, 1)

        self.contributors_badge = Gtk.Switch.new()
        self.contributors_badge.set_halign(Gtk.Align.START)
        self.attach(self.contributors_badge, 1, 6, 1, 1)

        label = Gtk.Label.new(_('Last commit badge:'))
        label.set_halign(Gtk.Align.START)
        label.set_margin_end(10)
        self.attach(label, 0, 7, 1, 1)

        self.lastcommit_badge = Gtk.Switch.new()
        self.lastcommit_badge.set_halign(Gtk.Align.START)
        self.attach(self.lastcommit_badge, 1, 7, 1, 1)

        label = Gtk.Label.new(_('CodeFactor badge:'))
        label.set_halign(Gtk.Align.START)
        label.set_margin_end(10)
        self.attach(label, 0, 8, 1, 1)

        self.codefactor_badge = Gtk.Switch.new()
        self.codefactor_badge.set_halign(Gtk.Align.START)
        self.attach(self.codefactor_badge, 1, 8, 1, 1)

    def get_project_title(self):
        """Get the name of the project
        :returns: the name of the project

        """
        return self.project_title.get_text()

    def get_license(self):
        """Get license
        :returns: TODO

        """
        return get_selected_in_combo(self.license)

    def get_general_text(self):
        text = '<!--\n'
        text += 'project_title: {}\n'.format(self.project_title.get_text())
        text += 'github_project: {}\n'.format(self.github_project.get_text())
        license = get_selected_in_combo(self.license)
        text += 'license: {}\n'.format(license)
        text += 'icon: {}\n'.format(self.icon.get_filename())
        text += 'homepage: {}\n'.format(self.homepage.get_text())
        text += 'license-badge: {}\n'.format(self.licencia_badge.get_active())
        text += 'contributors-badge: {}\n'.format(
                self.codefactor_badge.get_active())
        text += 'lastcommit-badge: {}\n'.format(
                self.lastcommit_badge.get_active())
        text += 'codefactor-badge: {}\n'.format(
                self.codefactor_badge.get_active())
        text += '--->\n'
        return text

    def get_badges(self):
        burl = 'https://img.shields.io'
        project = self.github_project.get_text().replace(
                'https://github.com/', '')
        text = ''
        if self.licencia_badge.get_active():
            license = get_selected_in_combo(self.license)
            license_badge = '![License {}]({})'.format(
                license, '{}/badge/license-{}-green'.format(burl, license))
            text += '\n{}'.format(license_badge)
        if self.contributors_badge.get_active():
            c_badge = '![Contributors]({}/github/contributors-anon/{}'.format(
                burl, project)
            text += '\n{}'.format(c_badge)
        if self.lastcommit_badge.get_active():
            lc_badge = '![Last commit]({}/github/last-commit/{}'.format(
                burl, project)
            text += '\n{}'.format(lc_badge)
        if self.codefactor_badge.get_active():
            cd_url = 'https://www.codefactor.io/repository/github'
            cf_badge = '[![CodeFactor]({url}/{project}/badge/master)]'
            cf_badge += '({url}/{project}/overview/master)'
            cf_badge = cf_badge.format(url=cd_url, project=project)
            text += '\n{}'.format(cf_badge)
        return text

    def set_license(self, license):
        select_in_combo(self.license, license)

    def get_project_title(self):
        """TODO: Docstring for get_project_title.
        :returns: TODO

        """
        return self.project_title.get_text()

    def get_homepage(self):
        """TODO: Docstring for get_homepage.
        :returns: TODO

        """
        return self.homepage.get_text()

    def get_icon(self):
        """TODO: Docstring for get_icon.
        :returns: TODO

        """
        return self.icon.get_filename()

    def get_github_project(self):
        """TODO: Docstring for get_github_project.
        :returns: TODO

        """
        return self.github_project.get_text()
