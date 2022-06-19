#!/usr/bin/python3

example_config = {
    "window-title": "navi window",
    "window-size": (1600, 1000),
    "window-offset": (200, 100),
    "window-zoom": 0.5,
    "move-sensitive": 50,
    "battle-field": {
        "terrains": [
            ("base", "steppe-0"),
            ("rect", "forest-0", -1100, -90, 150, 230),
            ("rect", "forest-0", -1000, -150, 150, 350),
            ("rect", "forest-0", -850, -100, 350, 250),
            ("rect", "forest-0", -550, -125, 350, 250),
            ("rect", "forest-0", -300, -70, 150, 250),
            ("rect", "forest-0", -150, -100, 100, 260),
            ("rect", "forest-0", -100, -60, 200, 460),
            ("rect", "forest-0", 100, -100, 100, 500),
            ("rect", "forest-0", 200, -150, 100, 820),
            ("rect", "forest-0", 300, -200, 100, 880),
            ("rect", "forest-0", 400, -150, 100, 750),
            ("rect", "forest-0", 500, -100, 100, 760),
            ("rect", "forest-0", 600, -50, 100, 830),
            ("rect", "forest-0", 700, 0, 150, 850),
            ("rect", "forest-0", 830, 100, 100, 580),
            ("rect", "forest-0", 900, 200, 100, 380),

            ("rect", "forest-0", 500, 1500, 100, 300),
            ("rect", "forest-0", 600, 1400, 100, 500),
            ("rect", "forest-0", 700, 1300, 150, 500),
            ("rect", "forest-0", 850, 1400, 100, 300),


            
            ("rect", "highland-0", -200, 250, 200, 100),
            ("rect", "highland-0", -300, 350, 100, 200),
            ("rect", "highland-0", -250, 300, 300, 400),
            ("rect", "highland-0", -100, 400, 300, 450),
            ("rect", "highland-0", -50, 450, 300, 450),
            ("rect", "highland-0", 200, 650, 100, 150),

            ("rect", "highland-1", -500, 270, 250, 100),
            ("rect", "highland-1", -550, 370, 250, 200),
            ("rect", "highland-1", -500, 550, 250, 100),
            ("rect", "highland-1", -450, 650, 250, 100),
            ("rect", "highland-1", -400, 700, 300, 150),
            ("rect", "highland-1", -350, 850, 300, 150),
            ("rect", "highland-1", -250, 900, 350, 150),
            ("rect", "highland-1", -50, 900, 200, 50),

            ("rect", "forest-1", -200, 325, 150, 100),
            ("rect", "forest-1", -150, 350, 150, 100),

            ("rect", "highland-0", 100, -650, 101, 220),
            ("rect", "highland-0", 200, -700, 101, 400),
            ("rect", "highland-0", 300, -650, 101, 450),
            ("rect", "highland-0", 400, -600, 101, 450),
            ("rect", "highland-0", 500, -650, 101, 550),
            ("rect", "highland-0", 600, -700, 101, 550),
            ("rect", "highland-0", 700, -600, 101, 300),
            ("rect", "highland-0", 800, -550, 101, 200),

            ("rect", "highland-1", -100, -700, 101, 160),
            ("rect", "highland-1", 0, -750, 101, 250),
            ("rect", "highland-1", 100, -800, 101, 150),
            ("rect", "highland-1", 200, -750, 101, 50),
            
            ("rect", "highland-1", 700, -300, 101, 100),
            ("rect", "highland-1", 800, -350, 101, 100),
            ("rect", "highland-1", 900, -500, 101, 300),
            ("rect", "highland-1", 1000, -450, 101, 200),

            ("rect", "forest-1", 350, -350, 150, 100),
            ("rect", "forest-1", 450, -325, 150, 100),
            ("rect", "forest-1", 520, -300, 120, 100),

            ("rect", "water-0", -12000, 225, 10200, 50),
            ("rect", "water-0", -1900, 200, 150, 50),
            ("rect", "water-0", -1800, 175, 150, 50),
            ("rect", "water-0", -1700, 150, 150, 50),
            ("rect", "water-0", -1600, 125, 150, 50),
            ("rect", "water-0", -1500, 100, 150, 50),
            ("rect", "water-0", -1400, 75, 250, 50),
            ("rect", "water-0", -1200, 50, 250, 50),
            ("rect", "water-0", -1000, 20, 250, 50),
            ("rect", "water-0", -800, -5, 250, 50),
            ("rect", "water-0", -600, -30, 250, 50),
            ("rect", "water-0", -400, -10, 200, 50),
            ("rect", "water-0", -250, 10, 200, 50),
            ("rect", "water-0", -100, 30, 200, 50),
            ("rect", "water-0", 50, 50, 150, 50),
            ("rect", "water-0", 150, 60, 150, 50),
            ("rect", "water-0", 250, 70, 250, 50),
            ("rect", "water-0", 410, 80, 190, 75),
            ("rect", "water-0", 425, 150, 70, 50),
            ("rect", "water-0", 580, 90, 60, 150),
            ("rect", "water-0", 440, 180, 40, 150),
            ("rect", "water-0", 460, 270, 40, 150),
            ("rect", "water-0", 480, 380, 40, 80),
            ("rect", "water-0", 500, 410, 40, 60),
            ("rect", "water-0", 520, 440, 40, 40),
            ("rect", "water-0", 540, 460, 40, 40),
            ("rect", "water-0", 560, 480, 40, 40),
            ("rect", "water-0", 580, 500, 40, 40),
            ("rect", "water-0", 600, 520, 40, 40),
            ("rect", "water-0", 620, 540, 80, 40),
            ("rect", "water-0", 660, 580, 40, 40),
            ("rect", "water-0", 620, 150, 50, 200),
            ("rect", "water-0", 640, 250, 50, 150),
            ("rect", "water-0", 660, 300, 50, 150),
            ("rect", "water-0", 680, 400, 50, 150),
            ("rect", "water-0", 700, 500, 50, 400),
            ("rect", "water-0", 680, 860, 50, 400),
            ("rect", "water-0", 660, 1200, 50, 400),
            ("rect", "water-0", 680, 1550, 50, 100),
            ("rect", "water-0", 700, 1600, 50, 100),
            ("rect", "water-0", 720, 1650, 50, 100),
            ("rect", "water-0", 740, 1700, 50, 100),
            ("rect", "water-0", 760, 1750, 50, 100),
            ("rect", "water-0", 780, 1800, 50, 100),
            ("rect", "water-0", 800, 1850, 50, 100),
            ("rect", "water-0", 820, 1900, 50, 150),
            ("rect", "water-0", 840, 2000, 50, 200),
            ("rect", "water-0", 860, 2100, 50, 200),
            ("rect", "water-0", 880, 2200, 50, 200),
            ("rect", "water-0", 900, 2300, 50, 10000),
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
            "cover-level": 0,
            "water-level": 0,
            "land-level": 0
        },
        "highland-0": {
            "desc": "flat highland",
            "color": (1, 0.8, 0.75),
            "cover-level": 0,
            "water-level": 0,
            "land-level": 2
        },
        "highland-1": {
            "desc": "flat highland",
            "color": (1, 0.85, 0.8),
            "cover-level": 0,
            "water-level": 0,
            "land-level": 1
        },
        "forest-0": {
            "desc": "flat forest",
            "color": (0.7, 0.9, 0.75),
            "cover-level": 2,
            "water-level": 0,
            "land-level": 0
        },
        "forest-1": {
            "desc": "flat forest",
            "color": (0.6, 0.8, 0.7),
            "cover-level": 1,
            "water-level": 0,
            "land-level": 2
        },
        "water-0": {
            "desc": "shallow water",
            "color": (0.5, 0.85, 1.0),
            "cover-level": 0,
            "water-level": 1,
            "land-level": 0           
        }
    }
}
