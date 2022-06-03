#!/usr/bin/python3

import gi
from SingleWindow import SingleWindow

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

SingleWindow("title", 400, 300)

try: Gtk.main()
except KeyboardInterrupt:
    print("KeyboardInterrupt")
