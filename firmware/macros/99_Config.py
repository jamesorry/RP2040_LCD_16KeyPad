from adafruit_hid.mouse import Mouse
from adafruit_hid.keycode import Keycode

app = {               # REQUIRED dict, must be named 'app'
    'name' : 'RGB Config', # Application name
    'macros' : [      # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x200000, 'Light_Up', [{'RGB_Light':0.1}]),
        (0x000000, '', []),
        (0x202000, 'Light_Down', [{'RGB_Light':-0.1}]),
        (0x000000, '', []),
        # 2nd row ----------
        (0x202000, 'RGB on', [{'RGB_AT':'on'}]),
        (0x000000, '', []),
        (0x202000, 'RGB off', [{'RGB_AT':'off'}]),
        (0x000000, '', []),
        # 3rd row ----------
        (0x202000, 'RGB Next', [{'RGB_AT':'next'}]),
        (0x000000, '', []),
        (0x000000, '', []),
        (0x000000, '', []),
        # 4th row ----------
        (0x202000, 'info', [{'info':0}]),
        (0x000000, '', []),
        (0x202000, 'image', [{'image':3}]),
        (0x000000, '', []),
        # Encoder button ---
        (0x000000, '', [])
    ]
}
