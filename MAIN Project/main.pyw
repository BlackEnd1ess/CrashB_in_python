from ursina import Ursina
import settings,ui

app=Ursina(title='Cresh B',icon='res/cb.ico')
def game():
	settings.load()
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
	level.main_instance(idx)
	del idx

game()
app.run()