# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2014 Aleksander Morgado <aleksander@aleksander.es>
# Copyright (C) 2022 Tao J <tao-j@outlook.com>

from datetime import datetime
import gi

gi.require_version("ModemManager", "1.0")
from gi.repository import Gio, GLib, GObject, ModemManager


class Messaging:
    def __init__(self, mesg):
        self.mesg = mesg

        for msg in mesg.list_sync():
            self.on_new_mesg(msg)

    def on_new_mesg(self, msg):
        print("got new mesg ----------")
        number = msg.get_number()
        ts = msg.get_timestamp()
        if ts:
            dt = datetime.strptime(ts + "00", "%Y-%m-%dT%H:%M:%S%z")
            iso_time = dt.astimezone().isoformat()
        else:
            iso_time = "N/A"
        text = msg.get_text()
        store = ModemManager.SmsStorage.get_string(msg.get_storage())
        state = ModemManager.SmsState.get_string(msg.get_state())
        pdu = ModemManager.SmsPduType.get_string(msg.get_pdu_type())

        print(f"number: \t\t\t{number}")
        print(f"timestamp: \t\t\t{ts}")
        print(f"text: \t\t\t\t{text}")
        print(f"store: \t\t\t\t{store}")
        print(f"state: \t\t\t\t{state}")
        print(f"pdu: \t\t\t\t{pdu}")

    def new_mesg(self, number=None, text=""):
        sms_properties = ModemManager.SmsProperties.new()
        if number is None or text == "":
            return
        sms_properties.set_number(number)
        sms_properties.set_text(text)
        sms = self.mesg.create_sync(sms_properties)
        return sms.send_sync()
