import settings,level
from ursina import *

app=Ursina(title='Crash Bandicoot',icon='res/cb.ico')
application.time_scale=.98

def start_game():
	settings.load()
	level.main_instance(4)
start_game()
app.run()