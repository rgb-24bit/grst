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
    out_fmt = '{path} {branch} -> {name}'

    path = click.style(repo.get_path(), fg='white')
    name = click.style(repo.get_name(), fg='white')

    branch_name = repo.get_branch()
    branch = {
        Status.STATUS_PERFECT: click.style('(%s)' % branch_name, fg='white'),
        Status.STATUS_CLEAN: click.style('(%s)' % branch_name, fg='yellow'),
        Status.STATUS_CHANGE: click.style('(%s)' % branch_name, fg='red')
    }.get(repo.get_status())

    click.echo(out_fmt.format(path=path, branch=branch, name=name))
