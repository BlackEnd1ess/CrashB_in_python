import status,settings,_loc,sound,effect
from ursina import *

st=status
c=color
SKY_COL={'day':c.rgb32(200,230,255),
		'empty':c.black,
		'evening':c.rgb32(255,110,90),
		'night':c.rgb32(0,0,85),
		'dark':c.black,
		'rain':c.rgb32(70,70,80),
		'snow':c.white,
		'woods':c.rgb32(70,120,110)}

FOG_COL={'day':c.rgb32(120,140,140),
		'empty':c.black,
		'evening':c.rgb32(10,40,10),
		'night':c.rgb32(0,0,0),
		'dark':c.rgb32(0,0,0),
		'rain':c.rgb32(0,0,0),
		'snow':c.white,
		'woods':c.rgb32(30,80,60)}

AMB_COL={'day':c.rgb32(180,180,180),
		'empty':c.rgb32(180,180,180),
		'evening':c.rgb32(220,180,150),
		'night':c.rgb32(0,0,0),
		'dark':c.rgb32(0,0,0),
		'rain':c.rgb32(0,0,0),
		'snow':c.rgb32(200,160,210),
		'woods':c.rgb32(120,130,120)}

LGT_COL={'day':c.rgb32(0,0,0),
		'empty':c.rgb32(100,180,100),
		'evening':c.rgb32(255,100,0),
		'night':c.rgb32(0,0,0),
		'dark':c.rgb32(0,0,0),
		'rain':c.rgb32(0,0,0),
		'snow':c.rgb32(0,230,255),
		'woods':c.rgb32(50,150,100)}

def env_switch(env,wth):
	st.day_mode=env
	SkyBox()
	LightAmbience()
	Fog()
	if wth == 1:
		RainFall()

class SkyBox(Sky):
	def __init__(self):
		super().__init__(texture='res/env/sky.jpg',color=SKY_COL[st.day_mode],unlit=False)
		self.setting=SKY_COL[st.day_mode]
		self.thunder_time=3
	def thunder_bolt(self):
		self.color=color.white
		_loc.bgT.texture='res/background/bg_ruins_th.jpg'
		_loc.bgT.texture_scale=_loc.bgT.orginal_tsc
		sound.thu_audio(ID=0,pit=random.uniform(.1,.5))
		invoke(lambda:sound.thu_audio(ID=random.randint(1,2),pit=random.uniform(.1,.5)),delay=.5)
		invoke(self.reset_sky,delay=random.uniform(.1,.4))
	def reset_sky(self):
		self.color=self.setting
		_loc.bgT.texture='res/background/bg_ruins.jpg'
		_loc.bgT.texture_scale=_loc.bgT.orginal_tsc
		self.thunder_time=random.randint(4,10)
	def update(self):
		if not st.gproc():
			if st.weather_thunder:
				self.thunder_time=max(self.thunder_time-time.dt,0)
				if self.thunder_time <= 0:
					self.thunder_bolt()
				return
			if st.bonus_round:
				self.color=c.black
				return
			self.color=self.setting

class LightAmbience(AmbientLight):
	def __init__(self):
		super().__init__(color=AMB_COL[status.day_mode])

class Fog(Entity):
	def __init__(self):
		super().__init__()
		self.L_DST={0:(3,30),1:(2,20),2:(3,15),3:(10,30),4:(5,30),5:(5,20),6:(5,10)}
		self.B_DST={0:(0,0),1:(-5,20),2:(0,10),3:(4,27),4:(8,15),5:(10,20),6:(5,10)}
		scene.fog_color=FOG_COL[st.day_mode]
		scene.fog_density=self.L_DST[st.level_index]
	def update(self):
		if st.bonus_round:
			scene.fog_density=self.B_DST[st.level_index]
			return
		if st.is_death_route:
			scene.fog_density=(10,40)
			return
		scene.fog_density=self.L_DST[st.level_index]

class RainFall(FrameAnimation3d):
	def __init__(self):
		j=.004
		super().__init__('res/objects/ev/rain/rain',scale=(j,j/1.5,j),color=color.rgb32(180,180,200),fps=80,loop=True,alpha=0,rotation=(0,10,10),visible=False)
		sound.Rainfall()
		self.ta=_loc.ACTOR
		self.ta.indoor=.5
	def rain_start(self):
		self.fps=80
		self.resume()
		self.visible=True
		self.alpha=lerp(self.alpha,.7,time.dt*2)
	def rain_stop(self):
		self.fps=0
		self.pause()
		self.alpha=lerp(self.alpha,0,time.dt*2)
	def follow_p(self):
		s=self
		tpp=s.ta.position
		if distance(s,s.ta) > 5:
			s.position=(tpp.x,tpp.y,tpp.z+.5)
			return
		s.position=lerp(s.position,(s.ta.x,camera.y-1.2,s.ta.z+-.1),time.dt*4)
	def update(self):
		if not st.gproc() and self.ta.warped:
			if self.ta.indoor > 0:
				self.rain_stop()
				return
			self.rain_start()
			self.follow_p()

class SnowFall(Entity):
	def __init__(self):
		return