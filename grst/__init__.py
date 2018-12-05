# -*- coding: utf-8 -*-

"""
Get status information showing the local git repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2018 by rgb-24bit.
:license: GPL 3.0, see LICENSE for more details.
"""

from .__version__ import __version__, __description__
from .__version__ import __author__, __author_email__
from .__version__ import __license__, __copyright__

from grst.cli import cli


if __name__ == '__main__':
    cli()
