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

# crash death actions/animations
dt_act={0:'fall_endl',1:'angel',2:'water',3:'explode',4:'burn',5:'electric',6:'eat_by_plant'}

#item/obj name list
item_lst=['wumpa_fruit','extra_live','gem_stone','energy_crystal','trial_clock','cam_switch','indoor_zone','level_finish','elwt']

#danger zone
d_zone=['water_hit','falling_zone']
dangers=['wood_log','role']

# checkpoint - bonus
bonus_checkpoint=[None,(0,2,-6),(.3,2,2.3),(0,1.5,.85*8),(0,2,3),(0,5,0)]

#LOD
LOD_VAR=['rmd1','rmd2','ctsc']
LV1_LOD=LOD_VAR+['bush','tree2_d','tree_scene','t2b1','t2b2','mptf']
LV2_LOD=LOD_VAR+['plank','ice_chunk','wdlg','pillar','icec']
LV3_LOD=LOD_VAR+['wtfa','stone_tile','mptf','bush','tree2_d','stL']
LV4_LOD=LOD_VAR+['sewer_platform','swp2','sewer_pipe','dripping_water']
#LV5_LOD=LOD_VAR+['water_fall']

#day mode
day_m={0:'default',
	1:'woods',
	2:'snow',
	3:'evening',
	4:'pipe',
	5:'pipe'}

#ui wumpa position
uiW=None

# shadow
shdw=None

# color gem
C_GEM=None