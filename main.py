import settings,level
from ursina import *

app=Ursina(title='Crash Bandicoot',icon='res/cb.ico')
application.compressed_models_folder=None
application.time_scale=.97

def start_game():
	settings.load()
	level.main_instance(3)
start_game()
app.run()