from ursina import *

## one load level settings
checkpoint=None

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

## crate audio limit
br_sn=False
ex_sn=False
ni_sn=False

## level processing
LV_CLEAR_PROCESS=False
LEVEL_CLEAN=False
game_over=False

level_crystal=False
level_col_gem=False
level_cle_gem=False

bonus_solved=False
bonus_round=False
death_route=False

weather_thunder=False
gem_path_solved=False

bonus_warp_room=False
is_time_trial=False
is_invincible=False
wait_screen=False
death_event=False
aku_exist=False
gem_death=False
crd_seen=False
loading=False
pause=False

## global funcs
def p_idle(c):
	return (c.landed and not any([c.jumping,c.is_attack,c.walking,c.is_landing]))

def p_rst(c):
	return (not c.warped or any([c.standup,c.freezed,death_event]))

def gproc():
	return any([loading,pause,LV_CLEAR_PROCESS,game_over])