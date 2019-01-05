# -*- coding: utf-8 -*-

"""
Implement relevant to the user repository function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2018 by rgb-24bit.
:license: GPL 3.0, see LICENSE for more details.
"""

import os


if os.name == 'nt':
    USER_HOME = os.environ['USERPROFILE']
else:
    USER_HOME = os.environ['HOME']


GRST_USER_FILE = os.path.join(USER_HOME, '.gitrepositories')


class UserRepository(object):
    """Objects that are convenient for managing user repositories."""
    def __init__(self):
        self.repositories = set()

    def add(self, path):
        path = self.absposix(path)
        if os.path.isdir(os.path.join(path, '.git')):
            self.repositories.add(path)

    def remove(self, path):
        path = self.absposix(path)
        if path in self.repositories:
            self.repositories.remove(path)

    def absposix(self, path):
        """Convert path to posix-style absolute path."""""
        return os.path.abspath(path).replace(os.sep, '/')

    def __contains__(self, path):
        return self.absposix(path) in self.repositories

    def __iter__(self):
        for repo in self.repositories:
            yield repo

    def __repr__(self):
        return 'UserRepository(%s)' % self.repositories.__repr__()


def get_user_repository(path, encoding='utf-8'):
    """Get the user repositories from the specified file."""
    user_repo = UserRepository()

    if not os.path.isfile(path):
        return user_repo

    with open(path, encoding=encoding) as f:
        for line in f:
            user_repo.add(line.strip())
    return user_repo


def save_user_repository(user_repo, path, encoding='utf-8'):
    """The specified file to save the user repositories."""
    with open(path, 'w', encoding=encoding) as f:
        for repo in user_repo:
            f.write(repo + '\n')
