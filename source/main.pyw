from _core import preload_ui_texture,preload_box_texture,preload_object_animation,preload_player_animation
from panda3d.core import loadPrcFileData
import settings,ui,sys,_debug_
from ursina import Ursina

sys.dont_write_bytecode=True
loadPrcFileData('','model-cache-dir ')
loadPrcFileData('','model-cache-textures 0')

app=Ursina(title='Cresh B - Retro Treveler v1.6',icon='res/cb.ico')
def game():
	#_debug_.COUNT_ENGINE_READ_FILE(typ=1)
	settings.load()
	preload_player_animation()
	preload_object_animation()
	preload_box_texture()
	preload_ui_texture()
	if settings.debg:
		print('SELECT LEVEL: type level number')
		iv=input('')
		dev_start(int(iv))
		del iv
		return
	ui.ProjectInfo()

def dev_start(idx):
	import status,level
	ui.LoadingScreen()
	status.level_index=idx
	if idx == 0:
		ui.TitleScreen()
		return
	level.load(idx)

game()
app.run()