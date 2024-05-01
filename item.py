from ursina.shaders import *
import _core,status,sound,ui
from ursina import *

cc=_core
item_list=['wumpa_fruit',
		'extra_live',
		'gem_stone',
		'energy_crystal',
		'trial_clock']

i_path='res/item/'
b='box'

class WumpaFruit(Entity):
	def __init__(self,pos):
		w_model='wumpa/WumpaFruitGameplay.obj'
		w_tex='wumpa/images/Crash_WumpaFruit_C.png'
		super().__init__(model=w_model,texture=w_tex,position=(pos[0],pos[1]+.3,pos[2]),scale=.005,collider=b,shader=lit_with_shadows_shader,visible=False)
		self.org_tex=self.texture
		if _core.level_ready:
			status.W_RESET.append(self)
	def destroy(self):
		self.parent=None
		self.disable()
		scene.entities.remove(self)
	def collect(self):
		self.disable()
		cc.wumpa_count(1)
	def update(self):
		if not status.gproc():
			if self.visible:
				self.rotation_y-=time.dt*200

class ExtraLive(Entity):
	def __init__(self,pos):
		super().__init__(model='quad',texture=i_path+'/extra_live/live.png',position=pos,scale=0.25,collider=b)
	def collect(self):
		self.disable()
		_core.give_extra_live()

class GemStone(Entity):
	def __init__(self,pos,c):
		if c == 2:
			ge_m=i_path+'gemstone/gem1.ply'
			ge_t=i_path+'gemstone/gem1.tga'
		elif c == 3:
			ge_m=i_path+'gemstone/gem2.ply'
			ge_t=i_path+'gemstone/gem2.tga'
		else:
			ge_m=i_path+'gemstone/gem.ply'
			ge_t=i_path+'gemstone/gem.tga'
		R=120
		ge_c={0:color.rgb(R,R,R+10),1:color.rgb(R,0,0),2:color.rgb(0,R,0),3:color.rgb(R,0,R),4:color.rgb(0,0,R),5:color.rgb(R,R,0)}
		super().__init__(model=ge_m,texture=ge_t,color=ge_c[c],scale=.0011,position=pos,rotation_x=-90,unlit=False)
		self.collider=b
		if c == 4:
			self.scale_z/=2
		if c == 5:
			self.scale_z*=1.25
		self.gemID=c
	def collect(self):
		if self.gemID == 0:
			status.level_cle_gem=True
		else:
			status.level_col_gem=True
		Audio(sound.snd_c_gem,volume=1)
		status.show_gems=5
		self.disable()
	def update(self):
		sli=status.level_index
		geC=self.intersects()
		if not status.gproc():
			self.rotation_y-=time.dt*60
		if self.gemID == 4 and sli == 1 and status.crate_count > 0 or self.gemID == 1 and sli == 2 and status.fails > 0:
			self.collider=None
			self.disable()
			return
		if geC and self.gemID == 0:
			geE=geC.entity
			if str(geE) == 'gem_stone':
				if not self.y == self.y+.5:
					self.y+=time.dt

class EnergyCrystal(Entity):
	def __init__(self,pos):
		CRY='crystal/crystal'
		super().__init__(model=i_path+CRY+'.ply',texture=i_path+CRY+'.tga',scale=.0013,rotation_x=-90,position=pos,double_sided=True,color=color.magenta,shader=unlit_shader,unlit=False)
		self.collider=b
	def collect(self):
		status.level_crystal=True
		Audio(sound.snd_c_gem,volume=1)
		status.show_gems=5
		self.disable()
	def update(self):
		if not status.gproc():
			self.rotation_y-=time.dt*70

class TrialClock(Entity):
	def __init__(self,pos):
		Clk='clock/clock'
		super().__init__(model=i_path+Clk+'.obj',texture=i_path+Clk+'.png',position=pos,scale=.003,unlit=False,double_sided=True)
	def collect(self):
		self.disable()
		status.is_time_trial=True
	def update(self):
		self.rotation_y+=time.dt*120

class TimeRelic(Entity):
	def __init__(self,pos,t):
		tc={0:color.azure,1:color.gold,2:color.rgb(150,150,180)}
		super().__init__(model=i_path+'relic/relic.ply',texture=i_path+'relic/relic.tga',scale=0.004,position=pos,rotation_x=-90,color=tc[t],unlit=False,shader=unlit_shader)
	def update(self):
		if not status.gproc():
			self.rotation_y-=time.dt*70