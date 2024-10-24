import status,settings,_core,_loc
from ursina import *
se=settings
cc=_core
st=status
LC=_loc

VS='res/snd/ambience/'
SP='res/snd/player/'
SN='res/snd/misc/'
SA='res/snd/npc/'

##footstep
def footstep(c):
	if c.is_slippery:
		pc_audio(ID=8,pit=1.5)
		return
	if c.in_water > 0:
		pc_audio(ID=11,pit=random.uniform(.9,1))
		return
	else:
		if st.level_index == 4:
			pc_audio(ID=12)
			return
		pc_audio(ID=0)

##landing sound material
def landing_sound(c,o):
	fn=o.name
	if fn in ['swpt','swpl']:
		pc_audio(ID=13)
		return
	if not cc.is_crate(o):
		pc_audio(ID=2)

## ambience sound
snd_rain=VS+'rain.wav'
SND_THU={0:'thunder_start',
		1:'thunder0',
		2:'thunder1'}
def thu_audio(ID,pit=1):
	pth=Audio(VS+SND_THU[ID]+'.wav',pitch=pit,volume=se.SFX_VOLUME)
	cc.purge_instance(pth)

## INTERFACE SFX
SND_UI={0:'select',
		1:'enter',
		2:'collect',
		3:'lives',
		4:'reward',
		5:'gem'}
def ui_audio(ID,pit=1):
	if ID == 1:
		ua=Audio(SN+SND_UI[ID]+'.wav',pitch=pit,volume=se.SFX_VOLUME/2)
	else:
		ua=Audio(SN+SND_UI[ID]+'.wav',pitch=pit,volume=se.SFX_VOLUME)
	cc.purge_instance(ua)

## PLAYER SFX
SND_PC={0:'walk',
		1:'jump',
		2:'land_sand',
		3:'attack',
		4:'atk_wait',
		5:'jump_hit',
		6:'damage',
		7:'woah',
		8:'ice_slide',
		9:'ice_slide_stop',
		10:'splash',
		11:'water_step',
		12:'metal_step',
		13:'land_metal',
		14:'fall_death'}
def pc_audio(ID,pit=1):
	pc=Audio(SP+SND_PC[ID]+'.wav',pitch=pit,volume=se.SFX_VOLUME)
	cc.purge_instance(pc)

## CRATE SFX
SND_CRT={0:'steel',
		1:'block',
		2:'break1',
		3:'break2',
		4:'bnc',
		5:'spring',
		6:'checkp',
		7:'check_d',
		8:'tnt',
		9:'nitro_idle',
		10:'explode',
		11:'glass',
		12:'switch',
		13:'air',
		14:'aku'}
def crate_audio(ID,pit=1):
	if ID in [2,11]:
		if st.block_audio:
			return
		st.block_audio=True
	ca=Audio(SN+SND_CRT[ID]+'.wav',pitch=pit,volume=se.SFX_VOLUME*2)
	cc.purge_instance(ca)
	invoke(lambda:setattr(st,'block_audio',False),delay=.1)

## NPC SFX
SND_NPC={0:'plant_bite',
		1:'scrubber',
		2:'mouse',
		3:'seal',
		4:'rat_idle'}
def npc_audio(ID,pit=1):
	np=Audio(SA+SND_NPC[ID]+'.wav',pitch=pit,volume=se.SFX_VOLUME)
	cc.purge_instance(np)

## OBJECTS/ITEM SFX
SND_OBJ={0:'spawn',
		1:'door_open',
		2:'portal',
		3:'wlog',
		4:'role',
		5:'waterf',
		6:'bubble',
		7:'electric',
		8:'npc_beat',
		9:'collapse_floor',
		10:'fire_throw',
		11:'log_hit'}
def obj_audio(ID,pit=1):
	ob=Audio(SN+SND_OBJ[ID]+'.wav',pitch=pit,volume=se.SFX_VOLUME)
	cc.purge_instance(ob)

## Background Sounds
class WaterRiver(Audio):
	def __init__(self):
		super().__init__(VS+'waterf.wav',volume=0,loop=True)
	def update(self):
		if not st.gproc() and not (st.bonus_round or st.is_death_route):
			self.volume=se.SFX_VOLUME
			return
		self.volume=0

class AmbienceSound(Entity):
	def __init__(self):
		super().__init__()
		self.rpt=1
	def update(self):
		if not st.gproc():
			s=self
			s.rpt=max(s.rpt-time.dt,0)
			if s.rpt <= 0:
				s.rpt=1
				fb=Audio(VS+'jungle.wav',pitch=random.uniform(1,1.1),volume=se.SFX_VOLUME)
				cc.purge_instance(fb)

class Rainfall(Audio):
	def __init__(self):
		super().__init__(snd_rain,loop=True,volume=0)
	def update(self):
		s=self
		if (LC.ACTOR.indoor <= 0 and LC.ACTOR.warped) and not st.gproc():
			s.volume=settings.SFX_VOLUME
			return
		s.volume=0

## Background Music
MC='res/snd/music/'
class LevelMusic(Audio):
	def __init__(self,T):
		lM=MC+'lv'+str(T)+'/0.mp3'
		super().__init__(lM,volume=se.MUSIC_VOLUME,loop=True)
	def update(self):
		s=self
		if (st.bonus_round or st.is_death_route):
			s.fade_out()
			cc.purge_instance(s)
		if st.gproc() or st.aku_hit > 2:
			s.volume=0
			return
		s.volume=se.MUSIC_VOLUME

class BonusMusic(Audio):
	def __init__(self,T):
		lB=MC+'lv'+str(T)+'/0b.mp3'
		super().__init__(lB,volume=se.MUSIC_VOLUME,loop=True)
	def update(self):
		s=self
		if not st.bonus_round or st.is_death_route:
			s.fade_out()
			cc.purge_instance(s)
			LevelMusic(T=st.level_index)
			return
		if st.gproc():
			s.volume=0
			return
		s.volume=se.MUSIC_VOLUME

class SpecialMusic(Audio):
	def __init__(self,T):
		super().__init__(MC+'lv'+str(T)+'/0c.mp3',volume=se.MUSIC_VOLUME,loop=True)
	def update(self):
		s=self
		if not st.is_death_route:
			s.fade_out()
			cc.purge_instance(s)
			LevelMusic(T=st.level_index)

class AkuMusic(Audio):
	def __init__(self):
		super().__init__(MC+'ev/invinc'+str(random.randint(0,1))+'.mp3',volume=se.MUSIC_VOLUME,loop=True)
		self.tme=20
	def update(self):
		s=self
		if st.gproc():
			s.volume=0
			return
		s.volume=se.MUSIC_VOLUME
		s.tme=max(s.tme-time.dt,0)
		if s.tme <= 0 or (st.death_event or st.bonus_round or LC.ACTOR.freezed):
			st.aku_hit=2
			st.is_invincible=False
			pc_audio(ID=6,pit=.8)
			s.fade_out()
			cc.purge_instance(s)

class GameOverMusic(Audio):
	def __init__(self):
		super().__init__(MC+'ev/game_over.mp3',volume=se.MUSIC_VOLUME)
	def update(self):
		if not self.playing:
			self.fade_out()
			cc.purge_instance(self)