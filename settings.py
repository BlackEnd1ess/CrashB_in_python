from ursina.shaders import *
from ursina import *
import _core,ui

w=window
def load():
	w.windowed_size=(1600,900)
	w.render_mode='default'
	w.exit_button.visible=False
	w.fps_counter.enabled=True
	w.fullscreen=False
	w.borderless=False
	ui.LoadingScreen()
	cam()

def cam():
	camera.rotation_x=15
	camera.fov=65
	camera.y=1.2
	print('settings loaded')
	#camera.shader=ssao_shader

SFX_VOLUME=1
MUSIC_VOLUME=1

#----------------------------
#camera_contrast_shader
#camera_vertical_blur_shader
#camera_grayscale_shader
#lit_with_shadows_shader
#ssao_shader
#colored_lights_shader
#matcap_shader
#unlit_shader