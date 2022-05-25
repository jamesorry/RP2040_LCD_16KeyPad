from adafruit_hid.mouse import Mouse
from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values
# You can still import Keycode and/or ConsumerControl as well if a macro file
# mixes types! See other macro files for typical Keycode examples.

app = {               # REQUIRED dict, must be named 'app'
    'name' : 'Mouse', # Application name
    'macros' : [      # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x200000, 'L', [{'buttons':Mouse.LEFT_BUTTON}]),
        (0x202000, 'M', [{'buttons':Mouse.MIDDLE_BUTTON}]),
        (0x002000, 'R', [{'buttons':Mouse.RIGHT_BUTTON}]),
        (0x000000, '', []),
        # 2nd row ----------
        (0x000000, '', []),
        (0x202020, 'Up', [{'y':-10}]),
        (0x000000, '', []),
        (0x0A0000, 'Zoom +', [Keycode.CONTROL, {'wheel':1}]),
        # 3rd row ----------
        (0x202020, 'Left', [{'x':-10}]),
        (0x000000, '', []),
        (0x202020, 'Right', [{'x':10}]),
        (0x000000, '', []),
        # 4th row ----------
        (0x000000, '', []),
        (0x202020, 'Down', [{'y':10}]),
        (0x000000, '', []),
        (0x0A0000, 'Zoom -', [Keycode.CONTROL, {'wheel':-1}]),
        # Encoder button ---
        (0x000000, '', [])
    ]
}