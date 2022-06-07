#!/usr/bin/python3

import sys, gi
from BaseWindow import BaseWindow
from ColorWindow import ColorWindow

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

if len(sys.argv) == 1:
    BaseWindow("base window", 400, 300)
elif sys.argv[1] == "base":
    BaseWindow("base window", 400, 300)
elif sys.argv[1] == "color":
    ColorWindow("color window", 400, 300)
else: raise ValueError(sys.argv[1])

try: Gtk.main()
except KeyboardInterrupt:
    print("KeyboardInterrupt")
