from ursina import Entity,Audio,invoke,distance
import status,settings,_core,_loc,random,time
from ursina.ursinastuff import destroy
import _SFX_DATABASE as sfx_db

se=settings
cc=_core
st=status
LC=_loc

MC='res/music/'
SF='res/snd/'

loop_snd_info={6:3,8:4,9:4,10:1,11:2,15:5,17:6}

BLD_ROLL=f'{SF}/{sfx_db.OBJECT[18]}.wav'#boulder roll
TC=f'{SF}{sfx_db.CRATE[7]}.wav'#tnt box
dd=1.2

##footstep
def footstep(c):
	if c.is_slp:
		pc_audio(ID=8,pit=1.5)
		return
	if c.in_water:
		pc_audio(ID=11,pit=random.uniform(.9,1))
		return
	else:
		if st.level_index in (4,7):#(st.level_index == 7 and c.indoor <= 0):
			pc_audio(ID=12)
			return
		if st.level_index in (2,8):
			pc_audio(ID=18)
			return
		pc_audio(ID=0)

##landing sound material
def landing_sound(o):
	if hasattr(o,'matr') and o.matr == 'metal':
		pc_audio(ID=13)
		return
	if LC.ACTOR.in_water:
		pc_audio(ID=10)
		return
	if cc.is_crate(o) and ((o.vnum in {7,8}) or (o.vnum in {9,10,11} and not o.activ)) or cc.is_enemie(o):
		pc_audio(ID=5)
		return
	ldnp=.6 if LC.ACTOR.b_smash else 1
	pc_audio(ID=2,pit=ldnp)
	del ldnp

##ambience sound
def thu_audio(ID,pit=1):
	pth=Audio(SF+sfx_db.AMBIENCE[ID]+'.wav',pitch=random.uniform(.1,.5),volume=se.SFX_VOLUME,add_to_scene_entities=False)
	invoke(lambda:destroy(pth),delay=pth.length*4)

## INTERFACE SFX
def ui_audio(ID,pit=1):
	if ID == 1:
		ua=Audio(SF+sfx_db.INTERFACE[ID]+'.wav',pitch=pit,volume=se.SFX_VOLUME/2,add_to_scene_entities=False)
	else:
		ua=Audio(SF+sfx_db.INTERFACE[ID]+'.wav',pitch=pit,volume=se.SFX_VOLUME,add_to_scene_entities=False)
	invoke(lambda:destroy(ua),delay=ua.length*6)

## PLAYER SFX
def pc_audio(ID,pit=1):
	pc=Audio(SF+sfx_db.PLAYER[ID]+'.wav',pitch=pit,volume=se.SFX_VOLUME,add_to_scene_entities=False)
	invoke(lambda:destroy(pc),delay=pc.length*4)

## CRATE SFX
def crate_audio(ID,pit=1):
	if any([(ID == 2 and st.br_sn > 4),(ID == 9 and st.ex_sn > 2),(ID == 10 and st.ni_sn > 2)]):
		return
	if ID == 2 and st.br_sn < 5:
		st.br_sn+=1
	if ID == 9 and st.ex_sn < 3:
		st.ex_sn+=1
	if ID == 10 and st.ni_sn < 6:
		st.ni_sn+=1
	ca=Audio(SF+sfx_db.CRATE[ID]+'.wav',pitch=pit,volume=se.SFX_VOLUME*2,add_to_scene_entities=False)
	invoke(lambda:destroy(ca),delay=ca.length*2)
	del ID,pit

## NPC SFX
def npc_audio(ID,pit=1,vol=None):
	if not vol:
		vol=se.SFX_VOLUME
	np=Audio(SF+sfx_db.NPC[ID]+'.wav',pitch=pit,volume=vol,add_to_scene_entities=False)
	invoke(lambda:destroy(np),delay=np.length*3)
	del vol,pit,ID

def npc_loop_audio(n,PIT,tme_r):
	if n.vnum in loop_snd_info:
		if distance(n,LC.ACTOR) < 10:
			n.tme=max(n.tme-time.dt,0)
			if n.tme <= 0:
				n.tme=tme_r
				cds=distance(n,LC.ACTOR)
				nvv=max(0,1-(cds/10))
				npc_audio(ID=loop_snd_info[n.vnum],vol=nvv,pit=PIT)
				del n,PIT,tme_r,cds

## OBJECTS/ITEM SFX
def obj_audio(ID,pit=1):
	ob=Audio(SF+sfx_db.OBJECT[ID]+'.wav',pitch=pit,volume=se.SFX_VOLUME,add_to_scene_entities=False)
	invoke(lambda:destroy(ob),delay=ob.length*2)

## Background Sounds
class WaterRiver(Audio):
	def __init__(self):
		super().__init__(f'{SF}/{sfx_db.OBJECT[5]}.wav',volume=0,loop=True)
		self.tme=.5
	def update(self):
		s=self
		s.tme=max(s.tme-time.dt,0)
		if s.tme <= 0:
			s.volume=0 if st.gproc() or st.bonus_round else se.SFX_VOLUME

class AmbienceSound(Audio):
	def __init__(self):
		super().__init__(f'{SF}/{sfx_db.AMBIENCE[4]}.wav',loop=True,volume=0)
	def update(self):
		self.volume=0 if st.gproc() else se.SFX_VOLUME

class Rainfall(Audio):
	def __init__(self):
		super().__init__(f'{SF}/{sfx_db.AMBIENCE[0]}.wav',loop=True,volume=0)
		self.tme=0
	def update(self):
		s=self
		s.tme=max(s.tme-time.dt,0)
		if s.tme <= 0:
			s.tme=.5
			s.volume=settings.SFX_VOLUME if (LC.ACTOR.indoor <= 0 and LC.ACTOR.warped) and not st.gproc() else 0

## Background Music
class BackgroundMusic(Audio):
	def __init__(self,m):
		s=self
		ix=st.level_index
		kt=MC+'level/'+sfx_db.MUSIC[ix]+'.mp3'
		if m == 1:
			kt=MC+'bonus/'+sfx_db.MUSIC[ix]+'.mp3'
		if m == 2:
			kt=MC+'special/'+sfx_db.MUSIC[ix]+'.mp3'
		super().__init__(kt,loop=True,volume=se.MUSIC_VOLUME)
		s.mode=m
		s.tm=.5
		del ix,kt,m,s
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
			s.volume=0 if st.aku_hit > 2 else se.MUSIC_VOLUME
			s.check_scene()

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
			st.aku_inv_time=20
			pc_audio(ID=6,pit=.8)
			s.fade_out()
			destroy(s)

class GameOverMusic(Audio):
	def __init__(self):
		super().__init__(MC+'game_over.mp3',volume=se.MUSIC_VOLUME)
	def update(self):
		if not self.playing:
			self.fade_out()
			cc.purge_instance(self)