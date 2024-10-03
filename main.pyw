import settings,ui
from ursina import *

app=Ursina(title='Crash Bandicoot',icon='res/cb.ico',vsync=False)
def game():
	settings.load()
	#ui.ProjectInfo()
	dev_start(2)

def dev_start(idx):
	import status,level
	ui.LoadingScreen()
	status.level_index=idx
	level.main_instance(idx)
game()
app.run()