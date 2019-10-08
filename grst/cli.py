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
from grst.git import Repository, Status, is_repository, find_repository
from grst.__version__ import __version__


@click.group()
@click.version_option(prog_name='grst', version=__version__)
def cli():
    pass


@click.command(short_help="Add the repository.")
@click.argument('path', default='.', nargs=1, type=click.Path())
@click.option('-r', '--recursion', is_flag=True,
              help='Recursive lookup repository.')
@click.option('-d', '--depth', default=1,
              help='Recursive depth')
@click.option('-s', '--submodule', is_flag=True,
              help='Whether searching submodule.')
def add(path, recursion, depth, submodule):
    user_repo = get_user_repository(GRST_USER_FILE)
    if is_repository(path):
        user_repo.add(path)
    if recursion:
        for repo in find_repository(path, depth, submodule):
            user_repo.add(repo)
    save_user_repository(user_repo, GRST_USER_FILE)


@click.command(short_help="Check the status of the repository.")
@click.option('-s', '--sync', is_flag=True,
              help='List only the repository for the status bit Sync.')
@click.option('-c', '--clean', is_flag=True,
              help='List only the repository for the status bit Clean.')
@click.option('-m', '--modify', is_flag=True,
              help='List only the repository for the status bit Modify.')
def status(sync, clean, modify):
    status_set = set()

    if sync:
        status_set.add(Status.STATUS_SYNC)
    if clean:
        status_set.add(Status.STATUS_CLEAN)
    if modify:
        status_set.add(Status.STATUS_MODIFY)

    # List all repositories if no selection is specified
    if len(status_set) == 0:
        for repo_path in get_user_repository(GRST_USER_FILE):
            output.status(Repository(repo_path))
    else:
        for repo_path in get_user_repository(GRST_USER_FILE):
            repo_obj = Repository(repo_path)
            if repo_obj.get_status() in status_set:
                output.status(repo_obj)


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
