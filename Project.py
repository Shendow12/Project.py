import tkinter as tk
from PIL import Image, ImageTk
import os

# --- Configurare ---
# !!! MODIFICĂ ACEASTĂ LINIE !!!
FOLDER_PATH = "C:/Users/tbogh/Pictures/Saved Pictures/imagine"

# --- Dimensiuni maxime pentru afișare ---
MAX_WIDTH = 800
MAX_HEIGHT = 600

# --- Crearea Ferestrei Principale ---
root = tk.Tk()

# --- Găsirea tuturor imaginilor din folder ---
image_paths = []
if os.path.isdir(FOLDER_PATH):
    for filename in sorted(os.listdir(FOLDER_PATH)):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_paths.append(os.path.join(FOLDER_PATH, filename))

# --- Variabile pentru starea aplicației ---
current_image_index = 0
all_coordinates = {path: [] for path in image_paths} # Dicționar pentru a stoca coordonatele

# --- Variabile globale pentru elementele Tkinter ---
canvas = None
photo_image = None

# --- Funcții ---

def on_image_click(event):
    """Adaugă coordonatele la lista pentru imaginea curentă."""
    x, y = event.x, event.y
    current_path = image_paths[current_image_index]
    all_coordinates[current_path].append((x, y))
    print(f"Clicked at: ({x}, {y}) on {os.path.basename(current_path)}")
    print("Coordinates for this image:", all_coordinates[current_path])

def save_coordinates(event):
    """Salvează coordonatele pentru imaginea curentă, adăugând un antet cu numele imaginii."""
    if not image_paths:
        return

    current_path = image_paths[current_image_index]
    coordinates_to_save = all_coordinates[current_path]

    image_filename = os.path.basename(current_path)
    base_filename, _ = os.path.splitext(image_filename)
    output_filename = os.path.join(os.path.dirname(current_path), f"{base_filename}.txt")

    try:
        with open(output_filename, "w") as f:
            print(f"Saving {len(coordinates_to_save)} coordinates to {output_filename}...")
            
            # Adăugăm un antet (header) la începutul fișierului
            f.write(f"# Coordonate pentru imaginea: {image_filename}\n")

            for coord in coordinates_to_save:
                f.write(f"{coord[0]},{coord[1]}\n")
        print("Coordinates saved successfully!")
    except Exception as e:
        print(f"Error saving file: {e}")

def show_next_image(event):
    """Trece la imaginea următoare."""
    global current_image_index
    if image_paths:
        current_image_index = (current_image_index + 1) % len(image_paths)
        load_and_display_image()

def show_previous_image(event):
    """Trece la imaginea anterioară."""
    global current_image_index
    if image_paths:
        current_image_index = (current_image_index - 1) % len(image_paths)
        load_and_display_image()

def load_and_display_image():
    """Încarcă, redimensionează și afișează imaginea de la indexul curent."""
    global canvas, photo_image

    if canvas:
        canvas.destroy()

    if not image_paths:
        error_label = tk.Label(root, text=f"Nu am găsit nicio imagine în folderul:\n{FOLDER_PATH}")
        error_label.pack(padx=20, pady=20)
        return

    image_path = image_paths[current_image_index]
    root.title(f"Image Annotator - {os.path.basename(image_path)} ({current_image_index + 1}/{len(image_paths)})")

    try:
        pil_image = Image.open(image_path)
        original_width, original_height = pil_image.size
        ratio = min(MAX_WIDTH / original_width, MAX_HEIGHT / original_height)
        
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        photo_image = ImageTk.PhotoImage(pil_image)
        
        canvas = tk.Canvas(root, width=new_width, height=new_height)
        canvas.pack(padx=10, pady=10)
        canvas.create_image(0, 0, anchor=tk.NW, image=photo_image)
        
        canvas.bind("<Button-1>", on_image_click)
    except Exception as e:
        error_label = tk.Label(root, text=f"Eroare la deschiderea imaginii:\n{e}")
        error_label.pack(padx=20, pady=20)

# --- Legarea tastelor (Key Bindings) ---
root.bind("<s>", save_coordinates)
root.bind("<Right>", show_next_image)
root.bind("<Left>", show_previous_image)

# --- Pornirea Aplicației ---
load_and_display_image() # Afișează prima imagine la start
root.mainloop()