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
    gi.require_version('Gio', '2.0')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Gtk
from gi.repository import Gio
import re
import os
from bs4 import BeautifulSoup
from config import _
from config import TEMPLATE
from basedialog import BaseDialog
from box_general import BoxGeneral
from box_text import BoxText
from box_contributors import BoxContributors
from contributor import Contributor


def generate_button(icon, tooltip_text, callback):
    button = Gtk.Button()
    button.set_margin_start(10)
    button.set_margin_end(10)
    button.set_margin_top(10)
    button.set_margin_bottom(10)
    button.set_tooltip_text(tooltip_text)
    button.set_image(Gtk.Image.new_from_gicon(Gio.ThemedIcon(
        name=icon), Gtk.IconSize.BUTTON))
    button.connect('clicked', callback)
    return button


class ReadmeMaker(BaseDialog):

    """Docstring for AddContextDialog. """

    def __init__(self):
        """TODO: to be defined. """
        BaseDialog.__init__(self, _('Readme Maker. Create README'), None,
                            ok_button=False, cancel_button=False)
        self.filename = None

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

        self.boxDependencies = BoxText(_('Prerequisites:'), True)
        notebook.append_page(self.boxDependencies,
                             Gtk.Label.new(_('Prerequisites')))

        self.boxInstalling = BoxText(_('Installing:'), True)
        notebook.append_page(self.boxInstalling,
                             Gtk.Label.new(_('Installing')))

        self.boxUsing = BoxText(_('Using:'), True)
        notebook.append_page(self.boxUsing,
                             Gtk.Label.new(_('Using')))

        self.boxContributing = BoxText(_('Contibuting:'), True)
        notebook.append_page(self.boxContributing,
                             Gtk.Label.new(_('Contributing')))

        self.boxContributors = BoxContributors(_('Contributors:'), True)
        notebook.append_page(self.boxContributors,
                             Gtk.Label.new(_('Contributors')))
        self.init_headbar()

    def init_headbar(self):
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.set_title(self.get_title())
        self.set_titlebar(hb)

        button1 = Gtk.Button()
        button1.set_size_request(40, 40)
        button1.set_tooltip_text(_('Update'))
        button1.connect('clicked', self.on_button_update_clicked)
        button1.set_image(Gtk.Image.new_from_gicon(Gio.ThemedIcon(
            name='preferences-system-symbolic'), Gtk.IconSize.BUTTON))
        hb.pack_start(button1)

        self.popover = self.create_popover()
        button4 = Gtk.MenuButton()
        button4.set_size_request(40, 40)
        button4.set_tooltip_text(_('Options'))
        button4.set_popover(self.popover)
        button4.set_image(Gtk.Image.new_from_gicon(Gio.ThemedIcon(
            name='pan-down-symbolic'), Gtk.IconSize.BUTTON))
        hb.pack_end(button4)

    def create_popover(self):
        popover = Gtk.Popover()

        grid = Gtk.Grid.new()
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        popover.add(grid)

        label = Gtk.Label.new(_('New Readme'))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 0, 1, 1)

        button_open = generate_button('gtk-new', _('New Readme'),
                                      self.new_readme)
        grid.attach(button_open, 1, 0, 1, 1)

        grid.attach(Gtk.Separator(), 0, 1, 2, 1)

        label = Gtk.Label.new(_('Open Readme'))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 1, 1, 1)

        button_open = generate_button('gtk-open', _('Open Readme'),
                                      self.open_readme)
        grid.attach(button_open, 1, 1, 1, 1)

        label = Gtk.Label.new(_('Save Readme'))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 2, 1, 1)

        button_save = generate_button('gtk-save', _('Save Readme'),
                                      self.save_readme)
        grid.attach(button_save, 1, 2, 1, 1)

        grid.attach(Gtk.Separator(), 0, 3, 2, 1)

        label = Gtk.Label.new(_('Exit'))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 4, 1, 1)

        button_exit = generate_button('gtk-quit', _('Exit'),
                                      self.exit_dialog)
        grid.attach(button_exit, 1, 4, 1, 1)

        popover.show_all()
        popover.hide()
        return popover

    def on_button_update_clicked(self, widget):
        self.update_readme()

    def update_content(self, content):
        if self.filename:
            origin = self.filename
        else:
            origin = TEMPLATE
        project_title = self.boxGeneral.get_project_title()
        homepage = self.boxGeneral.get_homepage()
        icon = os.path.relpath(self.boxGeneral.get_icon(),
                               os.path.dirname(origin))
        github_project = self.boxGeneral.get_github_project()

        content_soup = BeautifulSoup(content, 'html.parser')
        for span in content_soup.select('span[id]'):
            if span['id'] == 'project_title':
                span.string = project_title
        for tag_a in content_soup.select('a[id]'):
            if tag_a['id'] == 'homepage':
                tag_a['href'] = homepage 
        for tag_img in content_soup.select('img[id]'):
            if tag_img['id'] == 'icon':
                tag_img['src'] = icon 
        return str(content_soup)

    def update_readme(self):
        description = self.boxDescription.get_content()
        self.boxDescription.set_content(self.update_content(description))
        prerequisites = self.boxDependencies.get_content()
        self.boxDependencies.set_content(self.update_content(prerequisites))
        installing = self.boxInstalling.get_content()
        self.boxInstalling.set_content(self.update_content(installing))
        using = self.boxUsing.get_content()
        self.boxUsing.set_content(self.update_content(using))
        contributing = self.boxContributing.get_content()
        self.boxContributing.set_content(self.update_content(contributing))
        intro_contributors = self.boxContributors.get_content()
        self.boxContributors.set_content(self.update_content(
            intro_contributors))

    def read_file(self, filename):
        general = self.read_section('project-info', filename)
        self.parse_general(general)
        description = self.read_section('description', filename)
        self.boxDescription.set_content(description)
        prerequisites = self.read_section('prerequisites', filename)
        self.boxDependencies.set_content(prerequisites)
        installing = self.read_section('installing', filename)
        self.boxInstalling.set_content(installing)
        using = self.read_section('using', filename)
        self.boxUsing.set_content(using)
        contributing = self.read_section('contributing', filename)
        self.boxContributing.set_content(contributing)
        intro_contributors = self.read_section('contributors', filename)
        self.boxContributors.set_content(intro_contributors)
        contributors = self.read_section('table-contributors', filename)
        soup = BeautifulSoup(contributors, 'html.parser')
        for table in soup.findAll('table'):
            if table['id'] == 'contributors':
                columns = table.findAll('td')
                rows = table.findAll('tr')
                ncolumns = len(columns)
                nrows = len(rows)
                if ncolumns > 0 and nrows > 0 and ncolumns % nrows ==0:
                    ncontributors = int(ncolumns/nrows)
                pcontributors = {}
                for row in rows:
                    columns = row.findAll('td')
                    for column in columns:
                        if column['id'] and column['id'] not in pcontributors:
                            pcontributors[column['id']] = Contributor(
                                column['id'])
                        if row['id'] == 'info_avatar':
                            pcontributors[column['id']].set_url(
                                column.a['href'])
                            pcontributors[column['id']].set_avatar_url(
                                column.a.img['src'])
                        elif row['id'] == 'info_name':
                            pcontributors[column['id']].set_name(
                                column.a.get_text().strip())
                        elif row['id'] == 'info_commit':
                            pcontributors[column['id']].set_role(
                                column.a.span.get_text())
                self.boxContributors.set_contributors(pcontributors.values())
                break

    def new_readme(self, widget):
        """TODO: Docstring for new_readme.
        :returns: TODO

        """
        user_folder = os.path.expanduser('~')
        custom_template = os.path.join(user_folder, '.config', 'readmemaker',
                                       'template.md')
        if os.path.exists(custom_template):
            template = custom_template
        else:
            template = TEMPLATE
        self.read_file(template)
        self.popover.hide()

    def open_readme(self, widget):
        dialog = Gtk.FileChooserDialog(_('Open File'), self,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OK,
                                        Gtk.ResponseType.ACCEPT))
        filter_md = Gtk.FileFilter()
        filter_md.set_name(_('Markdown files'))
        filter_md.add_mime_type('text/plain')
        dialog.add_filter(filter_md)
        if dialog.run() == Gtk.ResponseType.ACCEPT:
            self.filename = dialog.get_filename()
            self.read_file(dialog.get_filename())
        dialog.destroy()
        self.popover.hide()

    def save_readme(self, widget):
        dialog = Gtk.FileChooserDialog(_('Save File'), self,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OK,
                                        Gtk.ResponseType.ACCEPT))
        filter_md = Gtk.FileFilter()
        filter_md.set_name(_('Markdown files'))
        filter_md.add_mime_type('text/plain')
        dialog.add_filter(filter_md)
        if dialog.run() == Gtk.ResponseType.ACCEPT:
            filename = dialog.get_filename()
            if os.path.exists(filename):
                msg = _('The file exists, overwrite?')
                msg_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                               Gtk.ButtonsType.OK_CANCEL,
                                               msg)
                if msg_dialog.run() == Gtk.ResponseType.OK:
                    self.save_filename(filename)
                msg_dialog.destroy()
            else:
                self.save_filename(filename)
        dialog.destroy()
        self.popover.hide()

    def save_filename(self, filename):
        origin = self.filename if self.filename else TEMPLATE
        self.filename = filename
        all_text = ''
        all_text += '\n<!-- start project-info -->\n'
        all_text += self.boxGeneral.get_general_text()
        all_text += '\n<!-- end project-info -->\n'
        all_text += '\n<!-- start badges -->\n'
        all_text += self.boxGeneral.get_badges()
        all_text += '\n<!-- end badges -->\n'
        all_text += '\n<!-- start description -->\n'
        all_text += self.boxDescription.get_content()
        all_text += '\n<!-- end description -->\n'
        all_text += '\n<!-- start prerequisites -->\n'
        all_text += self.boxDependencies.get_content()
        all_text += '\n<!-- end prerequisites -->\n'
        all_text += '\n<!-- start installing -->\n'
        all_text += self.boxInstalling.get_content()
        all_text += '\n<!-- end installing -->\n'
        all_text += '\n<!-- start using -->\n'
        all_text += self.boxUsing.get_content()
        all_text += '\n<!-- end using -->\n'
        all_text += '\n<!-- start contributing -->\n'
        all_text += self.boxContributing.get_content()
        all_text += '\n<!-- end contributing -->\n'
        all_text += '\n<!-- start contributors -->\n'
        all_text += self.boxContributors.get_content()
        all_text += '\n<!-- end contributors -->\n'
        all_text += '\n<!-- start table-contributors -->\n'
        all_text += self.boxContributors.get_table_contributors()
        all_text += '\n<!-- end table-contributors -->\n'
        with open(filename, 'w') as fw:
            fw.write(all_text)

    def save_filename2(self, filename):
        origin = self.filename if self.filename else TEMPLATE
        self.filename = filename
        with open(origin, 'r') as fr:
            self.update_readme()
            all_text = fr.read()
            all_text = self.replace_section(
                    'project-info', all_text,
                    self.boxGeneral.get_general_text())
            all_text = self.replace_section(
                    'badges', all_text,
                    self.boxGeneral.get_badges())
            all_text = self.replace_section(
                    'description', all_text,
                    self.boxDescription.get_content())
            all_text = self.replace_section(
                    'prerequisites', all_text,
                    self.boxDependencies.get_content())
            all_text = self.replace_section(
                    'installing', all_text,
                    self.boxInstalling.get_content())
            all_text = self.replace_section(
                    'using', all_text,
                    self.boxUsing.get_content())
            all_text = self.replace_section(
                    'contributing', all_text,
                    self.boxContributing.get_content())
            all_text = self.replace_section(
                    'contributors', all_text,
                    self.boxContributors.get_content())
            all_text = self.replace_section(
                    'table-contributors', all_text,
                    self.boxContributors.get_table_contributors())
            with open(filename, 'w') as fw:
                fw.write(self.clean_between_sections(all_text))

    def exit_dialog(self, widtgt):
        self.popover.hide()
        exit(0)

    def parse_general(self, info):
        project_title = re.search(r'project_title:\s*(.*)$', info, re.M|re.I)
        if project_title:
            self.boxGeneral.project_title.set_text(project_title.groups()[0])
        github_project = re.search(r'github_project:\s*(.*)$', info, re.M|re.I)
        if github_project:
            self.boxGeneral.github_project.set_text(github_project.groups()[0])
        license = re.search(r'license:\s*(.*)$', info, re.M|re.I)
        if license:
            self.boxGeneral.set_license(github_project.groups()[0])
        icon = re.search(r'icon:\s*(.*)$', info, re.M|re.I)
        if icon:
            self.boxGeneral.icon.set_filename(icon.groups()[0])
        homepage = re.search(r'homepage:\s*(.*)$', info, re.M|re.I)
        if homepage:
            self.boxGeneral.homepage.set_text(homepage.groups()[0])
        license_badge = re.search(r'license-badge:\strue$', info, re.M|re.I)
        self.boxGeneral.licencia_badge.set_active(
                True if license_badge else False)
        contributors_badge = re.search(
                r'contributors-badge:\strue$', info, re.M|re.I)
        self.boxGeneral.contributors_badge.set_active(
                True if contributors_badge else False)
        lastcommit_badge = re.search(
                r'lastcommit-badge:\strue$', info, re.M|re.I)
        self.boxGeneral.lastcommit_badge.set_active(
                True if lastcommit_badge else False)
        codefactor_badge = re.search(
                r'codefactor-badge:\strue$', info, re.M|re.I)
        self.boxGeneral.codefactor_badge.set_active(
                True if codefactor_badge else False)

    def clean_between_sections(self, text):
        clean_text = []
        is_section = False
        pattern_start = r'^<!--\s*start\s+[^-]*-->'
        pattern_end = r'<!--\s*end\s+[^-]*-->'
        for line in text.split('\n'):
            if re.match(pattern_start, line,
                    flags=re.IGNORECASE):
                is_section = True
            if is_section:
                clean_text.append(line)
            if re.match(pattern_end, line,
                    flags=re.IGNORECASE):
                is_section = False
        return '\n'.join(clean_text)

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

    def replace_section(self, section_name, all_text, new_text):
        where = 'before' # before, section, after
        before = ''
        after = ''
        pattern_start = r'^<!--\s*start\s+{}\s*-->'.format(section_name)
        pattern_end = r'<!--\s*end\s+{}\s*-->'.format(section_name)
        for line in all_text.split('\n'):
            if re.match(pattern_end, line,
                    flags=re.IGNORECASE):
                where = 'after'
                continue
            if re.match(pattern_start, line,
                    flags=re.IGNORECASE):
                where = 'section'
                continue
            if where == 'before':
                before += '\n{}'.format(line)
            elif where == 'after':
                after += '\n{}'.format(line)
        result = before
        result += '\n<!-- start {} -->\n'.format(section_name)
        result += new_text
        result += '\n<!-- end {} -->\n'.format(section_name)
        result += after
        return result


def main():
    """TODO: Docstring for main.
    :returns: TODO

    """
    readmeMaker = ReadmeMaker()
    response = readmeMaker.run()
    if response == Gtk.ResponseType.ACCEPT:
        print(readmeMaker.boxDescription.get_content())
        pass
    readmeMaker.destroy()


if __name__ == '__main__':
    main()
