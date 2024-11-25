from ursina import Entity,BoxCollider,Vec3,SpotLight,color,distance,lerp
import _core,status,sound,ui,_loc,random,time
from ursina.ursinastuff import destroy

lfic='res/ui/icon/crash_live.tga'
w_pa='res/ui/icon/wumpa/'
CRY='crystal/crystal'
i_path='res/item/'
b='box'

st=status
cc=_core
sn=sound
LC=_loc
r=random

##place wumpa fruits
def place_wumpa(pos,cnt,c_prg=False):
	for wpo in range(cnt):
		vpu=pos
		if cnt > 1:
			vpu=pos+(r.uniform(-.1,.1),r.uniform(0,.1),r.uniform(-.1,.1))
		WumpaFruit(p=vpu,c_prg=c_prg)
	del pos,cnt,c_prg,vpu,wpo

class WumpaFruit(Entity):
	def __init__(self,p,c_prg):
		s=self
		super().__init__(model='quad',texture=w_pa+'w0.png',name='wmpf',position=(p[0],p[1],p[2]),scale=.22)
		s.collider=BoxCollider(s,size=Vec3(1,1,1))
		s.follow=False
		s.c_purge=c_prg
		s.spawn_pos=p
		s.frm=0
		del p,c_prg
	def destroy(self):
		s=self
		if not s.c_purge:
			st.W_RESET.append(s.spawn_pos)
		destroy(s)
	def collect(self):
		s=self
		cc.wumpa_count(1)
		s.destroy()
	def update(self):
		if st.gproc():
			return
		s=self
		fp=distance(s,LC.ACTOR)
		if s.follow:
			s.position=lerp(s.position,(LC.ACTOR.x,LC.ACTOR.y+.2,LC.ACTOR.z),time.dt*18)
			return
		if fp < 5:
			ui.wmp_anim(s)
			if fp < .5:
				s.follow=True

class ExtraLive(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model='quad',texture=lfic,name='exlf',position=pos,scale=.3,collider=b)
		s.collider=BoxCollider(s,size=Vec3(1,1,1))
		s.follow=False
	def collect(self):
		cc.give_extra_live()
		destroy(self)
	def p_follow(self):
		s=self
		if distance(s,LC.ACTOR) < .6:
			s.follow=True
	def update(self):
		s=self
		if st.death_event:
			destroy(s)
			return
		if s.follow:
			q=LC.ACTOR
			s.position=lerp(s.position,(q.x,q.y+.2,q.z),time.dt*16)
			return
		s.p_follow()

class GemStone(Entity):
	def __init__(self,pos,c):
		s=self
		ge=i_path+'gemstone/gem'
		if c == 2:
			ge=i_path+'gemstone/gem1'
		elif c == 3:
			ge=i_path+'gemstone/gem2'
		super().__init__(model=ge+'.ply',texture=ge+'.tga',name='gems',scale=.0011,position=pos,rotation_x=-90,collider=b)
		s.gemID=c
		s.gem_visual()
		if c != 0:
			LC.C_GEM=s
			if (c == 5 and st.level_index == 3):
				ui.TrialTimer(t=90)
	def gem_visual(self):
		##color
		s=self
		cu=LC.ge_c[s.gemID]
		s.color=color.rgb32(cu[0],cu[1],cu[2])
		##scale - info: blue gem and yellow gem are Y scaled
		if s.gemID in {4,5}:
			gSC={4:s.scale_z/2,5:s.scale_z*1.5}
			s.scale_z=gSC[s.gemID]
			del gSC
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
		del s_pos,lgx,lgy,lgz
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
		LC.C_GEM=None
		s.shine.color=color.black
		destroy(s.shine)
		destroy(s)
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
		if not LC.C_GEM:
			return
		if abs(s.x-LC.C_GEM.x) < .5:
			if (s.y < LC.C_GEM.y+.25):
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
		s=self
		super().__init__(model=i_path+CRY+'.ply',texture=i_path+CRY+'.tga',name='crys',scale=.0013,rotation_x=-90,position=pos,double_sided=True,color=color.magenta)
		s.glow=Entity(model='quad',texture=i_path+CRY+'_shine.tga',scale=(.5,.8),position=s.position,color=color.magenta,unlit=False)
		s.collider=b
	def collect(self):
		s=self
		st.level_crystal=True
		sn.ui_audio(ID=5)
		st.show_gems=5
		destroy(s.glow)
		destroy(s)
	def update(self):
		if not st.gproc():
			s=self
			kr=distance(s,LC.ACTOR) < 12
			s.glow.visible=kr
			s.visible=kr
			s.rotation_y-=time.dt*70