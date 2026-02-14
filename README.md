# Image to ASCII Converter

A desktop GUI application built with Tkinter that converts images into ASCII art.

## Features
- Drag and drop image support
- Adjustable font size
- Adjustable aspect ratio
- Save ASCII output
- Open output folder directly

## Build

pip install -r requirements.txt
pyinstaller --onefile --windowed --icon=icon.ico --add-data "imagetoascii.png;." --add-data "icon.ico;." --collect-all tkinterdnd2 your_script.py
