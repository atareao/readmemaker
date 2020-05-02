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
import os
from basedialog import BaseDialog
from contributor import Contributor
from list_box_contributors import ListBoxContributors
from contributor_dialog import ContributorDialog
from config import _


class ListContributors(BaseDialog):
    """docstring for ListTodos"""
    def __init__(self, contributors=[]):
        BaseDialog.__init__(self, _('List of contributors'), None,
                            ok_button=True, cancel_button=True)
        self.load(contributors)

    def init_ui(self):
        BaseDialog.init_ui(self)

        self.contributors = ListBoxContributors()
        self.contributors.set_size_request(300, 500)
        self.grid.attach(self.contributors, 0, 0, 1, 1)

        box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
        self.grid.attach(box, 1, 0, 1, 2)

        button_add = Gtk.Button.new_with_label(_('Add contributor'))
        button_add.connect('clicked', self.on_button_add_clicked)
        box.add(button_add)

        button_edit = Gtk.Button.new_with_label(_('Edit contributor'))
        button_edit.connect('clicked', self.on_button_edit_clicked)
        box.add(button_edit)

        button_remove = Gtk.Button.new_with_label(_('Remove contributor'))
        button_remove.connect('clicked', self.on_button_remove_clicked)
        box.add(button_remove)

        button_clear = Gtk.Button.new_with_label(_('Clear contributor'))
        button_clear.connect('clicked', self.on_button_clear_clicked)
        box.add(button_clear)

    def on_priority_project_context_changed(self, widget):
        priority = get_selected_value_in_combo(self.priority)
        if priority == -1 or priority is None:
            priority = None
        else:
            priority = chr(priority + 65)
        project = get_selected_value_in_combo(self.project)
        if project == '-' or project is None:
            project = None
        context = get_selected_value_in_combo(self.context)
        if context == '-' or context is None:
            context = None
        self.todos.filter(priority, project, context)

    def on_toggled(self, widget):
        list_of_todos = self.todos.get_items()
        results = todotxtio.search(list_of_todos, contexts=self.contexts.get_items(), projects=self.projects.get_items())

    def on_button_clear_clicked(self, widget):
        self.todos.clear()

    def on_button_add_clicked(self, widget):
        addTodoDialog = AddTodoDialog()
        if addTodoDialog.run() == Gtk.ResponseType.ACCEPT:
            todo = addTodoDialog.get_task()
            self.todos.add_item(todo)
        addTodoDialog.destroy()

    def on_button_edit_clicked(self, widget):
        selected = self.todos.get_selected()
        if selected:
            todo = selected.get_todo()
            addTodoDialog = AddTodoDialog(todo)
            if addTodoDialog.run() == Gtk.ResponseType.ACCEPT:
                todo = addTodoDialog.get_task()
                self.todos.set_selected(todo)
            addTodoDialog.destroy()

    def on_button_remove_clicked(self, widget):
        selected = self.todos.get_selected()
        if selected:
            todo = selected.get_todo()
            self.todos.remove_item(todo)

    def load(self, contributors):
        pass


if __name__ == '__main__':
    listContributors = ListContributors()
    response = listContributors.run()
    if response == Gtk.ResponseType.ACCEPT:
        pass
    listContributors.destroy()
