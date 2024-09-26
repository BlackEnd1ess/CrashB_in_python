import status,_loc,level,sound,settings,ui,_core
from ursina import *
st=status
sn=sound

class LvSelect(Entity):
	def __init__(self):
		super().__init__()
		self.bgm=Audio('res/snd/music/ev/wroom.mp3',volume=settings.MUSIC_VOLUME,loop=True)
	def input(self,key):
		if key == 's' and st.selected_level < 5:
			st.selected_level+=1
			sn.ui_audio(ID=0,pit=.125)
			return
		if key == 'w' and st.selected_level > 1:
			st.selected_level-=1
			sn.ui_audio(ID=0,pit=.125)
			return
		if key == 'f2':
			sn.ui_audio(ID=1)
			_core.save_game()
			return
		if key == 'f3':
			sn.ui_audio(ID=1)
			_core.load_game()
			scene.clear()
			ui.BlackScreen()
			level_select()
			return
		if key == 'enter':
			sn.ui_audio(ID=1)
			scene.clear()
			st.level_index=st.selected_level
			st.loading=True
			level.main_instance(st.selected_level)

def level_select():
	st.LV_CLEAR_PROCESS=False
	st.level_index=0
	Entity(model='quad',texture='res/background/wroom.png',scale=(2,1),parent=camera.ui,color=color.rgb32(140,160,140),position=(0,0,2))
	LvSelect()
	for lvs in [1,2,3,4,5]:
		ui.LevelInfo(idx=lvs,pos=(-.8,.5-lvs/6))
	st.loading=False