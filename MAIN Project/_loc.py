## lists, arrays and list access

# checkpoint - bonus
bonus_checkpoint=[None,(0,2,-6),(23,6,3.3),(0,2.5,.85*8),(0,2,3),(12,1,-22),(0,1,-25)]

# display the name in pause menu and loading screen
lv_name=['CENTRAL - WARP ROOM',
		'LEVEL 1 - RAINY WOODS',
		'LEVEL 2 - WAY TO NOWHERE',
		'LEVEL 3 - RIVER STREAM',
		'LEVEL 4 - DRAIN DAMAGE',
		'LEVEL 5 - RUINED',
		'DEVELOPER TEST LEVEL']

# crash death actions/animations
dt_act={0:'fall_endl',
		1:'angel',
		2:'water',
		3:'explode',
		4:'burn',
		5:'electric',
		6:'eat_by_plant'}

#day mode
day_m={0:'empty',
	1:'woods',
	2:'snow',
	3:'evening',
	4:'sewer',
	5:'empty',
	6:'empty'}

#2d gem animation
ge_0='res/ui/icon/gem_0/gem'
ge_1='res/ui/icon/gem_1/gem'
ge_2='res/ui/icon/gem_2/gem'
fdc={1:ge_0,2:ge_0,3:ge_0,4:ge_1,5:ge_2,6:ge_0}

#gem color
O=180
cGLO={1:(0,0,O),
	2:(O,0,0),
	5:(O,0,O),
	4:(0,O,0),
	3:(O,O,0),
	6:(O,0,0)}

#triggers
trigger_lst={'indz','lvfi','elwt','fthr'}

#item/obj name list
item_lst={'wmpf','exlf','gems','crys'}

#danger zone
dangers={'wood_log','role','fllz'}

#default speed for move and gravity
dfsp=2.5

#Ambient Light
AMBIENT_LIGHT=None

#LevelScene for Thunderbolts
bgT=None

# color gem
C_GEM=None

#player
ACTOR=None

# shadow
shdw=None

#pause
p_menu=None