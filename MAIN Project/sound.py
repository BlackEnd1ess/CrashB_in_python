import status,settings,_core,_loc,random,time
from ursina import Entity,Audio,invoke
from ursina.ursinastuff import destroy
se=settings
cc=_core
st=status
LC=_loc

SNF='res/snd/'

TC=SNF+'misc/tnt.wav'
BE=SNF+'npc/bee.wav'
VS=SNF+'ambience/'
SP=SNF+'player/'
SN=SNF+'misc/'
SA=SNF+'npc/'
dd=1.2

##footstep
def footstep(c):
	if c.is_slp:
		pc_audio(ID=8,pit=1.5)
		return
	if c.inwt > 0:
		pc_audio(ID=11,pit=random.uniform(.9,1))
		return
	else:
		if st.level_index == 4 or (st.level_index == 7 and c.indoor <= 0):
			pc_audio(ID=12)
			return
		pc_audio(ID=0)

##landing sound material
def landing_sound(o):
	if (hasattr(o,'matr') and o.matr == 'metal'):
		pc_audio(ID=13)
		return
	if (cc.is_crate(o) and not o.vnum in {0,3}) or cc.is_enemie(o):
		pc_audio(ID=5)
		return
	ldnp=.6 if LC.ACTOR.b_smash else 1
	pc_audio(ID=2,pit=ldnp)
	del ldnp

## ambience sound
snd_rain=VS+'rain.wav'
SND_THU={0:'thunder_start',
		1:'thunder0',
		2:'thunder1'}
def thu_audio(ID,pit=1):
	pth=Audio(VS+SND_THU[ID]+'.wav',pitch=random.uniform(.1,.5),volume=se.SFX_VOLUME,add_to_scene_entities=False)
	invoke(lambda:destroy(pth),delay=pth.length*4)

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
	invoke(lambda:destroy(ua),delay=ua.length*8)

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
		14:'fall_death',
		15:'angel',
		16:'wings'}
def pc_audio(ID,pit=1):
	pc=Audio(SP+SND_PC[ID]+'.wav',pitch=pit,volume=se.SFX_VOLUME,add_to_scene_entities=False)
	invoke(lambda:destroy(pc),delay=pc.length*4)

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
		4:'rat_idle',
		5:'buzzing',
		6:'spider_robot',
		7:'lab_assistant_push',
		8:'lab_assistant_fall'}
def npc_audio(ID,pit=1):
	np=Audio(SA+SND_NPC[ID]+'.wav',pitch=pit,volume=se.SFX_VOLUME,add_to_scene_entities=False)
	invoke(lambda:destroy(np),delay=np.length*2)

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
		11:'log_hit',
		12:'land_mine',
		13:'piston',
		14:'pad_0',
		15:'pad_1',
		16:'steam',
		17:'volt'}
def obj_audio(ID,pit=1):
	ob=Audio(SN+SND_OBJ[ID]+'.wav',pitch=pit,volume=se.SFX_VOLUME,add_to_scene_entities=False)
	invoke(lambda:destroy(ob),delay=ob.length*2)

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
mdb={0:'wroom',
	1:'woods',
	2:'snow',
	3:'plant',
	4:'sewer',
	5:'ruin',
	6:'digin',
	7:'piston',
	8:'dash'}

class BackgroundMusic(Audio):
	def __init__(self,m):
		s=self
		ix=st.level_index
		kt=MC+'level/'+mdb[ix]+'.mp3'
		if m == 1:
			kt=MC+'bonus/'+mdb[ix]+'.mp3'
		if m == 2:
			kt=MC+'special/'+mdb[ix]+'.mp3'
		super().__init__(kt,loop=True,volume=se.MUSIC_VOLUME)
		s.mode=m
		s.tm=.5
		del ix,kt,m
	def rmv_music(self):
		s=self
		s.stop()
		s.fade_out()
		destroy(s)
	def check_scene(self):
		s=self
		if st.game_over or (s.mode == 0 and (st.bonus_round or st.death_route)) or (s.mode == 1 and (st.bonus_solved or not st.bonus_round)) or (s.mode == 2 and (not st.death_route or st.gem_path_solved)):
			s.rmv_music()
	def update(self):
		s=self
		s.tm=max(s.tm-time.dt,0)
		if s.tm <= 0:
			s.tm=.5
			s.check_scene()
			if st.aku_hit > 2:
				s.volume=0
				return
			s.volume=se.MUSIC_VOLUME

class AkuMusic(Audio):
	def __init__(self):
		super().__init__(MC+f'invinc{random.randint(0,1)}.mp3',volume=se.MUSIC_VOLUME,loop=True)
	def update(self):
		s=self
		if st.gproc():
			s.volume=0
			return
		s.volume=se.MUSIC_VOLUME
		st.aku_inv_time=max(st.aku_inv_time-time.dt,0)
		if st.aku_inv_time <= 0 or bool(st.death_event or st.bonus_round or LC.ACTOR.freezed):
			st.aku_hit=2
			st.is_invincible=False
			pc_audio(ID=6,pit=.8)
			s.fade_out()
			cc.purge_instance(s)

class GameOverMusic(Audio):
	def __init__(self):
		super().__init__(MC+'game_over.mp3',volume=se.MUSIC_VOLUME)
	def update(self):
		if not self.playing:
			self.fade_out()
			cc.purge_instance(self)