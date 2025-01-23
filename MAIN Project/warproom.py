from ursina import Audio,Text,Entity,camera,scene,color,invoke
import status,_loc,level,sound,settings,ui,_core,objects,time
cu=camera.ui
st=status
sn=sound

mc='res/ui/icon/memcard.png'
fn='res/ui/font.ttf'
q='quad'
class Memorycard(Entity):
	def __init__(self):
		s=self
		super().__init__(model=q,texture=mc,position=(.6,.24),scale=(.07,.1),parent=camera.ui)
		s.desc_s=Text('Save Game - F2',font=fn,scale=1.5,position=(s.x-.1,s.y-.07,s.z),color=color.green,parent=cu)
		s.desc_l=Text('Load Game - F3',font=fn,scale=1.5,position=(s.x-.1,s.y-.12,s.z),color=color.azure,parent=cu)

class BonusRoomEntry(Entity):
	def __init__(self):
		s=self
		super().__init__()
		mtt='WARP ROOM E2 - F1'
		if st.bonus_warp_room:
			mtt='WARP ROOM E1 - F1'
		s.desc_w=Text(mtt,font=fn,scale=2,position=(-.55,-.45,0),color=color.magenta,parent=cu)
		s.tme=.3
	def update(self):
		s=self
		s.tme=max(s.tme-time.dt,0)
		if s.tme <= 0:
			s.tme=.3
			if s.desc_w.color == color.white:
				s.desc_w.color=color.magenta
				return
			s.desc_w.color=color.white

class LvSelect(Entity):
	def __init__(self):
		super().__init__()
		self.bgm=Audio('res/snd/music/level/wroom.mp3',volume=settings.MUSIC_VOLUME,loop=True)
	def input(self,key):
		if key in settings.BCK_KEY:
			sn.ui_audio(ID=0,pit=.125)
			if st.bonus_warp_room:
				if st.selected_level < 8:
					st.selected_level+=1
			else:
				if st.selected_level < 5:
					st.selected_level+=1
			return
		if key == settings.FWD_KEY:
			sn.ui_audio(ID=0,pit=.125)
			if st.bonus_warp_room:
				if st.selected_level > 6:
					st.selected_level-=1
			else:
				if st.selected_level > 1:
					st.selected_level-=1
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
		if key == 'f1' and st.collected_crystals >= 5:
			sn.ui_audio(ID=1)
			if st.bonus_warp_room:
				st.bonus_warp_room=False
				st.selected_level=0
			else:
				st.bonus_warp_room=True
				st.selected_level=6
			scene.clear()
			level_select()
			return
		if key == 'enter':
			sn.ui_audio(ID=1)
			scene.clear()
			st.level_index=st.selected_level
			st.loading=True
			level.main_instance(st.selected_level)

class Credits(Entity):
	def __init__(self):
		s=self
		st.loading=False
		super().__init__(model='quad',texture='res/background/wroom.png',scale=(32,20),z=4,color=color.rgb32(100,150,100))
		s.bgm=Audio('res/snd/music/credits.mp3',loop=True,volume=settings.MUSIC_VOLUME)
		objects.PseudoCrash()
		s.index=0
		s.t0()
	def t0(self):
		s=self
		crd_text0=[
		'Congratulation!',
		'you have finished this Game!',
		'Thanks for playing it!']
		for v in crd_text0:
			s.index+=1
			ui.CreditText(t=v,d=s.index)
		s.index=0
		invoke(s.t1,delay=4)
	def t1(self):
		s=self
		crd_text1=[
		'This game is a inofficial and crash bandicoot',
		'inspired fan game! all resources, sounds, models and',
		'textures are made by sony computer entertainment',
		'presents, naughty dog! this project is full free and',
		'open source aviable on github.',
		'https://github.com/BlackEnd1ess/CrashB_in_python',
		'',
		'please support the orginal games on PS4,PS5,XBOX,PC:',
		'- crash bandicoot nsane trilogy',
		'- crash team racing nitro fueled',
		'- crash bandicoot 4 its about time',
		'- crash team rumble']
		for v in crd_text1:
			s.index+=1
			ui.CreditText(t=v,d=s.index)
		s.index=0
		invoke(s.t2,delay=10)
	def t2(self):
		s=self
		crd_text2=[
		'but I wouldnt have gotten this far without help!',
		'big Thanks to:',
		'',
		'- youtube and all crash bandicoot fans and comunities',
		'- warenhuis, cbhacks and crash modding comunities',
		'- chatgpt, github and reddit',
		'- sony computer naughty dog: for this game!',
		'- all my watchers on youtube',
		'- janis for testing my game']
		for v in crd_text2:
			s.index+=1
			ui.CreditText(t=v,d=s.index)
		s.index=0
		invoke(s.t3,delay=6)
	def t3(self):
		s=self
		crd_text3=[
		'in comming future i will work with a new',
		'game engine. i will choose unity and i will',
		'create more professional assets and resources.',
		'all physics and dynamics will work cleaner and faster.',
		'and we will have better mechanics like particle systems,',
		'pathfinding, professional LOD and better collisions.'
		'',
		'crash will returning back!']
		for v in crd_text3:
			s.index+=1
			ui.CreditText(t=v,d=s.index)
		s.index=0
		invoke(level_select,delay=16)

def level_select():
	scene.clear()
	st.LV_CLEAR_PROCESS=False
	st.level_index=0
	camera.position=(0,0,-20)
	camera.rotation=(0,0,0)
	scene.fog_color=color.gray
	scene.fog_density=(100,200)
	if st.collected_crystals >= 5:
		if not st.crd_seen:
			st.crd_seen=True
			Credits()
			return
		BonusRoomEntry()
	objects.PseudoCrash()
	Memorycard()
	LvSelect()
	if st.bonus_warp_room:
		for lvs in {6,7,8}:
			ui.SpecialLevelSelector(idx=lvs,pos=(-.8,1.2-lvs/6))
	else:
		for lvs in {1,2,3,4,5}:
			ui.LevelSelector(idx=lvs,pos=(-.8,.5-lvs/6))
	st.loading=False