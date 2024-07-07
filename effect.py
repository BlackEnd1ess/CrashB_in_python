from ursina.shaders import *
import status,_core,_loc
from ursina import *

ef='res/effects/'

class Sparkle(Entity):
	def __init__(self,pos):
		super().__init__(model='quad',texture=ef+'sparkle.tga',position=pos,scale=.05,shader=unlit_shader)
		self.mode=0
	def update(self):
		if not status.gproc():
			if self.mode == 0:
				self.scale+=Vec3(time.dt/2,time.dt/2,0)
				if self.scale_x > .1:
					self.mode=1
				return
			self.scale-=Vec3(time.dt/2,time.dt/2,0)
			if self.scale_x <= 0:
				self.disable()