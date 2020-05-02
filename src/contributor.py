#!/usr/bin/env python3
# one line to give the program's name and a brief description
# Copyright © 2020 yourname

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

class Contributor(object):

    """A contributor to the project"""

    def __init__(self, nickname, name, role, avatar_url, url):
        """TODO: to be defined.

        :nickname: TODO
        :name: TODO
        :role: TODO
        :url: TODO
        :avatar_url: TODO

        """
        self._nickname = nickname
        self._name = name
        self._role = role
        self._avatar_url = avatar_url
        self._url = url
        
    def get_nickname(self):
        """TODO: Docstring for get_nickname.
        :returns: TODO

        """
        return self._nickname

    def set_nickname(self, nickname):
        """TODO: Docstring for set_nickname.

        :nickname: TODO
        :returns: TODO

        """
        self._nickname = nickname

    def get_name(self):
        """TODO: Docstring for get_name.
        :returns: TODO

        """
        return self._name

    def set_name(self, name):
        """TODO: Docstring for set_name.

        :name: TODO
        :returns: TODO

        """
        self._name = name

    def get_role(self):
        """TODO: Docstring for get_role.
        :returns: TODO

        """
        return self._role

    def set_role(self, role):
        """TODO: Docstring for set_role.

        :role: TODO

        """
        self._role = role

    def get_avatar_url(self):
        """TODO: Docstring for get_avatar_url.
        :returns: TODO

        """
        return self._avatar_url

    def set_avatar_url(self, avatar_url):
        """TODO: Docstring for set_avatar_url.

        :avatar_url: TODO
        :returns: TODO

        """
        self._avatar_url = avatar_url

    def get_url(self):
        """Url for contributor

        :url: TODO
        :returns: TODO

        """
        return self._url

    def set_url(self, url):
        """Url for contributor

        :url: TODO
        :returns: TODO

        """
        self._url = url

    def __str__(self):
        string = 'Nickname: {}\n'.format(self._nickname)
        string += 'Name: {}\n'.format(self._name)
        string += 'Url: {}\n'.format(self._url)
        string += 'Avatar url: {}\n'.format(self._avatar_url)
        string += 'Role: {}'.format(self._role)
        return string

    def __eq__(self, other):
        return self.__class__ == other.__class__ and \
            self.get_nickname() == other.get_nickname()
        
