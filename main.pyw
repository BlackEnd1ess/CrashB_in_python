import settings,warproom,ui
from ursina import *

app=Ursina(title='Crash Bandicoot',icon='res/cb.ico',vsync=False)
def game():
	settings.load()
	ui.LoadingScreen()
	#warproom.level_select()
	dev_start(6)

def dev_start(idx):
	import status,level
	status.level_index=idx
	level.main_instance(idx)
game()
app.run()