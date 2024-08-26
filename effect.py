from ursina.shaders import *
import status,_core,_loc
from ursina import *
st=status
cc=_core
LC=_loc
ef='res/effects/'
class Sparkle(Entity):
	def __init__(self,pos):
		super().__init__(model='quad',texture=ef+'sparkle.tga',position=pos,scale=.05,shader=unlit_shader)
		self.mode=0
	def update(self):
		if not st.gproc():
			if self.mode == 0:
				self.scale+=Vec3(time.dt/2,time.dt/2,0)
				if self.scale_x > .1:
					self.mode=1
				return
			self.scale-=Vec3(time.dt/2,time.dt/2,0)
			if self.scale_x <= 0:
				_core.purge_instance(self)

class TeslaStroke(Entity):
	def __init__(self,pos):
		super().__init__(position=pos,scale=.001)

class FireThrow(Entity):
	def __init__(self,pos,ro_y):
		super().__init__(model='quad',texture=ef+'fire_ball.png',position=(pos[0],pos[1]+.25,pos[2]),scale=.2,collider='box',shader=unlit_shader,color=random.choice([color.orange,color.red]))
		self.life_time=.5
		self.direc=ro_y
		self.mvs=4
		if ro_y in [90,-90]:
			self.z=self.z+random.uniform(-.1,.1)
	def fly_away(self):
		if self.direc == 90:self.x-=time.dt*self.mvs
		if self.direc == -90:self.x+=time.dt*self.mvs
		if self.direc == 180:self.z+=time.dt*self.mvs
		if self.direc == 0:self.z-=time.dt*self.mvs
	def update(self):
		if not st.gproc():
			tdf=time.dt*1.1
			self.life_time=max(self.life_time-time.dt,0)
			if self.intersects(LC.ACTOR):
				cc.get_damage(LC.ACTOR,rsn=3)
			if self.life_time <= 0:
				cc.purge_instance(self)
				return
			self.scale+=(tdf,tdf,tdf)
			self.fly_away()