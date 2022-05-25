import os
import time
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from myMacroPad import MacroPad
import gc
import random
import adafruit_imageload

displayio.release_displays()
def DEBUG_STRING(string):
    pass
#     print(string)
def DEBUG_STRING_INFO(string, value):
    pass
#     print(string, value)
    
# CONFIGURABLES ------------------------

MACRO_FOLDER = '/macros'
KEY_TOTAL = 16
IMAGE_FOLDER = "/images"
change_press_RGB = True #when press btn change rgb color
now_RGB_animation_num = -1
start_picture_show = False #進入更新圖片迴圈(無法做其他事情)
break_flag = True #用來中斷迴圈
show_Information = False #進到此畫面
list_infomation = ['Version: 0.1.2',
                   'CircuitPython 7.2.5',
                   'RP2040-Zero',
                   '16key_SPI_ili9341_LCD',
                   '@James Lu']
# CLASSES AND FUNCTIONS ----------------
class App:
    """ Class representing a host-side application, for which we have a set
        of macro sequences. Project code was originally more complex and
        this was helpful, but maybe it's excessive now?"""
    def __init__(self, appdata):
        self.name = appdata['name']
        self.macros = appdata['macros']

    def switch(self):
        """ Activate application settings; update OLED labels and LED
            colors. """
        group[KEY_TOTAL + 1].text = self.name   # Application name
        DEBUG_STRING_INFO("self.name:", str(self.name))
        for i in range(KEY_TOTAL):
            if i < len(self.macros): # Key in use, set label + LED color
                if change_press_RGB:
                    macropad.pixels[i] = self.macros[i][0]
                group[i].text = self.macros[i][1]
            else:  # Key not in use, no label or LED
                if change_press_RGB:
                    macropad.pixels[i] = 0
                group[i].text = ''
        if self.name == "RGB Config":
            group[3].text = str(round(macropad.pixels.brightness,1))
            group[11].text = str(now_RGB_animation_num)
        macropad.keyboard.release_all()
        macropad.consumer_control.release()
        macropad.mouse.release_all()
        #if not macropad.animations.animate():
        if change_press_RGB:
            DEBUG_STRING("-----PAGE RGB-----")
            macropad.pixels.show()
        gc.collect()


# INITIALIZATION -----------------------

macropad = MacroPad()
macropad.pixels.auto_write = False
macropad.pixels.brightness = 0.1

# Set up displayio group with all the labels
group = displayio.Group()
DEBUG_STRING_INFO("width:", str(macropad.display.width))
DEBUG_STRING_INFO("height:", str(macropad.display.height))

for key_index in range(KEY_TOTAL):
    x = key_index % 4
    y = key_index // 4
    group.append(label.Label(terminalio.FONT, text='', color=0xFFFFFF,scale=2,
                             anchored_position=((macropad.display.width - 1) * x / 3,
                                                40+(macropad.display.height//5*(y+1))),
                             anchor_point=(x / 3, 1.0)))
    
group.append(Rect(0, 0, macropad.display.width, 40, fill=0xFFFFFF))
group.append(label.Label(terminalio.FONT, text='', color=0x000000,
                         scale=3,
                         anchored_position=(macropad.display.width / 2, -4),
                         anchor_point=(0.5, 0.0)))
macropad.display.show(group)

DEBUG_STRING_INFO("free mem@after bitmap", gc.mem_free())
gc.collect()
DEBUG_STRING_INFO("free mem@after gc.collect()", gc.mem_free())

# Load all the macro key setups from .py files in MACRO_FOLDER
apps = []
files = os.listdir(MACRO_FOLDER)
files.sort()
for filename in files:
    if filename.endswith('.py') and not filename.startswith('._'):
        try:
            module = __import__(MACRO_FOLDER + '/' + filename[:-3])
            apps.append(App(module.app))
        except (SyntaxError, ImportError, AttributeError, KeyError, NameError,
                IndexError, TypeError) as err:
            DEBUG_STRING_INFO("ERROR in", filename)
            import traceback
            traceback.print_exception(err, err, err.__traceback__)
            
images = []
image_files = os.listdir(IMAGE_FOLDER)
image_files.sort()
for filename in image_files:
    if filename.endswith('.bmp') and not filename.startswith('._'):
        try:
            image = IMAGE_FOLDER + '/' + filename
            images.append(image)
        except (SyntaxError, ImportError, AttributeError, KeyError, NameError,
                IndexError, TypeError) as err:
            DEBUG_STRING_INFO("ERROR in", filename)
            import traceback
            traceback.print_exception(err, err, err.__traceback__)
            
if not apps:
    group[KEY_TOTAL + 1].text = 'NO MACRO FILE'
    while True:
        pass

last_position = None
last_encoder_switch = macropad.encoder_switch_debounced.pressed
app_index = 0
apps[app_index].switch()
'''
# 'sequence' is an arbitrary-length list, each item is one of:
# Positive integer (e.g. Keycode.KEYPAD_MINUS): key pressed
# Negative integer: (absolute value) key released
# Float (e.g. 0.25): delay in seconds
# String (e.g. "Foo"): corresponding keys pressed & released
# List []: one or more Consumer Control codes (can also do float delay)
# Dict {}: mouse buttons/motion (might extend in future)

# Release any still-pressed keys, consumer codes, mouse buttons
# Keys and mouse buttons are individually released this way (rather
# than release_all()) because pad supports multi-key rollover, e.g.
# could have a meta key or right-mouse held down by one macro and
# press/release keys/buttons with others. Navigate popups, etc.
'''

# MAIN LOOP ----------------------------
DEBUG_STRING("---------Main Loop Start---------")
macropad.animations.freeze()

    
def Add_RGB_NUM():
    #global macropad
    global now_RGB_animation_num
    now_RGB_animation_num += 1
    if now_RGB_animation_num > macropad.total_animations_num-1:
        now_RGB_animation_num = 0
    group[11].text = str(now_RGB_animation_num)
    
def Sub_RGB_NUM():
    global now_RGB_animation_num
    now_RGB_animation_num -= 1
    if now_RGB_animation_num < -1:
        now_RGB_animation_num = macropad.total_animations_num-1
    group[11].text = str(now_RGB_animation_num)

while True:
    if start_picture_show == False:
        
        macropad.animations.animate()
        
        position = macropad.encoder
        if position != last_position:
            last_position = position
            DEBUG_STRING_INFO("encoder pos:", str(position))
            app_index = position % len(apps)
            DEBUG_STRING_INFO("app_index:", str(app_index))
            apps[app_index].switch()
            
        macropad.encoder_switch_debounced.update()
        encoder_switch = macropad.encoder_switch_debounced.pressed
        if encoder_switch != last_encoder_switch:
            last_encoder_switch = encoder_switch
            if len(apps[app_index].macros) < KEY_TOTAL+1:
                continue    # No 17th macro, just resume main loop
            key_number = KEY_TOTAL # else process below as 17th macro
            pressed = encoder_switch
        else:
            event = macropad.keys.events.get()
            if not event or event.key_number >= len(apps[app_index].macros):
                continue # No key events, or no corresponding macro, resume loop
            key_number = event.key_number
            pressed = event.pressed
            
        sequence = apps[app_index].macros[key_number][2]
        if pressed:
            if key_number < KEY_TOTAL: # No pixel for encoder button
                if change_press_RGB:
                    DEBUG_STRING("-----press RGB-----")
                    _r = random.randint(0, 255)
                    _g = random.randint(0, 255)
                    _b = random.randint(0, 255)
                    macropad.pixels[key_number] = (_r, _g, _b)
                    macropad.pixels.show()
                group[key_number].color = 0x000000
                group[key_number].background_color = 0xFFFFFF
            for item in sequence:
                DEBUG_STRING(str(item))
                if isinstance(item, int):
                    DEBUG_STRING("item is int")
                    if item >= 0:
                        macropad.keyboard.press(item)
                    else:
                        macropad.keyboard.release(-item)
                elif isinstance(item, float):
                    DEBUG_STRING("item is float")
                    time.sleep(item)
                elif isinstance(item, str):
                    DEBUG_STRING("item is str")
                    macropad.keyboard_layout.write(item)
                elif isinstance(item, list):
                    DEBUG_STRING("item is list")
                    for code in item:
                        if isinstance(code, int):
                            macropad.consumer_control.release()
                            macropad.consumer_control.press(code)
                        if isinstance(code, float):
                            time.sleep(code)
                elif isinstance(item, dict):
                    DEBUG_STRING("item is dict")
                    if 'buttons' in item:
                        if item['buttons'] >= 0:
                            macropad.mouse.press(item['buttons'])
                        else:
                            macropad.mouse.release(-item['buttons'])
                    elif 'RGB_Light' in item:
                        DEBUG_STRING_INFO("Light", item['RGB_Light'])
                        macropad.pixels.brightness += item['RGB_Light']
                        group[3].text = str(round(macropad.pixels.brightness,1))
                        DEBUG_STRING_INFO("now RGB_Light", macropad.pixels.brightness)
                    elif 'RGB_AT' in item:
                        DEBUG_STRING_INFO("RGB_AT", item['RGB_AT'])
                        if item['RGB_AT'] == 'on':
                            if change_press_RGB:
                                macropad.animations.fill(0)
                                macropad.animations.resume()
                                change_press_RGB = False
                                Add_RGB_NUM()
                        elif item['RGB_AT'] == 'off':
                            if not change_press_RGB:
                                macropad.animations.freeze()
                                macropad.animations.fill(0)
                                change_press_RGB = True
                                Sub_RGB_NUM()
                                apps[app_index].switch()
                        elif item['RGB_AT'] == 'next':
                            if not change_press_RGB:
                                macropad.animations.fill(0)
                                macropad.animations.next()
                                Add_RGB_NUM()
                    elif 'info' in item:
                        #macropad.display_image("images/Namin_1.bmp")
                        macropad.animations.fill(0)
                        start_picture_show = True
                        show_Information = True
                        gc.collect()
                    elif 'image' in item:
                        macropad.animations.fill(0)
                        image_show_time = item['image']
                        start_picture_show = True
                        show_Information = False
                        break_flag = False
                        gc.collect()
                    macropad.mouse.move(item['x'] if 'x' in item else 0,
                                        item['y'] if 'y' in item else 0,
                                        item['wheel'] if 'wheel' in item else 0)
        else:
            for item in sequence:
                if isinstance(item, int):
                    if item >= 0:
                        macropad.keyboard.release(item)
                elif isinstance(item, dict):
                    if 'buttons' in item:
                        if item['buttons'] >= 0:
                            macropad.mouse.release(item['buttons'])
            macropad.consumer_control.release()
            if key_number < KEY_TOTAL: # No pixel for encoder button
                if change_press_RGB:
                    DEBUG_STRING("-----release RGB-----")
                    macropad.pixels[key_number] = apps[app_index].macros[key_number][0]
                    macropad.pixels.show()
                group[key_number].color = 0xFFFFFF
                group[key_number].background_color = 0x000000
    
    if start_picture_show == True:
        if show_Information:
            DEBUG_STRING_INFO("list_infomation:",len(list_infomation))
            white_Rect = Rect(0, 0, macropad.display.width, macropad.display.height, fill=0x000000)
            group.append(white_Rect)
            info_1 = label.Label(terminalio.FONT, text=str(list_infomation[0]), color=0xFFFFFF,
                         scale=2,
                         anchored_position=(0, (macropad.display.height / 5)*0),
                         anchor_point=(0.0, 0.0))
            info_2 = label.Label(terminalio.FONT, text=str(list_infomation[1]), color=0xFFFFFF,
                         scale=2,
                         anchored_position=(0, (macropad.display.height / 5)*1),
                         anchor_point=(0.0, 0.0))
            info_3 = label.Label(terminalio.FONT, text=str(list_infomation[2]), color=0xFFFFFF,
                         scale=2,
                         anchored_position=(0, (macropad.display.height / 5)*2),
                         anchor_point=(0.0, 0.0))
            info_4 = label.Label(terminalio.FONT, text=str(list_infomation[3]), color=0xFFFFFF,
                         scale=2,
                         anchored_position=(0, (macropad.display.height / 5)*3),
                         anchor_point=(0.0, 0.0))
            info_5 = label.Label(terminalio.FONT, text=str(list_infomation[4]), color=0xFFFFFF,
                         scale=2,
                         anchored_position=(0, (macropad.display.height / 5)*4),
                         anchor_point=(0.0, 0.0))
            group.append(info_1)
            group.append(info_2)
            group.append(info_3)
            group.append(info_4)
            group.append(info_5)
            while True:
                macropad.encoder_switch_debounced.update()
                encoder_switch = macropad.encoder_switch_debounced.pressed
                if encoder_switch != last_encoder_switch:
                    last_encoder_switch = encoder_switch
                    start_picture_show = False
                    show_Information = False
                    group.remove(white_Rect)
                    group.remove(info_1)
                    group.remove(info_2)
                    group.remove(info_3)
                    group.remove(info_4)
                    group.remove(info_5)
                    break
        else:
            white_Rect = Rect(0, 0, macropad.display.width, macropad.display.height, fill=0xFFFFFF)
            group.append(white_Rect)
            while True:
                for bmpfile in images:
                    DEBUG_STRING("========================")
                    
                    DEBUG_STRING_INFO("bitmap file:", bmpfile)
                    
                    DEBUG_STRING_INFO("free mem@before bitmap", gc.mem_free())
                    
                    background = displayio.OnDiskBitmap(bmpfile)
                    tile_grid = displayio.TileGrid(
                        background,
                        pixel_shader=background.pixel_shader,
                    )
                    
                    DEBUG_STRING_INFO("free mem@after bitmap", gc.mem_free())
                    gc.collect()
                    DEBUG_STRING_INFO("free mem@after gc.collect()", gc.mem_free())

                    # Add the TileGrid to the Group
                    group.append(tile_grid)
                    DEBUG_STRING_INFO("index: ", group.index(tile_grid))
                    # Add the Group to the Display
                    macropad.display.show(group)
                    time.sleep(image_show_time)
                    group.remove(tile_grid)
                    
                    macropad.encoder_switch_debounced.update()
                    encoder_switch = macropad.encoder_switch_debounced.pressed
                    if encoder_switch != last_encoder_switch:
                        last_encoder_switch = encoder_switch
                        start_picture_show = False
                        break_flag = True
                        break
                if break_flag:
                    group.remove(white_Rect)
                    macropad.display.refresh()
                    break
DEBUG_STRING("-bye-")