import settings,level
from ursina import *

app=Ursina(title='Crash Bandicoot',icon='res/cb.ico')
application.time_scale=1

def start_game():
	settings.load()
	level.main_instance(1)
start_game()
app.run()