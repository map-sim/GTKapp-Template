#!/usr/bin/python3

import sys, gi, json
from BaseWindow import BaseWindow
from ColorWindow import ColorWindow
from NaviWindow import NaviWindow

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

if len(sys.argv) == 1:
    BaseWindow("base window", 400, 300)
elif sys.argv[1] == "base":
    BaseWindow("base window", 400, 300)
elif sys.argv[1] == "color":
    ColorWindow("color window", 400, 300)
elif sys.argv[1] == "navi":
    NaviWindow()
elif sys.argv[1] == "navi-load":
    with open("save.navi/config.json") as fd:
        config = json.loads(json.load(fd))
    with open("save.navi/library.json") as fd:
        library = json.loads(json.load(fd))
    with open("save.navi/battle-field.json") as fd:
        battle_field = json.loads(json.load(fd))
    NaviWindow(config, library, battle_field)
else: raise ValueError(sys.argv[1])

try: Gtk.main()
except KeyboardInterrupt:
    print("KeyboardInterrupt")
