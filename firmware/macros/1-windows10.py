from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values
#最多顯示六個字
app = {                # REQUIRED dict, must be named 'app'
    'name' : 'Win 10', # Application name
    'macros' : [       # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x202000, 'Win+D', [Keycode.WINDOWS, 'd']),
        (0x202000, 'Up', [Keycode.WINDOWS, Keycode.UP_ARROW]),
        (0x202000, 'Win+R', [Keycode.WINDOWS, 'r']),
        (0x202000, 'PrScr', [Keycode.WINDOWS, Keycode.SHIFT, 's']),
        # 2nd row ----------
        (0x202000, 'Left', [Keycode.WINDOWS, Keycode.LEFT_ARROW]),
        (0x202000, 'Down', [Keycode.WINDOWS, Keycode.DOWN_ARROW]),
        (0x202000, 'Right', [Keycode.WINDOWS, Keycode.RIGHT_ARROW]),
        (0x202000, 'File_M', [Keycode.WINDOWS, 'e']),
        # 3rd row ----------
        (0x202000, 'Ctrl+W', [Keycode.CONTROL, 'w']),
        (0x202000, 'Ctrl+T', [Keycode.CONTROL, 't']),
        (0x202000, 'C+S+N', [Keycode.CONTROL, Keycode.SHIFT, 'n']),
        (0x202000, 'Task_M', [Keycode.CONTROL, Keycode.SHIFT, Keycode.ESCAPE]),

        # 4th row ----------
        (0x202000, 'Ctrl+A', [Keycode.CONTROL, 'a']),
        (0x202000, 'Ctrl+C', [Keycode.CONTROL, 'c']),
        (0x202000, 'Ctrl+V', [Keycode.CONTROL, 'v']),
        (0x202000, 'Alt+F4', [Keycode.LEFT_ALT, Keycode.F4]),
        # Encoder button ---
        (0x000000, '', [Keycode.ESCAPE])
    ]
}
