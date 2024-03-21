import status,settings,_core
from ursina import *

sts=settings
class SkyBox(Sky):
	def __init__(self,m,t):
		self.setting=m
		self.thunder=t
		super().__init__(texture='res/env/sky.jpg',color=m,unlit=False)
		if self.thunder == 1:
			self.thunder_time=3
	def reset(self):
		self.color=self.setting
		self.thunder_time=random.randint(3,10)
	def thunder_bolt(self):
		tpp='/res/snd/ambience/'
		self.color=color.white
		Audio(tpp+'thunder_start.wav',pitch=random.uniform(.1,.5))
		invoke(lambda:Audio(tpp+'thunder'+str(random.randint(0,1))+'.wav',pitch=random.uniform(.1,.5)),delay=.5)
		invoke(self.reset,delay=random.uniform(.1,.4))
	def update(self):
		if status.bonus_round:
			self.color=color.black
		else:
			self.color=self.setting
		if self.thunder == 1:
			self.thunder_time-=time.dt
			if self.thunder_time <= 0:
				self.thunder_bolt()

class ShadowMap(DirectionalLight):
	def __init__(self,c):
		RS=1024*2
		super().__init__(shadows=True,shadow_map_resolution=(RS,RS),color=c,rotation_x=-260,position=(0,10,64))
		invoke(lambda:setattr(window,'render_mode','default'),delay=.2)

class LightAmbience(AmbientLight):
	def __init__(self,d):
		self.bg_col={'day':color.white,
				'evening':color.orange,
				'night':color.rgb(100,100,150),
				'dark':color.rgb(150,150,150),
				'rain':color.gray,
				'woods':color.rgb(80,140,80),
				'bonus':color.rgb(250,130,130)}
		super().__init__(color=self.bg_col[d])
	def update(self):
		self.color=self.bg_col[status.day_mode]

class Fog(Entity):
	def __init__(self,d):
		super().__init__()
		_day={'day':color.rgb(0,45,30),
			'evening':color.orange,
			'night':color.black,
			'dark':color.black,
			'rain':color.rgb(40,40,40),
			'woods':color.rgb(50,70,60)}
		scene.fog_color=_day[d]
		scene.fog_density=(-5,16)
	def update(self):
		if status.bonus_round:
			scene.fog_density=(-5,50)
			return
		scene.fog_density=(-5,16)

class RainFall(Animation):
	def __init__(self):
		super().__init__('res/env/rain.gif',parent=camera.ui,z=.1,fps=60,scale=(2,1),duration=.1,color=color.white,alpha=.4)
		self.soundR=Audio('res/snd/ambience/rain.wav',loop=True,volume=0)
		if status.day_mode == 'night':
			self.color=color.rgb(80,80,80)
	def update(self):
		if status.bonus_round and status.level_index == 1:
			self.soundR.volume=0
			self.visible=False
			return
		if status.c_indoor:
			self.soundR.volume=.05
			self.visible=False
			return
		if status.loading or status.pause:
			self.visible=False
			self.soundR.volume=0
		else:
			self.show()
			self.soundR.volume=.5

class SnowFall(Entity):
	def __init__(self):
		return