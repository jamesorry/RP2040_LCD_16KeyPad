from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values

app = {                       # REQUIRED dict, must be named 'app'
    'name' : 'Firefox', # Application name
    'macros' : [              # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x004000, '< Back', [Keycode.CONTROL, '[']),
        (0x004000, 'Fwd >', [Keycode.CONTROL, ']']),
        (0x004000, 'Up', [Keycode.SHIFT, ' ']),      # Scroll up
        (0x004000, 'Youtube', [Keycode.CONTROL, 't', -Keycode.CONTROL,
                           'www.youtube.com\n']),
        # 2nd row ----------
        (0x202000, '< Tab', [Keycode.CONTROL, Keycode.SHIFT, Keycode.TAB]),
        (0x202000, 'Tab >', [Keycode.CONTROL, Keycode.TAB]),
        (0x202000, 'Down', ' '),                     # Scroll down
        (0x202000, 'Github', [Keycode.CONTROL, 't', -Keycode.CONTROL,
                            'www.github.com\n']),
        # 3rd row ----------
        (0x000040, 'Reload', [Keycode.CONTROL, 'r']),
        (0x000040, 'Hist', [Keycode.CONTROL, 'h']),
        (0x000040, 'Priv', [Keycode.CONTROL, Keycode.SHIFT, 'p']),
        (0x000040, 'Gmail0', [Keycode.CONTROL, 't', -Keycode.CONTROL,
                            'https://mail.google.com/mail/u/0\n']),
        # 4th row ----------
        (0x101010, 'firefox', [Keycode.LEFT_GUI , 'r', -Keycode.LEFT_GUI, 0.5, 'firefox\n']),
        (0x101010, 'New', [Keycode.CONTROL, 't']),
        (0x101010, 'Namin', [Keycode.CONTROL, 't', -Keycode.CONTROL,
                            'www.twitch.tv/namin1004\n']),
        (0x101010, 'Gmail1', [Keycode.CONTROL, 't', -Keycode.CONTROL,
                            'https://mail.google.com/mail/u/1\n']),
        # Encoder button ---
        (0x000000, 'Close', [Keycode.CONTROL, 'w'])  # Close window/tab
    ]
}