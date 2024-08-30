import _core,status,sound,ui,_loc
from time import strftime,gmtime
from ursina.shaders import *
from ursina import *

i_path='res/item/'
b='box'

r=random
cc=_core
sn=sound
##place wumpa fruits
def place_wumpa(pos,cnt):
	for wpo in range(cnt):
		if cnt > 1:
			vpu=pos+(r.uniform(-.1,.1),r.uniform(0,.1),r.uniform(-.1,.1))
		else:
			vpu=pos
		WumpaFruit(p=vpu)

class WumpaFruit(Entity):##2D Animation
	def __init__(self,p):
		self.w_pa='res/ui/icon/wumpa_fruit/'
		super().__init__(model='quad',texture=self.w_pa+'w0.png',position=(p[0],p[1],p[2]),scale=.22)
		self.collider=BoxCollider(self,size=Vec3(1,1,1))
		self.frm=0
		if cc.level_ready and _loc.ACTOR.warped:
			self.auto_purge=True
			return
		self.auto_purge=False
	def destroy(self):
		cc.purge_instance(self)
	def collect(self):
		cc.wumpa_count(1)
		self.destroy()
	def update(self):
		if not status.gproc():
			ui.wmp_anim(self)

class ExtraLive(Entity):
	def __init__(self,pos):
		super().__init__(model='quad',texture=i_path+'/extra_live/live.png',position=pos,scale=.25,collider=b)
		self.collider=BoxCollider(self,size=Vec3(1,1,1))
	def collect(self):
		_core.give_extra_live()
		cc.purge_instance(self)

class GemStone(Entity):
	def __init__(self,pos,c):
		gPA={2:i_path+'gemstone/gem1',3:i_path+'gemstone/gem2'}
		if c in gPA:
			ge_=gPA[c]
		else:
			ge_=i_path+'gemstone/gem'
		R=120
		ge_c={0:color.rgb32(R,R,R+10),1:color.rgb32(R,0,0),2:color.rgb32(0,R,0),3:color.rgb32(R,0,R),4:color.rgb32(0,0,R),5:color.rgb32(R,R,0)}
		super().__init__(model=ge_+'.ply',texture=ge_+'.tga',color=ge_c[c],scale=.0011,position=pos,rotation_x=-90,collider=b)
		gSCA={4:self.scale_z/2,5:self.scale_z*1.5}
		self.gemID=c
		if c in gSCA:
			if c == 5:
				self.purge_time=90
				self.ptext=Text(text=str(self.purge_time),parent=camera.ui,scale=3,position=(.7,-.4),font='res/ui/font.ttf',color=color.rgb32(200,200,100))
			self.scale_z=gSCA[c]
		if c != 0:
			_loc.C_GEM=self
	def gem_fail(self):
		sli=status.level_index
		gID=self.gemID
		if gID == 4 and (sli == 1 and status.crate_count > 0):
			return True
		if gID == 1 and (sli == 2 and status.gem_death):
			return True
		if gID == 5 and self.purge_time <= 0:
			return True
		return False
	def purge(self):
		if self.gemID == 5:
			cc.purge_instance(self.ptext)
		self.collider=None
		cc.purge_instance(self)
		_loc.C_GEM=None
	def collect(self):
		if self.gemID == 0:
			status.level_cle_gem=True
		else:
			status.level_col_gem=True
		sn.ui_audio(ID=5)
		status.show_gems=5
		self.purge()
	def push_gem(self):
		kr=self.intersects()
		if _loc.C_GEM:
			if self.y < _loc.C_GEM.y+.2:
				self.y+=time.dt
		elif kr and isinstance(kr.entity,GemStone):
			self.y=lerp(self.y,self.y+.3,time.dt)
	def update(self):
		if not status.gproc():
			self.rotation_y-=time.dt*60
			if self.gem_fail():
				self.purge()
				return
			if self.gemID == 5 and self.purge_time > 0:
				self.ptext.text=strftime("%M:%S",gmtime(self.purge_time))
				self.purge_time-=time.dt
			if self.gemID == 0:
				self.push_gem()

class EnergyCrystal(Entity):
	def __init__(self,pos):
		CRY='crystal/crystal'
		super().__init__(model=i_path+CRY+'.ply',texture=i_path+CRY+'.tga',scale=.0013,rotation_x=-90,position=pos,double_sided=True,color=color.magenta,shader=unlit_shader,unlit=False)
		self.collider=b
	def collect(self):
		status.level_crystal=True
		sn.ui_audio(ID=5)
		status.show_gems=5
		cc.purge_instance(self)
	def update(self):
		if not status.gproc():
			self.visible=(distance(self,_loc.ACTOR) < 12)
			self.rotation_y-=time.dt*70

class TrialClock(Entity):
	def __init__(self,pos):
		Clk='clock/clock'
		super().__init__(model=i_path+Clk+'.obj',texture=i_path+Clk+'.png',position=pos,scale=.003,unlit=False,double_sided=True)
	def collect(self):
		cc.purge_instance(self)
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