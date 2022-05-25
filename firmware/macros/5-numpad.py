from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values
#最多顯示六個字
from adafruit_hid.consumer_control_code import ConsumerControlCode
app = {                # REQUIRED dict, must be named 'app'
    'name' : 'Numpad', # Application name
    'macros' : [       # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x202000, '7', ['7']),
        (0x202000, '8', ['8']),
        (0x202000, '9', ['9']),
        (0x202000, 'BackSP', [Keycode.BACKSPACE]),
        # 2nd row ----------
        (0x202000, '4', ['4']),
        (0x202000, '5', ['5']),
        (0x202000, '6', ['6']),
        (0x202000, '+', ['+']),
        # 3rd row ----------
        (0x202000, '1', ['1']),
        (0x202000, '2', ['2']),
        (0x202000, '3', ['3']),
        (0x202000, '-', ['-']),
        # 4th row ----------
        (0x202000, '00', ['00']),
        (0x202000, '0', ['0']),
        (0x202000, '.', ['.']),
        (0x202000, 'Enter', [Keycode.ENTER]),
        # Encoder button ---
        (0x000000, '', [])
    ]
}
