from ursina.shaders import *
import _core,environment
from ursina import *

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
	cam()

def cam():
	environment.init_amb_light()
	camera.rotation_x=15
	camera.fov=60
	print('default settings loaded')

MUSIC_VOLUME=0
SFX_VOLUME=0
#----------------------------
#camera_contrast_shader
#camera_vertical_blur_shader
#camera_grayscale_shader
#lit_with_shadows_shader
#ssao_shader
#colored_lights_shader
#matcap_shader
#unlit_shader