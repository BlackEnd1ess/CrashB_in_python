import settings,level,warproom
from ursina import *

app=Ursina(title='Crash Bandicoot',icon='res/cb.ico',vsync=False)
def game():
	settings.load()
	warproom.level_select()
	#level.main_instance(5)
game()
app.run()