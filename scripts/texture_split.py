from PIL import Image
import os

def split_image(input_image_path, output_folder, tile_width, tile_height):
	image = Image.open(input_image_path)
	image_width, image_height = image.size
	assert image_width % tile_width == 0, "Bildbreite ist nicht durch Kachelbreite teilbar"
	assert image_height % tile_height == 0, "Bildhöhe ist nicht durch Kachelhöhe teilbar"
	if not os.path.exists(output_folder):
		os.makedirs(output_folder)
	tile_number = 0
	for top in range(0, image_height, tile_height):
		for left in range(0, image_width, tile_width):
			right = left + tile_width
			bottom = top + tile_height
			tile = image.crop((left, top, right, bottom))
			tile.save(os.path.join(output_folder, f"anim_crt_{tile_number}.png"))
			tile_number += 1

# Parameter
input_image_path = "crate_anim.png"
output_folder = "crate_anim"
tile_width = 128
tile_height = 128

split_image(input_image_path,output_folder,tile_width,tile_height)
