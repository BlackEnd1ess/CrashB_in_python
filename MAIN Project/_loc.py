## lists, arrays and list access
from ursina import color
import crate as C
import npc as N

#checkpoint - bonus
bonus_checkpoint=[None,(0,2,-6),(23,6,3.3),(0,2.5,.85*8),(0,2,3),(12,1,-22),(9,5,20),(26,5,-36),(0,0,0)]

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
	'LEVEL 8 - ?????? ?????',
	'DEVELOPER TEST LEVEL']

#gem box info
ge_inf={0:'this is a developer test level, place the gem where you want',
		1:'blue gem - reach the end of this level without breaking boxes',
		2:'red gem - solve this level without loosing extra lifes.',
		3:'yellow gem - reach the end of level before time up',
		4:'green gem - unlock the yellow gem path',
		5:'purple gem - unlock the green gem path'}

#2d gem animation
ge_0='res/ui/icon/gem_0/gem'
ge_1='res/ui/icon/gem_1/gem'
ge_2='res/ui/icon/gem_2/gem'
fdc={1:ge_0,2:ge_0,3:ge_0,4:ge_1,5:ge_2,6:ge_0,7:ge_0,8:ge_0}

#gem ui color
O=180
cglr=color.rgb32(O,O,O)#clear gem
GMU={1:color.rgb32(0,0,O),#blue
	2:color.rgb32(O,0,0),#red
	3:color.rgb32(O,O,0),#violet
	4:color.rgb32(0,O,0),#green
	5:color.rgb32(O,0,O),#yellow
	6:cglr,#clear
	7:cglr,
	8:cglr}#clear

#gem color
GMC={0:cglr,
	1:color.rgb32(O,0,0),
	2:color.rgb32(0,O,0),
	3:color.rgb32(O,0,O),
	4:color.rgb32(0,0,O),
	5:color.rgb32(O,O,0),
	6:cglr,
	7:cglr,
	8:cglr}

#is crate
CCK={C.Iron,C.Normal,C.QuestionMark,C.Bounce,C.ExtraLife,
	C.AkuAku,C.Checkpoint,C.SpringWood,C.SpringIron,C.SwitchEmpty,
	C.SwitchNitro,C.TNT,C.Nitro,C.Air,C.Protected,C.LvInfo}

#is npc
NCC={N.Amadillo,N.Turtle,N.SawTurtle,
	N.Penguin,N.Hedgehog,N.Seal,
	N.EatingPlant,
	N.Eel,N.Scrubber,N.Mouse,N.SewerMine,
	N.Gorilla,N.Rat,N.Lizard,
	N.Bee,N.Lumberjack,
	N.SpiderRobotFlat,N.SpiderRobotUp,N.Robot,N.LabAssistant}

#fog dst
LV_DST=None
BN_DST=None

#lab taser height
ltth=1.7

#lv6 mine position
LDM_POS=[]
#triggers
trigger_lst={'indz','lvfi','elwt','fthr'}

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