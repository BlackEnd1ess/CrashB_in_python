## lists, arrays and list access

#player
ACTOR=None

# display the name in pause menu
lv_name=['Warp Room',
		'LEVEL 1 - TURTLE WOODS',
		'LEVEL 2 - WAY TO NOWHERE',
		'LEVEL 3 - UPSTREAM',
		'LEVEL 4 - DRAIN DAMAGE',
		'LEVEL 5 - RUINED',
		'DEVELOPER TEST LEVEL']

#item name list
item_lst=['wumpa_fruit','extra_live','gem_stone','energy_crystal','trial_clock','cam_switch']
free_cam=['t2b1','t2b2','t2b3','bush','tree_2d','tree_scene','STpltf','room_door','door_part']

# objects in this list will hidden by LOD
w_fruits=[]
LOD_LST=[]

#danger zone
d_zone=['water_hit','falling_zone']
dangers=['wood_log','role']

# checkpoint - bonus
bonus_checkpoint=[None,(0,2,-6),(.3,2,2.3),(0,1.5,.85*8),(0,5,0),(0,5,0)]

#day mode
day_m={0:'default',
	1:'woods',
	2:'snow',
	3:'evening',
	4:'pipe',
	5:'day'}

#ui wumpa position
uiW=None

# shadow
shdw=None

# color gem
C_GEM=None

# map terrain
map_height=None
map_zone=None