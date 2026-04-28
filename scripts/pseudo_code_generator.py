import re
from pathlib import Path

INPUT_FILE = "crashedit_clean_code.txt"
OUTPUT_FILE = "pseudo_readable.txt"

STATE_HEADER_RE = re.compile(r"^(State_\d+)\s+\[(.*?)\]\s+\((.*?)\)")
BLOCK_RE = re.compile(r"^(State_\d+_[a-z]+):$")
INSTR_RE = re.compile(r"^\s*(\d+)\s+([A-Z]{2,6})\s*(.*?)\s*(?:#\s*(.*))?$")

HEX_RE = re.compile(r"0x[0-9A-Fa-f]+")

def hex_to_dec(text):
	def repl(match):
		h = match.group(0)
		d = int(h, 16)
		return f"{h}) -> {d}"
	return HEX_RE.sub(repl, text)

IGNORE_OPS = {
	"MOV",
	"PUSH",
	"ANDB",#&& bit
	"ORB",# or bit
}

OP_NAMES = {
	"ADD"	:	"     incrase value=",
	"SUB"	:	"     decrase value=",
	"MUL"	:	"     multiply value=",
	"DIV"	:	"     divide value=",
	"CEQ"	:	'if',		#"Vergleich: gleich",
	"CNE"	:	'if',		#"Vergleich: ungleich",
	"SLT"	:	'if',		#"Vergleich: kleiner als",
	"SGT"	:	'if',		#"Vergleich: größer als",
	"SLE"	:	'if',		#"Vergleich: kleiner/gleich",
	"SGE"	:	'if',		#"Vergleich: größer/gleich",
	"ORL"	:	"(OR) ::: -> if",			#logic or
	"ANDL"	:	"(AND) ::: -> if",			#logic and
	"NOTL"	:	"(NOT) ::: -> if",			#logic not
	"SHA"	:	"     scale value=",#
	"DEGD"	:	'     math.degree'		,	#distance math
	"BEQZ"	:	'',		# "Springt, wenn Bedingung falsch ist",
	"BNEZ"	:	'',		# "Springt, wenn Bedingung wahr ist",
	"BRA"	:	'',		#"Unbedingter Sprung",
	"CST"	:	'     change_state=',		#"Wechselt den State",
	"RET"	:	'',		#"Beendet diesen Block",
	"ANIS"	:	'     AnimationSequence()',		# "Setzt Animationssequenz",
	"ANIF"	:	'     AnimationFrame()',		# "Spielt Animationsframe",
	"ANIM"	:	'     AnimationPlay()',		# "Spielt Animation",
	"CVMW"	:	'     model_vertex_color=',
	"ABS"	:	'     absolute',
	"MOVC"	:	'     move_code',
	"CHLD"	:	'init_class() ',		# "Erzeugt Child-Objekt",
	"EVNT"	:	'',		# "Sendet Event",
	"EVHA"	:	'',		# "Akzeptiert Event und wechselt ggf. State",
	"EVHR"	:	'',		# "Lehnt/behandelt Event",
	"RND" 	:	'     number.',		# "Zufallswert",
	"SNDA"	:	'     SND PARAM',		# "Setzt Audio-Parameter",
	"SNDP"	:	'     SND PLAY',		# "Spielt Sound",
	"VECA"	:	'',		# "Vektor-/Bewegungsoperation",
	"VECB"	:	'',		# "Vektor-/Prüfoperation",
	"SPD" 	:	'',		# "Geschwindigkeit/Bewegung",
	"SEEK"	:	'',		# "Nähert Wert an Zielwert an",
	"LOOP"	:	'for x in loop: ',		# "Loop-/Zähleroperation",
	"MISC"	:	'',		# "Engine-spezifische Hilfsfunktion",
	"TICK"	:	'     time.delta',		# "Tick-/Timeroperation",
	"RGL"	:	"     read global",# read global
	"WGL"	:	"     write global"# write gobal
}


def block_title(block_name):
	name = block_name.replace(":", "")
	parts = name.split("_")
	state_num = parts[1] if len(parts) > 1 else "?"
	kind = parts[2].upper() if len(parts) > 2 else "BLOCK"
	kind_desc = {
		"CPC": "class structure",
		"TPC": "update event",
		"EPC": "trigger event",
	}.get(kind, kind)
	return f"STATE {state_num} {kind} — {kind_desc}"


def describe_instruction(pc, op, arg_text, comment):
	desc = OP_NAMES.get(op, "unknown assembler operator")
	arg_text = hex_to_dec(arg_text)
	if comment:
		comment = hex_to_dec(comment)
		#return f"[{pc}] {op}: {desc}. {comment.strip()}"
		return f"{pc}: {desc} {comment.strip()}"
	#return f"[{pc}] {op}: {desc}. Args: {arg_text.strip()}"
	return f"{pc}: {op}: {desc}. Args: {arg_text.strip()}"


def convert(input_file, output_file):
	lines = Path(input_file).read_text(encoding="utf-8").splitlines()
	out = [
		"CrashEdit ASM dumper",		"=" * 58]
	for raw in lines:
		line = raw.strip()
		if not line:
			continue
		m_header = STATE_HEADER_RE.match(line)
		if m_header:
			state, cls, flags = m_header.groups()
			out.append("")
			out.append("-" * 58)
			out.append(f"{state} — Objektklasse: {cls}")
			out.append(f"Flags: {flags}")
			continue
		#if line.startswith("Event block"):
		#	out.append("Event-Block: nicht verfügbar.")
		#	continue
		#if line.startswith("Trans block"):
		#	out.append("Transition-Block: nicht verfügbar.")
		#	continue
		#if line.startswith(("CPC:", "TPC:")):
		#	out.append(line)
		#	continue
		m_block = BLOCK_RE.match(line)
		if m_block:
			title = block_title(m_block.group(1))
			out.append("")
			out.append(title)
			out.append("-" * len(title))
			continue
		m_instr = INSTR_RE.match(line)
		if m_instr:
			pc, op, arg_text, comment = m_instr.groups()
			if op in IGNORE_OPS:
				continue
			out.append(describe_instruction(pc, op, arg_text, comment))
			continue
	Path(output_file).write_text("\n".join(out), encoding="utf-8")
	print(f"Gespeichert: {output_file}")
	print(f"Zeilen: {len(out)}")


if __name__ == "__main__":
	convert(INPUT_FILE, OUTPUT_FILE)