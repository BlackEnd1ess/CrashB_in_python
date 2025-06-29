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
		st.wumpas_in_level+=1
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
		if st.level_index == 8 and p[1] < -10:
			s.unlit=False
		del p,c_prg,s
	def destroy(self):
		s=self
		if not s.c_purge:
			st.W_RESET.append(s.spawn_pos)
		destroy(s)
	def collect(self):
		cc.wumpa_count(1)
		self.destroy()
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
			if fp < .4:
				s.follow=True

class ExtraLive(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model='quad',texture=lfic,name='exlf',position=pos,scale=(.4,.3),collider=b,unlit=False)
		s.collider=BoxCollider(s,size=Vec3(1,1,1))
		s.follow=False
		del pos,s
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
			s.position=lerp(s.position,(LC.ACTOR.x,LC.ACTOR.y+.2,LC.ACTOR.z),time.dt*20)
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
		if st.level_index == 8:
			s.unlit=False
		del ge,pos,c,s
	def gem_visual(self):
		##color
		s=self
		s.color=LC.GMC[s.gemID]
		##scale - info: blue gem and yellow gem are Y scaled
		if s.gemID in {4,5}:
			s.scale_z={4:s.scale_z/2,5:s.scale_z*1.5}[s.gemID]
		##fake light reflection
		s.shine=SpotLight(position=(s.x-0,s.y+.32,s.z-.18),color=color.gray)
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
			if st.level_index == 6 and st.bonus_round:
				s.shine.color=color.black
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
		del pos,s
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