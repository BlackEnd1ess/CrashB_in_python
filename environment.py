import status,settings,_core
from ursina import *

SKY_COL={'day':color.rgb(200,230,255),
		'evening':color.rgb(255,110,90),
		'night':color.rgb(0,0,85),
		'dark':color.black,
		'rain':color.rgb(70,70,80),
		'snow':color.white,
		'woods':color.rgb(70,120,110)}

FOG_COL={'day':color.rgb(120,140,140),
		'evening':color.rgb(0,0,0),
		'night':color.rgb(0,0,0),
		'dark':color.rgb(0,0,0),
		'rain':color.rgb(0,0,0),
		'snow':color.white,
		'woods':color.rgb(0,70,70)}

AMB_COL={'day':color.rgb(180,180,180),
		'evening':color.rgb(0,0,0),
		'night':color.rgb(0,0,0),
		'dark':color.rgb(0,0,0),
		'rain':color.rgb(0,0,0),
		'snow':color.rgb(200,160,210),
		'woods':color.rgb(140,170,170)}

def env_switch(env,wth,tdr):
	status.day_mode=env
	ShadowMap()
	SkyBox(t=tdr)
	LightAmbience()
	Fog()
	if wth > 0:
		wthr={1:lambda:RainFall(),2:lambda:SnowFall()}
		wthr[wth]()

class ShadowMap(DirectionalLight):
	def __init__(self):
		RS=1024*2
		g=100
		sCL=SKY_COL[status.day_mode]
		aC=color.rgb(sCL[0]+g,sCL[1]+g,sCL[2]+g)
		super().__init__(shadows=True,shadow_map_resolution=(RS,RS),color=aC,rotation_x=-260,position=(0,10,0))
		invoke(lambda:setattr(window,'render_mode','default'),delay=.5)

class SkyBox(Sky):
	def __init__(self,t):
		super().__init__(texture='res/env/sky.jpg',color=SKY_COL[status.day_mode],unlit=False)
		self.setting=SKY_COL[status.day_mode]
		self.thunder=t
		if self.thunder == 1:
			self.thunder_time=3
	def reset(self):
		self.color=self.setting
		self.thunder_time=random.randint(4,10)
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

class LightAmbience(AmbientLight):
	def __init__(self):
		super().__init__(color=AMB_COL[status.day_mode])

class Fog(Entity):
	def __init__(self):
		super().__init__()
		self.F_DST={0:(-1,30),1:(-1,15),2:(-1,15),3:(-1,15),4:(-1,15)}
		scene.fog_color=FOG_COL[status.day_mode]
		scene.fog_density=self.F_DST[status.level_index]
	def update(self):
		if status.bonus_round:
			scene.fog_density=(-5,50)
			return
		scene.fog_density=self.F_DST[status.level_index]

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
			self.soundR.pitch=random.uniform(.9,1)
			self.soundR.volume=.5

class SnowFall(Entity):
	def __init__(self):
		return