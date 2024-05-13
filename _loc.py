## lists, arrays and list access

# display the name in pause menu
lv_name=['Warp Room',
		'LEVEL 1 - TURTLE WOODS',
		'LEVEL 2 - WAY TO NOWHERE',
		'LEVEL 3 - UPSTREAM',
		'LEVEL 4 - DRAIN DAMAGE',
		'LEVEL 5 - RUINED',
		'DEVELOPER TEST LEVEL']

#item name list
item_lst=['wumpa_fruit','extra_live','gem_stone','energy_crystal','trial_clock']

# objects in this list will hidden by LOD in _core.py
free_fv=['start_room','bush','t2b1','t2b2','t2b3','tree_scene','pillow','door_part','room_door']
LOD_LST=['tree2_d','tree_scene','bush','pillar','rock','moss_platform']

#danger zone
dangers=['water_hit','falling_zone']

# checkpoint - bonus
bonus_checkpoint=[None,(0,2,-6),(.3,2,2.3),(0,4,.85*8),(0,5,0),(0,5,0)]

#day mode
day_m={0:'default',1:'woods',2:'snow',3:'evening',4:'night',5:'night'}

# shadow
shdw=None

#hitbox dummy
htBOX=None

# map terrain
map_height=None
map_zone=None