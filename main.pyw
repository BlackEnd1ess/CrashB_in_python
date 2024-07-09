import settings,level
from ursina import *

app=Ursina(title='Crash Bandicoot',icon='res/cb.ico',vsync=False)
def game():
	settings.load()
	level.main_instance(4)
game()
app.run()