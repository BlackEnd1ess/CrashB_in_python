import _core,status,item,sound,animation,level,player,_loc,settings,effect
from ursina.shaders import *
from ursina import *

SFX=settings.SFX_VOLUME
st=status
sn=sound
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
		return
	if d.direct == 1:
		if d.turn == 0:
			d.z+=time.dt*.7
			if d.z >= d.spawn_pos[2]+1:
				d.turn=1
		if d.turn == 1:
			d.z-=time.dt*.7
			if d.z <= d.spawn_pos[2]-1:
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

def spawn_ice_wall(pos,cnt,d):
	ws={0:90,1:-90}
	for icew in range(cnt):
		SnowHill(pos=(pos[0],pos[1],pos[2]+icew*8.2),ro_y=ws[d])

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

#lv 5
def spw_ruin_ptf(p,cnt,way):
	for rpv in range(cnt):
		if way == 0:
			RuinsBlock(pos=(p[0]+rpv*.75,p[1],p[2]))
		else:
			RuinsBlock(pos=(p[0],p[1],p[2]+rpv*.75))

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
		super().__init__(model='cube',name='mptf',texture=None,position=p,scale=(.6,1,.6),collider=b,visible=False)
		self.opt_model=Entity(model=MVP+'.ply',texture=MVP+'.tga',scale=.75/1000,position=(p[0],p[1]+.475,p[2]),rotation_x=-90,double_sided=True)
		self.spawn_pos=p
		self.ta=LC.ACTOR
		self.ptm=ptm
		self.turn=0
		if ptm > 0:
			if self.ptm == 1:
				self.is_sfc=True
				self.a_tme=3
			ddg={1:0,2:0,3:1}
			self.direct=ddg[ptm]
	def mv_player(self):
		if not self.ta.walking and self.ptm > 1:
			self.ta.x=self.x
			self.ta.z=self.z
	def dive(self):
		self.a_tme=max(self.a_tme-time.dt,0)
		if self.a_tme == 0:
			self.a_tme=3
			if self.is_sfc:
				self.is_sfc=False
				self.opt_model.animate_y(self.opt_model.y-1,duration=.3)
				self.animate_y(self.y-1,duration=.3)
				sn.obj_audio(ID=6)
				return
			self.is_sfc=True
			self.animate_y(self.spawn_pos[1],duration=.3)
			self.opt_model.animate_y(self.spawn_pos[1]+.475,duration=.3)
	def update(self):
		if not st.gproc() and self.ptm > 0:
			if self.ptm in [2,3]:
				platform_move(self)
				self.opt_model.x=self.x
				self.opt_model.z=self.z
				return
			self.dive()

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
		sn.crate_audio(ID=2,pit=.8)
		self.animate_y(self.y-3,duration=.2)
		invoke(self.obj_reset,delay=5)
	def pl_touch(self):
		if not self.is_touched:
			self.is_touched=True
			invoke(self.fall_down,delay=1)
			invoke(self.hide,delay=1.5)

class Ropes(Entity):
	def __init__(self,pos,le):
		rpt=omf+'l2/rope/rope_pce.jpg'
		super().__init__(model='cube',scale=(.03,.03,le),texture=rpt,position=pos,texture_scale=(1,le*8),origin_z=-.5)
		self.dup=Entity(model='cube',scale=self.scale,position=(self.x+1,self.y,self.z),texture=rpt,texture_scale=(1,le*8),origin_z=self.origin_z)

class Pillar(Entity):
	def __init__(self,pos,ro):
		ppt=omf+'l2/pillar/s_pillar'
		super().__init__(model=ppt+'.ply',texture=ppt+'_0.jpg',scale=.2,rotation=ro,position=pos,color=color.rgb32(140,255,255),collider='mesh')
		IceCrystal(pos=(self.x,self.y+1.1,self.z+.075))
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
		super().__init__(model=omf+'l2/ice_crystal/ice_crystal.ply',name='icec',texture=omf+'l2/ice_crystal/snow_2.tga',scale=(.025,.02,.03),position=pos,rotation=(-90,45,0),color=color.cyan)
		unlit_obj(self)

class WoodLog(Entity):
	def __init__(self,pos):
		inp=omf+'l2/wood_log/wood_log'
		super().__init__(model=inp+'.ply',texture=inp+'.tga',name='wdlg',position=pos,scale=(.001,.001,.0015),rotation=(-90,0,0),collider=b)
		Entity(model='cube',texture='res/terrain/l1/bricks.png',position=(self.x,self.y+.8,self.z-.075),scale=(.5,2,.5),collider=b)
		self.danger=True
		self.or_pos=self.y
		self.stat=0
		unlit_obj(self)
	def reset_pos(self):
		self.y+=time.dt
		if self.y >= self.or_pos+1.3:
			self.danger=True
			self.stat=1
	def stomp(self):
		self.y-=time.dt*4
		if self.y <= self.or_pos:
			if distance(self,LC.ACTOR) < 2:
				sn.obj_audio(ID=3)
			self.danger=False
			self.stat=0
	def update(self):
		if not st.gproc() and self.visible:
			if self.intersects(LC.ACTOR) and self.danger:
				cc.get_damage(LC.ACTOR,rsn=1)
			ttr={0:self.reset_pos,1:self.stomp}
			ttr[self.stat]()

class IceGround(Entity):
	def __init__(self,pos,sca):
		super().__init__(model='cube',name='iceg',texture='res/terrain/l2/ice_ground.png',position=pos,scale=sca,collider=b,alpha=.8)
		self.texture_scale=(sca[0],sca[1])
		self.ta=LC.ACTOR
	def mv_player(self):
		self.ta.is_slippery=self.ta.landed

class SnowHill(Entity):
	def __init__(self,pos,ro_y):
		ep=omf+'l2/snow_hill/snow_hills'
		super().__init__(model=ep+'.ply',texture=ep+'.jpg',position=pos,scale=(.6,.5,.4),rotation=(-90,ro_y,0))

class IceChunk(Entity):
	def __init__(self,pos,rot,typ):
		ice_ch=omf+'l2/ice_pce/ice_pce'
		super().__init__(model=ice_ch+'_'+str(typ)+'.ply',texture=ice_ch+'.jpg',position=pos,scale=.8,rotation=rot)

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
			invoke(self.p_snd,delay=.5)
	def roll_left(self):
		self.x-=time.dt*2
		self.rotation_x-=time.dt*80
		if self.x <= self.main_pos[0]-1.8:
			self.roll_wait=1
			self.direc=0
			invoke(self.p_snd,delay=.5)
	def p_snd(self):
		if distance(self,LC.ACTOR) < 3:
			sn.obj_audio(ID=4)
	def update(self):
		if not st.gproc() and self.visible:
			if self.intersects(LC.ACTOR) and self.danger:
				cc.get_damage(LC.ACTOR,rsn=1)
			self.roll_wait=max(self.roll_wait-time.dt,0)
			if self.roll_wait <= 0:
				self.is_rolling=True
				self.danger=True
				rdi={0:self.roll_right,1:self.roll_left}
				rdi[self.direc]()
				return
			self.is_rolling=False
			self.danger=False

####################
## level 3 objects #
class WaterFlow(Entity):
	def __init__(self,pos,sca):
		self.wtr_t=omf+'l3/water_flow/'
		super().__init__(model='plane',texture=self.wtr_t+'water_flow0.tga',scale=(sca[0],.1,sca[1]),texture_scale=(1,11),position=pos,color=color.rgb32(170,170,170),alpha=.8)
		self.cbst=Entity(model='cube',name='CBst',texture='res/terrain/l3/cobble_stone.png',position=(pos[0],pos[1]-.7,pos[2]+.05),scale=(10,.1,sca[1]),texture_scale=(10,sca[1]))
		WaterHit(p=(pos[0],pos[1]-.1,pos[2]),sc=sca)
		self.frm=0
	def update(self):
		if not st.gproc():
			self.frm+=time.dt*9
			if self.frm > 3.9:
				self.frm=0
			self.texture=self.wtr_t+'water_flow'+str(int(self.frm))+'.tga'

class WaterFall(Entity):
	def __init__(self,pos):
		self.pa=omf+'l3/water_fall/waterf'
		super().__init__(model='plane',name='wtfa',texture=self.pa+'0.png',position=pos,scale=(5,0,1),rotation_x=-90,texture_scale=(10,1),color=color.rgb32(240,255,240))
		Entity(model='plane',color=color.black,scale=(12,1,20),position=(self.x,self.y-.7,self.z+1.3))
		self.y+=1
		self.frm=0
	def update(self):
		if not st.gproc():
			self.frm+=time.dt*7
			if self.frm > 31.9:
				self.frm=0
			self.texture=self.pa+str(int(self.frm))+'.png'

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
		self.vis=Entity(model=tlX+'tile.ply',name='stL',texture=tlX+'platform_top.png',position=(self.x,self.y,self.z),rotation_x=-90,scale=.35)
		unlit_obj(self.vis)

class MushroomTree(Entity):
	def __init__(self,pos,typ):
		lbP=omf+'l3/mtree_scn/'
		if typ == 1:
			super().__init__(model=lbP+'wtr_BTree1.ply',texture=lbP+'tm_scn.tga',position=pos,scale=.03)
			Entity(model='cube',color=color.blue,scale=(1.35,.5,.5),position=(self.x+.1,self.y+2.15,self.z-1.1),collider=b,visible=False)
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

class Foam(Entity):
	def __init__(self,pos):
		self.t=omf+'l3/foam/'
		super().__init__(model='quad',texture=self.t+'0.png',position=pos,scale=(5,1),texture_scale=(10,1),rotation_x=90)
		self.frm=0
	def update(self):
		if not st.gproc():
			self.frm+=time.dt*6
			if self.frm > 15.9:
				self.frm=0
			self.texture=self.t+str(int(self.frm))+'.png'


####################
## level 4 objects #
class SewerTunnel(Entity):
	def __init__(self,pos,c=color.white):
		_sPA=omf+'l4/scn/'
		super().__init__(model=_sPA+'tunnel.ply',texture=_sPA+'sewer2.tga',position=pos,color=c,scale=(.032,.034,.03),rotation=(-90,90,0),double_sided=True,collider='mesh')

class SewerEscape(Entity):
	def __init__(self,pos,typ=None,c=color.white):
		_SE=omf+'l4/scn/'
		super().__init__(model=_SE+'pipe_1.ply',texture=_SE+'sewers.tga',position=pos,scale=.048,color=c,rotation=(-90,90,0),double_sided=True)
		Entity(model='cube',scale=(.3,8,11),position=(self.x-1.5,self.y+3,self.z+2),collider=b,visible=False)
		Entity(model='cube',scale=(.3,8,11),position=(self.x+1.8,self.y+3,self.z+2),collider=b,visible=False)
		if typ == 1:
			self.color=color.rgb32(255,50,0)
			self.shader=unlit_shader

class SewerPlatform(Entity):
	def __init__(self,pos):
		pPF=omf+'l4/scn/'
		super().__init__(model='cube',scale=(.5,.2,.5),collider=b,position=pos,alpha=.7,visible=False)
		self.vis=Entity(model=pPF+'ptf.ply',texture=pPF+'swr_ptf.tga',name='swp2',position=(self.x,self.y+.05,self.z),scale=.02,rotation_x=-90)
		unlit_obj(self.vis)

class SewerWall(Entity):
	def __init__(self,pos):
		mo=omf+'l4/scn/sewer_wall_b'
		super().__init__(model=mo+'.ply',texture=mo+'.tga',position=pos,scale=.0175,rotation=(-90,90,0),double_sided=True)
		self.bgw=Entity(model='cube',color=color.black,scale=(5,8,.1),position=(self.x,self.y,self.z+1))
		self.color=color.rgb(.6,.5,.4)

class SwimPlatform(Entity):
	def __init__(self,pos):
		swmi=omf+'l4/swr_swim/swr_swim'
		super().__init__(model='cube',color=color.white,collider=b,position=pos,scale=(.5,.3,.5),visible=False)
		self.opt=Entity(model=swmi+'.ply',texture=swmi+'.tga',scale=.1/200,rotation_x=-90,position=(self.x,self.y+.06,self.z))
		self.active=False
		self.spawn_y=self.y
		self.f_time=0
	def sink(self):
		self.y-=time.dt
		self.opt.y-=time.dt
		if self.y <= self.spawn_y-.3:
			sn.pc_audio(ID=10)
			self.collider=None
			self.active=False
			self.f_time=0
			invoke(lambda:setattr(self,'y',self.spawn_y),delay=5)
			invoke(lambda:setattr(self,'collider',b),delay=5)
			invoke(lambda:setattr(self.opt,'y',self.spawn_y),delay=5)
	def update(self):
		if not st.gproc():
			if self.active:
				self.f_time+=time.dt
				if self.f_time >= .5:
					self.sink()

class SewerEntrance(Entity):
	def __init__(self,pos):
		swn=omf+'l4/swr_entrance/swr_entrance'
		super().__init__(model=swn+'.ply',texture=swn+'.jpg',position=pos,rotation_y=90,scale=2)

class SewerPipe(Entity):## danger
	def __init__(self,pos,typ):
		swrp=omf+'l4/pipe/pipe_'
		swu=str(typ)
		ro_y={0:-90,1:-90,2:90,3:90}
		super().__init__(model=swrp+swu+'.ply',texture=swrp+swu+'.png',position=pos,scale=.75,rotation=(-90,ro_y[typ],0))
		self.danger=(typ == 3)
		self.typ=typ
		if typ == 0:
			Entity(model=Circle(16,thickness=1,radius=.6),color=color.black,position=(self.x,self.y,self.z+.2))
			has_drips=random.randint(0,1)
			if has_drips == 1:
				DrippingWater(pos=(self.x,self.y-.75,self.z-.25),sca=(.9,.4))
		if typ == 2:
			Entity(model=Circle(16,thickness=1,radius=.5),color=color.black,position=(self.x,self.y+.8,self.z-.7),rotation_x=-30)
			DrippingWater(pos=(self.x,self.y-.2,self.z-.5),sca=(.9,.4))
		if typ == 3:
			self.collider=BoxCollider(self,size=Vec3(.5,.5,5))
			self.rotation_x=0
			self.color=color.red
			self.shader=unlit_shader
	def update(self):
		if not st.gproc() and self.typ == 3:
			if self.intersects(LC.ACTOR):
				cc.get_damage(LC.ACTOR,rsn=3)

class EletricWater(Entity):
	def __init__(self,pos,sca,ID):
		self.wtt=omf+'l4/wtr/'
		super().__init__(model='cube',texture=self.wtt+'0.png',name='elwt',position=pos,scale=(sca[0],.1,sca[1]),texture_scale=(sca[0],sca[1]),collider=b)
		self.color=color.rgb32(0,180,180)
		self.alpha=.9
		self.electric=False
		self.ta=LC.ACTOR
		self.tx=(sca[0],sca[1])
		self.can_splash=0
		self.vnum=ID
		self.frm=0
		if ID == 3:
			self.tme=random.uniform(.1,.2)
		else:
			self.tme=8
		self.switch_water()
	def anim(self):
		self.frm+=time.dt*8
		if self.frm > 31.9:
			self.frm=0
		self.texture=self.wtt+str(int(self.frm))+'.png'
	def switch_water(self):
		self.color=color.yellow
		self.shader=unlit_shader
		self.alpha=.9
		self.texture_scale=self.tx
		self.electric=True
		if (self.ta.warped and not st.bonus_round):
			if (self.vnum == 0 and self.ta.z < 3 and self.ta.z > -60) or (self.vnum == 1 and self.ta.z > 50 and self.ta.z < 80):
				sn.obj_audio(ID=7)
		invoke(self.harmless,delay=1.5)
	def harmless(self):
		self.color=color.rgb32(0,180,180)
		self.shader=None
		self.alpha=.95
		self.texture_scale=self.tx
		self.electric=False
	def do_act(self):
		self.ta.in_water=.3
		if self.can_splash <= 0:
			sn.pc_audio(ID=10)
			self.can_splash=.5
		if self.electric:
			cc.get_damage(self.ta,rsn=4)
	def update(self):
		if not st.gproc():
			self.can_splash=max(self.tme-time.dt,0)
			self.tme=max(self.tme-time.dt,0)
			self.anim()
			if self.tme <= 0:
				if self.vnum == 3:
					self.tme=random.uniform(.1,.2)
				else:
					self.tme=8
				self.switch_water()

class DrippingWater(Entity):
	def __init__(self,pos,sca):
		self.dpw=omf+'l4/drips/'
		super().__init__(model='quad',texture=self.dpw+'0.png',position=pos,scale=sca,rotation_z=90)
		self.frm=0
	def update(self):
		if not st.gproc():
			self.frm+=time.dt*10
			if self.frm > 7.9:
				self.frm=0
			self.texture=self.dpw+str(int(self.frm))+'.png'


####################
## level 5 objects #
class RuinsPlatform(Entity):##big platform
	def __init__(self,pos,m):
		rnp=omf+'l5/ruins_scn/'
		msc={True:-.03,False:.03}
		msv={True:-.9,False:.9}
		super().__init__(model='cube',collider=b,scale=(1.7,1,1.5),position=pos,visible=False)
		self.opt_model=Entity(model=rnp+'ruins_ptf1.ply',texture=rnp+'ruins_scn.tga',position=(self.x,self.y+.5,self.z),scale=(.03,msc[m],.03),rotation=(-90,90,0),double_sided=True)
		self.rail0=Entity(model='cube',scale=(1.7,.5,.3),collider=b,position=(self.x,self.y+.8,self.z+.9),visible=False)
		self.rail0=Entity(model='cube',scale=(.3,.5,1.7),collider=b,position=(self.x+msv[m],self.y+.8,self.z),visible=False)

class RuinsBlock(Entity):## small platform
	def __init__(self,pos):
		rnb=omf+'l5/ruins_scn/'
		super().__init__(model='cube',collider=b,scale=(.75,1,.75),position=pos,visible=False)
		self.opt_model=Entity(model=rnb+'ruins_ptf02.ply',name='rubl',texture=rnb+'ruins_scn.tga',position=(self.x,self.y+.5,self.z-.025),scale=.03,rotation=(-90,90,0),double_sided=False)

class RuinsCorridor(Entity):## corridor
	def __init__(self,pos):
		rco=omf+'l5/ruins_scn/'
		super().__init__(model='cube',position=pos,scale=(3,1,3),collider=b,visible=False)
		self.opt_model=Entity(model=rco+'ruins_cor.ply',texture=rco+'ruins_scn.tga',position=(self.x,self.y+.5,self.z),scale=.03,rotation=(-90,90,0),double_sided=True)
		IndoorZone(pos=(self.x,self.y+2.55,self.z),sca=3)

class MonkeySculpture(Entity):
	def __init__(self,pos,r,d,ro_y=90):
		rmsc=omf+'l5/m_sculpt/m_sculpt'
		super().__init__(model=rmsc+'.ply',texture=rmsc+'.tga',position=pos,scale=.003,rotation=(-90,ro_y,0),double_sided=True)
		self.podium=Entity(model='cube',texture='res/terrain/l5/moss.png',scale=(.5,1,.5),texture_scale=(1,2),position=(self.x,self.y-.5,self.z))
		self.f_pause=False
		self.s_audio=False
		self.f_throw=3
		self.f_cnt=0
		self.danger=d
		self.rot=r
		unlit_obj(self)
	def f_reset(self):
		self.f_pause=False
		self.f_cnt=0
	def fire_throw(self):
		effect.FireThrow(pos=self.position,ro_y=self.rotation_y)
	def update(self):
		if not st.gproc():
			if self.danger:
				if self.f_cnt >= 100:
					if not self.f_pause:
							self.f_pause=True
							invoke(self.f_reset,delay=5)
					return
				if distance(self,LC.ACTOR) < 12:
					self.f_throw=max(self.f_throw-time.dt,0)
					if self.f_throw <= 0:
						self.throw=3
						self.f_cnt+=1
						self.fire_throw()
						if not self.s_audio:
							self.s_audio=True
							sn.obj_audio(ID=10,pit=1)
							invoke(lambda:setattr(self,'s_audio',False),delay=3)
			if self.rot:
				if distance(self,LC.ACTOR) < 2:
					cc.rotate_to_crash(self)

class LoosePlatform(Entity):
	def __init__(self,pos,t):
		self.lpp=omf+'l5/loose_ptf'+str(t)+'/'
		super().__init__(model='cube',position=pos,scale=(.7,.5,.6),collider=b,visible=False)
		self.opt_model=Entity(model=self.lpp+'loose_ptf'+str(t)+'.ply',texture=self.lpp+'loose_ptf'+str(t)+'.tga',scale=.01/15,position=(self.x,self.y+.25,self.z),rotation=(-90,-90,0),double_sided=True)
		self.active=False
		self.typ=t
		if self.typ != 2:
			self.frm=0
		else:
			self.f_time=0
			self.scale=(.55,.2,.55)
			self.opt_model.position=(self.x-.275,self.y+.1,self.z+.25)
			self.spawn_h=self.y
	def respawn(self):
		self.collider=b
		self.frm=0
		self.opt_model.model=self.lpp+'0.ply'
	def fall(self):
		self.y-=time.dt*3
		self.opt_model.y-=time.dt*3
		if self.y <= self.spawn_h-1:
			self.active=False
			self.collider=None
			self.f_time=0
			invoke(lambda:setattr(self,'y',self.spawn_h),delay=5)
			invoke(lambda:setattr(self.opt_model,'y',self.spawn_h),delay=5)
			invoke(lambda:setattr(self,'collider',b),delay=5)
	def collapse(self):
		self.frm+=time.dt*18
		if self.frm > 26:
			self.collider=None
			if self.frm > 32.9:
				sn.obj_audio(ID=9,pit=1)
				self.active=False
				invoke(self.respawn,delay=7)
				return
		self.opt_model.model=self.lpp+str(int(self.frm))+'.ply'
	def update(self):
		if not st.gproc():
			if self.active:
				if self.typ != 2:
					self.collapse()
				else:
					self.f_time+=time.dt
					if self.f_time >= .5:
						self.fall()

class RuinRuins(Entity):
	def __init__(self,pos,typ,ro_y):
		rrn=omf+'l5/ruins_bgo/'
		super().__init__(model=rrn+'ruin_bg'+str(typ)+'.ply',texture=rrn+'ruin.tga',position=pos,scale=.03,rotation=(-90,ro_y,0),double_sided=True)
		unlit_obj(self)

###################
##################
## logic objects #
class FallingZone(Entity):## falling
	def __init__(self,pos,s):
		super().__init__(model='cube',collider=b,scale=s,position=pos,color=color.rgb32(0,0,0))
	def do_act(self):
		cc.dth_event(LC.ACTOR,rsn=0)

class WaterHit(Entity):## collider for water
	def __init__(self,p,sc):
		super().__init__(model='cube',collider=b,position=p,scale=(sc[0],.2,sc[1]),visible=False)

class CrateScore(Entity):## level reward
	def __init__(self,pos):
		ev='res/crate/'
		super().__init__(model=ev+'cr_t0.ply',name='ctsc',texture=ev+'1.png',alpha=.4,scale=.18,position=pos,origin_y=.5)
		self.cc_text=Text(parent=scene,position=(self.x-.2,self.y,self.z),text=None,font='res/ui/font.ttf',color=color.rgb32(255,255,100),scale=10)
	def update(self):
		if not st.gproc():
			tk=not(st.crates_in_level <= 0 or (LC.C_GEM and distance(self,LC.C_GEM) < .5))
			self.cc_text.visible=tk
			self.visible=tk
			if tk:
				self.cc_text.text=str(st.crate_count)+'/'+str(st.crates_in_level)
				self.rotation_y-=120*time.dt
			if st.crates_in_level > 0 and (st.crate_count >= st.crates_in_level):
				item.GemStone(pos=(self.x,self.y-.3,self.z),c=0)
				sn.ui_audio(ID=4)
				cc.purge_instance(self.cc_text)
				cc.purge_instance(self)

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
		status.checkpoint=(self.x,self.y+2,self.z)
		camera.position=(self.x,self.y+2,self.z-3)
		IndoorZone(pos=(self.x,self.y+1.5,self.z),sca=(3,2,7))
		unlit_obj(self)
		if lvID > 0:
			m_info={1:lambda:level.level1(),
					2:lambda:level.level2(),
					3:lambda:level.level3(),
					4:lambda:level.level4(),
					5:lambda:level.level5(),
					6:lambda:level.test()}
			m_info[lvID]()

class EndRoom(Entity):## finish level
	def __init__(self,pos,c):
		eR=omf+'ev/e_room/e_room'
		super().__init__(model=eR+'.ply',texture=eR+'.tga',scale=.025,rotation=(-90,90,0),position=pos,color=c,double_sided=True,unlit=False)
		self.curt=Entity(model='plane',color=color.black,scale=(4,1,16),position=(self.x-1,self.y-1.8,self.z+3))
		self.grnd=Entity(model='cube',scale=(4,1,16),position=(self.x-1,self.y-2,self.z+3),collider=b,visible=False)
		self.wa_l=Entity(model='cube',scale=(1,3,16),position=(self.x-2.2,self.y,self.z+3),collider=b,visible=False)
		self.wa_r=Entity(model='cube',scale=(1,3,16),position=(self.x,self.y,self.z+3),collider=b,visible=False)
		self.ceil=Entity(model='cube',name='clr2',scale=(5,3,16),position=(self.x-1,self.y+1.4,self.z+3),collider=b,visible=False)
		self.bck=Entity(model='cube',scale=(6,4,2),position=(self.x,self.y,self.z+9),collider=b,visible=False)
		self.pod1=Entity(model='cube',scale=(6,1,2.5),position=(self.x-1,self.y-1.85,self.z+.45),collider=b,visible=False)
		self.pod2=Entity(model='cube',scale=(.85,1,.85),position=(self.x-1.1,self.y-1.6,self.z+.3),collider=b,visible=False)
		self.pod3=Entity(model='cube',scale=(1.6,1,1),position=(self.x-1.1,self.y-1.51,self.z+6.5),collider=b,visible=False)
		if st.level_index != 5:
			Entity(model='cube',scale=(20,10,.1),position=(self.x,self.y-5,self.z+16),color=color.black)
		LevelFinish(p=(self.x-1.1,self.y-1.1,self.z+7))
		RoomDoor(pos=(self.x-1.1,self.y+.25,self.z-4.78),typ=1)
		CrateScore(pos=(self.x-1.1,self.y-.7,self.z))
		IndoorZone(pos=(self.x-1,self.y,self.z+1),sca=(5,2,12))
		if st.level_index == 1 and not 4 in st.COLOR_GEM:
			item.GemStone(pos=(self.x-1.1,self.y-1,self.z),c=4)
		if st.level_index == 2 and not 1 in st.COLOR_GEM:
			item.GemStone(pos=(self.x-1.1,self.y-1,self.z),c=1)

class RoomDoor(Entity):## door for start and end room
	def __init__(self,pos,typ):
		self.dPA=omf+'ev/door/'
		super().__init__(model=self.dPA+'u0.ply',texture=self.dPA+'u_door.tga',name='rmd1',position=pos,scale=.001,rotation_x=90,collider=b)
		self.door_part=Entity(model=self.dPA+'d0.ply',name='rmd2',texture=self.dPA+'d_door.tga',position=(self.x,self.y+.1,self.z),scale=.001,rotation_x=90,collider=b)
		self.DS={0:2,1:3}
		self.d_open=False
		self.typ=typ
		unlit_obj(self)
		unlit_obj(self.door_part)
	def update(self):
		if not st.gproc():
			if distance(self,LC.ACTOR) < self.DS[self.typ]:
				if not self.d_open:
					self.d_open=True
					animation.door_open(self)
					sn.obj_audio(ID=1)
				return
			if self.d_open:
				self.d_open=False
				if self.typ == 0:
					cc.purge_instance(self.door_part)
					cc.purge_instance(self)
					return
				animation.door_close(self)
				sn.obj_audio(ID=1,pit=.9)

class BonusPlatform(Entity):## switch -> bonus round
	def __init__(self,pos):
		sIN='ev/bonus/bonus'
		super().__init__(model=omf+sIN+'.ply',texture=omf+sIN+'.tga',collider=b,scale=-.001,rotation_x=90,position=pos)
		self.start_y=self.y
		self.catch_p=False
		self.ta=LC.ACTOR
		unlit_obj(self)
	def update(self):
		if not st.gproc():
			if self.catch_p:
				cc.ptf_up(p=self,c=self.ta)
			if st.bonus_solved:
				cc.purge_instance(self)
				return

class GemPlatform(Entity):## gem platform
	def __init__(self,pos,t):
		if t in st.COLOR_GEM:
			ne='gem_ptf'
			self.is_enabled=True
		else:
			ne='gem_ptf_e'
			self.is_enabled=False
		L=180
		GMC={0:color.rgb32(130,130,140),1:color.rgb32(L,0,0),2:color.rgb32(0,L,0),3:color.rgb32(L-50,0,L-50),4:color.rgb32(0,0,L+40),5:color.rgb32(L-30,L-30,0)}
		super().__init__(model=omf+'ev/'+ne+'/'+ne+'.ply',texture=omf+'ev/'+ne+'/'+ne+'.tga',rotation_x=-90,scale=0.001,position=pos,collider=b,color=GMC[t],double_sided=True)
		self.bg_darkness=Entity(model=Circle(16,mode='ngon',thickness=.1),position=(self.x,self.y-.011,self.z),rotation_x=90,color=color.black,scale=.7,alpha=.98)
		self.start_y=self.y
		self.catch_p=False
		self.ta=LC.ACTOR
		if not self.is_enabled:
			self.collider=None
			self.bg_darkness.hide()
		unlit_obj(self)
	def update(self):
		if not st.gproc():
			if st.gem_path_solved:
				cc.purge_instance(self.bg_darkness)
				cc.purge_instance(self)
				return
			self.bg_darkness.position=(self.x,self.y-.01,self.z)
			if self.is_enabled:
				self.rotation_y+=time.dt*20
			if self.catch_p:
				cc.ptf_up(p=self,c=self.ta)

class LevelScene(Entity):
	def __init__(self,pos,sca):
		self.vpa='res/background/'
		super().__init__(model='quad',texture=None,scale=sca,position=pos,texture_scale=(sca[0]/50,1),unlit=False)
		if st.level_index == 1:
			self.texture=self.vpa+'bg_woods.png'
		if st.level_index == 5:
			self.texture=self.vpa+'bg_ruins.jpg'
			self.color=color.rgb32(170,170,170)
			self.orginal_tsc=self.texture_scale
			self.orginal_y=self.y
			self.bonus_y=-70
			self.unlit=True
			self.shader=unlit_shader
			_loc.bgT=self
	def update(self):
		if st.level_index == 5:
			if not st.bonus_round:
				self.y=self.orginal_y
				return
			self.y=self.bonus_y

class PseudoGemPlatform(Entity):
	def __init__(self,pos,t):
		if t in st.COLOR_GEM:
			ne='gem_ptf'
			self.is_enabled=True
		else:
			ne='gem_ptf_e'
			self.is_enabled=False
		L=180
		GMC={0:color.rgb32(130,130,140),1:color.rgb32(L,0,0),2:color.rgb32(0,L,0),3:color.rgb32(L-50,0,L-50),4:color.rgb32(0,0,L+40),5:color.rgb32(L-30,L-30,0)}
		super().__init__(model=omf+'ev/'+ne+'/'+ne+'.ply',texture=omf+'ev/'+ne+'/'+ne+'.tga',rotation_x=-90,scale=.001,position=pos,color=GMC[t],double_sided=True,shader=unlit_shader)
		self.bg_darkness=Entity(model=Circle(16,mode='ngon',thickness=.1),position=(self.x,self.y-.01,self.z),rotation_x=90,color=color.black,scale=.7,alpha=.98)
		self.hitbox=Entity(model='cube',position=(self.x,self.y-.15,self.z),scale=(.6,.4,.6),collider=b,visible=False)
		if not self.is_enabled:
			self.collider=None
			self.bg_darkness.hide()
		unlit_obj(self)

## Switches
class CamSwitch(Entity):## allow cam move y if player collide with them
	def __init__(self,pos,sca):
		super().__init__(model='cube',position=pos,scale=sca,collider=b,visible=False)
	def do_act(self):#avoid pyhsics with them
		if not st.gproc() and LC.ACTOR != None:
			camera.y=lerp(camera.y,LC.ACTOR.y+1.2,time.dt*2)

class LevelFinish(Entity):## finish level
	def __init__(self,p):
		trpv=omf+'ev/teleport/warp_effect'
		super().__init__(model='sphere',collider=b,scale=1,position=p,visible=False)
		self.eff_w0=Entity(model=trpv+'.ply',texture=trpv+'.png',color=color.yellow,rotation_x=90,position=(self.x,self.y,self.z),scale=.6,alpha=.5,shader=unlit_shader)
		self.eff_w1=Entity(model=trpv+'.ply',texture=trpv+'.png',color=color.orange,rotation_x=90,position=(self.x,self.y+.2,self.z),scale=.7,alpha=.5,shader=unlit_shader)
		self.eff_w2=Entity(model=trpv+'.ply',texture=trpv+'.png',color=color.yellow,rotation_x=90,position=(self.x,self.y+.4,self.z),scale=.8,alpha=.5,shader=unlit_shader)
		self.eff_w3=Entity(model=trpv+'.ply',texture=trpv+'.png',color=color.orange,rotation_x=90,position=(self.x,self.y+.6,self.z),scale=.7,alpha=.5,shader=unlit_shader)
		self.eff_w4=Entity(model=trpv+'.ply',texture=trpv+'.png',color=color.yellow,rotation_x=90,position=(self.x,self.y+.8,self.z),scale=.6,alpha=.5,shader=unlit_shader)
		self.w_audio=Audio('res/snd/misc/portal.wav',volume=0,loop=True)
	def do_act(self):
		cc.jmp_lv_fin()
	def update(self):
		if not st.gproc():
			cnnb=(distance(self,LC.ACTOR) < 12)
			csnd=(distance(self,LC.ACTOR) < 6)
			vrs=time.dt*600
			self.eff_w0.rotation_y+=vrs
			self.eff_w1.rotation_y-=vrs
			self.eff_w2.rotation_y+=vrs
			self.eff_w3.rotation_y-=vrs
			self.eff_w4.rotation_y+=vrs
			self.eff_w0.visible=cnnb
			self.eff_w1.visible=cnnb
			self.eff_w2.visible=cnnb
			self.eff_w3.visible=cnnb
			self.eff_w4.visible=cnnb
			if csnd:
				self.w_audio.volume=SFX
				return
			self.w_audio.volume=0

class IndoorZone(Entity):## disable rain
	def __init__(self,pos,sca):
		super().__init__(model='cube',scale=sca,position=pos,collider=b,visible=False)
	def do_act(self):
		LC.ACTOR.indoor=.3

class LODProcess(Entity):## Level of Detail
	def __init__(self):
		super().__init__()
		self.rt=.5
		CLW={1:LC.LV1_LOD,2:LC.LV2_LOD,3:LC.LV3_LOD,4:LC.LV4_LOD,5:LC.LV5_LOD,6:LC.LV3_LOD}
		self.MAIN_LOD=CLW[st.level_index]
		if st.level_index == 4:
			self.dst_a=3
			self.dst_b=26
			return
		if st.level_index == 5:
			self.dst_a=3
			self.dst_b=25
			return
		else:
			self.dst_a=2
			self.dst_b=20
			return


	def wmp_lod(self,w,p):
		w.enabled=distance(w,p) < 8
	def crt_lod(self,c,p):
		c.visible=distance(p,c) < 16
	def enm_lod(self,e,p):
		e.enabled=distance(e,p) < 20
	def vwi_lod(self,v,p):
		v.enabled=(p.z < v.z+self.dst_a and v.z < p.z+self.dst_b)
	def refr(self):
		for b in scene.entities[:]:
			A=LC.ACTOR
			if isinstance(b,item.WumpaFruit):self.wmp_lod(w=b,p=A)
			if 'tnt.wav' in str(b) and not b.playing:scene.entities.remove(b)
			if cc.is_crate(b):self.crt_lod(c=b,p=A)
			if cc.is_enemie(b):self.enm_lod(e=b,p=A)
			if str(b) in self.MAIN_LOD:self.vwi_lod(v=b,p=A)
	def update(self):
		if not status.gproc():
			self.rt=max(self.rt-time.dt,0)
			if self.rt <= 0:
				self.rt=.5
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

class Water(Entity):
	def __init__(self,pos,s,c,a):
		self.wtfc=omf+'ev/water/wtr_srfc/water_'
		super().__init__(model='plane',texture=self.wtfc+'0.tga',position=pos,scale=(s[0],.1,s[1]),color=c,alpha=a)
		WaterHit(p=(pos[0],pos[1]-.1,pos[2]),sc=s)
		self.texture_scale=(s[0]/4,s[1]/4)
		self.frm=0
	def update(self):
		if not st.gproc():
			if st.level_index != 2:
				self.frm+=time.dt*15
				if self.frm > 57.9:
					self.frm=0
				self.texture=self.wtfc+str(int(self.frm))+'.tga'

class mTerrain(Entity):
	def __init__(self,pos,sca,typ):
		terra='res/terrain/l'+str(st.level_index)+'/'
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