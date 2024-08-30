from ursina.shaders import *
from ursina import *
import _core,ui

debg=True
w=window
def load():
	w.windowed_size=(1600,900)
	w.render_mode='default'
	w.exit_button.visible=False
	##debug infos
	w.collider_counter.enabled=debg
	w.entity_counter.enabled=debg
	w.fps_counter.enabled=debg
	w.cog_button.enabled=debg
	##
	w.fullscreen=False
	w.borderless=False
	ui.LoadingScreen()
	cam()

def cam():
	camera.rotation_x=15
	camera.fov=60
	print('settings loaded')

MUSIC_VOLUME=1
SFX_VOLUME=1
#----------------------------
#camera_contrast_shader
#camera_vertical_blur_shader
#camera_grayscale_shader
#lit_with_shadows_shader
#ssao_shader
#colored_lights_shader
#matcap_shader
#unlit_shader