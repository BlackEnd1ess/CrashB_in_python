from ursina import Sky,Entity,PointLight,AmbientLight,Animation,color,invoke,scene,camera,window
import status,_loc,sound,time,random

st=status
LC=_loc
c=color
def init_amb_light():#called 1 time
	LC.AMBIENT_LIGHT=AmbientLight(color=c.gray)

##start environment
def env_switch():
	LC.AMBIENT_LIGHT.color=LC.AMB_M_COLOR
	window.color=LC.SKY_BG_COLOR
	if st.toggle_thunder:
		Thunderbolt()
	if st.toggle_rain:
		WeatherRain()
	set_fog()
	print(f'<info> Environment Setting for Level {st.level_index} loaded.')

##Fog Distance
def set_fog():
	if st.bonus_round:
		scene.fog_color=LC.FOG_B_COLOR
		scene.fog_density=LC.BN_DST
		return
	scene.fog_density=LC.LV_DST
	scene.fog_color=LC.FOG_L_COLOR

##Rainfall Func
rnf='res/ui/misc/rain/'
class WeatherRain(Entity):
	def __init__(self):
		s=self
		super().__init__(model='quad',texture=None,scale=(1.8,1),parent=camera.ui,z=1,visible=False)
		LC.ACTOR.indoor=.5
		sound.Rainfall()
		s.frm=0
		s.fp=40
		if st.level_index == 5:
			s.fp=50
		del s
	def update(self):
		s=self
		if st.pause:
			return
		s.frm=0 if s.frm > 58.99 else min(s.frm+time.dt*s.fp,58.999)
		s.texture=rnf+f'{int(s.frm)}.png'
		if LC.ACTOR.warped and LC.ACTOR.indoor <= 0:
			s.visible=True
			s.alpha=lerp(s.alpha,1,time.dt*2.3)
			return
		s.alpha=lerp(s.alpha,0,time.dt*2.3)

##Thunder SFX/SKY
skp='res/background/ruin'
class Thunderbolt(Entity):
	def __init__(self):
		s=self
		super().__init__()
		s.flash=PointLight(position=s.position,color=color.black)
		s.org_bgc=window.color
		s.thnt=3
	def thunder_bolt(self):
		s=self
		AC=LC.ACTOR
		if LC.bgT:
			LC.bgT.texture=skp+'_th.jpg'
			LC.bgT.texture_scale=LC.bgT.orginal_tsc
		else:
			window.color=color.white
		s.flash.position=(AC.x,AC.y+3,AC.z)
		s.flash.color=color.white
		sound.thu_audio(ID=0,pit=random.uniform(.1,.5))
		invoke(lambda:sound.thu_audio(ID=random.randint(1,2),pit=random.uniform(.1,.5)),delay=.5)
		invoke(s.reset_sky,delay=random.uniform(.1,.4))
		del AC
	def reset_sky(self):
		s=self
		if LC.bgT:
			LC.bgT.texture=skp+'.jpg'
			LC.bgT.texture_scale=LC.bgT.orginal_tsc
		else:
			window.color=s.org_bgc
		s.flash.color=color.black
		s.thnt=random.randint(4,10)
	def update(self):
		if st.gproc():
			return
		s=self
		s.thnt=max(s.thnt-time.dt,0)
		if s.thnt <= 0:
			s.thunder_bolt()