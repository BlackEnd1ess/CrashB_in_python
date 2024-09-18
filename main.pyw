import settings,warproom,ui
from ursina import *

app=Ursina(title='Crash Bandicoot',icon='res/cb.ico',vsync=False)
def game():
	settings.load()
	ui.LoadingScreen()
	warproom.level_select()
game()
app.run()