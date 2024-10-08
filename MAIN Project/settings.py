from ursina.shaders import *
import _core,environment,os
from ursina import *

debg=True

## keyboard bindings
MNU_KEY='p'#pause
JMP_KEY='space'#jump
ATK_KEY='alt'#attack
IFC_KEY='tab'#show interface
BLY_KEY='v'#belly smash
FWD_KEY='w'#'up arrow'#forward
BCK_KEY='s'#'down arrow'#backward
RGT_KEY='d'#'right arrow'#right
LFT_KEY='a'#'left arrow'#left

## global volume
MUSIC_VOLUME=1
SFX_VOLUME=1

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