import settings,ui,status,level
from ursina import Ursina

app=Ursina(title='Cresh B',icon='res/cb.ico',asset_folder='res/',vsync=True)
def game():
	settings.load()
	if settings.debg:
		print('SELECT LEVEL: type level number')
		iv=input('')
		dev_start(int(iv))
		return
	ui.ProjectInfo()

def dev_start(idx):
	ui.LoadingScreen()
	status.level_index=idx
	level.main_instance(idx)
game()
app.run()