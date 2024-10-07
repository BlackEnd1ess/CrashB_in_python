import status,_loc,sound
from ursina import *

st=status
LC=_loc
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
		'evening':c.rgb32(25,45,25),
		'night':c.rgb32(0,0,0),
		'dark':c.rgb32(0,0,0),
		'rain':c.rgb32(0,0,0),
		'snow':c.white,
		'woods':c.rgb32(30,80,60)}

AMB_COL={'day':c.rgb32(180,180,180),
		'empty':c.rgb32(140,140,140),#c.rgb32(180,180,180),
		'evening':c.rgb32(255,215,185),
		'night':c.rgb32(0,0,0),
		'dark':c.rgb32(0,0,0),
		'rain':c.rgb32(0,0,0),
		'snow':c.rgb32(200,160,210),
		'woods':c.rgb32(140,150,140)}

def init_amb_light():#called 1 time
	amv=AmbientLight(color=c.gray)
	LC.AMBIENT_LIGHT=amv

def env_switch(idx):
	st.day_mode=LC.day_m[idx]
	SkyBox()
	LC.AMBIENT_LIGHT.color=AMB_COL[st.day_mode]
	Fog()
	if idx in [1,5]:#rain in level 1 and 5
		RainFall()

class SkyBox(Sky):
	def __init__(self):
		self.bgr='res/background/'
		super().__init__(texture=self.bgr+'sky.jpg',color=SKY_COL[st.day_mode],unlit=False)
		self.setting=SKY_COL[st.day_mode]
		self.thunder_time=3
	def thunder_bolt(self):
		self.color=color.white
		LC.bgT.texture=self.bgr+'bg_ruins_th.jpg'
		LC.bgT.texture_scale=LC.bgT.orginal_tsc
		sound.thu_audio(ID=0,pit=random.uniform(.1,.5))
		invoke(lambda:sound.thu_audio(ID=random.randint(1,2),pit=random.uniform(.1,.5)),delay=.5)
		invoke(self.reset_sky,delay=random.uniform(.1,.4))
	def reset_sky(self):
		self.color=self.setting
		LC.bgT.texture=self.bgr+'bg_ruins.jpg'
		LC.bgT.texture_scale=LC.bgT.orginal_tsc
		self.thunder_time=random.randint(4,10)
	def weather_sky(self):
		if st.weather_thunder:
			self.thunder_time=max(self.thunder_time-time.dt,0)
			if self.thunder_time <= 0:
				self.thunder_bolt()
			return
		if st.bonus_round:
			self.color=c.black
			return
		self.color=self.setting
	def update(self):
		if not st.gproc():
			if st.level_index == 5:
				self.weather_sky()
				return
			if st.level_index == 1:
				if st.is_death_route:
					self.color=c.rgb32(30,30,60)
				else:
					self.color=self.setting

class Fog(Entity):
	def __init__(self):
		super().__init__()
		self.L_DST={0:(3,30),1:(2,20),2:(3,15),3:(17,19),4:(5,30),5:(5,20),6:(15,30)}
		self.B_DST={0:(0,0),1:(-5,20),2:(0,10),3:(5,20),4:(8,15),5:(10,20),6:(15,30)}
		scene.fog_color=FOG_COL[st.day_mode]
		scene.fog_density=self.L_DST[st.level_index]
	def change_color(self):
		if st.is_death_route:
			scene.fog_color=c.rgb32(20,20,40)
			return
		scene.fog_color=FOG_COL[st.day_mode]
	def update(self):
		if st.bonus_round:
			scene.fog_density=self.B_DST[st.level_index]
			return
		scene.fog_density=self.L_DST[st.level_index]
		if st.level_index == 1:
			self.change_color()

class RainFall(Entity):
	def __init__(self):
		s=self
		super().__init__(model='quad',scale=(1.8,1),alpha=0,z=4,visible=False,color=c.light_gray,parent=camera.ui,unlit=False)
		s.tx_r='res/objects/ev/rain/'
		LC.ACTOR.indoor=.5
		sound.Rainfall()
		s.frm=0
		s.sp=30
		if st.level_index == 5:
			s.sp=50
		s.dup_rain=Entity(model='quad',scale=(12,6),alpha=s.alpha,visible=False,color=c.white,parent=scene,unlit=False)
	def refr_rain(self):
		s=self
		s.frm=min(s.frm+time.dt*s.sp,58.99)
		if s.frm > 58.98:
			s.frm=0
		rrt=s.tx_r+str(int(s.frm))+'.png'
		s.dup_rain.texture=rrt
		s.texture=rrt
	def update(self):
		if not st.gproc():
			s=self
			ft=time.dt*2
			s.refr_rain()
			if LC.ACTOR.warped and LC.ACTOR.indoor <= 0:
				s.dup_rain.visible=True
				s.visible=True
				s.dup_rain.position=(camera.x,camera.y-.1,camera.z+4)
				s.dup_rain.alpha=lerp(s.alpha,1,ft)
				s.alpha=lerp(s.alpha,.6,ft)
				return
			s.dup_rain.alpha=lerp(s.alpha,0,ft)
			s.alpha=lerp(s.alpha,0,ft)