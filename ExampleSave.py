#!/usr/bin/python3

example_config = {
    "window-title": "navi window",
    "window-size": (800, 600),
    "window-offset": (200, 100),
    "window-zoom": 0.5,
    "move-sensitive": 20,
    "battle-field": {
        "terrains": [
            ("base", "steppe-0"),
            ("rect", "forest-0", 100, 0, 100, 250),
            ("rect", "forest-0", 200, -50, 100, 350),
            ("rect", "forest-0", 300, -150, 100, 550),
            ("rect", "forest-0", 400, -100, 100, 550),
            ("rect", "forest-0", 500, -10, 100, 580),
            ("rect", "forest-0", 600, 20, 100, 630),
            ("rect", "forest-0", 700, 50, 100, 750),
            ("rect", "forest-0", 800, 150, 100, 450),
            ("rect", "water-0", -10000, 30, 10100, 50),
            ("rect", "water-0", 50, 50, 150, 50),
            ("rect", "water-0", 150, 60, 150, 50),
            ("rect", "water-0", 250, 70, 250, 50),
            ("rect", "water-0", 450, 80, 150, 50),
            ("rect", "water-0", 550, 90, 60, 100),
            ("rect", "water-0", 600, 150, 50, 200),
            ("rect", "water-0", 650, 250, 50, 300),
            ("rect", "water-0", 700, 450, 50, 10000),
        ],
        "infrastructure": [
        ]
    }
}

example_library = {
    "terrains": {
        "steppe-0": {
            "desc": "flat steppe",
            "color": (1, 0.9, 0.85),
        },
        "forest-0": {
            "desc": "flat forest",
            "color": (0.7, 0.9, 0.75),
        },
        "water-0": {
            "desc": "shallow water",
            "color": (0.5, 0.85, 1.0),
        }
    }
}
