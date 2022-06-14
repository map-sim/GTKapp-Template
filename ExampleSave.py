#!/usr/bin/python3

example_config = {
    "window-title": "navi window",
    "window-size": (400, 300),
    "battle-field": {
        "terrains": [
            ("base", "steppe-0"),
            ("rect", "forest-0", 100, 100, 100, 150),
            ("rect", "water-0", 50, 50, 100, 50),
        ],
        "infrastructure": [
        ]
    }
}

example_library = {
    "scale": 1,
    "terrains": {
        "steppe-0": {
            "color": (1, 0.8, 0.8),
        },
        "forest-0": {
            "color": (0, 0.8, 0.2),
        },
        "water-0": {
            "color": (0.5, 0.5, 1.0),
        }
    }
}
