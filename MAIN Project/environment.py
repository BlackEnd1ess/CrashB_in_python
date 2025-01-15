from ursina import Sky,Entity,PointLight,AmbientLight,Animation,color,invoke,scene,camera,window
import status,_loc,sound,time,random

st=status
LC=_loc
c=color

FOG_COLOR={
	0:c.black,
	1:c.rgb32(20,70,50),
	2:c.white,
	3:c.rgb32(25,45,25),
	4:c.rgb32(160,160,0),
	5:c.black,
	6:c.orange,
	7:c.black}

AMB_COLOR={
	0:c.gray,
	1:c.rgb32(140,140,140),
	2:c.rgb32(200,160,210),
	3:c.rgb32(240,200,170),
	4:c.rgb32(160,180,160),
	5:c.rgb32(140,140,160),
	6:c.rgb32(190,190,190),
	7:c.rgb32(150,150,150)}

SKY_COLOR={
	0:c.black,
	1:c.rgb32(0,60,80),
	2:c.white,
	3:c.rgb32(140,0,60),
	4:c.black,
	5:c.black,
	6:c.orange,
	7:c.black}

def init_amb_light():#called 1 time
	amv=AmbientLight(color=c.gray)
	LC.AMBIENT_LIGHT=amv

##start environment
def env_switch(idx):
	LC.AMBIENT_LIGHT.color=AMB_COLOR[idx]
	set_fog(idx)
	window.color=SKY_COLOR[idx]
	if idx in {1,5}:#rain in level 1 and 5
		if idx == 5:
			Thunderbolt()
		WeatherRain()

##Fog Distance
L_DST={0:(30,100),1:(10,15),2:(3,12),3:(16,20),4:(13,16),5:(8,15),6:(15,20),7:(14,16)}
B_DST={0:(0,0),1:(6,12),2:(4,4.5),3:(5,20),4:(8,15),5:(10,20),6:(15,30),7:(10,20)}
def set_fog(idx):
	scene.fog_color=FOG_COLOR[idx]
	scene.fog_density=L_DST[idx]
	if st.bonus_round:
		scene.fog_density=B_DST[idx]

##Rainfall Func
class WeatherRain(Entity):
	def __init__(self):
		s=self
		s.rnf='res/ui/misc/rain/'
		super().__init__(model='quad',texture=None,scale=(1.8,1),parent=camera.ui,z=1,visible=False)
		LC.ACTOR.indoor=.5
		sound.Rainfall()
		s.frm=0
		s.fp=40
		if st.level_index == 5:
			s.fp=50
	def refr_tex(self):
		s=self
		s.frm=min(s.frm+time.dt*s.fp,58.999)
		if s.frm > 58.99:
			s.frm=0
		s.texture=s.rnf+f'{int(s.frm)}.png'
	def update(self):
		s=self
		if st.pause:
			return
		ft=time.dt*2.3
		s.refr_tex()
		if LC.ACTOR.warped and LC.ACTOR.indoor <= 0:
			s.visible=True
			s.alpha=lerp(s.alpha,1,ft)
			return
		s.alpha=lerp(s.alpha,0,ft)

##Thunder SFX/SKY
class Thunderbolt(Entity):
	def __init__(self):
		s=self
		s.bgr='res/background/'
		super().__init__()
		s.flash=PointLight(position=s.position,color=color.black)
		s.thnt=3
	def thunder_bolt(self):
		s=self
		AC=LC.ACTOR
		LC.bgT.texture=s.bgr+'bg_ruins_th.jpg'
		LC.bgT.texture_scale=LC.bgT.orginal_tsc
		s.flash.position=(AC.x,AC.y+3,AC.z)
		s.flash.color=color.white
		sound.thu_audio(ID=0,pit=random.uniform(.1,.5))
		invoke(lambda:sound.thu_audio(ID=random.randint(1,2),pit=random.uniform(.1,.5)),delay=.5)
		invoke(s.reset_sky,delay=random.uniform(.1,.4))
	def reset_sky(self):
		s=self
		LC.bgT.texture=s.bgr+'bg_ruins.jpg'
		LC.bgT.texture_scale=LC.bgT.orginal_tsc
		s.flash.color=color.black
		s.thnt=random.randint(4,10)
	def update(self):
		if st.gproc():
			return
		s=self
		s.thnt=max(s.thnt-time.dt,0)
		if s.thnt <= 0:
			s.thunder_bolt()