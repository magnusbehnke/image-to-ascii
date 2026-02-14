import os
import sys
from datetime import datetime
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
from tkinterdnd2 import TkinterDnD, DND_FILES


# ASCII Characters by brightness (dark → light)
ASCII_CHARS = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", "."]
nH = 50  # base number of lines for font size 8
ascii_text = ""

# ---------------- GUI SETUP ----------------

root = TkinterDnD.Tk()
root.title("Image to ASCII")
root.geometry("800x660")

asciiFont = font.Font(
    root,
    family="Consolas",
    size=8,
    weight="bold"
)

# Global variables for output window
ascii_window = None
ascii_label = None
font_size = 8  # initial font size
height_ratio = 1.0  # initial height-to-font ratio

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ---------------- IMAGE PROCESSING ----------------

def resizeImage(image, newHeight=nH):
    width, height = image.size
    ratio = width / height

    char_width = asciiFont.measure("A")
    char_height = asciiFont.metrics("linespace")
    aspect_correction = char_width / char_height

    newWidth = int(newHeight * ratio / aspect_correction)
    return image.resize((newWidth, newHeight))

def grayscale(image):
    return image.convert("L")

def pixelsToAscii(image):
    pixels = image.get_flattened_data()
    return "".join(ASCII_CHARS[pixel // 25] for pixel in pixels)

# ---------------- MAIN LOGIC ----------------

def saveAscii():
    global ascii_text

    if not ascii_text:
        return 
    
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    output_folder = os.path.join(base_dir, "asciiOutput")
    os.makedirs(output_folder, exist_ok=True)

    timeStamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ascii_art_{timeStamp}.txt"

    filepath = os.path.join(output_folder,filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(ascii_text)

def openOutputFolder():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    output_folder = os.path.join(base_dir, "asciiOutput")

    os.makedirs(output_folder, exist_ok=True)

    os.startfile(output_folder)

def openAsciiWindow(path):
    global ascii_window, ascii_label, font_size, height_ratio
    global ascii_text

    try:
        image = Image.open(path)
    except Exception:
        print("Invalid image path")
        return

    # Create ascii_window if it doesn't exist
    if ascii_window is None or not ascii_window.winfo_exists():
        ascii_window = tk.Toplevel()
        ascii_window.title("ASCII Output")

        # ---- TOP BAR ----
        top_bar = tk.Frame(ascii_window, height=30, bg="lightgray")
        top_bar.pack(side="top", fill="x")
        
        # Add a button to the top bar
        save_button = tk.Button(
            top_bar, 
            text="Save ASCII",
            command=saveAscii
        )
        save_button.pack(side="left", padx=5, pady=2)

        open_folder_button = tk.Button(
            top_bar,
            text="Open Folder",
            command=openOutputFolder
        )
        open_folder_button.pack(side="left", padx=5, pady=2)

        ascii_label = tk.Label(
            ascii_window,
            font=asciiFont,
            justify="left",
            anchor="nw"
        )
        ascii_label.pack(fill="both", expand=True)
    else:
        # Clear previous ASCII label (but keep top bar)
        for widget in ascii_window.winfo_children():
            if widget != top_bar:
                widget.destroy()
        # Re-add the label
        ascii_label = tk.Label(
            ascii_window,
            font=asciiFont,
            justify="left",
            anchor="nw"
        )
        ascii_label.pack(fill="both", expand=True)

    # Resize image properly
    width, height = image.size
    ratio = width / height

    char_width = asciiFont.measure("A")
    char_height = asciiFont.metrics("linespace")
    aspect_correction = char_width / char_height

    # Adjust nH dynamically based on font size and slider ratio
    nH_dynamic = max(1, int(nH * 8 / font_size * height_ratio))  # 8 = original font size

    newWidth = int(nH_dynamic * ratio / aspect_correction)
    image = image.resize((newWidth, nH_dynamic)).convert("L")

    # Convert to ASCII
    asciiData = "".join(
        ASCII_CHARS[p * len(ASCII_CHARS) // 256] for p in image.getdata()
    )
    asciiImage = "\n".join(
        asciiData[i:(i + newWidth)] for i in range(0, len(asciiData), newWidth)
    )

    ascii_text = asciiImage

    # Update label with ASCII
    ascii_label.config(text=asciiImage)

    # Resize window to fit text
    pixel_width = newWidth * char_width
    pixel_height = (nH_dynamic * char_height) + 30
    ascii_window.geometry(f"{pixel_width}x{pixel_height}")
    ascii_window.resizable(False, False)
    ascii_window.lift()

# ---------------- DROP HANDLER ----------------

def drop(event):
    path = event.data.strip("{}")
    openAsciiWindow(path)

# ---------------- ROOT UI ----------------

root.title("Image To ASCII")
root.geometry("500x500")
root.iconbitmap(resource_path("icon.ico"))

# ---------------- LOGO ----------------

# Load logo image
logo_image = Image.open(resource_path("imagetoascii.png")) # put your logo file name here
logo_image = logo_image.resize((200, 200))  # adjust size as needed

logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = tk.Label(root, image=logo_photo)
logo_label.image = logo_photo  # prevent garbage collection
logo_label.pack(pady=(30, 10))  # space above and below

# ---------------- DRAG TEXT ----------------

label = tk.Label(
    root,
    text="Drag and drop an image file into this window",
    font=("Consolas", 12)
)
label.pack()

# Slider to control font size
def updateFontSize(value):
    global font_size, asciiFont
    font_size = int(value)
    asciiFont.configure(size=font_size)

slider_font = tk.Scale(
    root,
    from_=1,   # minimum font size
    to=24,     # maximum font size
    orient="horizontal",
    label="Font Size",
    command=updateFontSize
)
slider_font.set(font_size)
slider_font.pack(fill="x", padx=20, pady=5)

# Slider to control height-to-font ratio
def updateHeightRatio(value):
    global height_ratio
    height_ratio = float(value)

slider_ratio = tk.Scale(
    root,
    from_=0.2,   # small ratio = more lines
    to=4.0,       # large ratio = fewer lines
    resolution=0.2,
    orient="horizontal",
    label="Height / Font Ratio",
    command=updateHeightRatio
)
slider_ratio.set(1.0)
slider_ratio.pack(fill="x", padx=20, pady=5)

root.drop_target_register(DND_FILES)
root.dnd_bind("<<Drop>>", drop)

# ---------------- RUN ----------------

root.mainloop()
