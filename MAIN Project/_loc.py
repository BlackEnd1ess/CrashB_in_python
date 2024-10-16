## lists, arrays and list access

#player
ACTOR=None

#default speed for move and gravity
dfsp=2.5

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
trigger_lst=['indz','lvfi','elwt','fthr']

#item/obj name list
item_lst=['wmpf','exlf','gems','crys']

#danger zone
dangers=['wood_log','role','fllz']

#fog far values
fog_distance={
	0:100,
	1:14,
	2:14,
	3:16,
	4:15,
	5:16,
	6:30}

# checkpoint - bonus
bonus_checkpoint=[None,(0,2,-6),(23,6,3.3),(0,2.5,.85*8),(0,2,3),(12,1,-22),(0,1,-25)]

#LOD
LOD_VAR=['rmd1','rmd2','ctsc']
LV1_LOD=LOD_VAR+['bush','trd2','tssn','mptf']
LV2_LOD=LOD_VAR+['plnk','ickk','wdlg','pilr','icec']
LV3_LOD=LOD_VAR+['wtfa','mptf','bush','trd2','tile','foam']
LV4_LOD=LOD_VAR+['swpl','swp2','swpi','drpw','ssww']
LV5_LOD=LOD_VAR+['mnks','loos','rnsp','rubl','rncr']

#day mode
day_m={0:'empty',
	1:'woods',
	2:'snow',
	3:'evening',
	4:'sewer',
	5:'empty',
	6:'empty'}

#Ambient Light
AMBIENT_LIGHT=None

#LevelScene for Thunderbolts
bgT=None

# shadow
shdw=None

# color gem
C_GEM=None