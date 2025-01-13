# установка игры
WIDTH = 1280
HEIGTH = 720
FPS = 60
TILESIZE = 64
# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = "sprite/graphics/font/joystix.ttf"
UIFONT_SIZE = 18
HITBOX_OFFSET = {
    "player": -26,
    "object": -40,
    "grass": -10,
    "invisible": 0
}

# цвета
WATER_COLOR = "#71ddee"
UI_BG_COLOR = "#222222"
UI_BORDER_COLOR = "#111111"
TEXT_COLOR = "#54c70c"

# цвет ui
HEALTH_COLOR = "red"
ENERGY_COLOR = "blue"
UI_BORDER_COLOR_ACTIVE = "gold"

# апгрейд меню цвета
TEXT_COLOR_SELECTED = '#db0dc3'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

# оружия
weapon_data = {
    "sword": {"cooldown": 100, "damage": 15, "graphic": "sprite/graphics/weapons/sword/full.png"},
    "lance": {"cooldown": 400, "damage": 30, "graphic": "sprite/graphics/weapons/lance/full.png"},
    "axe": {"cooldown": 300, "damage": 8, "graphic": "sprite/graphics/weapons/axe/full.png"},
    "rapier": {"cooldown": 50, "damage": 8, "graphic": "sprite/graphics/weapons/rapier/full.png"},
    "sai": {"cooldown": 80, "damage": 10, "graphic": "sprite/graphics/weapons/sai/full.png"}}

magic_data = {
    "fire": {"strength": 5, "cost": 10, "graphic": "sprite/graphics/particles/flame/frames/03.png", "exp": 0},
    "flame": {"strength": 5, "cost": 20, "graphic": "sprite/graphics/particles/flame/flame.png", "exp": 100},
    "heal": {"strength": 20, "cost": 30, "graphic": "sprite/graphics/particles/heal/heal.png", "exp": 200},
    "boost_speed": {"strength": 20, "cost": 30, "graphic": "sprite/graphics/particles/boost_speed/boost_speed.png",
                    "exp": 50},
    "inferno": {"strength": 5, "cost": 40, "graphic": "sprite/graphics/particles/flame/inferno.png", "exp": 300}
}
monster_data = {
    'squid': {'health': 100, 'exp': 100, 'damage': 20, 'attack_type': 'slash',
              'attack_sound': 'audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80,
              'notice_radius': 360},
    'raccoon': {'health': 300, 'exp': 250, 'damage': 40, 'attack_type': 'claw',
                'attack_sound': 'audio/attack/claw.wav', 'speed': 2, 'resistance': 3, 'attack_radius': 120,
                'notice_radius': 400},
    'spirit': {'health': 100, 'exp': 110, 'damage': 8, 'attack_type': 'thunder',
               'attack_sound': 'audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60,
               'notice_radius': 350},
    'bamboo': {'health': 70, 'exp': 120, 'damage': 6, 'attack_type': 'slash',
               'attack_sound': 'audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50,
               'notice_radius': 300}}
