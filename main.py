#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2014 Aleksander Morgado <aleksander@aleksander.es>
# Copyright (C) 2022 Tao J <tao-j@outlook.com>

from MMWatcher import MMWatcher
from gi.repository import Gio, GLib, GObject, ModemManager
import signal
import sys
from datetime import datetime
import gi
gi.require_version('ModemManager', '1.0')


def signal_handler(loop):
    """SIGHUP and SIGINT handler."""
    loop.quit()


def main():

    MMWatcher()

    # Main loop
    main_loop = GLib.MainLoop()
    GLib.unix_signal_add(
        GLib.PRIORITY_HIGH, signal.SIGHUP, signal_handler, main_loop)
    GLib.unix_signal_add(
        GLib.PRIORITY_HIGH, signal.SIGTERM, signal_handler, main_loop)
    try:
        main_loop.run()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
