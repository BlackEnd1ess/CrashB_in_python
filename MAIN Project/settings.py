from ursina import color,window,camera
from ursina.ursinastuff import destroy
import environment

## debug options
debg_color=color.rgb32(180,180,180)
debg=True

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
MUSIC_VOLUME=1
SFX_VOLUME=1

## window
def load():
	w=window
	w.windowed_size=(1600,900)
	w.exit_button.visible=False
	w.fullscreen=False
	w.borderless=False
	w.cog_menu.eternal=False
	w.cog_menu.force_destroy=True
	w.fps_counter.enabled=False
	##debug info
	w.collider_counter.enabled=debg
	w.entity_counter.enabled=debg
	w.color=color.black
	camera.fov=65
	environment.init_amb_light()
	destroy(w.cog_menu)
	print('default settings loaded')