import status,settings,_core
from ursina import *

VS='res/snd/ambience/'
SN='res/snd/misc/'
SP='res/snd/player/'
SA='res/snd/npc/'
se=settings
cc=_core

## ambience sound
snd_thu2=[VS+'thunder0.wav',VS+'thunder1.wav']
snd_thu1=VS+'thunder_start.wav'
snd_rain=VS+'rain.wav'

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
	ca=Audio(SN+SND_CRT[ID]+'.wav',pitch=pit,volume=se.SFX_VOLUME)
	cc.purge_instance(ca)

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
		10:'fire_throw'}
def obj_audio(ID,pit=1):
	ob=Audio(SN+SND_OBJ[ID]+'.wav',pitch=pit,volume=se.SFX_VOLUME)
	cc.purge_instance(ob)

## Background Sounds
class WaterRiver(Audio):
	def __init__(self):
		super().__init__(VS+'waterf.wav',volume=0,loop=True)
	def update(self):
		if not status.gproc() and not (status.bonus_round or status.is_death_route):
			self.volume=se.SFX_VOLUME
			return
		self.volume=0

class AmbienceSound(Entity):
	def __init__(self):
		super().__init__()
		self.rpt=1
	def update(self):
		if not status.gproc():
			self.rpt=max(self.rpt-time.dt,0)
			if self.rpt <= 0:
				self.rpt=1
				fb=Audio(VS+'jungle.wav',pitch=random.uniform(1,1.1),volume=se.SFX_VOLUME)
				cc.purge_instance(fb)

## Background Music
MC='res/snd/music/'
class LevelMusic(Audio):
	def __init__(self,T):
		lM=MC+'lv'+str(T)+'/0.mp3'
		super().__init__(lM,volume=se.MUSIC_VOLUME,loop=True)
	def update(self):
		if (status.bonus_round or status.is_death_route):
			self.fade_out()
			cc.purge_instance(self)
		if status.gproc() or status.aku_hit > 2:
			self.volume=0
			return
		self.volume=se.MUSIC_VOLUME

class BonusMusic(Audio):
	def __init__(self,T):
		lB=MC+'lv'+str(T)+'/0b.mp3'
		super().__init__(lB,volume=se.MUSIC_VOLUME,loop=True)
	def update(self):
		if not status.bonus_round or status.is_death_route:
			self.fade_out()
			cc.purge_instance(self)
			LevelMusic(T=status.level_index)
			return
		if status.gproc():
			self.volume=0
			return
		self.volume=se.MUSIC_VOLUME

class SpecialMusic(Audio):
	def __init__(self,T):
		super().__init__(MC+'lv'+str(T)+'/0c.mp3',volume=se.MUSIC_VOLUME,loop=True)
	def update(self):
		if not status.is_death_route:
			self.fade_out()
			cc.purge_instance(self)
			LevelMusic(T=status.level_index)

class AkuMusic(Audio):
	def __init__(self):
		super().__init__(MC+'ev/invinc.mp3',volume=se.MUSIC_VOLUME)
	def update(self):
		if not status.gproc():
			if not self.playing:
				status.aku_hit=2
				pc_audio(ID=6,pit=.8)
				self.fade_out()
				cc.purge_instance(self)

class GameOverMusic(Audio):
	def __init__(self):
		super().__init__(MC+'ev/game_over.mp3',volume=se.MUSIC_VOLUME)
	def update(self):
		if not self.playing:
			self.fade_out()
			cc.purge_instance(self)