import status,settings,_core,_loc,random,time
from ursina import Entity,Audio,invoke
from ursina.ursinastuff import destroy
se=settings
cc=_core
st=status
LC=_loc

VS='res/snd/ambience/'
SP='res/snd/player/'
SN='res/snd/misc/'
SA='res/snd/npc/'
dd=.8

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
	if hasattr(o,'matr'):
		if o.matr == 'metal':
			pc_audio(ID=13)
			return
	if not (cc.is_crate(o) or cc.is_enemie(o)):
		pc_audio(ID=2)

## ambience sound
snd_rain=VS+'rain.wav'
SND_THU={0:'thunder_start',
		1:'thunder0',
		2:'thunder1'}
def thu_audio(ID,pit=1):
	pth=Audio(VS+SND_THU[ID]+'.wav',pitch=random.uniform(.1,.5),volume=se.SFX_VOLUME,add_to_scene_entities=False)
	invoke(lambda:destroy(pth),delay=pth.length*2)

## INTERFACE SFX
SND_UI={0:'select',
		1:'enter',
		2:'collect',
		3:'lives',
		4:'reward',
		5:'gem'}
def ui_audio(ID,pit=1):
	if ID == 1:
		ua=Audio(SN+SND_UI[ID]+'.wav',pitch=pit,volume=se.SFX_VOLUME/2,add_to_scene_entities=False)
	else:
		ua=Audio(SN+SND_UI[ID]+'.wav',pitch=pit,volume=se.SFX_VOLUME,add_to_scene_entities=False)
	invoke(lambda:destroy(ua),delay=dd)

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
	pc=Audio(SP+SND_PC[ID]+'.wav',pitch=pit,volume=se.SFX_VOLUME,add_to_scene_entities=False)
	invoke(lambda:destroy(pc),delay=dd)

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
	if (ID == 2 and st.br_sn) or (ID == 10 and st.ex_sn) or (ID == 11 and st.ni_sn):
		return
	if ID == 2 and not st.br_sn:
		st.br_sn=True
		invoke(lambda:setattr(st,'br_sn',False),delay=.1)
	if ID == 10 and not st.ex_sn:
		st.ex_sn=True
		invoke(lambda:setattr(st,'ex_sn',False),delay=.1)
	if ID == 11 and not st.ni_sn:
		st.ni_sn=True
		invoke(lambda:setattr(st,'ni_sn',False),delay=.1)
	ca=Audio(SN+SND_CRT[ID]+'.wav',pitch=pit,volume=se.SFX_VOLUME*2,add_to_scene_entities=False)
	invoke(lambda:destroy(ca),delay=dd)

## NPC SFX
SND_NPC={0:'plant_bite',
		1:'scrubber',
		2:'mouse',
		3:'seal',
		4:'rat_idle'}
def npc_audio(ID,pit=1):
	np=Audio(SA+SND_NPC[ID]+'.wav',pitch=pit,volume=se.SFX_VOLUME,add_to_scene_entities=False)
	invoke(lambda:destroy(np),delay=dd)

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
	ob=Audio(SN+SND_OBJ[ID]+'.wav',pitch=pit,volume=se.SFX_VOLUME,add_to_scene_entities=False)
	invoke(lambda:destroy(ob),delay=dd)

## Background Sounds
class WaterRiver(Audio):
	def __init__(self):
		super().__init__(VS+'waterf.wav',volume=0,loop=True)
		self.tme=.5
	def update(self):
		s=self
		s.tme=max(s.tme-time.dt,0)
		if s.tme <= 0:
			if st.gproc() or st.bonus_round:
				s.volume=0
				return
			s.volume=settings.SFX_VOLUME

class AmbienceSound(Audio):
	def __init__(self):
		super().__init__(VS+'jungle.wav',loop=True,volume=0)
	def update(self):
		s=self
		if st.gproc():
			s.volume=0
			return
		s.volume=settings.SFX_VOLUME

class Rainfall(Audio):
	def __init__(self):
		super().__init__(snd_rain,loop=True,volume=0)
		self.tme=0
	def update(self):
		s=self
		s.tme=max(s.tme-time.dt,0)
		if s.tme <= 0:
			s.tme=.5
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
		if (st.bonus_round or st.death_route):
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
		if not st.bonus_round or st.death_route:
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
		if not st.death_route:
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