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
import re
import os
from config import _
from config import TEMPLATE
from basedialog import BaseDialog
from box_general import BoxGeneral
from box_text import BoxText
from box_contributors import BoxContributors

class ReadmeMaker(BaseDialog):

    """Docstring for AddContextDialog. """

    def __init__(self):
        """TODO: to be defined. """
        BaseDialog.__init__(self, _('Readme Maker. Create README'), None,
                            ok_button=True, cancel_button=True)

    def init_ui(self):
        BaseDialog.init_ui(self)

        notebook = Gtk.Notebook.new()
        self.grid.attach(notebook, 0, 0, 1, 1)

        self.boxGeneral = BoxGeneral()
        notebook.append_page(self.boxGeneral,
                             Gtk.Label.new(_('General')))

        self.boxDescription = BoxText(_('Description:'), True)
        notebook.append_page(self.boxDescription,
                             Gtk.Label.new(_('Description')))
        description = self.read_section('description', TEMPLATE)
        self.boxDescription.set_content(description)

        self.boxDependencies = BoxText(_('Prerequisites:'), True)
        notebook.append_page(self.boxDependencies,
                             Gtk.Label.new(_('Prerequisites')))
        prerequisites = self.read_section('prerequisites', TEMPLATE)
        self.boxDependencies.set_content(prerequisites)

        self.boxInstalling = BoxText(_('Installing:'), True)
        notebook.append_page(self.boxInstalling,
                             Gtk.Label.new(_('Installing')))
        installing = self.read_section('installing', TEMPLATE)
        self.boxInstalling.set_content(installing)

        self.boxUsing = BoxText(_('Using:'), True)
        notebook.append_page(self.boxUsing,
                             Gtk.Label.new(_('Using')))
        using = self.read_section('using', TEMPLATE)
        self.boxUsing.set_content(using)

        self.boxContributing = BoxText(_('Contibuting:'), True)
        notebook.append_page(self.boxContributing,
                             Gtk.Label.new(_('Contributing')))
        contributing = self.read_section('contributing', TEMPLATE)
        self.boxContributing.set_content(contributing)

        self.boxContributors = BoxContributors(_('Contributors:'), True)
        notebook.append_page(self.boxContributors,
                             Gtk.Label.new(_('Contributors')))
        contributors = self.read_section('contributors', TEMPLATE)
        self.boxContributors.set_content(contributors)

    def read_section(self, section_name, filename):
        """Read a section

        :section: section name
        :returns: the section readed

        """
        section = ''
        is_section = False
        pattern_start = r'^<!--\s*start\s+{}\s*-->'.format(section_name)
        pattern_end = r'<!--\s*end\s+{}\s*-->'.format(section_name)
        if os.path.exists(filename):
            with open(filename, 'r') as fr:
                for line in fr.readlines():
                    if re.match(pattern_end, line,
                            flags=re.IGNORECASE):
                        break
                    if is_section:
                        section += line
                    if re.match(pattern_start, line,
                            flags=re.IGNORECASE):
                        is_section = True
        return section


def main():
    """TODO: Docstring for main.
    :returns: TODO

    """
    readmeMaker = ReadmeMaker()
    response = readmeMaker.run()
    if response == Gtk.ResponseType.ACCEPT:
        print(readmeMaker.boxDescription.get_description())
        pass
    readmeMaker.destroy()


if __name__ == '__main__':
    main()
