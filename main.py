import settings,level
from ursina import *

app=Ursina(title='Crash Bandicoot',icon='res/cb.ico')
def start_game():
	settings.load()
	level.level2()
start_game()
app.run()