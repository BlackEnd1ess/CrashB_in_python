from ursina import *

## this objects interacts with player
OBJ_LIST=['water_hit','falling_zone','level_finish','bonus_platform','gem_platform','moss_platform']

## objects in this list will hidden by LOD in _core.py
LOD_LST=['tree2_d','tree_scene','bush','pillar','rock','moss_platform']

## display the name in pause menu
level_name=['Warp Room',
			'LEVEL 1 - TURTLE WOODS',
			'LEVEL 2 - WAY TO NOWHERE',
			'LEVEL 3 - UPSTREAM',
			'LEVEL 4 - DRAIN DAMAGE',
			'LEVEL 5 - RUINED',
			'DEVELOPER TEST LEVEL']

## npc animation_frame count
npc_anim={'amadillo':7,'turtle':12,'saw_turtle':12,'penguin':15,
		'hedgehog':12,'seal':14,'eating_plant':13,'rat':10,
		'lizard':11,'scrubber':3,'mouse':8,'vulture':13}

## one load level settings
bonus_checkpoint=[None,(0,2,-6),(.3,2,2.3),(0,3,20.5),(0,0,0),(0,0,0)]
checkpoint=None
day_mode=''

## game progress items
COLOR_GEM=[]
CLEAR_GEM=[]
CRYSTAL=[]

## reset instances
NPC_RESET=[]
C_RESET=[]
W_RESET=[]

## player rule
player_protect=0
level_index=0
c_delay=0
d_delay=0
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

e_audio=False
n_audio=False

aku_exist=False
is_dying=False
c_indoor=True
loading=False
pause=False

gem_death=False
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
def gproc():
	if loading or pause:
		return True
	return False