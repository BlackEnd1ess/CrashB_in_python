import status,settings,_core,sound
from ursina import *

SKY_COL={'day':color.rgb32(200,230,255),
		'evening':color.rgb32(255,110,90),
		'night':color.rgb32(0,0,85),
		'dark':color.black,
		'rain':color.rgb32(70,70,80),
		'snow':color.white,
		'woods':color.rgb32(70,120,110)}

FOG_COL={'day':color.rgb32(120,140,140),
		'evening':color.rgb32(250,100,50),
		'night':color.rgb32(0,0,0),
		'dark':color.rgb32(0,0,0),
		'rain':color.rgb32(0,0,0),
		'snow':color.white,
		'woods':color.rgb32(30,80,60)}

AMB_COL={'day':color.rgb32(180,180,180),
		'evening':color.rgb32(250,150,100),
		'night':color.rgb32(0,0,0),
		'dark':color.rgb32(0,0,0),
		'rain':color.rgb32(0,0,0),
		'snow':color.rgb32(200,160,210),
		'woods':color.rgb32(140,170,170)}

LGT_COL={'day':color.rgb32(0,0,0),
		'evening':color.rgb32(255,100,0),
		'night':color.rgb32(0,0,0),
		'dark':color.rgb32(0,0,0),
		'rain':color.rgb32(0,0,0),
		'snow':color.rgb32(0,230,255),
		'woods':color.rgb32(50,150,100)}

def env_switch(env,wth,tdr):
	status.day_mode=env
	#ShadowMap()
	SkyBox(t=tdr)
	#LightAmbience()
	#Fog()
	if wth > 0:
		wthr={1:lambda:RainFall(),2:lambda:SnowFall()}
		wthr[wth]()

class ShadowMap(DirectionalLight):
	def __init__(self):
		RS=2048
		super().__init__(shadows=True,shadow_map_resolution=(RS,RS),color=LGT_COL[status.day_mode],rotation_x=-260,position=(0,10,0))
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
		self.color=color.white
		Audio(sound.thu1,pitch=random.uniform(.1,.5))
		invoke(lambda:Audio(random.choice(sound.snd_thu2),pitch=random.uniform(.1,.5)),delay=.5)
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
		self.F_DST={0:(-1,30),1:(-1,15),2:(-1,15),3:(-1,30),4:(-1,15)}
		scene.fog_color=FOG_COL[status.day_mode]
		scene.fog_density=self.F_DST[status.level_index]
	def update(self):
		if status.bonus_round:
			scene.fog_density=(-5,20)
			return
		scene.fog_density=self.F_DST[status.level_index]

#class RainFall(Animation):
#	def __init__(self):
#		anP='res/env/rain.gif'
#		_f=30
#		super().__init__(anP,parent=camera.ui,position=(-.49,0),scale=(1,1.5),fps=_f)
#		self.r_pt=Animation(anP,parent=camera.ui,position=(.49,0),scale=self.scale,fps=_f)
#	def update(self):
#		if not status.gproc():
#			self.position=(-.49,0)
#			self.r_pt.position=(.49,0)
#	def update(self):
#		print(self)
class RainFall(FrameAnimation3d):
	def __init__(self):
		super().__init__('res/objects/ev/rain/rain',scale=(.004,.002,.004),color=color.rgb32(180,180,200),fps=60,loop=True,alpha=.6,rotation=(0,10,10))
		self.soundR=Audio(sound.snd_rain,loop=True,volume=0)
		self.target=_core.playerInstance[0]
	def rain_start(self):
		self.fps=60
		self.soundR.pitch=random.uniform(.9,1)
		self.soundR.volume=.5
		self.alpha=lerp(self.alpha,.7,time.dt*2)
	def rain_stop(self):
		self.alpha=lerp(self.alpha,0,time.dt*2)
		self.soundR.volume=0
		self.fps=0
	def update(self):
		if not status.gproc():
			if status.c_indoor:
				self.rain_stop()
				return
			if distance(self,self.target) > 5:
				tpp=self.target.position
				self.position=(tpp.x,tpp.y,tpp.z+.5)
			else:
				self.position=lerp(self.position,(self.target.x,camera.y-1.2,self.target.z+-.1),time.dt*4)
			self.rain_start()

class SnowFall(Entity):
	def __init__(self):
		return