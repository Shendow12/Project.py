import tkinter as tk
from PIL import Image, ImageTk
import os

# --- Configurare ---
# !!! MODIFICĂ ACEASTĂ LINIE !!!
FOLDER_PATH = "C:/Users/tbogh/Pictures/Saved Pictures/imagine" 

# --- Dimensiuni maxime pentru afișare ---
MAX_WIDTH = 800
MAX_HEIGHT = 600

# --- NOU: Lista pentru a stoca coordonatele ---
coordinates_list = []

# --- Găsirea Primei Imagini JPG ---
first_image_path = None
if os.path.isdir(FOLDER_PATH):
    all_files = os.listdir(FOLDER_PATH)
    for filename in all_files:
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            first_image_path = os.path.join(FOLDER_PATH, filename)
            break
else:
    first_image_path = "path_not_found"

# --- Crearea Ferestrei Principale ---
root = tk.Tk()
root.title("Milestone 3: The Coordinate Logger")

# --- MODIFICAT: Funcția care gestionează click-ul ---
def on_image_click(event):
    """Această funcție este apelată la fiecare click pe canvas."""
    # Extragem coordonatele x si y din obiectul event
    x, y = event.x, event.y
    
    # Adăugăm coordonatele ca tuplu în lista noastră
    coordinates_list.append((x, y))
    
    # Afișăm în consolă pentru verificare
    print(f"Clicked at: ({x}, {y})")
    print("Current list of coordinates:", coordinates_list)

# --- Încărcarea și Afișarea Imaginii ---
if first_image_path and first_image_path != "path_not_found":
    try:
        pil_image = Image.open(first_image_path)

        # --- Logica de redimensionare a imaginii (rămâne la fel) ---
        original_width, original_height = pil_image.size
        ratio = min(MAX_WIDTH / original_width, MAX_HEIGHT / original_height)
        
        new_width = original_width
        new_height = original_height
        if ratio < 1:
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        photo_image = ImageTk.PhotoImage(pil_image)

        # --- Folosim Canvas în loc de Label (rămâne la fel) ---
        canvas = tk.Canvas(root, width=new_width, height=new_height)
        canvas.pack(padx=10, pady=10)
        
        canvas.create_image(0, 0, anchor=tk.NW, image=photo_image)
        
        canvas.image = photo_image 

        # --- Legăm evenimentul de click de funcția noastră (rămâne la fel) ---
        canvas.bind("<Button-1>", on_image_click)
        
    except Exception as e:
        error_label = tk.Label(root, text=f"Eroare la deschiderea imaginii:\n{e}")
        error_label.pack(padx=20, pady=20)
elif first_image_path == "path_not_found":
    error_label = tk.Label(root, text=f"Eroare: Folderul specificat nu există:\n{FOLDER_PATH}")
    error_label.pack(padx=20, pady=20)
else:
    error_label = tk.Label(root, text=f"Nu am găsit nicio imagine JPG/PNG în folderul:\n{FOLDER_PATH}")
    error_label.pack(padx=20, pady=20)

# --- Pornirea Aplicației ---
root.mainloop()