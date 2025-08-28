import tkinter as tk
from PIL import Image, ImageTk
import os

# --- Configurare ---
# !!! MODIFICĂ ACEASTĂ LINIE !!!
FOLDER_PATH = "C:/Users/tbogh/Pictures/Saved Pictures/imagine"

# --- ADAUGAT: Dimensiuni maxime pentru afișare ---
MAX_WIDTH = 800
MAX_HEIGHT = 600

# --- Găsirea Primei Imagini JPG ---
first_image_path = None
if os.path.isdir(FOLDER_PATH):
    all_files = os.listdir(FOLDER_PATH)
    for filename in all_files:
        if filename.lower().endswith(('.jpg', '.jpeg')):
            first_image_path = os.path.join(FOLDER_PATH, filename)
            break
else:
    first_image_path = "path_not_found"

# --- Crearea Ferestrei Principale ---
root = tk.Tk()
root.title("Milestone 1: Image Viewer (Cu Redimensionare)")

# --- Încărcarea și Afișarea Imaginii ---
if first_image_path and first_image_path != "path_not_found":
    try:
        pil_image = Image.open(first_image_path)

        # --- NOU: Logica de redimensionare a imaginii ---
        original_width, original_height = pil_image.size
        
        # Calculăm raportul de aspect pentru a păstra proporțiile
        ratio = min(MAX_WIDTH / original_width, MAX_HEIGHT / original_height)
        
        # Redimensionăm imaginea doar dacă este mai mare decât limitele maxime
        if ratio < 1:
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            # Folosim Image.Resampling.LANCZOS pentru o calitate bună la micșorare
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        # --- Sfârșitul secțiunii noi ---

        photo_image = ImageTk.PhotoImage(pil_image)
        image_label = tk.Label(root, image=photo_image)
        image_label.image = photo_image
        image_label.pack(padx=10, pady=10)
        
    except Exception as e:
        error_label = tk.Label(root, text=f"Eroare la deschiderea imaginii:\n{e}")
        error_label.pack(padx=20, pady=20)
elif first_image_path == "path_not_found":
    error_label = tk.Label(root, text=f"Eroare: Folderul specificat nu există:\n{FOLDER_PATH}")
    error_label.pack(padx=20, pady=20)
else:
    error_label = tk.Label(root, text=f"Nu am găsit nicio imagine JPG în folderul:\n{FOLDER_PATH}")
    error_label.pack(padx=20, pady=20)

# --- Pornirea Aplicației ---
root.mainloop()