# -*- coding: utf-8 -*-

"""
Command line interface implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2018 by rgb-24bit.
:license: GPL 3.0, see LICENSE for more details.
"""

import os

import click

from grst import output
from grst.userepository import GRST_USER_FILE
from grst.userepository import get_user_repository, save_user_repository
from grst.git import Repository, is_repository
from grst.__version__ import __version__


@click.group()
@click.version_option(prog_name='grst', version=__version__)
def cli():
    pass


@click.command(short_help="Add the repository.")
@click.argument('path', default='.', nargs=1, type=click.Path())
def add(path):
    if is_repository(path):
        user_repo = get_user_repository(GRST_USER_FILE)
        user_repo.add(path)
        save_user_repository(user_repo, GRST_USER_FILE)
    else:
        output.error('Not a git repository.')


@click.command(short_help="Check the status of the repository.")
def status():
    for repo in get_user_repository(GRST_USER_FILE):
        output.status(Repository(repo))


@click.command(short_help="Remove the repository from grst.")
@click.argument('path', default='.', nargs=1, type=click.Path())
def remove(path):
    user_repo = get_user_repository(GRST_USER_FILE)
    user_repo.remove(path)
    save_user_repository(user_repo, GRST_USER_FILE)


# Install click commands.
cli.add_command(add)
cli.add_command(status)
cli.add_command(remove)


if __name__ == '__main__':
    cli()
