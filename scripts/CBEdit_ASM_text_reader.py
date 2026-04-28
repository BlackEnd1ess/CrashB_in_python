from pywinauto import Desktop

raw_out = []

def dump(ctrl, depth=0):
	indent = "  " * depth

	try:
		name = ctrl.window_text()
	except Exception:
		name = ""

	try:
		cls = ctrl.class_name()
	except Exception:
		cls = "?"

	try:
		ctype = ctrl.element_info.control_type
	except Exception:
		ctype = "?"

	if name:
		line = f"{indent}{ctype} | {cls} | {name}"
	else:
		line = f"{indent}{ctype} | {cls}"

	print(line)
	raw_out.append(line)

	try:
		children = ctrl.children()
	except Exception:
		children = []

	for child in children:
		dump(child, depth + 1)


for w in Desktop(backend="uia").windows():
	try:
		title = w.window_text()
	except Exception:
		continue

	if "CrashEdit" in title:
		print("FOUND:", title)
		raw_out.append("FOUND: " + title)
		dump(w)

import re

with open("crashedit_clean_code.txt", "r", encoding="utf-8") as f:
	lines = f.readlines()

out = []

for line in lines:
	line = line.rstrip()

	# Alles nach dem zweiten | nehmen
	parts = line.split("|", 2)
	if len(parts) == 3:
		text = parts[2].strip()
	else:
		text = line.strip()

	if not text:
		continue

	if (
		text.startswith("State_")
		or text.startswith("Event block")
		or text.startswith("Trans block")
		or text.startswith("CPC:")
		or text.startswith("TPC:")
		or re.match(r"^\d+\s+[A-Z]{2,6}\s+", text)
	):
		out.append(text)

with open("crashedit_clean_code.txt", "w", encoding="utf-8") as f:
	f.write("\n".join(out))

print("Gefilterte Zeilen:", len(out))

print("RAW gespeichert.")
input(" ")