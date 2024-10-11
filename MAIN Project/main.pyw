from ursina import *
import settings,ui

app=Ursina(title='Crezsh Blendikut',icon='res/cb.ico',development_mode=False)
def game():
	settings.load()
	ui.ProjectInfo()
	#dev_start(6)

#def dev_start(idx):
#	import status,level
#	ui.LoadingScreen()
#	status.level_index=idx
#	level.main_instance(idx)
game()
app.run()