from ursina import Ursina
import settings,ui,sys

sys.dont_write_bytecode=True

app=Ursina(title='Cresh B - Retro Treveler',icon='res/cb.ico')
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
	if idx == 0:
		ui.TitleScreen()
	else:
		level.main_instance(idx)
	del idx

game()
app.run()