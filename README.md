# Image to ASCII Converter

A desktop GUI application built with Tkinter that converts images into ASCII art.

## Features
- Drag and drop image support
- Adjustable font size
- Adjustable aspect ratio
- Save ASCII output
- Open output folder directly

## How To Use
Drag and drop an image into the window, and use the sliders to adjust the settings. The top slider, font size, is defaulted at size 8 and can be adjusted from sizes 1 to 24. This will adjust the size of each ASCII character. The next slider, Height / Font Ratio, will adjust the height as a multiplier. The default setting is 1.0 which translates to 50 lines of ASCII characters, however the amount of lines can be multiplied by changing the slider. A warning with these two multipliers is to be careful with making the window too big, especially when paired with small font sizes as that can lag computers.

## Build

pip install -r requirements.txt
pyinstaller --onefile --windowed --icon=icon.ico --add-data "imagetoascii.png;." --add-data "icon.ico;." --collect-all tkinterdnd2 your_script.py
