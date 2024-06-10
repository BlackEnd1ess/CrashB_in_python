from ursina import *

## one load level settings
checkpoint=None
day_mode=''

## game progress items
COLOR_GEM=[4]
CLEAR_GEM=[]
CRYSTAL=[]

## reset instances
NPC_RESET=[]
C_RESET=[]
W_RESET=[]

## player rule
p_last_direc=None
level_index=0
aku_hit=0
fails=0

## wumpa count
wumpa_fruits=0
wumpa_bonus=0

## crate count
crates_in_level=0
crates_in_bonus=0
crate_to_sv=0
crate_count=0
crate_bonus=0

## live count
lives_bonus=0
extra_lives=4

## collected gems/crystal
collected_crystals=0
color_gems=0
clear_gems=0

## ui timer
show_wumpas=0
show_crates=0
show_lives=0
show_gems=0

## level processing
LV_CLEAR_PROCESS=False
LEVEL_CLEAN=False

level_crystal=False
level_col_gem=False
level_cle_gem=False
level_solved=False

bonus_solved=False
bonus_round=False

is_death_route=False
preload_phase=False
is_time_trial=False

b_audio=False
e_audio=False
n_audio=False

death_event=False
cam_unlock=False
aku_exist=False
on_terra=False
gem_death=False
is_dying=False
c_indoor=True
loading=False
pause=False

## global funcs
def p_walk(d):
	if held_keys['d'] or held_keys['a'] or held_keys['s'] or held_keys['w'] or d.walking:
		return True
	return False
def p_in_air(d):
	if not d.landed or d.jumping:
		return True
	return False
def p_idle(d):
	if not d.walking and not d.jumping and not d.is_attack and not p_walk(d) and d.landed:
		return True
	return False
def p_rst(d):
	if is_dying or not d.warped or d.freezed:
		return True
	return False
def gproc():
	if loading or pause or LV_CLEAR_PROCESS or level_solved:
		return True
	return False