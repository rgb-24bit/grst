# -*- coding: utf-8 -*-

"""
Implement configuration-related features
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2018 by rgb-24bit.
:license: GPL 3.0, see LICENSE for more details.
"""

import json
import os


if os.name == 'nt':
    HOME = os.environ['USERPROFILE']
else:
    HOME = os.environ['HOME']


CONFIG_FILE_NAME = os.path.join(HOME, '.gitrepositories')


class RepositoryConfig(object):
    """Object for managing repository configuration information."""
    def __init__(self):
        self.names = {}
        self.paths = {}

    def add_config(self, name, path):
        """Add a repository configuration item.

        Return:
            Add successfully returns True, otherwise returns False.

        Note:
            Name and Path are unique.
        """
        if name in self.names or path in self.paths:
            return False

        self.names[name] = path
        self.paths[path] = name

        return True

    def get_by_path(self, path):
        """Get the name corresponding to the path."""
        return self.paths.get(path)

    def get_by_name(self, name):
        """Get the path corresponding to the name."""
        return self.names.get(name)

    def set_by_path(self, path, new_name):
        """Set the name of the corresponding path to the new value."""
        old_name = self.path.get(path)
        if old_name is not None:
            del self.names[old_name]
            self.names[new_name] = path

    def set_by_name(self, name, new_path):
        """Set the path of the corresponding name to the new value."""
        old_path = self.names.get(name)
        if old_path is not None:
            del self.paths[old_path]
            self.paths[new_path] = name

    def del_by_name(self, name):
        """Delete the configuration item corresponding to the specified name."""
        path = self.names.get(name)
        if path is not None:
            del self.names[name]
            del self.paths[path]

    def del_by_path(self, path):
        """Delete the configuration item corresponding to the specified path."""
        name = self.paths.get(path)
        if name is not None:
            del self.paths[path]
            del self.names[name]

    def to_list(self):
        """Convert the RepositoryConfig object to a list."""
        lst = []
        for name in self.names:
            lst.append(dict(name=name, path=self.names[name]))
        return lst

    def from_list(self, lst):
        """Construct a RepositoryConfig object from the list."""
        for item in list:
            self.add_config(item['name'], item['path'])
        return self


def load_config(source=None, encoding='utf-8'):
    """Load the configuration from the specified source or CONFIG_FILE_NAME."""
    source = source or CONFIG_FILE_NAME

    repo_config = RepositoryConfig()

    # Return the empty configuration object directly if the configuration file does not exist
    if not os.path.isfile(source):
        return repo_config

    with open(source, encoding=encoding) as f:
        return repo_config.from_list(json.load(f))


def save_config(repo_config, target=None, encoding='uft-8'):
    """Save configuration to specified target or CONFIG_FILE_NAME."""""
    target = target or CONFIG_FILE_NAME

    with open(target, 'w', encoding=encoding) as f:
        json.dump(repo_config.to_list(), f, ensure_ascii=False, indent=4)
