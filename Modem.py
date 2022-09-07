# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2014 Aleksander Morgado <aleksander@aleksander.es>
# Copyright (C) 2022 Tao J <tao-j@outlook.com>

import gi

gi.require_version("ModemManager", "1.0")
from gi.repository import Gio, GLib, GObject, ModemManager


class Modem:
    def __init__(self, obj):
        # MM obj
        self.obj = obj
        # IDs for mesg conn
        self.mesg_added_id = 0
        self.mesg_removed_id = 0
        self.mesg = None

        modem = obj.get_modem()
        print(
            "[MMWatcher] %s: modem managed by ModemManager [%s]: %s (%s)"
            % (
                obj.get_object_path(),
                modem.get_equipment_identifier(),
                modem.get_manufacturer(),
                modem.get_model(),
            )
        )
        if modem.get_state() == ModemManager.ModemState.FAILED:
            print("[MMWatcher] %s: ignoring failed modem" % obj.get_object_path())
        else:
            modem.connect("state-changed", self.on_modem_state_updated)
            if modem.get_state() == ModemManager.ModemState.REGISTERED:
                self.set_mesg_available()

    def __del__(self):
        print("removing this modem, removing from ui.")

    def set_mesg_available(self):
        """
        Messaging service can be enabled
        """
        print("registered")

    def set_mesg_unavailable(self):
        """
        Messaging service to be disabled
        """
        print("unregistered")

    def on_modem_state_updated(self, modem, old, new, reason):
        """
        Modem state updated
        """
        print(
            "[MMWatcher] %s: modem state updated: %s -> %s (%s) "
            % (
                modem.get_object_path(),
                ModemManager.ModemState.get_string(old),
                ModemManager.ModemState.get_string(new),
                ModemManager.ModemStateChangeReason.get_string(reason),
            )
        )
        if new == ModemManager.ModemState.REGISTERED:
            self.set_mesg_available()
