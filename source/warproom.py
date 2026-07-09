import status,_loc,level,sound,settings,ui,_core,objects,time,gc
from ursina import Audio,Text,Entity,camera,scene,color,invoke
from objects import ObjType_Background,ObjType_Deco
from ursina.ursinastuff import destroy
from ursina import window

cu=camera.ui
st=status
sn=sound
LC=_loc

wrbg='res/background/warp_room.png'
icb='res/ui/misc/icon_box.png'
mc='res/ui/icon/memcard.png'
ivy_='res/ui/misc/ivy'
fn='res/ui/font.ttf'
q='quad'

ivc=.2

class LevelSelector(Entity):
	def __init__(self,typ):
		super().__init__()
		self.typ=typ
		if typ == 0:
			self.default_room()
			return
		self.special_room()
	def default_room(self):
		s=self
		set_warproom_scene(s.typ)
		for lvd in (1,2,3,4,5):
			ui.LevelName(pos=(-.85,.45-lvd/7),idx=lvd)
			if lvd in st.CRYSTAL:
				ui.UICrystal((-1.4,6.6-lvd*2.2,2),0)
			if lvd in st.CLEAR_GEM:
				ui.UINormalGem((-3.85,6.6-lvd*2.2,2),0)
			if lvd in st.COLOR_GEM:
				ui.UIColorGem((1,6.6-lvd*2.2,2),0,lvd)
			for lpr in st.RELIC:
				if lvd == lpr[0]:
					ui.UIRelic((3.5,6.6-lvd*2.2,2),0,lpr[1])
		for iwx in range(4):
			for iwy in range(5):
				Entity(model=q,texture=icb,position=(-4+iwx*2.5,4.5-iwy*2.25,2.5),scale=2.5,color=color.rgb32(80,100,80),unlit=False)
	def special_room(self):
		s=self
		set_warproom_scene(s.typ)
		for lvd in (6,7,8):
			ui.LevelName(pos=(-.85,1.1-lvd/7),idx=lvd)
			if lvd in st.CLEAR_GEM:
				ui.UINormalGem((-4.2,16.5-lvd*2.2,2),0)
			if lvd in st.COLOR_GEM:
				ui.UINormalGem((-1.75,16.5-lvd*2.2,2),0)
			for lpr in st.RELIC:
				if lvd == lpr[0]:
					ui.UIRelic((.75,16.5-lvd*2.2,2),0,lpr[1])
		for iwx in range(3):
			for iwy in range(3):
				Entity(model=q,texture=icb,position=(-4.3+iwx*2.5,3.5-iwy*2.25,2.5),scale=2.5,color=color.rgb32(80,100,80),unlit=False)

class Memorycard(Entity):
	def __init__(self):
		s=self
		super().__init__(model=q,texture=mc,position=(.65,.24),scale=(.07,.1),parent=camera.ui)
		s.desc_s=Text('Save Game - F2',font=fn,scale=1.5,position=(s.x-.1,s.y-.07,s.z),color=color.green,parent=cu)
		s.desc_l=Text('Load Game - F3',font=fn,scale=1.5,position=(s.x-.1,s.y-.12,s.z),color=color.azure,parent=cu)
		del s

class MusicInfo(Entity):
	def __init__(self):
		super().__init__()
		self.info_text=Text('',font=fn,scale=2,position=(.35,-.45),color=color.cyan,parent=cu)
	def update(self):
		if self.info_text.text != f'Music Crash Bandicoot - {st.WARP_ROOM_MUSIC}':
			self.info_text.text=f'WARP ROOM MUSIC - {st.WARP_ROOM_MUSIC}'

class SvSuccessInfo(Text):
	def __init__(self):
		super().__init__('game saved successfully',font=fn,scale=1.5,position=(.45,.05),color=color.orange,parent=cu)
		invoke(lambda:destroy(self),delay=3)

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
			s.desc_w.color=color.magenta if s.desc_w.color == color.white else color.white

class LvSelect(Entity):
	def __init__(self):
		super().__init__()
		self.bgm=Audio(f'res/music/level/wroom{st.WARP_ROOM_MUSIC}.mp3',volume=settings.MUSIC_VOLUME,loop=True)
		objects.PseudoCrash()
		Memorycard()
		MusicInfo()
		self.index=0
	def input(self,key):
		if key in settings.BCK_KEY:
			sn.ui_audio(ID=0,pit=.125)
			if st.bonus_warp_room:
				st.selected_level=st.selected_level+1 if st.selected_level < 8 else 8
			else:
				st.selected_level=st.selected_level+1 if st.selected_level < 5 else 5
			return
		if key == settings.FWD_KEY:
			sn.ui_audio(ID=0,pit=.125)
			if st.bonus_warp_room:
				st.selected_level=st.selected_level-1 if st.selected_level > 6 else 6
			else:
				st.selected_level=st.selected_level-1 if st.selected_level > 1 else 1
			return
		if key == 'm':
			sn.ui_audio(ID=1)
			st.WARP_ROOM_MUSIC+=1
			if st.WARP_ROOM_MUSIC > 3:
				st.WARP_ROOM_MUSIC=0
			return
		if key == 'f2':
			sn.ui_audio(ID=1)
			_core.save_game()
			SvSuccessInfo()
			return
		if key == 'f3':
			sn.ui_audio(ID=1)
			_core.load_game()
			ui.BlackScreen()
			level_select()
			return
		if key == 'f1' and len(st.CRYSTAL) >= 5:
			sn.ui_audio(ID=1)
			st.bonus_warp_room=not st.bonus_warp_room
			st.selected_level=6 if st.bonus_warp_room else 1
			level_select()
			return
		if key == 'enter':
			sn.ui_audio(ID=1)
			scene.clear()
			st.level_index=st.selected_level
			st.loading=True
			level.load(st.selected_level)
	def refr_music(self):
		s=self
		if s.bgm:
			s.bgm.stop()
			s.bgm.fade_out()
			destroy(s.bgm)
		s.bgm=Audio(f'res/music/level/wroom{st.WARP_ROOM_MUSIC}.mp3',volume=settings.MUSIC_VOLUME,loop=True)
	def update(self):
		if st.WARP_ROOM_MUSIC != self.index:
			self.index=st.WARP_ROOM_MUSIC
			self.refr_music()

class Credits(Entity):
	def __init__(self):
		s=self
		st.loading=False
		super().__init__(model='quad',texture=wrbg,scale=(32,20),z=4,color=color.rgb32(100,150,100))
		s.bgm=Audio('res/music/credits.mp3',loop=True,volume=settings.MUSIC_VOLUME)
		objects.PseudoCrash()
		s.index=0
		s.t0()
		del s
	def input(self,key):
		if key == settings.JMP_KEY:
			level_select()
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

def set_warproom_scene(n):
	scene.fog_color=color.rgb32(70,100,70)
	scene.fog_density=(20,60)
	window.color=color.black
	LC.AMBIENT_LIGHT.color=color.white
	camera.position=(0,0,-20)
	camera.rotation=(0,0,0)
	camera.fov=65
	Entity(model=q,texture=f'{ivy_}_m.png',scale=ivc,position=(-.8,.4,.1),parent=cu,unlit=False)
	Entity(model=q,texture=f'{ivy_}_m.png',scale=ivc,position=(-.8,-.4,.1),rotation_z=-90,parent=cu,unlit=False)
	Entity(model=q,texture=f'{ivy_}.png',scale=ivc,position=(.8,.4,.1),parent=cu,unlit=False)
	Entity(model=q,texture=f'{ivy_}.png',scale=ivc,position=(.8,-.4,.1),rotation_z=90,parent=cu,unlit=False)
	if n == 0:
		ObjType_Background(ID=0,sca=(40,20),pos=(0,0,4),col=color.rgb32(80,100,80),txa=(1,1),UL=True)
		return
	Entity(model='sphere',texture='res/terrain/grass_flat.png',scale=(16,5,8),texture_scale=(4,4),position=(10,-8,2),color=color.rgb32(0,120,0),unlit=False)
	ObjType_Background(ID=2,sca=(38,24),pos=(0,0,5),col=color.rgb32(0,50,50),txa=(1,1),UL=True)
	ObjType_Deco(ID=1,pos=(7.5,-3.6,2),sca=.06,col=color.gray,rot=(-90,0,0),UL=True)

def level_select():
	scene.clear()
	st.LV_CLEAR_PROCESS=False
	st.level_index=0
	if len(st.CRYSTAL) >= 5:
		if not st.crd_seen:
			st.crd_seen=True
			Credits()
			return
		BonusRoomEntry()
	LvSelect()
	if st.bonus_warp_room:
		LevelSelector(1)
	else:
		LevelSelector(0)
	st.loading=False