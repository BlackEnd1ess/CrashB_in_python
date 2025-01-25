import _core,__lv_generator
from ursina import *
cc=camera
##editor control info text
ct_info=f'MOUSE L = PLACE/DELETE OBJECT\nW,A,S,D = MOVE CAM\nU/O = GRID UP/DOWN\nQ/E = ROTATE CAM\nF4 = Delete Map\nF9 = OUTPUT DATA'

##menu text
mde={0:'SPAWN MAP',1:'SPAWN CRATE',2:'SPAWN NPC',3:'SPAWN WUMPA',4:'BONUS PLATFORM',5:'GEM PLATFORM'}
mmt=['MAP OBJECT','BOXES','WUMPA','NPC','BONUS PLATFORM','GEM PLATFORM']

##level name
lv_name='level/level8.py'

##key bindings
inp={'left arrow':	lambda:setattr(cc,'x',cc.x-1),
	'a':			lambda:setattr(cc,'x',cc.x-1),
#------------------------------------------------
	'right arrow':	lambda:setattr(cc,'x',cc.x+1),
	'd':			lambda:setattr(cc,'x',cc.x+1),
#------------------------------------------------
	'up arrow':		lambda:setattr(cc,'z',cc.z+1),
	'w':			lambda:setattr(cc,'z',cc.z+1),
#------------------------------------------------
	'down arrow':	lambda:setattr(cc,'z',cc.z-1),
	's':			lambda:setattr(cc,'z',cc.z-1),
#------------------------------------------------
	'e':			lambda:rotate_cam(0),
	'q':			lambda:rotate_cam(1),
#------------------------------------------------
	'u':			lambda:grid_up_down(m=1),
	'o':			lambda:grid_up_down(m=0),
#------------------------------------------------
	'r':			lambda:reset_cam(),
#------------------------------------------------
	'f4':			lambda:clear_scene(),
	'f9':			lambda:__lv_generator.output_data()}

##npc
NPC={0:'amadillo/0',
	1:'turtle/0',
	2:'saw_turtle/0',
	3:'vulture/0',
	4:'penguin/0',
	5:'hedgehog/0',
	6:'seal/0',
	7:'eating_plant/0',
	8:'rat/0',
	9:'lizard/0',
	10:'scrubber/0',
	11:'mouse/0',
	12:'eel/0',
	13:'sewer_mine/0',
	14:'gorilla/0',
	15:'bee/0',
	16:'lumberjack/0',
	17:'spider_robot_flat/0',
	18:'spider_robot_up/0',
	19:'robot/0',
	20:'lab_assistant/0'}

##map positions
CRATE_DATA=[]
MAP_DATA=[]
NPC_DATA=[]

##grid texture
grid_tex='res/terrain/grid.tga'

##appearance
selected_color=color.azure
grid_color=color.rgb32(100,100,100)
object_alpha=1

##cursor instance
cursor=None

##ID
CRATE_ID=0
OBJ_ID=0
NPC_ID=0

##place mode
pcm=0

##map size
m_size=[16,64]

##block height
bl_height=0

##grid threeshold
grid_trhs=.5

##editor settings/functions
#incrase map grid height
def grid_up_down(m):
	for v in scene.entities[:]:
		if v.name == 'sccb':
			if m == 1:
				v.y+=.5
			else:
				v.y-=.5
	del v,m

#remove all placed objects
def clear_scene():
	for dl in scene.entities[:]:
		if dl.name in {'snpc','block'} or _core.is_crate(dl):
			dl.disable()
			destroy(dl)
	del dl

#camera/window
def set_camera():
	w=window
	w.windowed_size=(1700,900)
	w.exit_button.visible=False
	w.fullscreen=False
	w.borderless=False
	w.color=color.black
	cc.rotation_x=30
	cc.x=m_size[0]/2
	cc.z=-8
	cc.fov=65
	cc.y=8

def reset_cam():
	cc.x=m_size[0]/2
	cc.z=-8
	cc.fov=65
	cc.rotation_y=0
	cc.y=8

def rotate_cam(drc):
	if drc == 0:
		cc.rotation_y-=90
		cc.x=21
		cc.z=m_size[1]/8
		return
	cc.rotation_y+=90
	cc.x=-21
	cc.z=m_size[1]/8