# -*- coding: utf-8 -*-

"""
Implement output-related functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2018 by rgb-24bit.
:license: GPL 3.0, see LICENSE for more details.
"""

import click

from grst.git import Status


def info(message):
    """Output information to standard output."""
    click.echo(click.style(message, fg='white'))


def warn(message):
    """Output warning message to standard output."""
    click.echo(click.style(message, fg='yellow'))


def error(message):
    """Output error message to standard output."""
    click.echo(click.style(message, fg='red'))


def status(repo):
    """Output repository status information to standard output.

    Args:
        repo: The `grst.git.Repository` object.
    """
    status_prefix = {
        Status.STATUS_SYNC: click.style('S', fg='green'),
        Status.STATUS_CLEAN: click.style('C', fg='blue'),
        Status.STATUS_MODIFY: click.style('M', fg='red')
    }.get(repo.get_status())
    path = repo.get_path()
    branch = repo.get_branch()
    output = '{status_prefix} {path} ({branch})'.format(
        status_prefix=status_prefix, path=path, branch=branch
    )
    click.echo(output)
