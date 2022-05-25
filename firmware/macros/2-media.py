from adafruit_hid.consumer_control_code import ConsumerControlCode
# You can still import Keycode as well if a macro file mixes types!
# See other macro files for typical Keycode examples.

app = {               # REQUIRED dict, must be named 'app'
    'name' : 'Media', # Application name
    'macros' : [      # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x000000, '', []),
        (0x000020, 'Vol+', [[ConsumerControlCode.VOLUME_INCREMENT]]),
        (0x202020, 'Bright+', [[ConsumerControlCode.BRIGHTNESS_INCREMENT]]),
        (0x000000, '', []),
        # 2nd row ----------
        (0x000000, '', []),
        (0x000020, 'Vol-', [[ConsumerControlCode.VOLUME_DECREMENT]]),
        (0x202020, 'Bright-', [[ConsumerControlCode.BRIGHTNESS_DECREMENT]]),
        (0x000000, '', []),
        # 3rd row ----------
        (0x000000, '', []),
        (0x200000, 'Mute', [[ConsumerControlCode.MUTE]]),
        (0x000000, '', []),
        (0x000000, '', []),
        # 4th row ----------
        (0x202000, '<<', [[ConsumerControlCode.SCAN_PREVIOUS_TRACK]]),
        (0x002000, 'Play/Pause', [[ConsumerControlCode.PLAY_PAUSE]]),
        (0x202000, '>>', [[ConsumerControlCode.SCAN_NEXT_TRACK]]),
        (0x000000, '', []),
        # Encoder button ---
        (0x000000, '', [])
    ]
}