import os

INPUT_DIR = "sound/"
OUTPUT_FILE = "SFX_DATABASE.py"
with open(OUTPUT_FILE,"w",encoding="utf-8") as out:
	out.write("PLAYER_SND={\n")
	for filename in os.listdir(INPUT_DIR):
		if not filename.lower().endswith(".wav"):
			continue
		name = os.path.splitext(filename)[0]
		with open(os.path.join(INPUT_DIR, filename), "rb") as f:
			data = f.read()
		out.write(f'    "{name}": {repr(data)},\n')
	out.write("}\n")

print("Soundbank erzeugt:", OUTPUT_FILE)
input("fertig")
