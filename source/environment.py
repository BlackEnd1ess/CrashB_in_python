from ursina import Sky,Entity,PointLight,AmbientLight,color,invoke,scene,camera,window,load_texture,Vec2
import status,_loc,sound,time,random,_core,settings
from ursina.ursinastuff import destroy

sn=sound
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
	if settings.debg:
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
class WeatherRain(Entity):
	def __init__(self):
		s=self
		ttxt=f'res/ui/misc/rain/{random.randint(0,4)}.png'
		super().__init__(model='quad',texture=ttxt,scale=(1.8,1),parent=camera.ui,z=1,visible=False,color=color.white,unlit=False)
		s.spd=65 if (st.level_index == 5) else 55
		s.alpha_fade_speed=2.3
		LC.ACTOR.indoor=.5
		sn.Rainfall()
		del s
	def check_indoor(self):
		s=self
		if LC.ACTOR.warped and LC.ACTOR.indoor <= 0:
			s.visible=True
			s.alpha=min(s.alpha+time.dt*s.alpha_fade_speed,1)
			return
		s.alpha=max(s.alpha-time.dt*s.alpha_fade_speed,0)
	def refr_texture(self):
		self.texture_offset+=Vec2(0,.06)
	def update(self):
		s=self
		if st.pause:
			return
		if st.LV_CLEAR_PROCESS:
			destroy(s)
			return
		s.check_indoor()
		s.refr_texture()


##Thunder SFX/SKY
skp='res/background/ruin'
class Thunderbolt(PointLight):
	def __init__(self):
		s=self
		super().__init__(color=color.black,scale=5)
		s.active=False
		s.reset_time=0
		s.tme=1
	def refr_lighbolt(self):
		s=self
		if LC.ACTOR.indoor <= 0:
			s.position=(LC.ACTOR.x+random.uniform(-.5,.5),LC.ACTOR.y+1,LC.ACTOR.z+random.uniform(1,2))
		sn.thu_audio(ID=1,pit=random.uniform(.1,.5))
		s.color=color.white
		s.active=True
	def reset_lightbolt(self):
		s=self
		s.reset_time+=time.dt
		if s.reset_time > .3:
			s.reset_time=0
			s.color=color.black
			sn.thu_audio(ID=random.randint(2,3),pit=random.uniform(.1,.5))
			s.active=False
	def update(self):
		if st.gproc():
			return
		s=self
		if s.active:
			s.reset_lightbolt()
			return
		s.tme-=time.dt
		if s.tme <= 0:
			s.tme=random.randint(4,10)
			s.refr_lighbolt()