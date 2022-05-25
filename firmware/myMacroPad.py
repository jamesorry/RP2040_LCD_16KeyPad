"""
A helper library for the Adafruit MacroPad RP2040.
  https://github.com/adafruit/Adafruit_CircuitPython_MacroPad

* Origin Author(s): Kattni Rembor
* Modify by: James Lu

**Hardware:**

* `Adafruit MacroPad RP2040 Bare Bones <https://www.adafruit.com/product/5100>`_
* `Adafruit MacroPad RP2040 Starter Kit <https://www.adafruit.com/product/5128>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads


* Adafruit's CircuitPython NeoPixel library:
  https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel

* Adafruit's CircuitPython HID library:
  https://github.com/adafruit/Adafruit_CircuitPython_HID

* Adafruit's CircuitPython Display Text library:
  https://github.com/adafruit/Adafruit_CircuitPython_Display_Text

* Adafruit's CircuitPython Simple Text Display library:
  https://github.com/adafruit/Adafruit_CircuitPython_Simple_Text_Display

* Adafruit's CircuitPython Debouncer library:
  https://github.com/adafruit/Adafruit_CircuitPython_Debouncer

* Adafruit's CircuitPython Ticks library
  https://github.com/adafruit/Adafruit_CircuitPython_Ticks

"""
import array
import math
import time
import board
import digitalio
import rotaryio
import keypad
import neopixel
import displayio
import busio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_base import KeyboardLayoutBase
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.mouse import Mouse
from adafruit_debouncer import Debouncer
import adafruit_ili9341
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.customcolorchase import CustomColorChase
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import *
from adafruit_led_animation import helper

try:
    from neopixel import NeoPixel
    from keypad import Keys
    import adafruit_hid
except ImportError:
    pass

__version__ = "1.0.1"
__repo__ = "https://github.com/jamesorry/RP2040_LCD_16KeyPad.git"

ROTATED_KEYMAP_0 = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
ROTATED_KEYMAP_90 = (3, 7, 11, 15, 2, 6, 10, 14, 1, 5, 9, 13, 0, 4, 8, 12)
ROTATED_KEYMAP_180 = (15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0)
ROTATED_KEYMAP_270 = (12, 8, 4, 0, 13, 9, 5, 1, 14, 10, 6, 2, 15, 11, 7, 3)


keycodes = Keycode
"""Module level Keycode class, to be changed when initing Macropad with a different language"""

class _PixelMapLite:
    """Generate a pixel map based on a specified order. Designed to work with a set of 15 pixels,
    e.g. the MacroPad keypad LEDs.

    :param pixels: The pixel object.
    :param tuple order: The specified order of the pixels. Pixels are numbered 0-15. Defaults to
                        numerical order, ``0`` to ``15``.
    """

    def __init__(
        self,
        pixels: NeoPixel,
        order: Tuple[
            int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int
        ] = ROTATED_KEYMAP_0,
    ):
        self._pixels = pixels
        self._order = order
        self._num_pixels = len(pixels)
        self.fill = pixels.fill
        self.show = pixels.show
        self.n = self._num_pixels

    def __setitem__(self, index: int, val: int) -> None:
        if isinstance(index, slice):
            for val_i, in_i in enumerate(range(*index.indices(self._num_pixels))):
                self._pixels[self._order[in_i]] = val[val_i]
        else:
            self._pixels[self._order[index]] = val

    def __getitem__(self, index: int) -> int:
        if isinstance(index, slice):
            return [
                self._pixels[self._order[idx]]
                for idx in range(*index.indices(self._num_pixels))
            ]
        if index < 0:
            index += self._num_pixels
        if index >= self._num_pixels or index < 0:
            raise IndexError
        return self._pixels[self._order[index]]

    def __repr__(self) -> str:
        return self._pixels.__repr__()

    def __len__(self) -> int:
        return len(self._pixels)

    @property
    def auto_write(self) -> bool:
        """
        True if the neopixels should immediately change when set. If False, ``show`` must be
        called explicitly.
        """
        return self._pixels.auto_write

    @auto_write.setter
    def auto_write(self, value: bool) -> None:
        self._pixels.auto_write = value

    @property
    def brightness(self) -> float:
        """Overall brightness of the pixel (0 to 1.0)."""
        return self._pixels.brightness

    @brightness.setter
    def brightness(self, value: float) -> None:
        self._pixels.brightness = value
        
class MacroPad:
    """
    Class representing a single MacroPad.

    :param int rotation: The rotational position of the MacroPad. Allows for rotating the MacroPad
                         in 90 degree increments to four different positions and rotates the keypad
                         layout and display orientation to match. Keypad layout is always left to
                         right, top to bottom, beginning with key number 0 in the top left, and
                         ending with key number 11 in the bottom right. Supports ``0``, ``90``,
                         ``180``, and ``270`` degree rotations. ``0`` is when the USB port is at
                         the top, ``90`` is when the USB port is to the left, ``180`` is when the
                         USB port is at the bottom, and ``270`` is when the USB port is to the
                         right. Defaults to ``0``.
    :param int or tuple midi_in_channel: The MIDI input channel. This can either be an integer for
                                         one channel, or a tuple of integers to listen on multiple
                                         channels. Defaults to 1.
    :param int midi_out_channel: The MIDI output channel. Defaults to 1.

    :param type[KeyboardLayoutBase] layout_class: Class for the keyboard layout, to setup an
                                                  international or alternative keyboard. Defaults
                                                  to KeyboardLayoutUS from adafruit_hid.
    :param type[Keycode] keycode_class: Class used for the keycode names provided by
                                        adafruit_macropad.Keycode. Defaults to the standard Keycode
                                        from adafruit_hid.


    The following shows how to initialise the MacroPad library with the board rotated 90 degrees,
    and the MIDI channels both set to 1.

    .. code-block:: python

        from adafruit_macropad import MacroPad

        macropad = MacroPad(rotation=90, midi_in_channel=1, midi_out_channel=1)
    """

    Keycode = Keycode
    """
    The contents of the Keycode module are available as a property of MacroPad. This includes all
    keycode constants available within the Keycode module, which includes all the keys on a
    regular PC or Mac keyboard.

    Remember that keycodes are the names for key _positions_ on a US keyboard, and may not
    correspond to the character that you mean to send if you want to emulate non-US keyboard.

    For usage example, see the ``keyboard`` documentation in this library.
    """

    ConsumerControlCode = ConsumerControlCode
    """
    The contents of the ConsumerControlCode module are available as a property of MacroPad.
    This includes the available USB HID Consumer Control Device constants. This list is not
    exhaustive.

    For usage example, see the ``consumer_control`` documentation in this library.
    """

    Mouse = Mouse
    """
    The contents of the Mouse module are available as a property of MacroPad. This includes the
    ``LEFT_BUTTON``, ``MIDDLE_BUTTON``, and ``RIGHT_BUTTON`` constants. The rest of the
    functionality of the ``Mouse`` module should be used through ``macropad.mouse``.

    For usage example, see the ``mouse`` documentation in this library.
    """
    
    def __init__(
        self,
        rotation: int = 0,
        midi_in_channel: int = 1,
        midi_out_channel: int = 1,
        layout_class: type[KeyboardLayoutBase] = KeyboardLayoutUS,
        keycode_class: type[Keycode] = Keycode,
    ):
        displayio.release_displays()
        if rotation not in (0, 90, 180, 270):
            raise ValueError("Only 90 degree rotations are supported.")

        # Define LEDs:
        pixel_pin = board.GP26
        num_pixels = 16
        self._pixels = neopixel.NeoPixel(pixel_pin, num_pixels)
        
        '''============================================================================================'''        
        self.blink = Blink(self._pixels, speed=0.5, color=JADE)
        self.colorcycle = ColorCycle(self._pixels, speed=0.4, colors=[MAGENTA, ORANGE])
        self.comet = Comet(self._pixels, speed=0.1, color=PURPLE, tail_length=10, bounce=True)
        self.chase = Chase(self._pixels, speed=0.1, size=3, spacing=6, color=WHITE)
        self.pulse = Pulse(self._pixels, speed=0.1, period=3, color=AMBER)
        #self.sparkle = Sparkle(self._pixels, speed=0.1, color=PURPLE, num_sparkles=16)
        #self.solid = Solid(self._pixels, color=JADE)
        pixel_wing_vertical = helper.PixelMap.vertical_lines(
            self._pixels, 4, 4, helper.horizontal_strip_gridmap(4, alternating=False)
            )
        pixel_wing_horizontal = helper.PixelMap.horizontal_lines(
            self._pixels, 4, 4, helper.horizontal_strip_gridmap(4, alternating=False)
            )
        self.rainbow_chase_h = RainbowChase(pixel_wing_horizontal, speed=0.1, size=3, spacing=2)
        self.rainbow_comet_v = RainbowComet(pixel_wing_vertical, speed=0.1, tail_length=7, bounce=True)
        self.comet_v = Comet(pixel_wing_vertical, speed=0.1, color=AMBER, tail_length=6, bounce=True)
        self.rainbow = Rainbow(self._pixels, speed=0.1, period=2)
        self.sparkle_pulse = SparklePulse(self._pixels, speed=0.1, period=3, color=JADE)
        self.rainbow_comet = RainbowComet(self._pixels, speed=0.1, tail_length=7, bounce=True)
        self.rainbow_chase = RainbowChase(self._pixels, speed=0.1, size=3, spacing=2, step=8)
        self.rainbow_sparkle = RainbowSparkle(self._pixels, speed=0.1, num_sparkles=8)
        self.custom_color_chase = CustomColorChase(
            self._pixels, speed=0.1, size=2, spacing=3, colors=[ORANGE, WHITE, JADE]
        )
        
        # colors default to RAINBOW as defined in color.py
        self.custom_color_chase_rainbow = CustomColorChase(self._pixels, speed=0.1, size=2, spacing=3)
        self.custom_color_chase_rainbow_r = CustomColorChase(
            self._pixels, speed=0.1, size=3, spacing=3, reverse=True
        )

        # Example with same colors as RainbowChase
        steps = 16
        # This was taken from rainbowchase.py
        rainbow_colors = [colorwheel(n % 256) for n in range(0, 512, steps)]
        # Now use rainbow_colors with CustomColorChase
        self.custom_color_chase_rainbowchase = CustomColorChase(
            self._pixels, speed=0.1, colors=rainbow_colors, size=2, spacing=3
        )

        self.custom_color_chase_bgp = CustomColorChase(
            self._pixels, speed=0.1, colors=[BLUE, GREEN, PINK], size=3, spacing=2
        )
        '''============================================================================================'''
        self.total_animations_num = 17 #need to define!!!
        self.animations = AnimationSequence(
            self.custom_color_chase_rainbow,
            self.custom_color_chase_rainbow_r,
            self.custom_color_chase_rainbowchase,
            self.custom_color_chase_bgp,
            self.comet,
            self.rainbow_comet_v,
            self.blink,
            self.rainbow_sparkle,
            self.chase,
            self.pulse,
            #self.sparkle,
            self.comet_v,
            self.rainbow_chase_h,
            self.rainbow,
            #self.solid,
            self.rainbow_comet,
            self.sparkle_pulse,
            self.rainbow_chase,
            self.custom_color_chase,
            #advance_interval=10,
            auto_clear=True,
        )
        
        # Define key and pixel maps based on rotation:
        self._rotated_pixels = None
        
        def _keys_and_pixels(
            order: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]
        ) -> None:
            """
            Generate key and pixel maps based on a specified order.
            :param order: Tuple containing the order of the keys and pixels.
            """
            self._rotated_pixels = _PixelMapLite(self._pixels, order=order)

        if rotation == 0:
            _keys_and_pixels(order=ROTATED_KEYMAP_0)

        if rotation == 90:
            _keys_and_pixels(order=ROTATED_KEYMAP_90)

        if rotation == 180:
            _keys_and_pixels(order=ROTATED_KEYMAP_180)

        if rotation == 270:
            _keys_and_pixels(order=ROTATED_KEYMAP_270)
        
        # Define keys:
        self._keys = keypad.KeyMatrix(
            column_pins=(board.GP0, board.GP1, board.GP2, board.GP3),
            row_pins=(board.GP9, board.GP8, board.GP4, board.GP5),
            columns_to_anodes=True
            )

        # Define rotary encoder and encoder switch:
        self._encoder = rotaryio.IncrementalEncoder(board.GP11, board.GP10)
        self._encoder_switch = digitalio.DigitalInOut(board.GP12)
        self._encoder_switch.switch_to_input(pull=digitalio.Pull.UP)
        self._debounced_switch = Debouncer(self._encoder_switch)

        # Define display:
        TFT_WIDTH = 320
        TFT_HEIGHT = 240

        tft_cs = board.GP13
        tft_dc = board.GP15
        tft_res = board.GP14
        spi_mosi = board.GP7
        spi_clk = board.GP6

        spi = busio.SPI(spi_clk, MOSI=spi_mosi)

        display_bus = displayio.FourWire(
            spi, command=tft_dc, chip_select=tft_cs, reset=tft_res)

        self.display = adafruit_ili9341.ILI9341(display_bus,
                            width=TFT_WIDTH, height=TFT_HEIGHT,
                            rowstart=0, colstart=0)
        self.display.rotation = rotation
        
        
        # Define HID:
        self._keyboard = None
        self._keyboard_layout = None
        self._consumer_control = None
        self._mouse = None
        self._layout_class = layout_class
        self.Keycode = keycode_class
        global keycodes
        keycodes = keycode_class
        
    @property
    def pixels(self) -> Optional[_PixelMapLite]:
        """Sequence-like object representing the twelve NeoPixel LEDs in a 3 x 4 grid on the
        MacroPad. Each pixel is at a certain index in the sequence, numbered 0-11. Colors can be an
        RGB tuple like (255, 0, 0) where (R, G, B), or an RGB hex value like 0xFF0000 for red where
        each two digits are a color (0xRRGGBB). Set the global brightness using any number from 0
        to 1 to represent a percentage, i.e. 0.3 sets global brightness to 30%. Brightness defaults
        to 1.

        See ``neopixel.NeoPixel`` for more info.

        The following example turns all the pixels green at 50% brightness.

        .. code-block:: python

            from adafruit_macropad import MacroPad

            macropad = MacroPad()

            macropad.pixels.brightness = 0.5

            while True:
                macropad.pixels.fill((0, 255, 0))

        The following example sets the first pixel red and the twelfth pixel blue.

        .. code-block:: python

            from adafruit_macropad import MacroPad

            macropad = MacroPad()

            while True:
                macropad.pixels[0] = (255, 0, 0)
                macropad.pixels[11] = (0, 0, 255)
        """
        return self._rotated_pixels
    
    @property
    def keys(self) -> Keys:
        """
        The keys on the MacroPad. Uses events to track key number and state, e.g. pressed or
        released. You must fetch the events using ``keys.events.get()`` and then the events are
        available for usage in your code. Each event has three properties:

        * ``key_number``: the number of the key that changed. Keys are numbered starting at 0.
        * ``pressed``: ``True`` if the event is a transition from released to pressed.
        * ``released``: ``True`` if the event is a transition from pressed to released.
                        ``released`` is always the opposite of ``pressed``; it's provided
                        for convenience and clarity, in case you want to test for
                        key-release events explicitly.

        The following example prints the key press and release events to the serial console.

        .. code-block:: python

            from adafruit_macropad import MacroPad

            macropad = MacroPad()

            while True:
                key_event = macropad.keys.events.get()
                if key_event:
                    print(key_event)
        """
        return self._keys
    
    @property
    def encoder(self) -> int:
        """
        The rotary encoder relative rotation position. Always begins at 0 when the code is run, so
        the value returned is relative to the initial location.

        The following example prints the relative position to the serial console.

        .. code-block:: python

            from adafruit_macropad import MacroPad

            macropad = MacroPad()

            while True:
                print(macropad.encoder)
        """
        return self._encoder.position * -1

    @property
    def encoder_switch(self) -> bool:
        """
        The rotary encoder switch. Returns ``True`` when pressed.

        The following example prints the status of the rotary encoder switch to the serial console.

        .. code-block:: python

            from adafruit_macropad import MacroPad

            macropad = MacroPad()

            while True:
                print(macropad.encoder_switch)
        """
        return not self._encoder_switch.value

    @property
    def encoder_switch_debounced(self) -> Debouncer:
        """
        The rotary encoder switch debounced. Allows for ``encoder_switch_debounced.pressed`` and
        ``encoder_switch_debounced.released``. Requires you to include
        ``encoder_switch_debounced.update()`` inside your loop.

        The following example prints to the serial console when the rotary encoder switch is
        pressed and released.

        .. code-block:: python

            from adafruit_macropad import MacroPad

            macropad = MacroPad()

            while True:
                macropad.encoder_switch_debounced.update()
                if macropad.encoder_switch_debounced.pressed:
                    print("Pressed!")
                if macropad.encoder_switch_debounced.released:
                    print("Released!")
        """
        self._debounced_switch.pressed = self._debounced_switch.fell
        self._debounced_switch.released = self._debounced_switch.rose
        return self._debounced_switch
    
    @property
    def keyboard(self) -> adafruit_hid.keyboard.Keyboard:
        """
        A keyboard object used to send HID reports. For details, see the ``Keyboard`` documentation
        in CircuitPython HID: https://circuitpython.readthedocs.io/projects/hid/en/latest/index.html

        The following example types out the letter "a" when the rotary encoder switch is pressed.

        .. code-block:: python

            from adafruit_macropad import MacroPad

            macropad = MacroPad()

            while True:
                if macropad.encoder_switch:
                    macropad.keyboard.send(macropad.Keycode.A)
        """
        if self._keyboard is None:
            self._keyboard = Keyboard(usb_hid.devices)
        return self._keyboard

    @property
    def keyboard_layout(self) -> adafruit_hid.keyboard_layout_base.KeyboardLayoutBase:
        """
        Map ASCII characters to the appropriate key presses on a standard US PC keyboard.
        Non-ASCII characters and most control characters will raise an exception. Required to send
        a string of characters.

        The following example sends the string ``"Hello World"`` when the rotary encoder switch is
        pressed.

        .. code-block:: python

            from adafruit_macropad import MacroPad

            macropad = MacroPad()

            while True:
                if macropad.encoder_switch:
                    macropad.keyboard_layout.write("Hello World")
        """
        if self._keyboard_layout is None:
            # This will need to be updated if we add more layouts. Currently there is only US.
            self._keyboard_layout = self._layout_class(self.keyboard)
        return self._keyboard_layout

    @property
    def consumer_control(self) -> adafruit_hid.consumer_control.ConsumerControl:
        """
        Send ConsumerControl code reports, used by multimedia keyboards, remote controls, etc.

        The following example decreases the volume when the rotary encoder switch is pressed.

        .. code-block:: python

            from adafruit_macropad import MacroPad

            macropad = MacroPad()

            while True:
                if macropad.encoder_switch:
                    macropad.consumer_control.send(macropad.ConsumerControlCode.VOLUME_DECREMENT)
        """
        if self._consumer_control is None:
            self._consumer_control = ConsumerControl(usb_hid.devices)
        return self._consumer_control

    @property
    def mouse(self) -> adafruit_hid.mouse.Mouse:
        """
        Send USB HID mouse reports.

        The following example sends a left mouse button click when the rotary encoder switch is
        pressed.

        .. code-block:: python

            from adafruit_macropad import MacroPad

            macropad = MacroPad()

            while True:
                if macropad.encoder_switch:
                    macropad.mouse.click(macropad.Mouse.LEFT_BUTTON)
        """
        if self._mouse is None:
            self._mouse = Mouse(usb_hid.devices)
        return self._mouse
        
    def display_image_clear(self) -> None:
        self.group.remove(self.sprite)
        
    def display_image(
        self,
        file_name: Optional[str] = None,
        position: Optional[Tuple[int, int]] = None,
    ) -> None:
        """
        Display an image on the built-in display.

        :param str file_name: The path to a compatible bitmap image, e.g. ``"/image.bmp"``. Must be
                              a string.
        :param tuple position: Optional ``(x, y)`` coordinates to place the image.

        The following example displays an image called "image.bmp" located in / on the CIRCUITPY
        drive on the display.

        .. code-block:: python

            from adafruit_macropad import MacroPad

            macropad = MacroPad()

            macropad.display_image("image.bmp")

            while True:
                pass
        """
        if not file_name:
            return
        if not position:
            position = (0, 0)
        self.group = displayio.Group(scale=1)
        self.display.show(self.group)
        with open(file_name, "rb") as image_file:
            background = displayio.OnDiskBitmap(image_file)
            self.sprite = displayio.TileGrid(
                background,
                pixel_shader=background.pixel_shader,
                x=position[0],
                y=position[1],
            )
            self.group.append(self.sprite)
            self.display.refresh()
        
    @staticmethod
    def display_text(
        title: Optional[str] = None,
        title_scale: int = 1,
        title_length: int = 80,
        text_scale: int = 1,
        font: Optional[str] = None,
    ) -> SimpleTextDisplay:
        """
        Display lines of text on the built-in display. Note that if you instantiate this without
        a title, it will display the first (``[0]``) line of text at the top of the display - use
        this feature to have a dynamic "title".

        :param str title: The title displayed above the data. Set ``title="Title text"`` to provide
                          a title. Defaults to None.
        :param int title_scale: Scale the size of the title. Not necessary if no title is provided.
                                Defaults to 1.
        :param int title_length: The maximum number of characters allowed in the title. Only
                                 necessary if the title is longer than the default 80 characters.
                                 Defaults to 80.
        :param int text_scale: Scale the size of the data lines. Scales the title as well.
                               Defaults to 1.
        :param font: The font or the path to the custom font file to use to display the text.
                     Defaults to the built-in ``terminalio.FONT``. Custom font files must be
                     provided as a string, e.g. ``"/Arial12.bdf"``.

        The following example displays a title and lines of text indicating which key is pressed,
        the relative position of the rotary encoder, and whether the encoder switch is pressed.
        Note that the key press line does not show up until a key is pressed.

        .. code-block:: python

            from adafruit_macropad import MacroPad

            macropad = MacroPad()

            text_lines = macropad.display_text(title="MacroPad Info")

            while True:
                key_event = macropad.keys.events.get()
                if key_event:
                    text_lines[0].text = "Key {} pressed!".format(key_event.key_number)
                text_lines[1].text = "Rotary encoder {}".format(macropad.encoder)
                text_lines[2].text = "Encoder switch: {}".format(macropad.encoder_switch)
                text_lines.show()
        """
        return SimpleTextDisplay(
            title=title,
            title_color=SimpleTextDisplay.WHITE,
            title_scale=title_scale,
            title_length=title_length,
            text_scale=text_scale,
            font=font,
            colors=(SimpleTextDisplay.WHITE,),
            display=board.DISPLAY,
        )