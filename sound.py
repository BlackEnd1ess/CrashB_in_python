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
SND_UI={0:'select.wav',
		1:'enter.wav',
		2:'collect.wav',
		3:'lives.wav',
		4:'reward.wav',
		5:'gem.wav'}
def ui_audio(ID,pit=1):
	if ID == 1:
		ua=Audio(SN+SND_UI[ID],pitch=pit,volume=se.SFX_VOLUME/2)
	else:
		ua=Audio(SN+SND_UI[ID],pitch=pit,volume=se.SFX_VOLUME)
	cc.purge_instance(ua)

## PLAYER SFX
SND_PC={0:'walk.wav',
		1:'jump.wav',
		2:'land0.wav',
		3:'attack.wav',
		4:'atk_wait.wav',
		5:'jump_hit.wav',
		6:'damage.wav',
		7:'woah.wav',
		8:'ice_slide.wav',
		9:'ice_slide_stop.wav',
		10:'water_land.wav',
		11:'water_step'}
def pc_audio(ID,pit=1):
	pc=Audio(SP+SND_PC[ID],pitch=pit,volume=se.SFX_VOLUME)
	cc.purge_instance(pc)

## CRATE SFX
SND_CRT={0:'steel.wav',
		1:'block.wav',
		2:'break1.wav',
		3:'break2.wav',
		4:'bnc.wav',
		5:'spring.wav',
		6:'checkp.wav',
		7:'check_d.wav',
		8:'tnt.wav',
		9:'nitro_idle.wav',
		10:'explode.wav',
		11:'glass.wav',
		12:'switch.wav',
		13:'air.wav',
		14:'aku.wav'}
def crate_audio(ID,pit=1):
	ca=Audio(SN+SND_CRT[ID],pitch=pit,volume=se.SFX_VOLUME)
	cc.purge_instance(ca)

## NPC SFX
SND_NPC={0:'plant_bite.wav',
		1:'scrubber.wav',
		2:'mouse.wav',
		3:'seal.wav',
		4:'rat_idle.wav'}
def npc_audio(ID,pit=1):
	np=Audio(SA+SND_NPC[ID],pitch=pit,volume=se.SFX_VOLUME)
	cc.purge_instance(np)

## OBJECTS/ITEM SFX
SND_OBJ={0:'spawn.wav',
		1:'door_open.wav',
		2:'portal.wav',
		3:'wlog.wav',
		4:'role.wav',
		5:'waterf.wav',
		6:'bubble.wav',
		7:'electric.wav',
		8:'npc_beat.wav'}
def obj_audio(ID,pit=1):
	ob=Audio(SN+SND_OBJ[ID],pitch=pit,volume=se.SFX_VOLUME)
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
		VOL=settings.MUSIC_VOLUME
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
				self.disable()
			if status.is_dying:
				self.fade_out()
				cc.purge_instance(self)