import status,settings
from ursina import *

## misc sound effects
SN='res/snd/misc/'

#crate sfx
snd_nitro=SN+'nitro_idle.wav'
snd_explo=SN+'explode.wav'
snd_break=SN+'break1.wav'
snd_glass=SN+'glass.wav'
snd_steel=SN+'steel.wav'
snd_sprin=SN+'spring.wav'
snd_bounc=SN+'bnc.wav'
snd_c_tnt=SN+'tnt.wav'
snd_c_air=SN+'air.wav'

#misc sfx

snd_nbeat=SN+'npc_beat.wav'
snd_d_opn=SN+'door_open.wav'
snd_spawn=SN+'spawn.wav'

#game/ui sfx
snd_rward=SN+'reward.wav'
snd_enter=SN+'enter.wav'
snd_lifes=SN+'lives.wav'
snd_aku_m=SN+'aku.wav'
snd_c_gem=SN+'gem.wav'

def snd_switch():
	Audio(SN+'switch.wav',volume=1)
	Audio(SN+'block.wav',volume=1)
def snd_checkp():
	Audio(SN+'check_d.wav')
	Audio(SN+'checkp.wav')
def snd_collect():
	Audio(SN+'collect.wav',volume=.5)
	invoke(lambda:Audio(snd_enter,volume=.3),delay=.5)

## player sound
SP='res/snd/player/'
snd_jmph=SP+'jump_hit.wav'
snd_jump=SP+'jump.wav'
snd_attk=SP+'attack.wav'
snd_walk=SP+'walk.wav'
snd_land=SP+'land0.wav'
snd_woah=SP+'woah.wav'
snd_damg=SP+'damage.wav'

## npc sound
SA='res/snd/npc/'

snd_eating_plant=SA+'plant_bite.wav'
snd_scrubber=SA+'scrubber.wav'
snd_mouse=SA+'mouse.wav'
snd_seal=SA+'seal.wav'
snd_rat=SA+'rat_idle.wav'

## BGM
MC='res/snd/music/'
class LevelMusic(Audio):
	def __init__(self,T):
		lM=MC+'lv'+str(T)+'/'+str(random.randint(0,1))+'.mp3'
		super().__init__(lM,volume=settings.MUSIC_VOLUME,loop=True)
	def update(self):
		if status.bonus_round or status.is_death_route:
			self.fade_out()
			self.disable()
		if status.pause:
			self.volume=0
			return
		self.volume=1

class BonusMusic(Audio):
	def __init__(self,T):
		lB=MC+'lv'+str(T)+'/'+str(random.randint(0,1))+'b.mp3'
		super().__init__(lB,volume=settings.MUSIC_VOLUME,loop=True)
	def update(self):
		if not status.bonus_round or status.is_death_route:
			self.fade_out()
			self.disable()
			LevelMusic(T=status.level_index)
			return
		if status.pause:
			self.volume=0
			return
		self.volume=1

class SpecialMusic(Audio):
	def __init__(self,T):
		super().__init__(MC+'lv'+str(T)+'/0c.mp3',volume=settings.MUSIC_VOLUME,loop=True)
	def update(self):
		if not status.is_death_route:
			self.fade_out()
			self.disable()
			LevelMusic(T=status.level_index)
			return