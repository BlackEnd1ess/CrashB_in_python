## lists, arrays and list access

#player
ACTOR=None

# display the name in pause menu and loading screen
lv_name=['CENTRAL - WARP ROOM',
		'LEVEL 1 - TURTLE WOODS',
		'LEVEL 2 - WAY TO NOWHERE',
		'LEVEL 3 - UPSTREAM',
		'LEVEL 4 - DRAIN DAMAGE',
		'LEVEL 5 - RUINED',
		'DEVELOPER TEST LEVEL']

# crash death actions/animations
dt_act={0:'fall_endl',1:'angel',2:'water',3:'explode',4:'burn',5:'electric',6:'eat_by_plant'}

#triggers
trigger_lst=['cam_switch','indoor_zone','level_finish','elwt','falling_zone']

#item/obj name list
item_lst=['wumpa_fruit','extra_live','gem_stone','energy_crystal','trial_clock']

#danger zone
d_zone=['water_hit']
dangers=['wood_log','role','falling_zone']

# checkpoint - bonus
bonus_checkpoint=[None,(0,2,-6),(23,6,3.3),(0,1.5,.85*8),(0,2,3),(12,1,-22),(0,1,-25)]

#LOD
LOD_VAR=['rmd1','rmd2','ctsc']
LV1_LOD=LOD_VAR+['bush','tree2_d','tree_scene','t2b1','t2b2','mptf']
LV2_LOD=LOD_VAR+['plank','ice_chunk','wdlg','pillar','icec']
LV3_LOD=LOD_VAR+['wtfa','stone_tile','mptf','bush','tree2_d','stL']
LV4_LOD=LOD_VAR+['sewer_platform','swp2','sewer_pipe','dripping_water']
LV5_LOD=LOD_VAR+['monkey_sculpture','loose_platform','ruins_block','rubl']

#day mode
day_m={0:'empty',
	1:'woods',
	2:'snow',
	3:'evening',
	4:'empty',
	5:'empty',
	6:'empty'}

#LevelScene for Thunderbolts
bgT=None

#ui wumpa position
uiW=None

# shadow
shdw=None

# color gem
C_GEM=None