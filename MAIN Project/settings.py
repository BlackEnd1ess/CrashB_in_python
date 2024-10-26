from ursina.shaders import *
import environment,os
from ursina import *

## debug options
debg_color=color.rgb32(255,128,0)
debg=False

## keyboard bindings
MNU_KEY='p'#		pause
JMP_KEY='space'#	jump
ATK_KEY='alt'#		attack
IFC_KEY='tab'#		show interface
BLY_KEY='v'#		belly smash
FWD_KEY='w'#		forward
BCK_KEY='s'#		backward
RGT_KEY='d'#		right
LFT_KEY='a'#		left

DEV_WARP='u'#		dev warp
DEV_INFO='b'#		map tools info
DEV_ECAM='e'#		edior camera


## global volume
MUSIC_VOLUME=.5
SFX_VOLUME=.5

## window
def load():
	w=window
	os.system('cls')
	w.windowed_size=(1600,900)
	w.render_mode='default'
	w.exit_button.visible=False
	##debug infos
	w.collider_counter.enabled=debg
	w.entity_counter.enabled=debg
	w.fps_counter.enabled=debg
	w.cog_button.enabled=debg
	w.fullscreen=False
	w.borderless=False
	camera.fov=65
	environment.init_amb_light()
	print('default settings loaded')