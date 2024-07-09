import status,settings,_loc,sound
from ursina import *

SKY_COL={'day':color.rgb32(200,230,255),
		'pipe':color.black,
		'evening':color.rgb32(255,110,90),
		'night':color.rgb32(0,0,85),
		'dark':color.black,
		'rain':color.rgb32(70,70,80),
		'snow':color.white,
		'woods':color.rgb32(70,120,110)}

FOG_COL={'day':color.rgb32(120,140,140),
		'pipe':color.black,
		'evening':color.rgb32(10,40,10),
		'night':color.rgb32(0,0,0),
		'dark':color.rgb32(0,0,0),
		'rain':color.rgb32(0,0,0),
		'snow':color.white,
		'woods':color.rgb32(30,80,60)}

AMB_COL={'day':color.rgb32(180,180,180),
		'pipe':color.rgb32(180,180,180),
		'evening':color.rgb32(220,180,150),
		'night':color.rgb32(0,0,0),
		'dark':color.rgb32(0,0,0),
		'rain':color.rgb32(0,0,0),
		'snow':color.rgb32(200,160,210),
		'woods':color.rgb32(120,130,120)}

LGT_COL={'day':color.rgb32(0,0,0),
		'pipe':color.rgb32(100,180,100),
		'evening':color.rgb32(255,100,0),
		'night':color.rgb32(0,0,0),
		'dark':color.rgb32(0,0,0),
		'rain':color.rgb32(0,0,0),
		'snow':color.rgb32(0,230,255),
		'woods':color.rgb32(50,150,100)}

def env_switch(env,wth,tdr):
	status.day_mode=env
	SkyBox(t=tdr)
	LightAmbience()
	Fog()
	if wth > 0:
		wthr={1:lambda:RainFall(),2:lambda:SnowFall()}
		wthr[wth]()

#class ShadowMap(DirectionalLight):
#	def __init__(self):
#		RS=1024
#		super().__init__(shadows=True,shadow_map_resolution=(RS,RS),color=LGT_COL[status.day_mode],rotation_x=-260,position=(0,10,0))
#		invoke(lambda:setattr(window,'render_mode','default'),delay=.5)

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
		#Audio(sound.snd_thu1,pitch=random.uniform(.1,.5))
		#invoke(lambda:Audio(random.choice(sound.snd_thu2),pitch=random.uniform(.1,.5)),delay=.5)
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
		self.L_DST={0:(3,30),1:(2,20),2:(3,15),3:(10,30),4:(5,30),5:(5,20)}
		self.B_DST={0:(0,0),1:(-5,20),2:(0,10),3:(4,27),4:(13,15),5:(10,20)}
		scene.fog_color=FOG_COL[status.day_mode]
		scene.fog_density=self.L_DST[status.level_index]
	def update(self):
		if status.bonus_round:
			scene.fog_density=self.B_DST[status.level_index]
			return
		if status.is_death_route:
			scene.fog_density=(10,40)
			return
		scene.fog_density=self.L_DST[status.level_index]

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
		j=.004
		super().__init__('res/objects/ev/rain/rain',scale=(j,j/2,j),color=color.rgb32(180,180,200),fps=60,loop=True,alpha=0,rotation=(0,10,10),visible=False)
		#self.soundR=Audio(sound.snd_rain,loop=True,volume=0)
		self.ta=_loc.ACTOR
		self.ta.indoor=.5
	def rain_start(self):
		self.fps=60
		self.visible=True
		#self.soundR.pitch=random.uniform(.9,1)
		#self.soundR.volume=settings.SFX_VOLUME
		self.alpha=lerp(self.alpha,.7,time.dt*2)
	def rain_stop(self):
		self.fps=0
		#self.soundR.volume=0
		self.alpha=lerp(self.alpha,0,time.dt*2)
	def follow_p(self):
		s=self
		tpp=s.ta.position
		if distance(s,s.ta) > 5:
			s.position=(tpp.x,tpp.y,tpp.z+.5)
			return
		s.position=lerp(s.position,(s.ta.x,camera.y-1.2,s.ta.z+-.1),time.dt*4)
	def update(self):
		if not status.gproc() and self.ta.warped:
			if self.ta.indoor <= 0:
				self.rain_start()
				self.follow_p()
				return
			self.rain_stop()

class SnowFall(Entity):
	def __init__(self):
		return