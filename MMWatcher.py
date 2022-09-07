# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2014 Aleksander Morgado <aleksander@aleksander.es>
# Copyright (C) 2022 Tao J <tao-j@outlook.com>

import sys
from datetime import datetime

import gi

gi.require_version("ModemManager", "1.0")
from gi.repository import Gio, GLib, GObject, ModemManager

from Modem import Modem


class MMWatcher:
    """
    The MMWatcher class is responsible for monitoring ModemManager.
    """

    def __init__(self):
        # Flag for initial logs
        self.initializing = True
        # Setup DBus monitoring
        self.connection = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)
        self.manager = ModemManager.Manager.new_sync(
            self.connection, Gio.DBusObjectManagerClientFlags.DO_NOT_AUTO_START, None
        )
        # IDs for added/removed signals
        self.object_added_id = 0
        self.object_removed_id = 0
        # a dict holding modem path to objs
        self.modem_objs = dict()
        # Follow availability of the ModemManager process
        self.available = False
        self.manager.connect("notify::name-owner", self.on_name_owner)
        self.on_name_owner(self.manager, None)
        # Finish initialization
        self.initializing = False

    def set_available(self):
        """
        ModemManager is now available.
        """
        if not self.available or self.initializing:
            print(
                "[MMWatcher] ModemManager %s service is available in bus"
                % self.manager.get_version()
            )
        self.object_added_id = self.manager.connect(
            "object-added", self.on_object_added
        )
        self.object_removed_id = self.manager.connect(
            "object-removed", self.on_object_removed
        )
        self.available = True
        # Initial scan
        if self.initializing:
            for obj in self.manager.get_objects():
                self.on_object_added(self.manager, obj)

    def set_unavailable(self):
        """
        ModemManager is now unavailable.
        """
        if self.available or self.initializing:
            print("[MMWatcher] ModemManager service not available in bus")
        if self.object_added_id:
            self.manager.disconnect(self.object_added_id)
            self.object_added_id = 0
        if self.object_removed_id:
            self.manager.disconnect(self.object_removed_id)
            self.object_removed_id = 0
        self.available = False

    def on_name_owner(self, manager, prop):
        """
        Name owner updates.
        """
        if self.manager.get_name_owner():
            self.set_available()
        else:
            self.set_unavailable()

    def on_object_added(self, manager, obj):
        """
        Object added.
        """
        obj_path = obj.get_object_path()
        assert obj_path not in self.modem_objs
        self.modem_objs[obj_path] = Modem(obj)

    def on_object_removed(self, manager, obj):
        """
        Object removed.
        """
        obj_path = obj.get_object_path()
        print("[MMWatcher] %s: modem unmanaged by ModemManager" % obj_path())
        self.modem_objs.pop(obj_path)
