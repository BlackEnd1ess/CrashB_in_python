import settings,level
from ursina import *

app=Ursina(title='Crash Bandicoot',icon='res/cb.ico')
application.time_scale=.95
def start_game():
	settings.load()
	level.main_instance(3)
start_game()
app.run()