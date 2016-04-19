#!/bin/sh -
# -*- coding: UTF-8 -*-
#
# (c) Chiara Malagoli
#
# v 0.0.1.0
#
# file: ircbot/__main__.py
# auth: Chiara Malagoli <malagoli@gbinside.com>
# desc:
#
# --------------

""":"
exec python $0 ${1+"$@"}
"""

from ircbot import main
import sys

if __name__ == '__main__':
    sys.exit(main(sys.argv))
