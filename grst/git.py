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


def find_repository(path, depth, submodule):
    """Find subdirectories recursively in the repository.

    Args:
        path: To find the parent directory.
        depth: Find depth.
        submodule: Whether searching submodule.
    """
    if depth > 0:
        for subitem in os.listdir(path):
            if subitem == '.git':
                continue
            subpath = os.path.join(path, subitem)
            if os.path.isdir(subpath):
                if is_repository(subpath):
                    yield subpath
                    if submodule:
                        yield from find_repository(subpath, depth - 1, submodule)
                else:
                    yield from find_repository(subpath, depth - 1, submodule)


class Repository(object):
    """A simplified git repository object.

    Args:
        path: the repository path.
        name: the repository name, if `None`, use the directory where
            the repository is located as the name of the repository.

    Note:
        If the path is invalid, an exception will be thrown `_pygit2.GitError`.
    """
    def __init__(self, path):
        self._repo = pygit2.Repository(path)
        self._path = os.path.abspath(path)
        self._status = Status(self._repo)

    def get_path(self):
        """Returns the absolute path of the repository."""
        return self._path

    def get_branch(self):
        """Get the current branch or HEAD of the repository."""
        if self._repo.head_is_detached:
            head = self._repo.head.target.hex[:7]
            return 'HEAD detached at %s' % head
        return self._repo.head.shorthand

    def get_status(self):
        """Get the status information of the repository.

        The meaning of the return value is shown in the class Status.
        """
        return self._status.get_status()

    def __repr__(self):
        return 'Repository(%s)' % self._path


class Status(object):
    """Abstraction of repository state information.

    Args:
        repo: A pygit2.Repository object.

    Status Type:
        STATUS_SYNC: The work tree is clean and synchronized with the tracked branch.
        STATUS_CLEAN: The work tree is clean.
        STATUS_MODIFY: Uncommitted changes in the work tree.
    """

    STATUS_SYNC = 0
    STATUS_CLEAN = 1
    STATUS_MODIFY = 2

    def __init__(self, repo):
        self._repo = repo
        self._status = None

    def get_status(self):
        """Get the status of the repository."""
        # Obtaining status is a relatively time consuming operation,
        # through _status cache status, not repeated acquisition
        if self._status is None:
            self._status = self._get_status()
        return self._status

    def _get_status(self):
        if self._is_clean():
            if self._is_sync():
                return Status.STATUS_SYNC
            return Status.STATUS_CLEAN
        return Status.STATUS_MODIFY

    def _is_clean(self):
        """Determine if the repository work tree is clean."""
        # https://libgit2.org/libgit2/ex/HEAD/status.html
        not_clean_status = {
            GIT_STATUS_INDEX_NEW,
            GIT_STATUS_INDEX_MODIFIED,
            GIT_STATUS_INDEX_DELETED,
            GIT_STATUS_INDEX_RENAMED,
            GIT_STATUS_INDEX_TYPECHANGE,
            GIT_STATUS_WT_NEW,
            GIT_STATUS_WT_MODIFIED,
            GIT_STATUS_WT_DELETED,
            GIT_STATUS_WT_RENAMED,
            GIT_STATUS_WT_TYPECHANGE,
        }
        curr_repo_status = set(self._repo.status().values())
        return len(not_clean_status & curr_repo_status) == 0

    def _is_sync(self):
        """Determine if the current branch and the remote branch are synchronized.

        If you have not tracked the remote branch, False is returned by default.
        """
        # https://www.pygit2.org/references.html#the-branch-type
        for branch in self._repo.branches:
            if self._repo.branches[branch].is_head():
                head_branch = self._repo.branches[branch]
                break

        if head_branch.upstream:
            return head_branch.target == head_branch.upstream.target
        else:
            return False
