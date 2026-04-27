## lists, arrays and list access
from ursina import color
c=color

#checkpoint - bonus
bonus_checkp={
	0:None,#			#sel menu
	1:(0,2,-6),#		#level 1
	2:(23,6,3.3),#		#level 2
	3:(0,2.5,.85*8),#	#level 3
	4:(0,2,3),#			#level 4
	5:(12,1.3,-22),#	#level 5
	6:(9,5,20),#		#level 6
	7:(26,5,-36),#		#level 7
	8:(34,6,60.5)}#		#level 8

#time trial clock position
CLOCK_POSITION={0:(0,0,0),
				1:(.3,1.25,-57),
				2:(.9,1.25,-57.4),
				3:(.6,.5,-21.6),
				4:(.6,.75,-57.7),
				5:(5.3,.5,-55.5),
				6:(.4,.3,-60.6),
				7:(-1,.3,-59),
				8:(7.6,.8,7.7),
				9:(-1.75,.3,7)}

##LV_INDEX:(platinum, gold, saphire)
RELIC_TIME_LIMIT_LEVEL={
	1:(35,40,50),#ok
	2:(45,50,60),#ok
	3:(25,30,45),#ok
	4:(35,45,55),#ok
	5:(50,55,60),#ok
	6:(25,30,40),#ok
	7:(45,50,55),#ok
	8:(40,45,55),#ok
	9:(10,15,20)}#test

#display the name in pause menu and loading screen
lv_name=['CENTRAL - WARP ROOM',
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

#splash water entity
splash_entity='splash_wtr'

#render culling distance
RCX=0#x pos
RCZ=0#z pos
RCB=0#back dst

#2d gem animation
relic='res/ui/icon/relic/'
ge_0='res/ui/icon/gem0/'
ge_1='res/ui/icon/gem1/'
ge_2='res/ui/icon/gem2/'

#relic color
relic_color={0:color.light_gray,1:color.gold,2:color.azure}

#gem ui color
ui_crystal_color=c.rgb32(170,0,170)
ui_normal_gem_color=c.rgb32(220,220,230)

ui_red_gem_color=c.rgb32(180,50,50)
ui_green_gem_color=c.rgb32(0,160,0)
ui_purple_gem_color=c.rgb32(160,0,160)
ui_blue_gem_color=c.rgb32(0,0,160)
ui_yellow_gem_color=c.rgb32(160,160,0)

#gem model color
mesh_normal_gem_color=c.rgb32(160,160,160)
mesh_red_gem_color=c.rgb32(255,50,50)
mesh_green_gem_color=c.rgb32(0,160,0)
mesh_purple_gem_color=c.rgb32(140,0,140)
mesh_blue_gem_color=c.rgb32(0,0,150)
mesh_yellow_gem_color=c.rgb32(150,150,0)

GEM_MESH_COLOR={1:mesh_blue_gem_color,2:mesh_red_gem_color,3:mesh_yellow_gem_color,4:mesh_green_gem_color,5:mesh_purple_gem_color}
GEM_PLATFORM_COLOR={1:color.rgb32(0,0,130),2:color.rgb32(130,0,0),3:color.rgb32(130,130,0),4:color.rgb32(0,130,0),5:color.violet}

#fog dst/color/dst
SKY_BG_COLOR=None
AMB_M_COLOR=None
FOG_L_COLOR=None
FOG_B_COLOR=None
LV_DST=None
BN_DST=None

#gem podium position
gem_pod_position=(0,-120,0)

#level fin
lv_fin_pos=(0,0,0)

NPC_SND_DISTANCE=8
NPC_FLY_SPEED=40

#lab taser height
ltth=1.7

#lv6 mine position
LDM_POS=[]

#triggers
trigger_lst={'indz','lvfi','elwt','fthr','eball'}

#item/obj name list
item_lst={'wmpf','exlf','gem','crys','clock','relic'}

#danger zone
dangers={'wood_log','role','fllz','piston'}

#gem interface frames
GEM_MAX_FRM=150.99

#default speed for move and gravity
dfsp=2.6

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

#shadow and player collision
IGNORE=[]

#preloading textures
wmp_texture=[]
box_texture=[]

crystal_texture=[]
normal_gem_texture=[]
green_gem_texture=[]
purple_gem_texture=[]
relic_texture=[]

#water effect texture
wtr_texture=[]
wtf_texture=[]
wff_texture=[]
drp_texture=[]
fre_texture=[]