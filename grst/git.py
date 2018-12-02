# -*- coding: utf-8 -*-

"""
Implementing git repository related functionality
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2018 by rgb-24bit.
:license: GPL 3.0, see LICENSE for more details.
"""

import os
import pygit2


# https://github.com/libgit2/libgit2/blob/master/include/git2/status.h
# pygit2 has some missing constants

GIT_STATUS_INDEX_NEW = 1 << 0
GIT_STATUS_INDEX_MODIFIED = 1 << 1
GIT_STATUS_INDEX_DELETED = 1 << 2
GIT_STATUS_INDEX_RENAMED = 1 << 3
GIT_STATUS_INDEX_TYPECHANGE = 1 << 4

GIT_STATUS_WT_NEW = 1 << 7
GIT_STATUS_WT_MODIFIED = 1 << 8
GIT_STATUS_WT_DELETED = 1 << 9
GIT_STATUS_WT_TYPECHANGE = 1 << 10
GIT_STATUS_WT_RENAMED = 1 << 11
GIT_STATUS_WT_UNREADABLE = 1 << 12

GIT_STATUS_IGNORED = 1 << 14
GIT_STATUS_CONFLICTED = 1 << 15


def is_repository(path):
    """Determine if the path is a repository path."""
    return os.path.isdir(os.path.join(path, '.git'))


class Repository(object):
    """A simplified git repository object.

    Args:
        path: the repository path.
        name: the repository name, if `None`, use the directory where
            the repository is located as the name of the repository.

    Note:
        If the path is invalid, an exception will be thrown `_pygit2.GitError`.
    """
    def __init__(self, path, name=None):
        self._repo = pygit2.Repository(path)
        self._path = os.path.abspath(path)
        self._name = name

    def get_name(self):
        """Returns the name of the repository."""
        if self._name is None:
            self._name = os.path.basename(self._path)
        return self._name

    def get_path(self):
        """Returns the absolute path of the repository."""
        return self._path

    def get_branch(self):
        """Get the current branch or HEAD of the repository."""
        if self._repo.head_is_detached:
            head = self._repo.head.target.hex[:7]
            return 'HEAD detached at %s' % head
        return self._repo.head.shorthand

    def __repr__(self):
        return 'Repository(%s)' % self._name
