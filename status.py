from ursina import *

level_name=['Warp Room',
			'LEVEL 1 - TURTLE WOODS',
			'LEVEL 2 - WAY TO NOWHERE',
			'LEVEL 3 - UPSTREAM',
			'LEVEL 4 - DRAIN DAMAGE',
			'LEVEL 5 - RUINED',
			'DEVELOPER TEST LEVEL']

#npc / frame count
npc_anim={'amadillo':7,'turtle':12,'saw_turtle':12,'penguin':15,
		'hedgehog':12,'seal':14,'eating_plant':13,'rat':10,
		'lizard':11,'scrubber':3,'mouse':8,'vulture':13}

bonus_zone_position=[None,(0,-25,-3),(0,-25,-3),(0,-25,-3),(0,-25,-3),(0,-25,-3)]
bonus_checkpoint=[None,(0,2,-7),(0,0,0),(0,0,0),(0,0,0),(0,0,0)]
checkpoint=None
day_mode=''

COLOR_GEM=[]
CLEAR_GEM=[]
CRYSTAL=[]

NPC_RESET=[]
C_RESET=[]
W_RESET=[]

level_index=0

crates_in_level=0
crates_in_bonus=0

collected_crystals=0
player_protect=0
crate_to_sv=0
crate_count=0
extra_lives=4
wumpa_fruits=0
color_gems=0
clear_gems=0

wumpa_bonus=0
crate_bonus=0
lives_bonus=0

show_wumpas=0
show_crates=0
show_lives=0
show_gems=0
c_delay=0
d_delay=0
aku_hit=0

level_crystal=False
level_col_gem=False
level_cle_gem=False

LV_CLEAR_PROCESS=False
level_solved=False
bonus_solved=False
bonus_round=False
LEVEL_CLEAN=False
aku_exist=False
is_dying=False
c_indoor=True
loading=False
pause=False

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