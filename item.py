from ursina.shaders import *
import _core,status,sound
from ursina import *

item_list=[]
cc=_core

b='box'
i_path='res/item/'
class WumpaFruit(Entity):
	def __init__(self,pos):
		w_model='wumpa/WumpaFruitGameplay.obj'
		self.w_tex='wumpa/images/Crash_WumpaFruit_C.png'
		super().__init__(model=i_path+w_model,texture=i_path+self.w_tex,position=(pos[0],pos[1]+0.3,pos[2]),scale=0.005,collider=b,shader=lit_with_shadows_shader)
		self.world_visible=False
		item_list.append(self)
		if _core.level_ready:
			status.W_RESET.append(self)
	def destroy(self):
		self.parent=None
		self.disable()
		scene.entities.remove(self)
	def collect(self):
		item_list.remove(self)
		self.disable()
		_core.wumpa_count(1)
	def update(self):
		if not status.gproc():
			if self.world_visible:
				self.texture=self.w_tex
				self.show()
				self.rotation_y-=time.dt*200
				return
			self.texture=None
			self.hide()

class ExtraLive(Entity):
	def __init__(self,pos):
		super().__init__(model='quad',texture=i_path+'/extra_live/live.png',position=pos,scale=0.25,collider=b)
		item_list.append(self)
	def collect(self):
		self.disable()
		item_list.remove(self)
		_core.give_extra_live()

class GemStone(Entity):
	def __init__(self,pos,c):
		V=160
		_col={0:color.rgb(V,V,V+10),1:color.rgb(V,0,0),2:color.rgb(0,V,0),3:color.rgb(V,0,V),4:color.rgb(0,0,V),5:color.rgb(V,V,0)}
		_mod={0:'gem/gem.obj',1:'gem/gem.obj',2:'gem/gem1.obj',3:'gem/gem2.obj',4:'gem/gem.obj',5:'gem/gem.obj'}
		_tex={0:'gem/gem.tga',1:'gem/gem.tga',2:'gem/gem1.tga',3:'gem/gem2.tga',4:'gem/gem.tga',5:'gem/gem.tga'}
		super().__init__(model=i_path+_mod[c],texture=i_path+_tex[c],color=_col[c],scale=0.1/1.5,position=pos,double_sided=True,shader=unlit_shader,unlit=False)
		self.collider=b
		if c == 4:
			self.scale_y/=2
		if c == 5:
			self.scale_y*=1.25
		self.gemID=c
		item_list.append(self)
	def collect(self):
		if self.gemID == 0:
			status.level_cle_gem=True
		else:
			status.level_col_gem=True
		Audio(sound.snd_c_gem,volume=1)
		status.show_gems=5
		item_list.remove(self)
		self.disable()
	def update(self):
		if not status.gproc():
			self.rotation_y-=time.dt*60
		if self.gemID == 4:
			if status.level_index == 1 and status.crate_count > 0:
				self.collider=None
				self.disable()
				return

class EnergyCrystal(Entity):
	def __init__(self,pos):
		CRY='crystal/crystal'
		super().__init__(model=i_path+CRY+'.obj',texture=i_path+CRY+'.tga',scale=0.003,position=pos,double_sided=True,color=color.rgb(255,0,255),shader=unlit_shader,unlit=False)
		self.collider=b
		item_list.append(self)
	def collect(self):
		status.level_crystal=True
		Audio(sound.snd_c_gem,volume=1)
		status.show_gems=5
		item_list.remove(self)
		self.disable()
	def update(self):
		if not status.gproc():
			self.rotation_y-=time.dt*70

class TrialClock(Entity):
	def __init__(self,pos):
		Clk='clock/clock'
		super().__init__(model=i_path+Clk+'.obj',texture=i_path+Clk+'.png',position=pos,scale=.003,unlit=False,double_sided=True)
		item_list.append(self)
	def collect(self):
		item_list.remove(self)
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