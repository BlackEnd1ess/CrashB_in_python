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
		s=self
		s.w_pa='res/ui/icon/wumpa_fruit/'
		super().__init__(model='quad',texture=s.w_pa+'w0.png',name='wmpf',position=(p[0],p[1],p[2]),scale=.22)
		s.collider=BoxCollider(s,size=Vec3(1,1,1))
		s.c_purge=c_prg
		s.frm=0
	def destroy(self):
		cc.purge_instance(self)
	def collect(self):
		s=self
		cc.wumpa_count(1)
		if not s.c_purge:
			st.W_RESET.append(s.position)
		self.destroy()
	def update(self):
		if not st.gproc():
			ui.wmp_anim(self)

class ExtraLive(Entity):
	def __init__(self,pos):
		super().__init__(model='quad',texture='res/ui/icon/crash_live.tga',name='exlf',position=pos,scale=.3,collider=b)
		self.collider=BoxCollider(self,size=Vec3(1,1,1))
	def collect(self):
		cc.give_extra_live()
		cc.purge_instance(self)
	def update(self):
		if st.death_event:
			cc.purge_instance(self)

class GemStone(Entity):
	def __init__(self,pos,c):
		s=self
		if c == 3:
			ge=i_path+'gemstone/gem2'
		elif c == 2:
			ge=i_path+'gemstone/gem1'
		else:
			ge=i_path+'gemstone/gem'
		super().__init__(model=ge+'.ply',texture=ge+'.tga',name='gems',color=color.gray,scale=.0011,position=pos,rotation_x=-90,collider=b)
		s.gemID=c
		s.gem_visual()
		if c != 0:
			_loc.C_GEM=s
			if (c == 5 and st.level_index == 3):
				ui.TrialTimer(t=90)
				return
		s.purge_time=1
	def gem_visual(self):
		##color
		s=self
		R=220
		ge_c={0:color.rgb32(R-10,R-10,R),#clear gem
			1:color.rgb32(R,0,0),#red gem
			2:color.rgb32(0,R,0),#green gem
			3:color.rgb32(R,0,R),#purple gem
			4:color.rgb32(0,0,R),#blue gem
			5:color.rgb32(R-20,R-20,0)}#yellow gem
		s.color=ge_c[s.gemID]
		##scale - info: blue gem and yellow gem are Y scaled
		if s.gemID in [4,5]:
			gSC={4:s.scale_z/2,5:s.scale_z*1.5}
			s.scale_z=gSC[s.gemID]
		##light reflection
		lgx=0
		lgy=.32
		lgz=.18
		s_pos={0:(s.x-lgx,s.y+lgy,s.z-lgz),
			1:(s.x-lgx,s.y+lgy,s.z-lgz),
			2:(s.x-lgx,s.y+lgy,s.z-lgz),
			3:(s.x-lgx,s.y+lgy,s.z-lgz),
			4:(s.x-lgx,s.y+lgy,s.z-lgz),
			5:(s.x-lgx,s.y+lgy,s.z-lgz)}
		s.shine=SpotLight(position=s_pos[s.gemID],color=color.gray)
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
		s=self
		s.collider=None
		_loc.C_GEM=None
		s.shine.color=color.black
		cc.purge_instance(s.shine)
		cc.purge_instance(s)
	def collect(self):
		if self.gemID == 0:
			st.level_cle_gem=True
		else:
			st.level_col_gem=True
		sn.ui_audio(ID=5)
		st.show_gems=5
		self.purge()
	def push_gem(self):
		s=self
		if not _loc.C_GEM:
			return
		if abs(s.x-_loc.C_GEM.x) < .5:
			if (s.y < _loc.C_GEM.y+.2):
				s.y+=time.dt
	def update(self):
		if not st.gproc():
			s=self
			s.rotation_y-=time.dt*60
			if s.gem_fail():
				s.purge()
				return
			if s.gemID == 0:
				s.push_gem()

class EnergyCrystal(Entity):
	def __init__(self,pos):
		CRY='crystal/crystal'
		super().__init__(model=i_path+CRY+'.ply',texture=i_path+CRY+'.tga',name='crys',scale=.0013,rotation_x=-90,position=pos,double_sided=True,color=color.magenta,shader=unlit_shader,unlit=False)
		self.collider=b
	def collect(self):
		st.level_crystal=True
		sn.ui_audio(ID=5)
		status.show_gems=5
		cc.purge_instance(self)
	def update(self):
		if not st.gproc():
			s=self
			s.visible=(distance(s,_loc.ACTOR) < 12)
			s.rotation_y-=time.dt*70

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