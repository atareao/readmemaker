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
from basedialog import BaseDialog
from box_general import BoxGeneral
from box_text import BoxText


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

        self.boxDescription = BoxText(_('Description:'))
        notebook.append_page(self.boxDescription,
                             Gtk.Label.new(_('Description')))

        self.boxDependencies = BoxText(_('Prerrequisites:'), True)
        notebook.append_page(self.boxDependencies,
                             Gtk.Label.new(_('Prerrequisites')))
        prerrequisites=''' Before you begin, ensure you have met the \
following requirements:

* If you install it from PPA don't worry about, becouse all the requirements \
are included in the package
* If you clone the repository, you need, at least, these dependecies,

```
```
'''
        self.boxDependencies.set_content(prerrequisites)

        self.boxInstalling = BoxText(_('Installing:'))
        notebook.append_page(self.boxInstalling,
                             Gtk.Label.new(_('Installing')))
        installing = '''To install **${title}**, follow these steps:

* In a terminal (`Ctrl+Alt+T`), run these commands

```
```
'''
        self.boxInstalling.set_content(installing)

        self.boxInstalling = BoxText(_('Using:'))
        notebook.append_page(self.boxInstalling,
                             Gtk.Label.new(_('Using')))

        self.boxInstalling = BoxText(_('Contibuting:'))
        notebook.append_page(self.boxInstalling,
                             Gtk.Label.new(_('Contributing')))

        self.boxInstalling = BoxText(_('Contributors:'))
        notebook.append_page(self.boxInstalling,
                             Gtk.Label.new(_('Contributing')))


if __name__ == '__main__':
    readmeMaker = ReadmeMaker()
    response = readmeMaker.run()
    if response == Gtk.ResponseType.ACCEPT:
        print(readmeMaker.boxDescription.get_description())
        pass
    readmeMaker.destroy()

