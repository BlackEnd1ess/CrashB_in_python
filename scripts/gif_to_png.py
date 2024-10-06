from PIL import Image
import os

def extract_and_resize_frames(gif_path, output_folder, new_size=(128,128)):
    # Erstelle den Ausgabeordner, falls dieser nicht existiert
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Öffne die GIF-Datei
    with Image.open(gif_path) as img:
        frame = 0
        while True:
            # Aktuellen Frame extrahieren und skalieren
            resized_frame = img.resize(new_size, Image.Resampling.LANCZOS)
            frame_path = os.path.join(output_folder, f"water_flow{frame}.tga")
            resized_frame.save(frame_path, 'TGA')

            frame += 1
            try:
                img.seek(frame)  # Gehe zum nächsten Frame
            except EOFError:
                break  # Ende der GIF erreicht

    print(f"Alle Frames wurden extrahiert, auf {new_size} skaliert und in {output_folder} gespeichert.")

# Beispielanwendung
gif_path = 'water_flow.gif'  # Pfad zur GIF-Datei
output_folder = 'output_frames'     # Ordner für die extrahierten Frames
extract_and_resize_frames(gif_path, output_folder)
