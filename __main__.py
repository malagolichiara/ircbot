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

config = dict(
    host="euroserv.fr.quakenet.org",
    port=6667,
    nick="Kabot",
    ident="kabot",
    realname="Gbinside Bot",
    # channel = "#" + md5(time.strftime('%Y%m%d')).hexdigest(),
    channel="#kabot",
    channel_password='12345',  # or None
    ssl=False  # or put the filename for the certificates
)

if __name__ == '__main__':
    sys.exit(main(**config))
