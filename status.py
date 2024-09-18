from ursina import *

## one load level settings
checkpoint=None
day_mode=''

## game progress items
COLOR_GEM=[]
CLEAR_GEM=[]
CRYSTAL=[]

## reset instances
NPC_RESET=[]
W_RESET=[]
C_RESET=[]

## player rule
p_last_direc=None
selected_level=1
level_index=0
aku_hit=1
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

weather_thunder=False
gem_path_solved=False
is_death_route=False
is_time_trial=False

b_audio=False
e_audio=False
n_audio=False

wait_screen=False
death_event=False
aku_exist=False
gem_death=False
loading=False
pause=False

## global funcs
def p_idle(c):
	if c.landed and not (c.jumping or c.is_attack or c.walking or c.is_landing):
		return True
	return False
def p_rst(c):
	if death_event or not c.warped or c.freezed:
		return True
	return False
def gproc():
	if loading or pause or LV_CLEAR_PROCESS or level_solved:
		return True
	return False