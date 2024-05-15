import _core,status,sound,ui,_loc
from ursina.shaders import *
from ursina import *

i_path='res/item/'
b='box'

cc=_core
class WumpaFruit(Entity):
	def __init__(self,pos):
		w_model='wumpa/WumpaFruitGameplay.obj'
		w_tex='wumpa/images/Crash_WumpaFruit_C.png'
		super().__init__(model=w_model,texture=w_tex,position=(pos[0],pos[1]+.3,pos[2]),scale=.005,collider=b,visible=False)
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
		gPA={2:i_path+'gemstone/gem1',3:i_path+'gemstone/gem2'}
		if c in gPA:
			ge_=gPA[c]
		else:
			ge_=i_path+'gemstone/gem'
		R=120
		ge_c={0:color.rgb32(R,R,R+10),1:color.rgb32(R,0,0),2:color.rgb32(0,R,0),3:color.rgb32(R,0,R),4:color.rgb32(0,0,R),5:color.rgb32(R,R,0)}
		super().__init__(model=ge_+'.ply',texture=ge_+'.tga',color=ge_c[c],scale=.0011,position=pos,rotation_x=-90,collider=b,unlit=False)
		gSCA={4:self.scale_z/2,5:self.scale_z*1.5}
		if c in gSCA:
			self.scale_z=gSCA[c]
		if c != 0:
			_loc.C_GEM=self
		self.gemID=c
	def gem_fail(self):
		sli=status.level_index
		gID=self.gemID
		if gID == 4 and (sli == 1 and status.crate_count > 0):
			return True
		if gID == 1 and (sli == 2 and status.gem_death):
			return True
		return False
	def purge(self):
		self.collider=None
		self.parent=None
		self.disable()
		_loc.C_GEM=None
	def collect(self):
		if self.gemID == 0:
			status.level_cle_gem=True
		else:
			status.level_col_gem=True
		Audio(sound.snd_c_gem,volume=1)
		status.show_gems=5
		self.purge()
	def update(self):
		if not status.gproc():
			geC=self.intersects()
			self.rotation_y-=time.dt*60
			if self.gem_fail():
				self.purge()
				return
			if geC and self.gemID == 0:
				geE=geC.entity
				if isinstance(geE,GemStone):
					self.y=lerp(self.y,self.y+.5,time.dt)

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
		tc={0:color.azure,1:color.gold,2:color.rgb32(150,150,180)}
		super().__init__(model=i_path+'relic/relic.ply',texture=i_path+'relic/relic.tga',scale=0.004,position=pos,rotation_x=-90,color=tc[t],unlit=False,shader=unlit_shader)
	def update(self):
		if not status.gproc():
			self.rotation_y-=time.dt*70