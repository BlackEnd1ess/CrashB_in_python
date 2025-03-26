## lists, arrays and list access
from ursina import color
c=color
#checkpoint - bonus
bonus_checkpoint=[None,(0,2,-6),(23,6,3.3),(0,2.5,.85*8),(0,2,3),(12,1,-22),(9,5,20),(26,5,-36),(34,6,60.5)]

#display the name in pause menu and loading screen
lv_name=[
	'CENTRAL - WARP ROOM',
	'LEVEL 1 - RAINY WOODS',
	'LEVEL 2 - WAY TO NOWHERE',
	'LEVEL 3 - RIVER STREAM',
	'LEVEL 4 - DRAIN DAMAGE',
	'LEVEL 5 - RUINED',
	'LEVEL 6 - TOTALLY BEE',
	'LEVEL 7 - PISTON PUSH',
	'LEVEL 8 - POLAR LIGHTS',
	'DEVELOPER TEST LEVEL']

#gem box info
ge_inf={0:'this is a developer test level, place the gem where you want',
		1:'blue gem - reach the end of this level without breaking boxes',
		2:'red gem - solve this level without loosing extra lifes.',
		3:'yellow gem - reach the end of level before time up',
		4:'green gem - unlock the yellow gem path',
		5:'purple gem - unlock the green gem path'}

#warp room bg
wrbg='res/background/warp_room.png'

#crash default texture
ctx='res/pc/crash'

#render culling distance
RCX=0#x pos
RCZ=0#z pos
RCB=0#back dst

#2d gem animation
ge_0='res/ui/icon/gem_0/gem'
ge_1='res/ui/icon/gem_1/gem'
ge_2='res/ui/icon/gem_2/gem'
fdc={1:ge_0,2:ge_0,3:ge_0,4:ge_1,5:ge_2,6:ge_0,7:ge_0,8:ge_0}

#gem ui color
O=180
cglr=c.rgb32(O,O,O)#clear gem
GMU={1:c.rgb32(0,0,O),#blue
	2:c.rgb32(O,0,0),#red
	3:c.rgb32(O,O,0),#violet
	4:c.rgb32(0,O,0),#green
	5:c.rgb32(O,0,O),#yellow
	6:cglr,#clear
	7:cglr,
	8:cglr}#clear

#gem color
GMC={0:cglr,
	1:c.rgb32(O,0,0),
	2:c.rgb32(0,O,0),
	3:c.rgb32(O,0,O),
	4:c.rgb32(0,0,O),
	5:c.rgb32(O,O,0),
	6:cglr,
	7:cglr,
	8:cglr}

#crate break animation color
cbrc={3:c.rgb32(140,70,0),
	11:c.rgb32(190,0,0),
	12:c.rgb32(0,190,0),
	16:c.rgb32(160,0,160)}

#fog dst/color/dst
SKY_BG_COLOR=None
AMB_M_COLOR=None
FOG_L_COLOR=None
FOG_B_COLOR=None
LV_DST=None
BN_DST=None

#lab taser height
ltth=1.7

#lv6 mine position
LDM_POS=[]

#triggers
trigger_lst={'indz','lvfi','elwt','fthr','eball'}

#item/obj name list
item_lst={'wmpf','exlf','gems','crys'}

#danger zone
dangers={'wood_log','role','fllz','piston'}

#default speed for move and gravity
dfsp=2.5

#Ambient Light
AMBIENT_LIGHT=None

#Lv 5 Level Background for Thunderbolt
bgT=None

#color gem
C_GEM=None

#player
ACTOR=None

#shadow
shdw=None

#pause
p_menu=None