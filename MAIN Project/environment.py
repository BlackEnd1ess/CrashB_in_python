from ursina import Sky,Entity,PointLight,AmbientLight,Sequence,Wait,Animation,color,invoke,scene,camera
import status,_loc,sound,time,random

st=status
LC=_loc
c=color

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

##start environment
def env_switch(idx):
	st.day_mode=LC.day_m[idx]
	LC.AMBIENT_LIGHT.color=AMB_COL[st.day_mode]
	set_fog(idx)
	if idx in {1,5}:#rain in level 1 and 5
		if idx == 5:
			Thunderbolt()
		RainFall()

##Fog Distance
L_DST={0:(30,100),1:(10,14),2:(3,12),3:(16,20),4:(13,16),5:(8,18),6:(10,20)}
B_DST={0:(0,0),1:(6,12),2:(4,4.5),3:(5,20),4:(8,15),5:(10,20),6:(15,30)}
def set_fog(idx):
	scene.fog_color=FOG_COL[st.day_mode]
	scene.fog_density=L_DST[idx]
	if st.bonus_round:
		scene.fog_density=B_DST[idx]

##Rainfall Func
class RainFall(Animation):
	def __init__(self):
		s=self
		super().__init__('res/ui/misc/rain/',scale=(1.8,1),fps=40,parent=camera.ui,z=1,visible=False,loop=True)
		LC.ACTOR.indoor=.5
		sound.Rainfall()
		s.fps=40
		if st.level_index == 5:
			s.fps=50
	def update(self):
		s=self
		if st.pause:
			s.pause()
			return
		ft=time.dt*2
		if LC.ACTOR.warped and LC.ACTOR.indoor <= 0:
			s.resume()
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