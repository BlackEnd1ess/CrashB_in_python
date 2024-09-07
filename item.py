import _core,status,sound,ui,_loc
from ursina.shaders import *
from ursina import *

i_path='res/item/'
b='box'

st=status
cc=_core
sn=sound
r=random

##place wumpa fruits
def place_wumpa(pos,cnt,c_prg=False):
	for wpo in range(cnt):
		if cnt > 1:
			vpu=pos+(r.uniform(-.1,.1),r.uniform(0,.1),r.uniform(-.1,.1))
		else:
			vpu=pos
		WumpaFruit(p=vpu,c_prg=c_prg)

class WumpaFruit(Entity):
	def __init__(self,p,c_prg):
		self.w_pa='res/ui/icon/wumpa_fruit/'
		super().__init__(model='quad',texture=self.w_pa+'w0.png',position=(p[0],p[1],p[2]),scale=.22)
		self.collider=BoxCollider(self,size=Vec3(1,1,1))
		self.c_purge=c_prg
		self.frm=0
	def destroy(self):
		cc.purge_instance(self)
	def collect(self):
		cc.wumpa_count(1)
		if not self.c_purge:
			st.W_RESET.append(self.position)
		self.destroy()
	def update(self):
		if not st.gproc():
			ui.wmp_anim(self)

class ExtraLive(Entity):
	def __init__(self,pos):
		super().__init__(model='quad',texture='res/ui/icon/crash_live.tga',position=pos,scale=.3,collider=b)
		self.collider=BoxCollider(self,size=Vec3(1,1,1))
	def collect(self):
		cc.give_extra_live()
		cc.purge_instance(self)

class GemStone(Entity):
	def __init__(self,pos,c):
		if c == 3:
			ge=i_path+'gemstone/gem2'
		elif c == 2:
			ge=i_path+'gemstone/gem1'
		else:
			ge=i_path+'gemstone/gem'
		super().__init__(model=ge+'.ply',texture=ge+'.tga',color=color.gray,scale=.0011,position=pos,rotation_x=-90,collider=b)
		self.gemID=c
		self.gem_visual()
		if c != 0:
			_loc.C_GEM=self
			if (c == 5 and st.level_index == 3):
				ui.TrialTimer(t=90)
				return
		self.purge_time=1
	def gem_visual(self):
		##color
		R=220
		ge_c={0:color.rgb32(R-10,R-10,R),#clear gem
			1:color.rgb32(R,0,0),#red gem
			2:color.rgb32(0,R,0),#green gem
			3:color.rgb32(R,0,R),#purple gem
			4:color.rgb32(0,0,R),#blue gem
			5:color.rgb32(R-20,R-20,0)}#yellow gem
		self.color=ge_c[self.gemID]
		##scale - info: blue gem and yellow gem are Y scaled
		if self.gemID in [4,5]:
			gSC={4:self.scale_z/2,5:self.scale_z*1.5}
			self.scale_z=gSC[self.gemID]
		##light reflection
		lgx=0
		lgy=.32
		lgz=.18
		s_pos={0:(self.x-lgx,self.y+lgy,self.z-lgz),
			1:(self.x-lgx,self.y+lgy,self.z-lgz),
			2:(self.x-lgx,self.y+lgy,self.z-lgz),
			3:(self.x-lgx,self.y+lgy,self.z-lgz),
			4:(self.x-lgx,self.y+lgy,self.z-lgz),
			5:(self.x-lgx,self.y+lgy,self.z-lgz)}
		self.shine=SpotLight(position=s_pos[self.gemID],color=color.gray)
		Entity(model='quad',scale=.01,position=self.shine.position,alpha=.7)
	def gem_fail(self):
		gi=self.gemID
		if gi == 4 and (st.level_index == 1 and st.crate_count > 0):#blue gem
			return True
		if gi == 1 and (st.level_index == 2 and st.gem_death):#red gem
			return True
		if gi == 5 and (st.level_index == 3 and st.gem_death):#yellow gem
			return True
		return False
	def purge(self):
		self.collider=None
		_loc.C_GEM=None
		self.shine.color=color.black
		cc.purge_instance(self.shine)
		cc.purge_instance(self)
	def collect(self):
		if self.gemID == 0:
			st.level_cle_gem=True
		else:
			st.level_col_gem=True
		sn.ui_audio(ID=5)
		st.show_gems=5
		self.purge()
	def push_gem(self):
		if not _loc.C_GEM:
			return
		if abs(self.x-_loc.C_GEM.x) < .5:
			if (self.y < _loc.C_GEM.y+.2):
				self.y+=time.dt
	def update(self):
		if not st.gproc():
			self.rotation_y-=time.dt*60
			if self.gem_fail():
				self.purge()
				return
			if self.gemID == 0:
				self.push_gem()

class EnergyCrystal(Entity):
	def __init__(self,pos):
		CRY='crystal/crystal'
		super().__init__(model=i_path+CRY+'.ply',texture=i_path+CRY+'.tga',scale=.0013,rotation_x=-90,position=pos,double_sided=True,color=color.magenta,shader=unlit_shader,unlit=False)
		self.collider=b
	def collect(self):
		st.level_crystal=True
		sn.ui_audio(ID=5)
		status.show_gems=5
		cc.purge_instance(self)
	def update(self):
		if not st.gproc():
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
		if not st.gproc():
			self.rotation_y-=time.dt*70