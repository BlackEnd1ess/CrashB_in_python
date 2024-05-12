import settings,level
from ursina import *

app=Ursina(title='Crash Bandicoot',icon='res/cb.ico')
application.development_mode=False
application.print_warnings=False
application.print_info=None
application.time_scale=.98

def start_game():
	settings.load()
	level.main_instance(1)
start_game()
app.run()