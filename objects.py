import _core,status,item,sound,animation,level,player,_loc,settings
from ursina.shaders import *
from ursina import *

SFX=settings.SFX_VOLUME
st=status
cc=_core
LC=_loc

omf='res/objects/'
m='mesh'
b='box'

#####################
## object functions #
def platform_move(d):
	if d.direct == 0:
		if d.turn == 0:
			d.x+=time.dt*.7
			if d.x >= d.spawn_pos[0]+1:
				d.turn=1
		if d.turn == 1:
			d.x-=time.dt*.7
			if d.x <= d.spawn_pos[0]-1:
				d.turn=0

def unlit_obj(o):
	o.double_sided=True
	o.unlit=False

####################
##multible objects #
#lv1
def spawn_tree_wall(pos,cnt,d):
	tro={0:-45,1:45}
	for tsp in range(0,cnt):
		Tree2D(pos=(pos[0]+random.uniform(-.2,.2),pos[1],pos[2]+tsp*2),rot=tro[d])

def bush(pos,s,c,ro_y=None):
	if ro_y == None:
		ro_y=0
	BUSH=Entity(model='quad',texture=omf+'l1/bush/bush1.png',name='bush',position=pos,scale=s,color=c,rotation_y=ro_y)

#lv2
def plank_bridge(pos,typ,cnt,ro_y,DST):
	for wP in range(cnt):
		plNK={90:lambda:Plank(pos=(pos[0]+wP*DST,pos[1],pos[2]),ro_y=ro_y,typ=typ),
			0:lambda:Plank(pos=(pos[0],pos[1],pos[2]+wP*DST),ro_y=ro_y,typ=typ)}
		plNK[ro_y]()

def pillar_twin(p,ro_y):
	Pillar(pos=(p[0],p[1],p[2]),ro=ro_y)
	Pillar(pos=(p[0]+1.5,p[1],p[2]),ro=ro_y)

#lv3
def block_row(p,cnt,way):
	for sBl in range(cnt):
		bWlo={0:lambda:SingleBlock(pos=(p[0]+.8*sBl,p[1],p[2])),
			1:lambda:SingleBlock(pos=(p[0],p[1],p[2]+.8*sBl))}
		bWlo[way]()

def block_plane(p,cnt):
	for sbX in range(cnt):
		for sbZ in range(cnt):
			SingleBlock(pos=(p[0]+.8*sbX,p[1],p[2]+.8*sbZ))

def side_hills(p,cnt):
	for sHil in range(cnt):
		Entity(model='sphere',texture='grass',position=(p[0],p[1],p[2]+sHil),scale=(1,2+random.uniform(.3,.5),1.5),color=color.rgb32(0,120,0),texture_scale=(8,8))

def multi_tile(p,cnt):#usage [x,y]
	for _tlx in range(cnt[0]):
		for _tly in range(cnt[1]):
			StoneTile(pos=(p[0]+.85*_tlx,p[1],p[2]+.85*_tly))

#lv 4
def swr_multi_ptf(p,cnt):
	for swX in range(cnt[0]):
		for swZ in range(cnt[1]):
			SewerPlatform(pos=(p[0]+.501*swX,p[1],p[2]+.501*swZ))

####################
## level 1 objects #
class Tree2D(Entity):
	def __init__(self,pos,rot):
		tCOL=random.choice([color.rgb32(128,128,128),color.rgb32(200,200,200),color.rgb32(255,255,255)])
		super().__init__(model='quad',texture=omf+'l1/tree/tree'+str(random.randint(1,4))+'.png',scale=2,position=pos,rotation_y=rot,color=tCOL)

class MossPlatform(Entity):
	def __init__(self,p,ptm):
		#scale=.00075
		MVP=omf+'l1/p_moss/moss'
		super().__init__(model='cube',texture=None,position=p,scale=(.6,1,.6),collider=b,visible=False)
		self.opt_model=Entity(model=MVP+'.ply',texture=MVP+'.tga',scale=.75/1000,position=(p[0],p[1]+.475,p[2]),rotation_x=-90,double_sided=True)
		self.spawn_pos=p
		self.ptm=ptm
		self.direct=0
		self.turn=0
		if ptm == 1:
			self.is_sfc=True
			self.a_tme=3
	def dive(self):
		if self.a_tme > 0:self.a_tme-=time.dt
		if self.a_tme <= 0:
			print(time.dt)
			self.a_tme=3
			if self.is_sfc:
				self.is_sfc=False
				self.animate_y(self.y-1,duration=.3)
				Audio(sound.snd_bubbl,volume=SFX)
				return
			self.is_sfc=True
			self.animate_y(self.spawn_pos[1],duration=.3)
	def update(self):
		if not status.gproc() and self.ptm > 0:
			ptA={1:lambda:self.dive(),2:lambda:platform_move(self)}
			ptA[self.ptm]()

class BackgroundWall(Entity):
	def __init__(self,p):
		super().__init__(model=omf+'l1/wall_0/tW_wall.ply',texture=omf+'l1/wall_0/wall_wood.tga',scale=.02,position=p,rotation=(-90,90,0))
		self.curtain=Entity(model='quad',texture=omf+'l1/bush/bush1.png',position=(self.x,self.y,self.z+1.5),scale=(20,6),color=color.rgb32(0,50,0))
		self.inv_wall=Entity(model='cube',scale=(20,6),position=self.position,collider=b,visible=False)
		for bu in range(8):
			aC=random.choice([color.green,color.orange,color.yellow])
			Entity(model='quad',texture=omf+'l1/bush/bush1.png',position=(self.x-8+bu*2,self.y+2.75,self.z-1+random.uniform(.1,.5)),scale=random.uniform(3,4),color=aC)
		unlit_obj(self)

class TreeScene(Entity):
	def __init__(self,pos,s):
		sBU=omf+'l1/bush/bush1.png'
		super().__init__(model=omf+'l1/tree/tree.ply',texture=omf+'l1/tree/wd_scn.tga',rotation_x=-90,scale=s,position=pos)
		self.leaf0=Entity(model='quad',name='t2b1',texture=sBU,position=(self.x-.4,self.y+1.2,self.z-.249),scale=1.6,color=color.rgb32(0,120,0),rotation_y=0)
		self.leaf1=Entity(model='quad',name='t2b2',texture=sBU,position=(self.x+.4,self.y+1.2,self.z-.249),scale=1.6,color=color.rgb32(0,110,0),rotation_y=-1)
		self.wall0=Entity(model='cube',scale=(1,10,1),position=(self.x,self.y+4.6,self.z),visible=False,collider=b)
		unlit_obj(self)

class GrassSide(Entity):
	def __init__(self,pos,ry):
		gr=omf+'l1/grass_side/grass_side'
		super().__init__(model=gr+'1.ply',texture=gr+'.jpg',position=pos,scale=(1,2,1.4),unlit=False,rotation=(-90,ry,0))

####################
## level 2 objects #
class Plank(Entity):
	def __init__(self,pos,typ,ro_y):
		super().__init__(model='cube',texture=omf+'l2/plank/plank.png',scale=(1,.1,.4),position=pos,collider=b,rotation_y=ro_y,texture_scale=(2,2))
		self.spawn_pos=self.position
		if typ == 1:
			self.is_touched=False
			self.color=color.brown
		else:
			self.color=color.gray
		self.typ=typ
	def obj_reset(self):
		self.is_touched=False
		self.position=self.spawn_pos
		self.collider=b
		self.show()
	def fall_down(self):
		self.collider=None
		Audio(sound.snd_break,pitch=.8)
		self.animate_y(self.y-3,duration=.2)
		invoke(self.obj_reset,delay=5)
	def pl_touch(self):
		if not self.is_touched:
			self.is_touched=True
			invoke(self.fall_down,delay=1)
			invoke(self.hide,delay=1.5)

class Ropes(Entity):
	def __init__(self,pos,le):
		super().__init__(model='cube',scale=(.03,.03,le),position=pos,color=color.brown,origin_z=-.5)
		self.dup=Entity(model='cube',scale=self.scale,position=(self.x+1,self.y,self.z),color=color.brown,origin_z=self.origin_z)

class Pillar(Entity):
	def __init__(self,pos,ro):
		super().__init__(model=omf+'l2/pillar/pillar.ply',texture=omf+'l2/pillar/wd_scn1.tga',scale=.025,rotation=ro,position=pos,color=color.rgb32(140,255,255))
		IceCrystal(pos=(self.x,self.y+1.35,self.z+.075))
		unlit_obj(self)

class SnowWall(Entity):
	def __init__(self,pos):
		super().__init__(model=omf+'l2/snow_wall/snow_bonus.ply',texture=omf+'l2/snow_wall/snow_bonus.tga',scale=.02,position=pos,rotation=(-90,-90,0),collider=b)
		unlit_obj(self)

class Rock(Entity):
	def __init__(self,pos):
		super().__init__(model=omf+'l2/rock/rock.ply',color=color.rgb32(40,40,0),rotation_x=-90,position=pos,scale=.5)
		unlit_obj(self)

class IceCrystal(Entity):
	def __init__(self,pos):
		super().__init__(model=omf+'l2/ice_crystal/ice_crystal.ply',texture=omf+'l2/ice_crystal/snow_2.tga',scale=(.025,.02,.03),position=pos,rotation=(-90,45,0),color=color.cyan)
		unlit_obj(self)

class WoodLog(Entity):
	def __init__(self,pos):
		inp='l2/wood_log/wood_log'
		super().__init__(model=omf+inp+'.ply',texture=omf+inp+'.tga',position=pos,scale=(.001,.001,.0015),rotation=(-90,0,0),collider=b)
		Entity(model='cube',texture=texp+'bricks.png',position=(self.x,self.y+.8,self.z-.075),scale=(.5,2,.5),collider=b)
		self.danger=False
		self.or_pos=self.y
		self.stat=0
		unlit_obj(self)
	def update(self):
		if not status.gproc():
			if self.stat == 0:
				self.y+=time.dt
				if self.y >= self.or_pos+1.3:
					self.danger=True
					self.stat=1
			elif self.stat == 1:
				self.y-=time.dt*4
				if self.y <= self.or_pos:
					if cc.is_nearby_pc(n=self,DX=2,DY=2):
						Audio(sound.snd_w_log)
					self.danger=False
					self.stat=0

class IceGround(Entity):
	def __init__(self,pos,sca):
		super().__init__(model='cube',texture=texp+'ice_ground.png',position=pos,scale=sca,collider=b,alpha=.8)
		self.texture_scale=(sca[0],sca[1])

class SnowPlatform(Entity):
	def __init__(self,pos):
		snPL='l2/snow_platform/snow_platform'
		super().__init__(model=omf+snPL+'.ply',texture=omf+snPL+'.tga',position=pos,scale=.0075,rotation_x=-90)
		Entity(model='cube',scale=(.85,1,.85),position=(self.x,self.y-.5,self.z),collider=b,visible=False)
		unlit_obj(self)

class Role(Entity):
	def __init__(self,pos,di):
		rol='l2/role/role'
		super().__init__(model=omf+rol+'.ply',texture=omf+rol+'.tga',rotation=(-90,90,90),position=pos,scale=.01,collider=b)
		self.main_pos=self.position
		self.is_rolling=False
		self.danger=False
		self.roll_wait=1
		self.direc=di
		unlit_obj(self)
	def roll_right(self):
		self.x+=time.dt*2
		self.rotation_x+=time.dt*80
		if self.x >= self.main_pos[0]+1.8:
			self.roll_wait=1
			self.direc=1
	def roll_left(self):
		self.x-=time.dt*2
		self.rotation_x-=time.dt*80
		if self.x <= self.main_pos[0]-1.8:
			self.roll_wait=1
			self.direc=0
	def update(self):
		if not status.gproc():
			if self.roll_wait > 0:
				self.is_rolling=False
				self.roll_wait-=time.dt
				self.danger=False
				if self.roll_wait <= 0:
					if cc.is_nearby_pc(self,DX=5,DY=5):
						Audio(sound.snd_roles)
				return
			if self.roll_wait <= 0:
				self.danger=True
				self.is_rolling=True
				rdi={0:self.roll_right,1:self.roll_left}
				rdi[self.direc]()

####################
## level 3 objects #
class WaterFlow(Animation):
	def __init__(self,pos,sca):
		super().__init__('l3/water_flow/water_flow.gif',scale=sca,texture_scale=(1,sca[1]/4),position=pos,rotation_x=90,fps=40,color=color.rgb32(240,255,240),alpha=.8)
		self.cbst=Entity(model='cube',name='CBst',texture='res/terrain/l3/cobble_stone.png',position=(pos[0],pos[1]-.7,pos[2]+.05),scale=(10,.1,sca[1]),texture_scale=(10,sca[1]))
		WaterHit(p=pos,sc=sca)
	def update(self):
		if not status.gproc() and self.visible:
			self.resume()
			return
		self.pause()

class WaterFall(Entity):
	def __init__(self,pos):
		super().__init__(model='plane',texture=omf+'l3/water_fall/waterf0.png',position=pos,scale=(5,0,1),rotation_x=-90,texture_scale=(10,1),color=color.rgb32(240,255,240))
		Entity(model='plane',color=color.black,scale=(6,1,16),position=(self.x,self.y-.71,self.z+1.3))
		self.y+=1
		self.frm=0
	def update(self):
		if not status.gproc():
			self.frm+=time.dt*7
			if self.frm > 31.75:
				self.frm=0
			self.texture=omf+'l3/water_fall/waterf'+str(int(self.frm))+'.png'

class SceneWall(Entity):
	def __init__(self,pos,s):
		sWCN=omf+'l3/scn_w/'
		super().__init__(model=sWCN+'side'+str(s)+'.ply',texture=sWCN+'water2_scn.tga',position=pos,scale=.04,rotation_x=-90)
		roTY={1:91,2:90}
		self.rotation_y=roTY[s]
		unlit_obj(self)

class TempleWall(Entity):
	def __init__(self,pos,side):
		tmpleW=omf+'l3/temple_wall/w_'+str(side)
		super().__init__(model=tmpleW+'.ply',texture='l3/temple_wall/water_z.tga',position=pos,scale=.025,rotation=(-90,90,0),collider=b)
		unlit_obj(self)

class WoodStage(Entity):
	def __init__(self,pos):
		wdStg=omf+'l3/wood_stage/w_stage'
		super().__init__(model=wdStg+'.ply',texture=omf+'l3/wood_stage/stage_z.tga',position=pos,scale=.03,rotation=(-90,90,0),color=color.rgb32(100,100,0))
		Entity(model='cube',position=(self.x,self.y-.46,self.z-1.5),scale=(4.2,1,1.2),collider=b,visible=False)
		Entity(model='cube',position=(self.x,self.y-.46,self.z+.2),scale=(1.2,1,2.3),collider=b,visible=False)
		unlit_obj(self)

class StoneTile(Entity):
	def __init__(self,pos):
		tlX=omf+'l3/tile/'
		super().__init__(model='cube',position=pos,scale=(.85,.3,.85),collider=b,visible=False)
		self.vis=Entity(model=tlX+'tile.ply',name='STpltf',texture=tlX+'platform_top.png',position=(self.x,self.y,self.z),rotation_x=-90,scale=.35)
		unlit_obj(self.vis)

class MushroomTree(Entity):
	def __init__(self,pos,typ):
		lbP=omf+'l3/mtree_scn/'
		if typ == 1:
			super().__init__(model=lbP+'wtr_BTree1.ply',texture=lbP+'tm_scn.tga',position=pos,scale=.03)
			Entity(model='cube',color=color.blue,scale=(1.35,.5,.5),position=(self.x+.1,self.y+2.1,self.z-1.1),collider=b,visible=False)
			Entity(model='cube',position=(self.x,self.y+3,self.z-.6),scale=(1,7,.5),collider=b,visible=False)
			bush(pos=(self.x+.2,self.y+3.6,self.z-1.3),s=1,c=color.rgb32(0,160,0),ro_y=-35)
			bush(pos=(self.x-.6,self.y+3.6,self.z-1.4),s=1,c=color.rgb32(0,160,0),ro_y=35)
			bush(pos=(self.x-.1,self.y+3.8,self.z-1.45),s=1,c=color.rgb32(0,160,0))
			bush(pos=(self.x+.1,self.y+1.7,self.z-1.75),s=1.3,c=color.rgb32(0,160,0),ro_y=.1)
			bush(pos=(self.x-.4,self.y+1.5,self.z-1.6),s=1.3,c=color.rgb32(0,160,0),ro_y=.1)
		else:
			super().__init__(model=lbP+'wtr_BTree2.ply',texture=lbP+'tm_scn.tga',position=pos,scale=.06,)
			Entity(model='cube',color=color.blue,scale=(.75,.5,.6),position=(self.x+.05,self.y-.1,self.z),collider=b,visible=False)
			Entity(model='cube',position=(self.x,self.y+1.5,self.z+.5),scale=(1,3,.5),collider=b,visible=False)
		self.rotation=(-90,90,0)
		unlit_obj(self)


####################
## level 4 objects #
class SewerTunnel(Entity):
	def __init__(self,pos):
		_sPA=omf+'l4/scn/'
		super().__init__(model=_sPA+'tunnel.ply',texture=_sPA+'sewer2.tga',position=pos,scale=(.032,.034,.03),rotation=(-90,90,0),double_sided=True)

class SewerEscape(Entity):
	def __init__(self,pos):
		_SE=omf+'l4/scn/'
		super().__init__(model=_SE+'pipe_1.ply',texture=_SE+'sewers.tga',position=pos,scale=.045,rotation=(-90,90,0),double_sided=True)

class SewerPlatform(Entity):
	def __init__(self,pos):
		pPF=omf+'l4/scn/'
		super().__init__(model='cube',scale=(.5,.2,.5),collider=b,position=pos,alpha=.7,visible=False)
		self.vis=Entity(model=pPF+'ptf.ply',texture=pPF+'swr_ptf.tga',position=(self.x,self.y+.05,self.z),scale=.02,rotation_x=-90)
		unlit_obj(self.vis)

###################
##################
## logic objects #
class IndoorZone(Entity):## disable rain
	def __init__(self,pos,sca):
		super().__init__(model='cube',scale=sca,position=pos,collider=b,visible=True,alpha=.3)
	def collect(self):
		LC.ACTOR.indoor=.3

class FallingZone(Entity):## falling
	def __init__(self,pos,s):
		super().__init__(model='cube',collider=b,scale=s,position=pos,visible=False)

class WaterHit(Entity):## collider for water
	def __init__(self,p,sc):
		super().__init__(model='cube',collider=b,position=p,scale=(sc[0],.2,sc[1]),visible=False)

class CrateScore(Entity):## level reward
	def __init__(self,pos):
		ev='res/crate/'
		super().__init__(model=ev+'cr_t0.ply',texture=ev+'1.png',alpha=.4,scale=.18,position=pos,origin_y=.5)
		self.cc_text=Text(parent=scene,position=(self.x-.2,self.y,self.z),text=None,font='res/ui/font.ttf',color=color.rgb32(255,255,100),scale=10)
	def update(self):
		if not st.gproc():
			if st.crates_in_level <= 0 or st.is_time_trial or (LC.C_GEM and distance(self,LC.C_GEM) < .5):
				self.cc_text.hide()
				self.hide()
			else:
				self.cc_text.show()
				self.show()
				self.cc_text.text=str(st.crate_count)+'/'+str(st.crates_in_level)
				self.rotation_y-=120*time.dt
			if st.crates_in_level > 0 and st.crate_count >= st.crates_in_level:
				item.GemStone(pos=(self.x,self.y-.3,self.z),c=0)
				Audio(sound.snd_rward)
				self.cc_text.disable()
				self.disable()

class Corridor(Entity):
	def __init__(self,pos):
		super().__init__(model=omf+'l1/w_corr/corridor.ply',texture=omf+'l1/w_corr/f_room.tga',scale=.1,position=pos,rotation=(-90,90,0))
		self.wall0=Entity(model='cube',visible=False,scale=(3,3,2.2),position=(self.x+2.3,self.y,self.z),collider=b)
		self.wall1=Entity(model='cube',visible=False,scale=(3,3,2.2),position=(self.x-2.3,self.y,self.z),collider=b)
		self.wall1=Entity(model='cube',visible=False,scale=(3,3,2.2),position=(self.x,self.y+3,self.z),collider=b)
		IndoorZone(pos=(self.x,self.y+1.6,self.z),sca=3)
		unlit_obj(self)

class StartRoom(Entity):## game spawn point
	def __init__(self,pos,lvID):
		super().__init__(model=omf+'ev/s_room/room1.ply',texture=omf+'ev/s_room/room.tga',position=pos,scale=(.07,.07,.08),rotation=(270,90))
		self.floor0=Entity(model='cube',collider=b,position=(self.x,self.y+.6,self.z-.2),scale=(1.7,.5,1.7),visible=False)
		self.floor1=Entity(model='cube',collider=b,position=(self.x,self.y+.2,self.z+1.7),scale=(2,.5,2),visible=False)
		self.wall0=Entity(model='cube',collider=b,position=(self.x-1,self.y+1.5,self.z),scale=(.4,13,6),visible=False)
		self.wall1=Entity(model='cube',collider=b,position=(self.x+1,self.y+1.5,self.z),scale=(.4,13,6),visible=False)
		self.bck0=Entity(model='cube',collider=b,position=(self.x,self.y+1.5,self.z-1),scale=(5,13,.6),visible=False)
		self.ceil=Entity(model='cube',name='clr1',collider=b,position=(self.x,self.y+2.6,self.z-.2),scale=(6,1,6),visible=False,alpha=.4)
		self.curt=Entity(model='plane',position=(self.x,self.y+0.01,self.z),color=color.black,scale=3)
		RoomDoor(pos=(self.x,self.y+1.9,self.z+2.3),typ=0)
		player.CrashB(pos=(self.x,self.y+.85,self.z-.1))
		cc.preload_items()
		status.checkpoint=(self.x,self.y+2,self.z)
		camera.position=(self.x,self.y+2,self.z-3)
		IndoorZone(pos=(self.x,self.y+1.5,self.z),sca=(3,2,5))
		unlit_obj(self)
		if lvID > 0:
			m_info={1:lambda:level.level1(),
					2:lambda:level.level2(),
					3:lambda:level.level3(),
					4:lambda:level.level4(),
					5:lambda:level.test()}
			m_info[lvID]()

class EndRoom(Entity):## finish level
	def __init__(self,pos,c):
		eR=omf+'ev/e_room/e_room'
		super().__init__(model=eR+'.ply',texture=eR+'.tga',scale=.025,rotation=(-90,90,0),position=pos,color=c,unlit=False)
		self.curt=Entity(model='plane',color=color.black,scale=(4,1,16),position=(self.x-1,self.y-1.8,self.z+3))
		self.grnd=Entity(model='cube',scale=(4,1,16),position=(self.x-1,self.y-2,self.z+3),collider=b,visible=False)
		self.wa_l=Entity(model='cube',scale=(1,3,16),position=(self.x-2.2,self.y,self.z+3),collider=b,visible=False)
		self.wa_r=Entity(model='cube',scale=(1,3,16),position=(self.x,self.y,self.z+3),collider=b,visible=False)
		self.ceil=Entity(model='cube',name='clr2',scale=(5,3,16),position=(self.x-1,self.y+1.4,self.z+3),collider=b,visible=False)
		self.bck=Entity(model='cube',scale=(6,4,2),position=(self.x,self.y,self.z+9),collider=b,visible=False)
		self.pod1=Entity(model='cube',scale=(6,1,2.5),position=(self.x-1,self.y-1.85,self.z+.45),collider=b,visible=False)
		self.pod2=Entity(model='cube',scale=(.85,1,.85),position=(self.x-1.1,self.y-1.6,self.z+.3),collider=b,visible=False)
		self.pod3=Entity(model='cube',scale=(1.6,1,1),position=(self.x-1.1,self.y-1.5,self.z+6.5),collider=b,visible=False)
		Entity(model='cube',scale=(20,10,.1),position=(self.x,self.y-5,self.z+16),color=color.black)
		LevelFinish(p=(self.x-1.1,self.y-1.4,self.z+7),V=False)
		RoomDoor(pos=(self.x-1.1,self.y+.25,self.z-4.78),typ=1)
		CrateScore(pos=(self.x-1.1,self.y-.7,self.z))
		IndoorZone(pos=(self.x-1,self.y,self.z+3),sca=3)
		if status.level_index == 1 and not 4 in status.COLOR_GEM:
			item.GemStone(pos=(self.x-1.1,self.y-1,self.z),c=4)
		elif status.level_index == 2 and not 1 in status.COLOR_GEM:
			item.GemStone(pos=(self.x-1.1,self.y-1,self.z),c=1)
		self.double_sided=True
		self.unlit=False

class RoomDoor(Entity):## door for start and end room
	def __init__(self,pos,typ):
		self.dPA=omf+'ev/door/'
		super().__init__(model=self.dPA+'u0.ply',texture=self.dPA+'u_door.tga',position=pos,scale=.001,rotation_x=90,collider=b)
		self.door_part=Entity(model=self.dPA+'d0.ply',name='door_part',texture=self.dPA+'d_door.tga',position=(self.x,self.y+.1,self.z),scale=.001,rotation_x=90,collider=b)
		self.DS={0:2,1:3}
		self.d_open=False
		self.typ=typ
		unlit_obj(self)
		unlit_obj(self.door_part)
	def update(self):
		if not status.gproc():
			if distance(self,LC.ACTOR) < self.DS[self.typ]:
				if not self.d_open:
					self.d_open=True
					animation.door_open(self)
					Audio(sound.snd_d_opn)
				return
			if self.d_open:
				self.d_open=False
				animation.door_close(self)
				Audio(sound.snd_d_opn,pitch=.9)

class BonusPlatform(Entity):## switch -> bonus round
	def __init__(self,pos):
		sIN='ev/bonus/bonus'
		super().__init__(model=omf+sIN+'.ply',texture=omf+sIN+'.tga',collider=b,scale=-.001,rotation_x=90,position=pos)
		self.target=LC.ACTOR
		self.orginal_pos=self.position
		self.catch_player=False
		self.air_time=0
		unlit_obj(self)
	def update(self):
		if not status.gproc() and LC.ACTOR != None:
			if st.bonus_solved:
				self.visible=False
				self.collider=None
				return
			if self.catch_player:
				cc.platform_floating(m=self,c=self.target)

class GemPlatform(Entity):## gem platform
	def __init__(self,pos,t):
		if t in status.COLOR_GEM:
			ne='gem_ptf'
			self.is_enabled=True
		else:
			ne='gem_ptf_e'
			self.is_enabled=False
		L=180
		GMC={0:color.rgb32(130,130,140),1:color.rgb32(L,0,0),2:color.rgb32(0,L,0),3:color.rgb32(L-50,0,L-50),4:color.rgb32(0,0,L+40),5:color.rgb32(L-30,L-30,0)}
		super().__init__(model=omf+'ev/'+ne+'/'+ne+'.ply',texture=omf+'ev/'+ne+'/'+ne+'.tga',rotation_x=-90,scale=0.001,position=pos,collider=b,double_sided=True)
		self.bg_darkness=Entity(model=Circle(16,mode='ngon',thickness=.1),position=(self.x,self.y-.011,self.z),rotation_x=90,color=color.black,scale=.7,alpha=.98)
		self.target=LC.ACTOR
		self.orginal_pos=self.position
		self.catch_player=False
		self.air_time=0
		self.color=GMC[t]
		if not self.is_enabled:
			self.collider=None
			self.bg_darkness.hide()
		unlit_obj(self)
	def update(self):
		if not status.gproc() and LC.ACTOR != None:
			if self.is_enabled:
				self.bg_darkness.position=(self.x,self.y-.01,self.z)
				self.rotation_y+=time.dt*20
				if self.catch_player:
					cc.platform_floating(m=self,c=self.target)
					return

class LevelFinish(Entity):## finish level
	def __init__(self,p,V):
		super().__init__(model=omf+'ev/podium/gear.obj',collider=b,texture=omf+'ev/podium/gear_diffuse.png',scale=(.6,.8,.6),position=p,visible=V)
		self.prt_snd=Audio(sound.snd_portl,volume=0,loop=True)
	def update(self):
		if not status.gproc() and LC.ACTOR != None:
			if cc.is_nearby_pc(n=self,DX=4,DY=3):
				self.prt_snd.volume=1
			else:
				self.prt_snd.volume=0

class CamSwitch(Entity):## allow cam move y if player collide with them
	def __init__(self,pos,sca):
		super().__init__(model='cube',position=pos,scale=sca,collider=b,visible=False,alpha=.5)
	def collect(self):#avoid pyhsics with them
		if not status.gproc() and LC.ACTOR != None:
			camera.y=lerp(camera.y,LC.ACTOR.y+1.2,time.dt*2)

class LevelScene(Entity):
	def __init__(self,pos,sca):
		bg={0:'0.png',1:'res/sprite/bg_woods.png',2:''}
		super().__init__(model='quad',texture=bg[status.level_index],scale=sca,position=pos,texture_scale=(sca[0]/50,1),unlit=False)

class LODProcess(Entity):
	def __init__(self):
		super().__init__()
		self.rtime=.5
	def wmp_lod(self,w,p):
		if distance(w,p) < 8:
			w.enabled=True
			return
		w.enabled=False
	def crt_lod(self,c,p):
		if distance(c,p) < 16:
			c.show()
			return
		c.hide()
	def enm_lod(self,e,p):
		if distance(e,p) < 20:
			e.enabled=True
			return
		e.enabled=False
	def vwi_lod(self,v,p):
		if p.z > v.z+2 or v.z > p.z+28:
			v.enabled=False
			return
		v.enabled=True
	def refr(self):
		for b in scene.entities[:]:
			ac=LC.ACTOR
			if isinstance(b,item.WumpaFruit):
				self.wmp_lod(w=b,p=ac)
			elif cc.is_crate(b):
				self.crt_lod(c=b,p=ac)
			elif cc.is_enemie(b):
				self.enm_lod(e=b,p=ac)
			elif str(b) in LC.LOD_LST:
				self.vwi_lod(v=b,p=ac)
	def update(self):
		if not status.gproc():
			if self.rtime > 0:
				self.rtime-=time.dt
				if self.rtime <= 0:
					self.rtime=.5
					self.refr()

###################
## global objects #
class InvWall(Entity):
	def __init__(self,pos,sca):
		super().__init__(model='cube',position=pos,scale=sca,visible=False,collider=b,color=color.red)

class SingleBlock(Entity):
	def __init__(self,pos):
		sBL=omf+'l3/sblock/sblock'
		super().__init__(model=sBL+'.obj',texture=sBL+'.png',scale=(.8,.5,.8),collider=b,position=pos)
		unlit_obj(self)

class Water(Animation):
	def __init__(self,pos,s,c,a,typ):
		super().__init__(omf+'ev/water/water.gif',position=pos,scale=(s[0],s[1]),rotation_x=90,fps=20,color=c,alpha=a)
		self.typ=typ
		if typ == 1:
			self.texture_scale=(3,12)
			self.electric=False
			self.active=False
			self.unlit=False
			self.transp=a
			self.e_time=5
		if typ == 2:
			WaterHit(p=(pos[0],pos[1]-.1,pos[2]),sc=s)
			self.texture_scale=(s[0]/4,s[1]/4)
	def set_normal(self):
		self.electric=False
		self.active=False
		self.color=color.rgb(100,100,130)
		self.alpha=self.transp
		self.shader=lit_with_shadows_shader
	def set_danger(self):
		Audio(sound.snd_elect,volume=SFX,pitch=.9)
		self.electric=True
		self.active=True
		self.shader=unlit_shader
		self.texture_scale=(4,16)
		self.color=color.yellow
		self.slpha=self.transp
		invoke(self.set_normal,delay=2)
	def update(self):
		if not status.gproc() and self.visible:
			self.resume()
			if self.typ == 1 and self.e_time > 0:
				if not self.active:
					self.e_time-=time.dt
					if self.e_time <= 0:
						self.e_time=5
						self.set_danger()
			return
		self.pause()

class mTerrain(Entity):
	def __init__(self,pos,sca,typ):
		terra='res/terrain/l'+str(status.level_index)+'/'
		super().__init__(model='cube',position=pos,collider=b,scale=sca,texture=terra+typ,texture_scale=(sca[0],sca[2]))

class mBlock(Entity):
	def __init__(self,pos,sca):
		cHo=st.level_index
		PA='res/terrain/l'+str(cHo)+'/'
		tPL={0:'grass.png',1:'grass.png',2:'snow.png',3:'moss.png',4:'snow.png'}
		wPL={0:'grass.png',1:'bricks.png',2:'ice_wall.png',3:'moss.png',4:'ice_wall.png'}
		super().__init__(model='cube',texture=PA+tPL[cHo],position=pos,scale=(sca[0],.25,sca[1]),collider=b)
		self.mWall=Entity(model='cube',texture=wPL[cHo],scale=(sca[0]-.01,1,sca[1]),position=(self.x,self.y-(self.scale_y*2.5),self.z+.01),collider=b)
		vts=(sca[0],1)
		if sca[1] > 2:
			vts=(sca[0],sca[1]/2)
		self.mWall.texture_scale=(sca[0],1)
		self.texture_scale=vts