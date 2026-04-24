from _core import preload_ui_texture,preload_animator
from panda3d.core import loadPrcFileData
from ursina import Ursina
import settings,ui,sys

sys.dont_write_bytecode=True

loadPrcFileData('','model-cache-dir ')
loadPrcFileData('','model-cache-textures 0')

app=Ursina(title='Cresh B - Retro Treveler v1.3',icon='res/cb.ico')
def game():
	settings.load()
	preload_ui_texture()
	preload_animator()
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