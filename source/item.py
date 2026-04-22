from ursina import Entity,BoxCollider,Vec3,SpotLight,color,distance,lerp,scene
import _core,status,sound,ui,_loc,random,time,crate
from ursina.ursinastuff import destroy

lfic='res/ui/icon/crash_live.png'
w_pa='res/ui/icon/wumpa/'
CRY='crystal/crystal'
CLK='clock/clock'
RLC='relic/relic'
i_path='res/item/'
b='box'

st=status
cc=_core
sn=sound
LC=_loc
r=random

##place wumpa fruits
def spawn_wumpa(pos,cnt,c_prg=False):
	for wpo in range(cnt):
		vpu=pos
		if cnt > 1:
			vpu=pos+(r.uniform(-.1,.1),r.uniform(0,.1),r.uniform(-.1,.1))
		else:
			vpu=pos+(0,0,r.uniform(-.01,.01))
		WumpaFruit(p=vpu,c_prg=c_prg)
		st.wumpas_in_level+=1
	del pos,cnt,c_prg,vpu,wpo

class WumpaFruit(Entity):
	def __init__(self,p,c_prg):
		s=self
		super().__init__(model='quad',texture=w_pa+'w0.png',name='wmpf',position=(p[0],p[1],p[2]),scale=.22)
		s.collider=BoxCollider(s,size=Vec3(1.25,1.25,1.25))
		s.max_frm=len(LC.wmp_texture)-1+.99
		s.follow=False
		s.c_purge=c_prg
		s.spawn_pos=p
		s.spd=18
		s.frm=0
		s.unlit=bool(st.level_index == 8 and p[1] < -10)
		del p,c_prg,s
	def destroy(self):
		if not self.c_purge:
			st.WMP_RESET.append(self.spawn_pos)
		destroy(self)
	def collect(self):
		cc.wumpa_count(1)
		self.destroy()
	def update(self):
		if st.gproc():
			return
		s=self
		fp=distance(s,LC.ACTOR)
		if s.follow:
			s.position=lerp(s.position,(LC.ACTOR.x,LC.ACTOR.y+.2,LC.ACTOR.z),time.dt*s.spd)
			return
		if fp < 5:
			ui.wmp_anim(s)
			if fp < .4:
				s.follow=True

class ExtraLive(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model='quad',texture=lfic,name='exlf',position=pos,scale=(.4,.3),collider=None,unlit=False)
		s.collider=BoxCollider(s,size=Vec3(1.25,1.25,1.25))
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

sh=f'{i_path}gemstone/gem_shine.png'
class GemStone(Entity):
	def __init__(self,pos,c):
		s=self
		s.gemID=c
		ge=f'{i_path}gemstone/gem'
		if c == 4:
			ge=f'{i_path}gemstone/gem1'
		elif c == 5:
			ge=f'{i_path}gemstone/gem2'
		super().__init__(model=f'{ge}.ply',texture=f'{ge}.png',name='gem',scale=.0011,position=pos,rotation_x=-90,collider=b)
		s.gem_visual()
		if st.level_index == 8:
			s.unlit=False
		LC.C_GEM=s if (c > 0) else None
		s.check_block_position()
		del ge,pos,c,s
	def check_block_position(self):
		s=self
		for vk in scene.entities[:]:
			if not vk or vk == s:
				continue
			if not isinstance(vk,GemStone):
				continue
			if distance(s,vk) < .2:
				vk.position=(s.x,s.y+.225,s.z)
		del vk
	def set_gem_size(self):
		s=self
		if s.gemID in (1,3):
			s.scale_z={1:s.scale_z/2,3:s.scale_z*1.5}[s.gemID]
			return
		s.scale_z=s.scale_z
	def set_gem_color(self):
		s=self
		if s.gemID in LC.GEM_MESH_COLOR:
			s.color=LC.GEM_MESH_COLOR[s.gemID]
			return
		s.color=LC.mesh_normal_gem_color
	def gem_visual(self):
		s=self
		s.set_gem_color()
		s.set_gem_size()
		gm_pos=(s.x-0,s.y+.32,s.z-.18) if s.gemID != 2 else (s.x-0,s.y+.32,s.z-.2)
		s.shine=SpotLight(position=gm_pos,color=s.color)
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
			st.color_gem_id=self.gemID
			st.level_col_gem=True
		sn.ui_audio(ID=5)
		st.show_gems=5
		self.purge()
	def refr_func(self):
		s=self
		s.shine.color=color.black if (st.bonus_round) else color.gray
		s.rotation_y-=time.dt*60
	def update(self):
		if st.gproc():
			return
		s=self
		s.refr_func()
		if cc.gem_challange_fail(s.gemID) or st.relic_challange:
			s.purge()

class EnergyCrystal(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=f'{i_path}{CRY}.ply',texture=f'{i_path}{CRY}.png',name='crys',scale=.0013,rotation_x=-90,position=pos,double_sided=True,color=color.magenta)
		s.glow=Entity(model='quad',texture=f'{i_path}{CRY}_shine.png',scale=(.5,.8),position=s.position,color=color.magenta,unlit=False)
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

class TimeTrialClock(Entity):
	def __init__(self,pos):
		super().__init__(model=f'{CLK}.ply',texture=f'{CLK}.png',position=pos,scale=.0035,color=color.rgb32(240,230,0),double_sided=True,rotation_x=-90,name='clock',collider=b)
		self.rsp=90
		if st.level_index == 8:
			self.unlit=False
	def transform_box(self,bp,l):
		st.BOX_RESET.append((bp.vnum,bp.spawn_pos,bp.poly,bp.mark,bp.c_ID))
		crate.spawn(ID=15,p=bp.position,l=l)
		destroy(bp)
	def check_boxes(self):
		s=self
		for v in scene.entities[:]:
			if v:
				if cc.is_box(v):
					if v.vnum in (1,7):
						s.transform_box(v,1)
					elif v.vnum in (2,6):
						s.transform_box(v,2)
					elif v.vnum == 4:
						s.transform_box(v,3)
					elif v.vnum == 13 and v.c_ID != 0:
						destroy(v)
		del v
	def collect(self):
		self.check_boxes()
		ui.RelicTimer()
		if st.aku_hit > 0:
			st.aku_hit=0
			sn.pc_audio(ID=6,pit=.8)
		TimeRelic(LC.gem_pod_position)
		destroy(self)
	def update(self):
		if st.gproc():
			return
		self.rotation_y+=time.dt*self.rsp

class TimeRelic(Entity):
	def __init__(self,pos,rank=0):
		s=self
		super().__init__(model=f'{i_path}{RLC}.ply',texture=f'{i_path}{RLC}.png',position=pos,scale=.004,rotation_x=-90,name='relic',unlit=False,collider=b)
		s.rank=rank
		s.spd=60
		del s,rank
	def collect(self):
		st.RELIC_TRIAL_DONE=True
		st.relic_rank=self.rank
		sn.ui_audio(ID=5)
		destroy(self)
	def refr_function(self):
		s=self
		if st.relic_challange:
			s.rank=cc.refresh_relic_rank(st.level_index)
		s.rotation_y+=time.dt*s.spd
		s.color=LC.relic_color[s.rank]
	def update(self):
		if st.gproc():
			return
		if st.death_event:
			destroy(self)
			return
		self.refr_function()