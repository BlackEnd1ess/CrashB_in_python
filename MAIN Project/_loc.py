## lists, arrays and list access
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

#triggers
trigger_lst={'indz','lvfi','elwt','fthr'}

#item/obj name list
item_lst={'wmpf','exlf','gems','crys'}

#danger zone
dangers={'wood_log','role','fllz'}

# checkpoint - bonus
bonus_checkpoint=[None,(0,2,-6),(23,6,3.3),(0,2.5,.85*8),(0,2,3),(12,1,-22),(0,1,-25)]

#day mode
day_m={0:'empty',
	1:'woods',
	2:'snow',
	3:'evening',
	4:'sewer',
	5:'empty',
	6:'empty'}