# RP2040_LCD_16KeyPad

![](https://i.imgur.com/ZOS9qN3.png)

## 元件
* 16 x Cherry MX 1u
* 16 x 1N4148 diodes
* 16 x RGB LEDs SK6812MINI-E([datasheet](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwja0Iy_nfr3AhUHDd4KHXZNDhUQFnoECAgQAQ&url=https%3A%2F%2Fcdn-shop.adafruit.com%2Fproduct-files%2F4960%2F4960_SK6812MINI-E_REV02_EN.pdf&usg=AOvVaw0GrdVBgLLdg_ElKRQJ0DWj))
* 1 x RP2040-zero([wiki](https://www.waveshare.net/wiki/RP2040-Zero))
* 1 x 2.4inch SPI ili9341 LCD module([wiki](http://www.lcdwiki.com/zh/2.4inch_SPI_Module_ILI9341_SKU:MSP2402))
* 1 x Rotary encoder switch

## Circuitpython 環境設定
### [官方教學文件](https://learn.adafruit.com/circuitpython-essentials)
### [API Reference](https://docs.circuitpython.org/en/latest/docs/index.html)
### [Library Bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases)
### [Community Library Bundle](https://github.com/adafruit/CircuitPython_Community_Bundle/releases)
### 燒綠官方韌體
1. [下載UF2](https://circuitpython.org/board/raspberry_pi_pico/)
![](https://i.imgur.com/lGj5TJ6.png)
![](https://i.imgur.com/si01fVX.png)
2. 將板子按住BOOT键後連接電腦，鬆開BOOT鍵，電腦會出現一個新的磁碟空間，將下載的.uf2檔案複製進去即可完成燒錄。
### Thonny IDE
[官網下載](https://thonny.org/)
1. 下载Thonny IDE Windows版 並依照步驟安裝
2. 安裝完成後，第一次要配置語言和主板環境，為了使用Pico，所以注意主板環境選擇Raspberry Pi 選項。
3. 完成後，修改編譯環境，選擇CircuitPython，若已經接上設備，則可選擇連結埠
![](https://i.imgur.com/bWxCJJF.png)
![](https://i.imgur.com/Cr8OZUe.png)

1. 點擊OK回到Thonny主界面，然后點擊停止按鈕，在Shell中即可顯示當前使用到的環境
![](https://i.imgur.com/Sefn45E.png)
以上都有出現即完成安裝設定
