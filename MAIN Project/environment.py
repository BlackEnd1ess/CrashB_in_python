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
		'woods':c.rgb32(70,120,110),
		'sewer':c.black}

FOG_COL={'day':c.rgb32(120,140,140),
		'empty':c.black,
		'evening':c.rgb32(25,45,25),
		'night':c.rgb32(0,0,0),
		'dark':c.rgb32(0,0,0),
		'rain':c.rgb32(0,0,0),
		'snow':c.white,
		'woods':c.rgb32(20,70,50),
		'sewer':c.rgb32(160,160,0)}

AMB_COL={'day':c.rgb32(180,180,180),
		'empty':c.rgb32(140,140,140),#c.rgb32(180,180,180),
		'evening':c.rgb32(240,200,170),
		'night':c.rgb32(0,0,0),
		'dark':c.rgb32(0,0,0),
		'rain':c.rgb32(0,0,0),
		'snow':c.rgb32(200,160,210),
		'woods':c.rgb32(140,150,140),
		'sewer':c.rgb32(160,180,160)}

def init_amb_light():#called 1 time
	amv=AmbientLight(color=c.gray)
	LC.AMBIENT_LIGHT=amv

def env_switch(idx):
	st.day_mode=LC.day_m[idx]
	SkyBox()
	LC.AMBIENT_LIGHT.color=AMB_COL[st.day_mode]
	set_fog(idx)
	if idx in [1,5]:#rain in level 1 and 5
		RainFall()

L_DST={0:(30,100),1:(8,16),2:(3,14),3:(14,20),4:(13,18),5:(8,20),6:(10,20)}
B_DST={0:(0,0),1:(6,12),2:(4,4.5),3:(5,20),4:(8,15),5:(10,20),6:(15,30)}
def set_fog(idx):
	scene.fog_color=FOG_COL[st.day_mode]
	scene.fog_density=L_DST[idx]
	if st.bonus_round:
		scene.fog_density=B_DST[idx]
	del idx

class SkyBox(Sky):
	def __init__(self):
		s=self
		s.bgr='res/background/'
		super().__init__(texture=s.bgr+'sky.jpg',color=SKY_COL[st.day_mode],unlit=False)
		s.setting=SKY_COL[st.day_mode]
		if st.level_index == 1:
			Sequence(s.wood_sky,Wait(1),loop=True)()
			return
		if st.level_index == 5:
			s.thunder_time=3
			Sequence(s.weather_sky,loop=True)()
	def thunder_bolt(self):
		s=self
		s.color=color.white
		LC.bgT.texture=s.bgr+'bg_ruins_th.jpg'
		LC.bgT.texture_scale=LC.bgT.orginal_tsc
		sound.thu_audio(ID=0,pit=random.uniform(.1,.5))
		invoke(lambda:sound.thu_audio(ID=random.randint(1,2),pit=random.uniform(.1,.5)),delay=.5)
		invoke(s.reset_sky,delay=random.uniform(.1,.4))
	def reset_sky(self):
		s=self
		s.color=s.setting
		LC.bgT.texture=s.bgr+'bg_ruins.jpg'
		LC.bgT.texture_scale=LC.bgT.orginal_tsc
		s.thunder_time=random.randint(4,10)
	def weather_sky(self):
		s=self
		if st.weather_thunder:
			s.thunder_time=max(s.thunder_time-time.dt,0)
			if s.thunder_time <= 0:
				s.thunder_bolt()
			return
		if st.bonus_round:
			s.color=c.black
			return
		s.color=s.setting
	def wood_sky(self):
		s=self
		if st.is_death_route:
			s.color=c.rgb32(30,30,60)
			return
		s.color=s.setting

class RainFall(Entity):
	def __init__(self):
		s=self
		super().__init__(model='quad',scale=(1.8,1),z=4,visible=False,color=c.white,parent=camera.ui,unlit=False)
		s.tx_r='res/objects/ev/rain/'
		LC.ACTOR.indoor=.5
		sound.Rainfall()
		s.frm=0
		s.sp=40
		if st.level_index == 5:
			s.sp=50
	def refr_rain(self):
		s=self
		s.frm=min(s.frm+time.dt*s.sp,16.1)
		if s.frm > 16:
			s.frm=0
		s.texture=s.tx_r+f'{str(int(s.frm))}.png'
	def update(self):
		if not st.gproc():
			s=self
			ft=time.dt*2
			s.refr_rain()
			if LC.ACTOR.warped and LC.ACTOR.indoor <= 0:
				s.visible=True
				s.alpha=lerp(s.alpha,.75,ft)
				return
			s.alpha=lerp(s.alpha,0,ft)