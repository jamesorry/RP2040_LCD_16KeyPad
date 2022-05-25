app = {                # REQUIRED dict, must be named 'app'
    'name' : 'De-stress', # Application name
    'macros' : [       # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x00FFFF, '00FFFF', []),
        (0x000000, '000000', []),
        (0x0000FF, '0000FF', []),
        (0xFF00FF, 'FF00FF', []),
        # 2nd row ----------
        (0x808080, '808080', []),
        (0x008800, '008800', []),
        (0x00FF00, '00FF00', []),
        (0x800000, '800000', []),
        # 3rd row ----------
        (0x000080, '000080', []),
        (0x808000, '808000', []),
        (0x800080, '800080', []),
        (0xFF0000, 'FF0000', []),
        # 4th row ----------
        (0xC0C0C0, 'C0C0C0', []),
        (0x008080, '008080', []),
        (0xFFFFFF, 'FFFFFF', []),
        (0xFFFF00, 'FFFF00', []),
        # Encoder button ---
        (0x000000, '', [])
    ]
}
