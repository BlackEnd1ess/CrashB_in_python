import _core,status,item,sound,animation,player,_loc,settings,effect,npc,ui
from ursina.shaders import *
from ursina import *

an=animation
ef=effect
st=status
sn=sound
cc=_core
LC=_loc

wfc='wireframe_cube'
omf='res/objects/'
bgg='res/background/'
b='box'

def wtr_dist(w,p):
	return ((p.z < w.z+(w.scale_z/2)+4) and (p.z > w.z-(w.scale_z/2)-4) and (p.x < w.x+(w.scale_x/2)+2) and (p.x > w.x-w.scale_x/2-2))

#multi tiles/blocks
trhs={1:1,2:.985,3:.85,4:.501,5:.75}
def spw_block(p,vx,ID,sca=.5):
	fgx=st.level_index
	for gbx in range(vx[0]):
		for gbz in range(vx[1]):
			FloorBlock(pos=(p[0]+trhs[fgx]*gbx,p[1],p[2]+trhs[fgx]*gbz),sca=.5,ID=ID)
	del p,vx,ID,sca,gbx,gbz,fgx

#lv2
def plank_bridge(pos,typ,cnt,ro_y,DST):
	for wP in range(cnt):
		plNK={90:lambda:Plank(pos=(pos[0]+wP*DST,pos[1],pos[2]),ro_y=ro_y,typ=typ),
			0:lambda:Plank(pos=(pos[0],pos[1],pos[2]+wP*DST),ro_y=ro_y,typ=typ)}
		plNK[ro_y]()
	del pos,typ,cnt,ro_y,DST

def pillar_twin(p):
	Pillar(pos=(p[0],p[1],p[2]))
	Pillar(pos=(p[0]+1.5,p[1],p[2]))
	del p

def spawn_ice_wall(pos,cnt,d):
	ws={0:90,1:-90}
	for icew in range(cnt):
		SnowHill(pos=(pos[0],pos[1],pos[2]+icew*16.4),ro_y=ws[d])
	del pos,cnt,d

#lv7
def spw_lab_tile(p,cnt,way,typ,sca_y=.8):
	for lbt in range(cnt):
		if way == 0:
			LabTile(pos=(p[0]+lbt,p[1],p[2]),typ=typ,ro_y=0,sca_y=sca_y)
		else:
			LabTile(pos=(p[0],p[1],p[2]+lbt),typ=typ,ro_y=90,sca_y=sca_y)
	del p,cnt,way,typ,lbt

def spw_multi_lab_tile(p,cnt,typ,way):
	for laX in range(cnt[0]):
		for laZ in range(cnt[1]):
			if way == 0:
				LabTile(pos=(p[0]+laX,p[1],p[2]+laZ),typ=typ,ro_y=0)
			else:
				LabTile(pos=(p[0]+laX,p[1],p[2]+laZ),typ=typ,ro_y=90)
	del p,cnt,typ,way,laX,laZ
## Pseudo CrashB in Warp Room

MVP=omf+'l1/p_moss/moss'
rp='res/pc/crash'
class PseudoCrash(Entity):
	def __init__(self):
		s=self
		super().__init__(model=rp+'.ply',texture=rp+'.tga',scale=.1/20,rotation=(-90,30,0),position=(9,-4,0),unlit=False)
		Entity(model=MVP+'.obj',texture=MVP+'.tga',scale=.75/30,position=(s.x,s.y,s.z),double_sided=True,color=color.rgb32(170,190,180))
		s.idfr=0
	def update(self):
		animation.idle(self,sp=18)

####################
## level 1 objects #
class MossPlatform(Entity):
	def __init__(self,p,ptm,pts=.5,ptw=3):
		s=self
		super().__init__(model=MVP+'.obj',name='mptf',texture=MVP+'.tga',scale=.0085,position=(p[0],p[1]+.475,p[2]),double_sided=True,collider=b)
		s.spawn_pos=p
		s.slp=ptw
		s.ptm=ptm
		s.pts=pts
		s.turn=0
		s.ptw=0
		s.is_sfc=(ptm == 1)
		if ptm > 1:
			s.drc='x'
			if ptm == 3:
				s.drc='z'
		del p,ptm,pts,ptw
	def ptf_move(self,di):
		s=self
		pdv={2:s.spawn_pos[0],3:s.spawn_pos[2]}
		spd=time.dt*s.pts
		kv=getattr(s,di)
		pmd={0:lambda:setattr(s,di,kv+spd),1:lambda:setattr(s,di,kv-spd)}
		pmd[s.turn]()
		if (s.turn == 0 and kv >= pdv[s.ptm]+1):
			s.turn=1
		if (s.turn == 1 and kv <= pdv[s.ptm]-1):
			s.turn=0
		del pmd,spd,kv,pdv
	def mv_player(self):
		s=self
		if s.ptm < 2:
			return
		LC.ACTOR.x=s.x
		LC.ACTOR.z=s.z
	def dive(self):
		s=self
		if s.is_sfc:
			s.is_sfc=False
			s.animate_y(s.y-1,duration=.3)
			if distance(s,LC.ACTOR) < 6:
				sn.obj_audio(ID=6)
			return
		s.is_sfc=True
		s.animate_y(s.spawn_pos[1],duration=.3)
	def update(self):
		if st.gproc():
			return
		s=self
		if s.ptm == 1:
			s.ptw=max(s.ptw-time.dt,0)
			if s.ptw <= 0:
				s.ptw=s.slp
				s.dive()
			return
		if s.ptm > 1:
			s.ptf_move(di=s.drc)

class BackgroundWall(Entity):
	def __init__(self,p):
		s=self
		super().__init__(model=omf+'l1/wall_0/tr_wall.ply',texture=omf+'l1/wall_0/wall_wood.tga',scale=.02,position=p,rotation=(-90,90,0),color=color.rgb32(160,190,160))
		if st.level_index == 1 and s.x > 190:
			s.color=color.rgb32(0,140,160)
		del p

wcw=omf+'l1/w_corr/w_cori'
class Corridor(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=wcw+'.ply',texture=wcw+'.tga',name='cori',scale=.1,position=pos,rotation=(-90,90,0))
		HitBox(sca=(3,3,2.2),pos=(s.x+2.3,s.y,s.z))
		HitBox(sca=(3,3,2.2),pos=(s.x-2.3,s.y,s.z))
		HitBox(sca=(3,3,2.2),pos=(s.x,s.y+3,s.z))
		IndoorZone(pos=(s.x,s.y+1.6,s.z),sca=3)
		del pos

trs=omf+'l1/tree/tree_w'
class TreeScene(Entity):
	def __init__(self,pos,sca):
		s=self
		super().__init__(model=trs+'.ply',name='tssn',texture=trs+'.tga',rotation_x=-90,scale=sca,position=pos)
		HitBox(pos=s.position,sca=(1,5,1))
		del pos,sca

trm=omf+'l1/tree/multi_tree'
class TreeRow(Entity):
	def __init__(self,pos,sca):
		super().__init__(model=trm+'.ply',texture=trm+'.png',name='trrw',position=pos,scale=sca,rotation_x=-90,color=color.rgb32(180,180,180))
		del pos,sca

gr=omf+'l1/grass_side/grass_sd'
class GrassSide(Entity):
	def __init__(self,pos,m=False):
		super().__init__(model=gr+'.ply',texture=gr+'.jpg',name='grsi',position=pos,scale=(1,2,1.4),rotation_x=-90)
		if m:
			self.scale_x=-1
		del pos,m

btt=omf+'l1/bush/bush1.png'
class Bush(Entity):
	def __init__(self,pos,sca,ro_y=0):
		super().__init__(model='quad',texture=btt,position=pos,scale=sca,rotation_y=ro_y,color=color.rgb32(0,170,0))
		del pos,sca,ro_y

class WoodScene(Entity):
	def __init__(self,pos):
		super().__init__(model='quad',texture=bgg+'bg_woods.png',position=pos,scale=(250,40),texture_scale=(5,1))
		del pos

class BrickWall(Entity):
	def __init__(self,pos,sca):
		super().__init__(model='plane',texture='res/terrain/l1/bricks.png',position=pos,scale=sca,texture_scale=(sca[0],sca[2]),rotation=(90,90,0),double_sided=True)
		del pos,sca

####################
## level 2 objects #
plob=omf+'l2/plank/plank.png'
class Plank(Entity):
	def __init__(self,pos,typ,ro_y):
		s=self
		super().__init__(model='cube',texture=plob,name='plnk',scale=(1,.1,.4),position=pos,collider=b,rotation_y=ro_y,texture_scale=(2,2))
		s.spawn_pos=s.position
		s.color=color.gray
		s.typ=typ
		if typ == 1:
			s.is_touched=False
			s.color=color.brown
		del pos,typ,ro_y
	def obj_reset(self):
		s=self
		s.is_touched=False
		s.position=s.spawn_pos
		s.collider=b
		s.show()
	def fall_down(self):
		s=self
		s.collider=None
		sn.crate_audio(ID=2,pit=.8)
		s.animate_y(s.y-3,duration=.2)
		invoke(s.obj_reset,delay=5)
	def pl_touch(self):
		s=self
		if not s.is_touched:
			s.is_touched=True
			invoke(s.fall_down,delay=1)
			invoke(s.hide,delay=1.5)

rpt=omf+'l2/rope/rope_pce.jpg'
class Ropes(Entity):
	def __init__(self,pos,le):
		s=self
		super().__init__(model='cube',scale=(.03,.03,le),name='snrp',texture=rpt,position=pos,texture_scale=(1,le*8),origin_z=-.5)
		s.dup=Entity(model='cube',scale=s.scale,name=s.name,position=(s.x+.95,s.y,s.z),texture=rpt,texture_scale=(1,le*8),origin_z=s.origin_z)
		del pos,le

ppt=omf+'l2/pillar/s_pillar'
class Pillar(Entity):
	def __init__(self,pos):
		super().__init__(model=ppt+'.ply',texture=ppt+'_0.jpg',name='pilr',scale=.2,rotation=(-90,45,0),position=pos,color=color.cyan,collider=b)
		IceCrystal(pos=(self.x,self.y+1.1,self.z+.075))
		del pos

swbo='l2/snow_wall/snow_bonus'
class SnowWall(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=omf+swbo+'.ply',texture=omf+swbo+'.tga',scale=.02,name='snwa',position=pos,rotation=(-90,-90,0))
		del pos

class IceCrystal(Entity):
	def __init__(self,pos):
		super().__init__(model=omf+'l2/ice_crystal/ice_crystal.ply',name='icec',texture=omf+'l2/ice_crystal/snow_2.tga',scale=(.025,.02,.03),position=pos,rotation=(-90,45,0),color=color.cyan)
		del pos

inp=omf+'l2/wood_log/wood_log'
class WoodLog(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=inp+'.ply',texture=inp+'.tga',name='wdlg',position=pos,scale=(.001,.001,.0015),rotation=(-90,0,0),collider=b)
		Entity(model='cube',texture='res/terrain/l1/bricks.png',name=s.name,position=(s.x,s.y+.8,s.z-.075),scale=(.5,2,.5),collider=b)
		Entity(model='cube',texture='res/terrain/l1/bricks.png',name=s.name,position=(s.x,s.y-.1,s.z+.6),scale=(.5,3,.5),texture_scale=(1,2),collider=b)
		s.danger=True
		s.or_pos=s.y
		s.stat=0
		del pos
	def reset_pos(self):
		s=self
		s.y=min(s.y+time.dt,s.or_pos+1.31)
		if s.y > (s.or_pos+1.3):
			s.danger=True
			s.stat=1
	def stomp(self):
		s=self
		s.y=max(s.y-time.dt*4,s.or_pos)
		if s.y <= s.or_pos:
			if distance(s,LC.ACTOR) < 2:
				sn.obj_audio(ID=3)
			s.danger=False
			s.stat=0
	def update(self):
		s=self
		if not st.gproc():
			if s.intersects(LC.ACTOR) and s.danger:
				cc.get_damage(LC.ACTOR,rsn=2)
			ttr={0:s.reset_pos,1:s.stomp}
			ttr[s.stat]()

class IceGround(Entity):
	def __init__(self,pos,sca):
		s=self
		super().__init__(model='cube',name='iceg',texture='res/terrain/l2/ice_ground.png',position=pos,scale=sca,collider=b,alpha=.85)
		s.texture_scale=(sca[0],sca[1])
		del pos,sca
	def mv_player(self):
		LC.ACTOR.is_slippery=LC.ACTOR.landed

snh=omf+'l2/snw_hill/sn_hill'
class SnowHill(Entity):
	def __init__(self,pos,ro_y):
		super().__init__(model=snh+'.ply',texture=snh+'.jpg',name='snhi',position=pos,scale=(.6,.5,.4),rotation=(-90,ro_y,0))
		del pos,ro_y

ice_ch=omf+'l2/ice_pce/ice_pce'
class IceChunk(Entity):
	def __init__(self,pos,rot,typ):
		super().__init__(model=ice_ch+'_'+str(typ)+'.ply',texture=ice_ch+'.jpg',name='ickk',position=pos,scale=.8,rotation=rot)
		del pos,rot,typ

snPL=omf+'l2/snow_platform/snow_platform'
class SnowPlatform(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=snPL+'.ply',texture=snPL+'.tga',name='sngg',position=pos,scale=.0075,rotation_x=-90)
		s.co=Entity(model=wfc,scale=(.85,1,.85),name=s.name,position=(s.x,s.y-.5,s.z),collider=b,visible=False)
		del pos

rol=omf+'l2/role/role'
class Role(Entity):
	def __init__(self,pos,di):
		s=self
		super().__init__(model=rol+'.ply',texture=rol+'.tga',rotation=(-90,90,90),position=pos,scale=.01,collider=b)
		s.main_pos=s.position
		s.is_rolling=False
		s.danger=False
		s.roll_wait=1
		s.direc=di
		del pos,di
	def roll_right(self):
		s=self
		s.x+=time.dt*2
		s.rotation_x+=time.dt*80
		if s.x >= s.main_pos[0]+1.5:
			s.roll_wait=1
			s.direc=1
			invoke(s.p_snd,delay=.5)
	def roll_left(self):
		s=self
		s.x-=time.dt*2
		s.rotation_x-=time.dt*80
		if s.x <= s.main_pos[0]-1.5:
			s.roll_wait=1
			s.direc=0
			invoke(s.p_snd,delay=.5)
	def p_snd(self):
		if distance(self,LC.ACTOR) < 3:
			sn.obj_audio(ID=4)
	def update(self):
		s=self
		if not st.gproc():
			if (s.intersects(LC.ACTOR) and s.danger):
				cc.get_damage(LC.ACTOR,rsn=2)
			s.roll_wait=max(s.roll_wait-time.dt,0)
			if s.roll_wait <= 0:
				s.is_rolling=True
				s.danger=True
				rdi={0:s.roll_right,1:s.roll_left}
				rdi[s.direc]()
				return
			s.is_rolling=False
			s.danger=False

####################
## level 3 objects #
wtr_t=omf+'l3/water_flow/'
class WaterFlow(Entity):
	def __init__(self,pos,sca):
		s=self
		super().__init__(model='plane',texture=wtr_t+'water_flow0.tga',name='wafl',scale=(sca[0],.1,sca[1]),texture_scale=(1,11),position=pos,color=color.rgb32(170,170,170),alpha=.8)
		s.cbst=Entity(model='cube',texture='res/terrain/l3/cobble_stone.png',name=s.name,position=(pos[0],pos[1]-.7,pos[2]+.05),scale=(10,.1,sca[1]),texture_scale=(10,sca[1]))
		WaterHit(p=(pos[0],pos[1]-.1,pos[2]),sc=sca)
		s.frm=0
		del pos,sca
	def update(self):
		if st.gproc():
			return
		s=self
		if wtr_dist(w=s,p=LC.ACTOR):
			s.frm=min(s.frm+time.dt*10,3.999)
			if s.frm > 3.99:
				s.frm=0
			s.texture=wtr_t+f'water_flow{int(s.frm)}.tga'

pa=omf+'l3/water_fall/waterf'
class WaterFall(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model='quad',name='wtfa',texture=pa+'0.png',position=pos,scale=(5,1),texture_scale=(10,1),color=color.rgb32(240,255,240))
		Entity(model='plane',color=color.black,scale=(12,1,20),position=(s.x,s.y-.7,s.z+1.3))
		s.frm=0
		Foam(pos=(s.x,s.y-.49,s.z-.5),t=0)
		Foam(pos=(s.x,s.y+.501,s.z+.49),t=1)
		del pos
	def update(self):
		if st.gproc():
			return
		s=self
		s.frm=min(s.frm+time.dt*8,31.999)
		if s.frm > 31.99:
			s.frm=0
		s.texture=pa+f'{int(s.frm)}.png'

sWCN=omf+'l3/scn_w/sd'
class SceneWall(Entity):
	def __init__(self,pos,typ):
		s=self
		super().__init__(model=sWCN+str(typ)+'.obj',texture=sWCN+'.tga',name='scwa',position=pos,scale=(.0225,.0265,.025),rotation_y=-90,color=color.rgb32(150,180,150),double_sided=True)
		del pos,typ

trw=omf+'l3/temple_wall/tm_wall'
class TempleWall(Entity):
	def __init__(self,pos,sd):
		kq=.025
		if sd == 2:
			kq=-.025
		super().__init__(model=trw+'.ply',texture=trw+'.tga',name='tmpw',position=pos,scale=(.025,kq,.025),rotation=(-90,90,0),collider=b)
		del pos,sd

wdStg=omf+'l3/wood_stage/w_stage'
class WoodStage(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=wdStg+'.ply',texture=omf+'l3/wood_stage/stage_z.tga',name='wdst',position=pos,scale=.03,rotation=(-90,90,0),color=color.rgb32(100,100,0))
		Entity(model=wfc,position=(s.x,s.y-.46,s.z-1.5),scale=(4.2,1,1.2),name=s.name,collider=b,visible=False)
		Entity(model=wfc,position=(s.x,s.y-.46,s.z+.2),scale=(1.2,1,2.3),name=s.name,collider=b,visible=False)
		del pos

tlX=omf+'l3/tile/tile'
class StoneTileBig(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=tlX+'_big.obj',texture=tlX+'.png',position=pos,scale=.35)
		s.collider=BoxCollider(s,center=Vec3(0,-.1,0),size=(7.3,1,7.3))
		del pos

lbP=omf+'l3/mtree_scn/'
class MushroomTree(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=lbP+'BNTree.ply',name='mtbt',texture=lbP+'tm_scn.tga',position=pos,scale=.03,color=color.rgb32(180,180,180),rotation=(-90,90,0))
		Entity(model=wfc,name=s.name,scale=(1.3,.5,.5),position=(s.x-.1,s.y+2.15,s.z-1.1),collider=b,visible=False)
		Entity(model=wfc,name=s.name,position=(s.x,s.y+3,s.z-.6),scale=(1,7,.5),collider=b,visible=False)
		del pos

tfm=omf+'l3/foam/'
class Foam(Entity):
	def __init__(self,pos,t):
		s=self
		super().__init__(model='quad',texture=tfm+'0.png',position=pos,scale=(5,1),texture_scale=(10,1),rotation=(90,{0:0,1:180}[t],0))
		s.typ=t
		s.frm=0
		if t == 1:
			s.color=color.rgb32(210,210,210)
			s.frm=15.99
		del pos,t
	def flow_normal(self):
		s=self
		s.frm+=time.dt*6
		if s.frm > 15.9:
			s.frm=0
	def flow_reverse(self):
		s=self
		s.frm-=time.dt*6
		if s.frm <= 0:
			s.frm=15.99
	def update(self):
		if st.gproc():
			return
		s=self
		s.texture=tfm+f'{int(s.frm)}.png'
		if s.typ == 1:
			s.flow_reverse()
			return
		s.flow_normal()

class BonusBackground(Entity):
	def __init__(self,pos,sca):
		super().__init__(model='quad',texture='res/background/bonus_1.jpg',name='bbgn',scale=sca,texture_scale=(1,1),position=pos,color=color.rgb32(100,60,80),unlit=False,shader=unlit_shader)
		del pos,sca

bcnn=omf+'l3/mtree_scn/'
class BonusScene(Entity):
	def __init__(self,pos):
		super().__init__(model=bcnn+'wtr_bSCN.ply',texture=bcnn+'tm_scn.tga',name='bnsc',position=pos,scale=.035,rotation=(-90,90,0))
		del pos

####################
## level 4 objects #
_sPA=omf+'l4/scn/'
class SewerTunnel(Entity):
	def __init__(self,pos,c=color.white):
		s=self
		super().__init__(model=_sPA+'tunnel.ply',texture=_sPA+'sewer2.tga',name='swtu',position=pos,color=c,scale=(.032,.034,.03),rotation=(-90,90,0))
		del pos,c

_SE=omf+'l4/scn/'
class SewerEscape(Entity):
	def __init__(self,pos,typ=None,c=color.white):
		s=self
		super().__init__(model=_SE+'pipe_1.ply',texture=_SE+'sewers.tga',name='swec',position=pos,scale=.048,color=c,rotation=(-90,90,0))
		if typ == 1:
			SewerGlowIron(pos=(s.x,s.y+.2,s.z+2.5),sca=(10,.01,10))
			s.color=color.rgb32(255,50,0)
			s.unlit=False
		del pos,c,typ

class SewerGlowIron(Entity):
	def __init__(self,pos,sca):
		super().__init__(model='cube',texture=_SE+'swr_iron.png',position=pos,scale=sca,color=color.rgb32(255,50,0),texture_scale=(sca[0],sca[2]),unlit=False,collider=b)
		del pos,sca
	def update(self):
		s=self
		if st.gproc():
			return
		if s.intersects(LC.ACTOR):
			cc.get_damage(LC.ACTOR,rsn=4)

mo=omf+'l4/scn/sewer_wall_bg'
class SewerWall(Entity):
	def __init__(self,pos):
		super().__init__(model=mo+'.ply',texture=mo+'.tga',name='ssww',position=pos,scale=.0175,color=color.rgb(.6,.5,.4),rotation=(-90,90,0))
		del pos

swmi=omf+'l4/swr_swim/swr_swim'
class SwimPlatform(Entity):##box collider
	def __init__(self,pos):
		s=self
		super().__init__(model=swmi+'.obj',texture=swmi+'.tga',name='swpt',scale=.00625,position=pos,color=color.rgb32(120,200,200),double_sided=True)
		s.collider=BoxCollider(s,size=Vec3(100,30,100))
		s.active=False
		s.matr='metal'
		s.spawn_y=s.y
		s.f_time=0
		del pos
	def sink(self):
		s=self
		s.y-=time.dt
		if s.y <= s.spawn_y-.3:
			sn.pc_audio(ID=10)
			s.collider=None
			s.active=False
			s.f_time=0
			invoke(lambda:setattr(s,'y',s.spawn_y),delay=5)
			invoke(lambda:setattr(s,'collider',b),delay=5)
	def update(self):
		if not st.gproc():
			s=self
			if s.active:
				s.f_time+=time.dt
				if s.f_time >= .5:
					s.sink()

swfl=omf+'l4/floor/swr_floor'
class SewerFloor(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=swfl+'.obj',texture=swfl+'.png',name='swff',position=pos,scale=.5)
		s.collider=BoxCollider(s,center=Vec3(0,-.5,0),size=(5,1.2,9.5))
		s.matr='metal'
		del pos

swn=omf+'l4/swr_entrance/swr_entrance'
class SewerEntrance(Entity):
	def __init__(self,pos):
		super().__init__(model=swn+'.ply',texture=swn+'.jpg',name='swri',position=pos,rotation_y=90,scale=2)
		del pos

swrp=omf+'l4/pipe/swpipe_'
class SewerPipe(Entity):## danger
	def __init__(self,pos,typ):
		s=self
		super().__init__(model=swrp+f'{typ}.ply',texture=swrp+f'{typ}.png',name='swpi',position=pos,scale=.75,rotation=(-90,{0:-90,1:-90,2:90,3:90}[typ],0))
		s.danger=(typ == 3)
		s.typ=typ
		if typ == 2:
			has_drips=random.randint(0,3)
			if has_drips == 3:
				DrippingWater(pos=(s.x,s.y-.2,s.z-.5),sca=(.9,.4))
		elif typ == 3:
			s.collider=BoxCollider(s,size=Vec3(.5,.5,5))
			s.rotation_x=0
			s.color=color.red
			s.unlit=False
		del pos,typ
	def update(self):
		s=self
		if not st.gproc() and s.typ == 3:
			if s.intersects(LC.ACTOR):
				cc.get_damage(LC.ACTOR,rsn=4)

wtt=omf+'l4/wtr/'
class EletricWater(Entity):
	def __init__(self,pos,sca):
		s=self
		super().__init__(model='cube',texture=wtt+'0.png',name='elwt',position=pos,scale=(sca[0],.1,sca[1]),texture_scale=(sca[0],sca[1]),color=color.rgb32(0,180,180),alpha=.9,collider=b)
		s.tx=(sca[0],sca[1])
		s.electric=False
		s.nr=False
		s.splash=0
		s.frm=0
		s.tme=8
		del pos,sca
	def wtr_anim(self):
		s=self
		s.frm=min(s.frm+time.dt*8,31.999)
		if s.frm > 31.99:
			s.frm=0
		s.texture=wtt+f'{int(s.frm)}.png'
	def wtr_danger(self):
		s=self
		if not s.electric:
			s.electric=True
			s.color=color.yellow
			s.unlit=False
			s.alpha=.9
			if (LC.ACTOR.warped and not st.bonus_round):
				if s.nr:
					sn.obj_audio(ID=7)
			invoke(s.wtr_normal,delay=1.5)
	def wtr_normal(self):
		s=self
		if not s:
			del s
			return
		s.electric=False
		s.color=color.rgb32(0,125,125)
		s.unlit=True
		s.alpha=.9
	def check_p(self):
		s=self
		ta=LC.ACTOR
		if ta.inwt <= 0:
			s.splash=max(s.splash-time.dt,0)
		if s.intersects(ta):
			ta.inwt=.3
			if s.electric:
				cc.get_damage(ta,rsn=6)
			if s.splash <= 0:
				s.splash=.3
				sn.pc_audio(ID=10)
	def update(self):
		if st.gproc():
			return
		s=self
		s.nr=wtr_dist(w=s,p=LC.ACTOR)
		if s.nr:
			s.check_p()
			s.wtr_anim()
			s.tme=max(s.tme-time.dt,0)
			if s.tme <= 0:
				if s.x > 180:
					s.tme=random.uniform(.1,.2)
				else:
					s.tme=8
				s.wtr_danger()

dpw=omf+'l4/drips/'
class DrippingWater(Entity):
	def __init__(self,pos,sca):
		s=self
		super().__init__(model='quad',texture=dpw+'0.png',name='drpw',position=pos,scale=sca,rotation_z=90)
		s.frm=0
		del pos,sca
	def update(self):
		s=self
		if st.gproc() or (distance(s,LC.ACTOR) > 8):
			return
		s.frm=min(s.frm+(time.dt*10),7.999)
		if s.frm > 7.99:
			s.frm=0
		s.texture=dpw+f'{int(s.frm)}.png'


####################
## level 5 objects #
rnp=omf+'l5/ruins_scn/ruins_'
class RuinsPlatform(Entity):##big platform
	def __init__(self,pos,m):
		s=self
		super().__init__(model=rnp+'ptf1.obj',texture=rnp+'scn.tga',name='rnsp',position=pos,rotation_y=-90,scale=.03,double_sided=True)
		s.collider=BoxCollider(s,center=Vec3(0,-5,0),size=(55,10,55))
		HitBox(pos=(s.x,s.y+.4,s.z+.9),sca=(1.7,.5,.3))
		if m:
			HitBox(pos=(s.x+.9,s.y+.4,s.z),sca=(.3,.5,1.7))
			s.scale_z=-.03
			del pos,m
			return
		HitBox(pos=(s.x-.9,s.y+.4,s.z),sca=(.3,.5,1.7))
		del pos,m

class RuinsCorridor(Entity):## corridor
	def __init__(self,pos):
		s=self
		super().__init__(model=wfc,position=pos,scale=(3,1,3),name='rncr',collider=b,visible=False)
		s.opt_model=Entity(model=rnp+'cor.ply',texture=rnp+'scn.tga',name=s.name,position=(s.x,s.y+.5,s.z),scale=.03,rotation=(-90,90,0))
		s.cor_w0=Entity(model=wfc,position=(s.x-1.4,s.y+1.7,s.z),name=s.name,scale=(.5,2,3),collider=b,visible=False)
		s.cor_w1=Entity(model=wfc,position=(s.x+1.4,s.y+1.7,s.z),name=s.name,scale=(.5,2,3),collider=b,visible=False)
		IndoorZone(pos=(s.x,s.y+2.55,s.z),sca=3)
		del pos

rmsc=omf+'l5/m_sculpt/m_sculpt'
class MonkeySculpture(Entity):
	def __init__(self,pos,r,d,ro_y=90):
		s=self
		super().__init__(name='mnks',position=pos,scale=.003,rotation=(-90,ro_y,0))
		s.model=rmsc+'1.ply'
		if r:
			s.model=rmsc+'.ply'
			s.podium=Entity(model='cube',texture='res/terrain/l5/moss.png',name=s.name,scale=(.5,1,.5),texture_scale=(1,2),position=(s.x,s.y-.5,s.z))
		s.texture=rmsc+'.tga'
		s.f_pause=False
		s.s_audio=False
		s.danger=d
		s.f_cnt=0
		s.tme=.08
		s.rot=r
		del ro_y,pos,r,d
	def f_reset(self):
		s=self
		s.f_pause=False
		s.f_cnt=0
	def fire_throw(self):
		s=self
		if (distance(s,LC.ACTOR) < 8 and not st.gproc()):
			if s.f_cnt >= 30:
				if not s.f_pause:
					s.f_pause=True
					invoke(s.f_reset,delay=5)
				return
			ef.FireThrow(pos=s.position,ro_y=s.rotation_y)
			s.f_cnt+=1
			if not s.s_audio:
				s.s_audio=True
				sn.obj_audio(ID=10,pit=1)
				invoke(lambda:setattr(s,'s_audio',False),delay=3)
	def rot_to_crash(self):
		s=self
		if distance(s,LC.ACTOR) < 2:
			cc.rotate_to_crash(s)
	def update(self):
		if st.gproc():
			return
		s=self
		if s.danger:
			s.tme=max(s.tme-time.dt,0)
			if s.tme <= 0:
				s.tme=.08
				s.fire_throw()
		if s.rot:
			s.rot_to_crash()

lpp=omf+'l5/loose_ptf/'
class LoosePlatform(Entity):
	def __init__(self,pos,t):
		s=self
		super().__init__(model=lpp+f'{t}/'+'lpf.obj',texture=lpp+f'{t}/'+'lpf.tga',name='loos',scale=.01/15,position=pos,rotation_y=90,double_sided=True)
		s.collider=BoxCollider(s,center=Vec3(0,-.5,0),size=(100*10,100,100*10))
		s.active=False
		s.typ=t
		del pos,t
	def reset(self):
		s=self
		s.collision,s.visible,s.active=True,True,False
	def collapse(self):
		s=self
		sn.obj_audio(ID=9,pit=1)
		s.collision=False
		invoke(s.reset,delay=8)
	def action(self):
		s=self
		s.visible=False
		an.CollapseFloor(t=s.typ,pos=s.position)
		invoke(s.collapse,delay=1)
	def pl_touch(self):
		s=self
		if not s.active:
			s.active=True
			s.action()

rrn=omf+'l5/ruins_bgo/'
class RuinRuins(Entity):
	def __init__(self,pos,typ,ro_y):
		if typ == 3:
			super().__init__(model=rrn+'ruin_bg'+str(typ)+'.ply',name='rrrr',texture=rrn+'ruin_scene.tga',position=pos,scale=.08,rotation=(-90,ro_y,0),unlit=False)
			del pos,typ,ro_y
			return
		super().__init__(model=rrn+'ruin_bg'+str(typ)+'.ply',name='rrrr',texture=rrn+'ruin.tga',position=pos,scale=.03,rotation=(-90,ro_y,0),unlit=False)
		del pos,typ,ro_y

class LogDanger(Entity):
	def __init__(self,pos,ro_y):
		s=self
		ldg=omf+'l5/log_danger/log_danger'
		super().__init__(model=ldg+'.ply',texture=ldg+'.tga',position=pos,scale=.001,rotation=(-90,ro_y,0),collider=b,unlit=False)
		s.spawn_pos=s.position
		s.stop_throw=False
		s.fly_time=0
		s.start_delay=.3
		s.life_time=3
		s.direc_y=0
		del pos,ro_y
	def fly(self):
		s=self
		fsp=3.2
		fdi={0:lambda:setattr(s,'z',s.z-time.dt*fsp),
			90:lambda:setattr(s,'x',s.x-time.dt*fsp),
			180:lambda:setattr(s,'z',s.z+time.dt*fsp),
			-90:lambda:setattr(s,'x',s.x+time.dt*fsp)}
		fdi[s.rotation_y]()
		s.rotation_x-=time.dt*100
	def fly_away(self,di):
		s=self
		s.position+=di*time.dt*40
		s.fly_time+=time.dt
		if s.fly_time > .5:
			cc.purge_instance(s)
			return
	def hit_ground(self):
		s=self
		if s.direc_y == 0:
			s.y-=time.dt*3
			if s.y <= s.spawn_pos[1]-.4:
				s.direc_y=1
				if distance(s,LC.ACTOR) < 5:
					sn.obj_audio(ID=11)
			return
		s.y+=time.dt*3
		if s.y >= s.spawn_pos[1]+.3:
			s.direc_y=0
	def update(self):
		if not st.gproc():
			ac=LC.ACTOR
			s=self
			s.life_time=max(s.life_time-time.dt,0)
			if s.life_time <= 0:
				cc.purge_instance(s)
				return
			if s.stop_throw:
				s.fly_away(di=Vec3(s.x-ac.x,0,s.z-ac.z))
				return
			s.fly()
			s.start_delay=max(s.start_delay-time.dt,0)
			if s.start_delay <= 0:
				s.hit_ground()
				if s.intersects(ac):
					if LC.ACTOR.is_attack:
						sn.obj_audio(ID=8)
						s.stop_throw=True
						return
					cc.get_damage(LC.ACTOR,rsn=2)

class RuinsScene(Entity):
	def __init__(self):
		s=self
		super().__init__(model='quad',texture=bgg+'bg_ruins.jpg',scale=(800,120),texture_scale=(2,1),position=(50,-38,128),color=color.rgb32(160,160,170),shader=unlit_shader)
		s.orginal_x,s.orginal_y=s.x,s.y
		s.orginal_tsc=s.texture_scale
		s.spawn_y=s.y
		s.bonus_y=-70
		LC.bgT=s
	def update(self):
		s=self
		if st.bonus_round:
			s.y=s.bonus_y
			return
		if s.y != s.spawn_y:
			s.y=s.spawn_y


####################
## level 6 objects #
besc=omf+'l6/bgscn/bscn'
class BeeSideWall(Entity):
	def __init__(self,pos,t):
		super().__init__(model=besc+f'{t}.obj',name='bewa',texture=besc+f'{t}.tga',position=pos,scale=.14,rotation_y=-90,double_sided=True,color=color.rgb32(160,160,160))
		del pos,t

befl=omf+'l6/floor/floor'
class BeeFloor(Entity):
	def __init__(self,pos,t):
		s=self
		super().__init__(model=befl+f'{t}.obj',texture=befl+'.png',name='bbfl',position=pos,scale=.6,double_sided=True,rotation_y=90)
		s.collider=BoxCollider(s,size=Vec3(4,6,4))
		del pos,t

betr=omf+'l6/wall/tree_wall'
class BeeSideTree(Entity):
	def __init__(self,pos,m=False):
		bsc=(.01,.01,.01)
		btr=-90
		if m:
			bsc=(-.01,.01,.01)
			btr=90
		super().__init__(model=betr+'.obj',name='bbst',texture=betr+'.tga',position=pos,scale=bsc,double_sided=True,rotation_y=btr)
		del bsc

brtv='res/terrain/l6/bee_terra.png'
class BeeBigGround(Entity):
	def __init__(self,pos,sca):
		super().__init__(model='cube',name='bbgn',texture=brtv,position=pos,texture_scale=(sca[0],sca[2]),scale=sca,collider=b)
		del pos,sca

behv=omf+'l6/hive/0'
class Hive(Entity):
	def __init__(self,pos,bID,bMAX):
		s=self
		super().__init__(model=behv+'.ply',texture=behv+'.tga',position=pos,scale=.1/150,rotation_x=-90)
		s.locked=False
		s.bees_out=0
		s.bMAX=bMAX
		s.bID=bID
		s.tme=.3
		s.frm=0
		del pos,bID,bMAX
	def is_own_bee(self):
		s=self
		s.bees_out=0
		for qv in scene.entities[:]:
			if isinstance(qv,npc.Bee) and qv.bID == s.bID:
				s.bees_out+=1
				s.locked=(s.bees_out >= s.bMAX)
	def spawn_bee(self):
		s=self
		npc.Bee(pos=s.position,bID=s.bID)
	def update(self):
		if st.gproc():
			return
		s=self
		s.tme=min(s.tme-time.dt,0)
		if s.tme <= 0:
			s.tme=.3
			s.is_own_bee()
		if (LC.ACTOR.z < s.z+10) and (LC.ACTOR.z > s.z-1.5):
			if not s.locked:
				an.hive_awake(s,sp=12)

tk=omf+'l6/tikki/'
class TikkiSculpture(Entity):
	def __init__(self,pos,spd,rng):
		s=self
		super().__init__(model=tk+'0.ply',texture=tk+'0.tga',position=pos,scale=.0004,rotation_x=-90,name='tksc',collider=b)
		s.is_moving=False
		s.move_speed=spd
		s.move_point=pos
		s.spawn_pos=pos
		s.an_pause=0
		s.an_mode=0
		s.tme=1
		s.frm=0
		s.rng=rng
		del pos,spd,rng
	def move_to_point(self):
		s=self
		if distance(s.position,s.move_point) < .1:
			s.is_moving=False
			return
		s.position=lerp(s.position,s.move_point,time.dt*s.move_speed)
	def update(self):
		if st.gproc():
			return
		s=self
		s.an_pause=max(s.an_pause-time.dt,0)
		if s.intersects(LC.ACTOR):
			cc.get_damage(LC.ACTOR,rsn=2)
		if s.an_pause <= 0:
			an.tikki_rotate(s,sp=14)
		if s.is_moving:
			s.move_to_point()
			return
		s.tme=max(s.tme-time.dt,0)
		if s.tme <= 0:
			s.tme=1/s.move_speed
			ksp=s.spawn_pos
			s.move_point=random.choice([(ksp[0]+s.rng,ksp[1],ksp[2]),(ksp[0]-s.rng,ksp[1],ksp[2]),(ksp[0],ksp[1],ksp[2]+s.rng),(ksp[0],ksp[1],ksp[2]-s.rng)])
			s.is_moving=True
			del ksp

lm=omf+'l6/lmine/'
class LandMine(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=lm+'0.ply',name='ldmn',texture=lm+'0.tga',position=pos,rotation_x=-90,scale=.00065)
		s.explode=False
		s.p_snd=False
		s.frm=0
		s.tme=1
		del pos
	def purge(self):
		s=self
		LC.LDM_POS.append(s.position)
		destroy(s)
	def m_audio(self):
		s=self
		s.tme=max(s.tme-time.dt,0)
		if s.tme <= 0:
			s.tme=random.randint(1,2)
			sn.obj_audio(ID=12,pit=random.uniform(.8,1))
	def explosion(self):
		s=self
		s.frm=0
		LC.ACTOR.stun_fd=(s.x,s.y,s.z+2)
		LC.ACTOR.stun=True
		s.explode=True
		if not s.p_snd:
			s.p_snd=True
			ef.Fireball(s)
			sn.crate_audio(ID=10)
	def update(self):
		if not st.gproc():
			s=self
			if s.explode:
				LC.ACTOR.y=lerp(LC.ACTOR.y,s.y+1,time.dt*12)
				an.mine_destroy(s,sp=12)
				return
			lmd=distance(s,LC.ACTOR)
			an.land_mine(s,sp=12)
			if lmd < .3:
				s.explosion()
				return
			if lmd < 2:
				s.m_audio()

stwl=omf+'l6/stone_wall/stone_wall'
class StoneWall(Entity):
	def __init__(self,pos):
		super().__init__(model=stwl+'.obj',texture=stwl+'.png',position=pos,scale=(.5,.5,.3),color=color.rgb32(90,140,180),collider=b)
		del pos

class FrontStoneWall(Entity):
	def __init__(self,pos):
		super().__init__(model=stwl+'_front.ply',texture=stwl+'.png',position=pos,scale=.6,rotation=(90,0,0),collider=b)
		del pos

bnbn=omf+'l6/bwall/bwall'
class BonusBeeWall(Entity):
	def __init__(self,pos):
		super().__init__(model=bnbn+'.obj',name='bnsw',texture=bnbn+'.tga',position=pos,scale=.02,rotation_y=-90,color=color.rgb32(120,160,120),double_sided=True)
		del pos

bsbq=omf+'l6/stone_wall/'
class BeeSideBlock(Entity):
	def __init__(self,pos):
		super().__init__(model=bsbq+'sblock.ply',texture=bsbq+'stone_wall.png',position=pos,scale=.5,rotation=(-90,0,0),color=color.rgb32(200,170,180),double_sided=True)
		del pos


####################
## level 7 objects #
lbcb=omf+'l7/lab_ptf/lab_ptf'
class LabTile(Entity):
	def __init__(self,pos,typ=0,ro_y=0,sca_y=.8):
		s=self
		super().__init__(model=lbcb+'.obj',texture=lbcb+'.png',name='labt',position=pos,scale=(.5,sca_y,.5),collider=b,rotation_y=ro_y)
		s.matr='metal'
		s.typ=typ
		s.danger=not(typ in {0,3})
		if typ == 1:
			s.color=color.red
			s.unlit=False
		if typ == 2:
			s.is_heat=True
			s.heat_color=0
			s.refr=0
			s.unlit=False
		if typ == 3:
			s.texture=lbcb+'_e.png'
		del pos
	def update(self):
		s=self
		if st.gproc() or s.typ in {0,1,3}:
			return
		s.danger=(s.heat_color <= 0)
		s.color=color.rgb32(255,int(s.heat_color),int(s.heat_color))
		s.refr=max(s.refr-time.dt,0)
		rtu=time.dt*80
		if s.refr <= 0:
			if s.is_heat:
				s.heat_color=min(s.heat_color+rtu,255)
				if s.heat_color >= 255:
					s.refr=1
					s.is_heat=False
				return
			s.heat_color=max(s.heat_color-rtu,0)
			if s.heat_color <= 0:
				s.refr=1
				s.is_heat=True

lbscn=omf+'l7/lab_bgs/lab_bgs'
class LabScene(Entity):
	def __init__(self,pos):
		super().__init__(model=lbscn+'.ply',texture=lbscn+'.tga',name='lbbr',position=pos,scale=.015,rotation=(-90,90,0),double_sided=True)
		if pos[1] < -15:
			self.color=color.rgb32(200,100,200)
		del pos

lbpi=omf+'l7/piston/piston'
class Piston(Entity):
	def __init__(self,pos,typ,spd):
		s=self
		rj=-90
		super().__init__(model=lbpi+'.ply',texture=lbpi+'.tga',position=pos,scale=(.1/110,.1/110,.1/100),rotation=(rj,0,0),collider=b)
		s.danger=True
		s.spawn_y=s.y
		s.mvspd=spd
		s.tme=spd
		s.typ=typ
		s.mode=0
		del pos,typ,spd
	def stomp(self):
		s=self
		s.y=max(s.y-time.dt*s.mvspd,s.spawn_y-2.051)
		if s.y <= s.spawn_y-2.05:
			jg=s.intersects(LC.ACTOR)
			if jg and jg.normal == Vec3(0,-1,0) and s.danger:
				cc.get_damage(LC.ACTOR,rsn=2)
			s.danger=False
			if distance(s,LC.ACTOR) < 8:
				sn.obj_audio(ID=13,pit=.8)
			s.mode=1
			s.tme=.5
	def reset(self):
		s=self
		s.y=min(s.y+time.dt*s.mvspd,s.spawn_y+.1)
		if s.y >= s.spawn_y:
			s.danger=True
			if distance(s,LC.ACTOR) < 8:
				sn.obj_audio(ID=13,pit=.5)
			s.mode=0
			s.tme=1-(1/s.mvspd)
	def update(self):
		if st.gproc():
			return
		s=self
		s.tme=max(s.tme-time.dt,0)
		if s.tme <= 0:
			pva={0:lambda:s.stomp(),1:lambda:s.reset()}
			pva[s.mode]()
			del pva

lbff=omf+'l7/piston_ptf/piston_ptf'
class PistonPlatform(Entity):
	def __init__(self,pos,spd,pa):
		s=self
		super().__init__(model=lbff+'.obj',texture=lbff+'.tga',name='pipf',position=pos,scale=.1/100,double_sided=True)
		s.collider=BoxCollider(s,size=Vec3(700,700,700),center=Vec3(0,1685,0))
		s.matr='metal'
		s.spw_y=s.y
		s.mvsp=spd
		s.wait=0
		s.stat=0
		s.wt=pa
		del pos,spd,pa
	def mv_down(self):
		s=self
		if s.y > s.spw_y-1.7:
			s.y-=time.dt*s.mvsp*2.5
			return
		s.wait=s.wt
		s.stat=1
		if distance(s,LC.ACTOR) < 8:
			sn.obj_audio(ID=13,pit=.5)
	def mv_up(self):
		s=self
		if s.y < s.spw_y:
			s.y+=time.dt*s.mvsp
			return
		s.wait=s.wt*2
		s.stat=0
		if distance(s,LC.ACTOR) < 8:
			sn.obj_audio(ID=13,pit=.8)
	def update(self):
		if st.gproc():
			return
		s=self
		s.wait=max(s.wait-time.dt,0)
		if s.wait <= 0:
			if s.stat == 0:
				s.mv_down()
				return
			s.mv_up()

lpad=omf+'l7/e_pad/'
class LabPad(Entity):
	def __init__(self,pos,ID):
		s=self
		super().__init__(model=lpad+'0/0.ply',texture=lpad+'0/0.tga',name='epad',position=pos,scale=.1/85,rotation_x=-90,collider=b)
		s.active=False
		s.locked=False
		s.matr='metal'
		s.mode=0
		s.frm=0
		s.tme=1
		s.ID=ID
		LabTaser(pos=(s.x,s.y+LC.ltth,s.z),ID=s.ID)
		del pos,ID
	def trigger_taser(self):
		for lpo in scene.entities[:]:
			if isinstance(lpo,LabTaser) and lpo.ID == self.ID:
				lpo.shoot_laser()
	def disable_pad(self):
		s=self
		s.mode=0
		s.unlit,s.locked=True,False
		s.texture=lpad+'0/0.tga'
	def enable_pad(self):
		s=self
		s.tme=.5
		if not s.locked:
			sn.obj_audio(ID=15,pit=.5)
			s.locked=True
			s.trigger_taser()
		s.mode=1
		s.texture=lpad+'1/0.tga'
		s.unlit=False
	def update(self):
		if st.gproc():
			return
		s=self
		an.pad_refr(s)
		s.tme=max(s.tme-time.dt,0)
		if s.active:
			s.active=False
			s.enable_pad()
			return
		if s.tme <= 0:
			s.disable_pad()

lbts=omf+'l7/lab_taser/'
class LabTaser(Entity):
	def __init__(self,pos,ID):
		s=self
		super().__init__(model=lbts+'0.ply',texture=lbts+'0.tga',name='ltts',position=pos,scale=.1/150,rotation_x=-90)
		s.frm=0
		s.ID=ID
		del pos,ID
	def shoot_laser(self):
		sn.obj_audio(ID=14)
		ef.ElectroBall(pos=self.position)
	def update(self):
		if not st.gproc():
			an.taser_rotation(self)

llpt=omf+'l7/space_ptf/space_ptf'
class LabPlatform(Entity):
	def __init__(self,pos,drc,spd,rng):
		s=self
		super().__init__(model=llpt+'.ply',texture=llpt+'.tga',position=pos,scale=.1/120,rotation_x=-90,unlit=False,collider=b)
		s.spawn_pos=pos
		s.matr='metal'
		s.mv_rng=rng
		s.mv_spd=spd
		s.direc=drc
		s.mode=0
		del pos,spd,drc,rng
	def ptf_fwd(self):
		s=self
		kfv={0:lambda:setattr(s,'z',s.z+time.dt*s.mv_spd),1:lambda:setattr(s,'z',s.z-time.dt*s.mv_spd)}
		kfv[s.mode]()
		del kfv
		if (s.mode == 0 and s.z >= s.spawn_pos[2]+s.mv_rng) or (s.mode == 1 and s.z <= s.spawn_pos[2]-s.mv_rng):
			if s.mode == 0:
				s.mode=1
				return
			s.mode=0
	def ptf_up(self):
		s=self
		kfv={0:lambda:setattr(s,'y',s.y+time.dt*s.mv_spd),1:lambda:setattr(s,'y',s.y-time.dt*s.mv_spd)}
		kfv[s.mode]()
		del kfv
		if (s.mode == 0 and s.y >= s.spawn_pos[1]+s.mv_rng) or (s.mode == 1 and s.y <= s.spawn_pos[1]-s.mv_rng):
			if s.mode == 0:
				s.mode=1
				return
			s.mode=0
	def ptf_sd(self):
		s=self
		kfv={0:lambda:setattr(s,'x',s.x+time.dt*s.mv_spd),1:lambda:setattr(s,'x',s.x-time.dt*s.mv_spd)}
		kfv[s.mode]()
		del kfv
		if (s.mode == 0 and s.x >= s.spawn_pos[0]+s.mv_rng) or (s.mode == 1 and s.x <= s.spawn_pos[0]-s.mv_rng):
			if s.mode == 0:
				s.mode=1
				return
			s.mode=0
	def update(self):
		if st.gproc():
			return
		s=self
		svd={0:lambda:s.ptf_sd(),1:lambda:s.ptf_fwd(),2:lambda:s.ptf_up()}
		svd[s.direc]()
		del svd

lbpg=omf+'l7/lab_pipe/lab_pipe'
class LabPipe(Entity):
	def __init__(self,pos):
		super().__init__(model=lbpg+'.ply',texture=lbpg+'.tga',name='lapi',position=pos,scale=.05,rotation=(-90,90,0))
		del pos

lbfa=omf+'l7/boiler/boiler'
class Boiler(Entity):
	def __init__(self,pos,ro_y=0):
		super().__init__(model=lbfa+'.ply',texture=lbfa+'.tga',name='labo',position=pos,scale=.04,rotation=(-90,ro_y,0))
		del pos,ro_y

##################
## logic objects #
class FallingZone(Entity):## falling
	def __init__(self,pos,s,v=False):
		super().__init__(model='cube',name='fllz',collider=b,scale=s,position=pos,color=color.black,visible=v)
	def update(self):
		ac=LC.ACTOR
		if self.intersects(ac):
			cc.dth_event(ac,rsn=1)

class WaterHit(Entity):## collider for water
	def __init__(self,p,sc):
		super().__init__(model=wfc,name='wtrh',collider=b,position=p,scale=(sc[0],.2,sc[1]),visible=False)

class CrateScore(Entity):## level reward
	def __init__(self,pos):
		s=self
		ev='res/crate/'
		super().__init__(model=ev+'cr_t0.ply',texture=ev+'1.tga',alpha=.4,scale=.18,position=pos,origin_y=.5)
		s.cc_text=Text(parent=scene,position=(s.x-.2,s.y,s.z),name=s.name,text=None,font=ui._fnt,color=color.rgb32(255,255,100),scale=10,unlit=False)
		print(f'<info> level {st.level_index} boxes:  {st.crates_in_level}')
		del pos
	def update(self):
		if st.gproc():
			return
		s=self
		dv=(LC.C_GEM and distance(s,LC.C_GEM) < .5)
		s.cc_text.visible,s.visible=not(dv),not(dv)
		if s.visible:
			s.cc_text.text=f'{st.crate_count}/{st.crates_in_level}'
			s.rotation_y-=120*time.dt
		if st.crate_count >= st.crates_in_level:
			item.GemStone(pos=(s.x,s.y-.3,s.z),c=0)
			sn.ui_audio(ID=4)
			destroy(s.cc_text)
			destroy(s)

rmp=omf+'ev/s_room/room'
class StartRoom(Entity):## game spawn point
	def __init__(self,pos):
		s=self
		super().__init__(model=rmp+'.ply',texture=rmp+'.tga',name='strm',position=pos,scale=(.07,.07,.08),rotation=(270,90),color=color.white)
		HitBox(pos=(s.x,s.y+.6,s.z-.2),sca=(1.7,.5,1.7))#floor 0
		HitBox(pos=(s.x,s.y+.2,s.z+1.7),sca=(2,.5,2))#floor 1
		HitBox(pos=(s.x-1,s.y+1.5,s.z),sca=(.4,13,6))#wall left
		HitBox(pos=(s.x+1,s.y+1.5,s.z),sca=(.4,13,6))#wall right
		HitBox(pos=(s.x,s.y+1.5,s.z-1),sca=(5,13,.6))#back wall
		HitBox(pos=(s.x,s.y+2.6,s.z-.2),sca=(6,1,6))#curtain
		Entity(model='plane',name=s.name,position=(s.x,s.y+0.01,s.z),color=color.black,scale=3)
		Entity(model='quad',name=s.name,color=color.black,scale=(6,.5),position=(s.x,s.y+2.3,s.z+2.4))
		RoomDoor(pos=(s.x,s.y+1.875,s.z+2.3))
		player.CrashB(pos=(s.x,s.y+.85,s.z-.1))
		if st.aku_hit > 0:
			npc.AkuAkuMask(pos=(s.x-.3,s.y+1,s.z+.5))
		st.checkpoint=(s.x,s.y+2,s.z)
		camera.position=(s.x,s.y+2,s.z-3)
		IndoorZone(pos=(s.x,s.y+1.5,s.z),sca=(3,2,7))
		del pos

eR=omf+'ev/e_room/e_room'
class EndRoom(Entity):## finish level
	def __init__(self,pos,c):
		s=self
		super().__init__(model=eR+'.ply',texture=eR+'.tga',scale=.025,name='enrm',rotation=(-90,90,0),position=pos,color=c,unlit=False)
		Entity(model='plane',name=s.name,color=color.black,scale=(4,1,16),position=(s.x-1,s.y-1.8,s.z+3))#curtain
		HitBox(sca=(4,1,16),pos=(s.x-1,s.y-2,s.z+3))#floor
		HitBox(sca=(1,3,16),pos=(s.x-2.2,s.y,s.z+3))#wall left
		HitBox(sca=(1,3,16),pos=(s.x,s.y,s.z+3))#wall right
		HitBox(sca=(5,3,16),pos=(s.x-1,s.y+1.4,s.z+3))#ceiling
		HitBox(sca=(6,4,2),pos=(s.x,s.y,s.z+9))#back
		HitBox(sca=(6,1,2.5),pos=(s.x-1,s.y-1.85,s.z+.45))#pod1
		HitBox(sca=(.85,1,.85),pos=(s.x-1.1,s.y-1.6,s.z+.3))#pod2
		HitBox(sca=(1.6,1,1),pos=(s.x-1.1,s.y-1.51,s.z+6.5))#pod3
		IndoorZone(pos=(s.x-1,s.y,s.z+1),sca=(5,2,12))
		LevelFinish(p=(s.x-1.1,s.y-1.1,s.z+7))
		RoomDoor(pos=(s.x-1.1,s.y+.25,s.z-4.78))
		if st.level_index != 5:
			Entity(model='cube',scale=(20,10,.1),name=s.name,position=(s.x,s.y-5,s.z+16),color=color.black)
		if st.crates_in_level > 0 and not st.level_index in st.CLEAR_GEM:
			if s.x < 180:# pos_x 190 is death zone in lv 5
				CrateScore(pos=(s.x-1.1,s.y-.7,s.z))
		if st.level_index == 1 and not 4 in st.COLOR_GEM:
			item.GemStone(pos=(s.x-1.1,s.y-.9,s.z),c=4)
		if st.level_index == 2 and not 1 in st.COLOR_GEM:
			item.GemStone(pos=(s.x-1.1,s.y-.9,s.z),c=1)
		if st.level_index == 7 and not 7 in st.COLOR_GEM:
			item.GemStone(c=7,pos=(s.x-1.1,s.y-.9,s.z))
		del pos,c

class RoomDoor(Entity):## door for start and end room
	def __init__(self,pos):
		s=self
		s.dPA=omf+'ev/door/'
		super().__init__(model=s.dPA+'u0.ply',texture=s.dPA+'u_door.tga',name='rmdr',position=pos,scale=.001,rotation_x=90,collider=b)
		s.door_part=Entity(model=s.dPA+'d0.ply',name=s.name,texture=s.dPA+'d_door.tga',position=(s.x,s.y+.1,s.z),scale=.001,rotation_x=90,collider=b)
		s.d_opn=False
		s.d_frm=0
		del pos
	def update(self):
		if not st.gproc():
			ta=LC.ACTOR
			s=self
			qf=(distance(ta.position,s.position) < 2.4 or ta.z > s.z)
			ptw={True:lambda:an.door_open(s),False:lambda:an.door_close(s)}
			ptw[qf]()

class BonusPlatform(Entity):## switch -> bonus round
	def __init__(self,pos):
		s=self
		sIN='ev/bonus/bonus'
		if st.level_index == 7:
			sIN='ev/bonus/bonus_e'
			s.matr='metal'
		super().__init__(model=omf+sIN+'.ply',texture=omf+sIN+'.tga',name='bnpt',collider=b,scale=-.001,rotation_x=90,position=pos,unlit=False)
		s.start_y=s.y
		del pos
	def update(self):
		if st.bonus_solved:
			cc.purge_instance(self)

class GemPlatform(Entity):## gem platform
	def __init__(self,pos,t):
		s=self
		ne='gem_ptf_e'
		s.is_enabled=False
		if t in st.COLOR_GEM or settings.debg:
			ne='gem_ptf'
			s.is_enabled=True
			if settings.debg:
				t=0
		super().__init__(model=wfc,name='gmpt',scale=(.6,.4,.6),position=pos,collider=b,visible=False)
		s.opt_model=Entity(model=omf+'ev/'+ne+'/'+ne+'.ply',name=s.name,texture=omf+'ev/'+ne+'/'+ne+'.tga',rotation_x=-90,scale=.001,position=pos,color=LC.GMC[t],unlit=False)
		s.org_color=s.color
		s.start_y=s.y
		s.typ=t
		if not s.is_enabled:
			s.collider=None
			s.alpha=.5
		del pos,t
	def update(self):
		if not st.gproc():
			s=self
			if st.gem_path_solved:
				cc.purge_instance(s.opt_model)
				cc.purge_instance(s)
				return
			s.opt_model.position=(s.x,s.y+.15,s.z)
			if s.is_enabled and not LC.ACTOR.freezed:
				s.opt_model.rotation_y+=time.dt*20

class PseudoGemPlatform(Entity):
	def __init__(self,pos,t):
		s=self
		ne='gem_ptf_e'
		s.is_enabled=False
		if t in st.COLOR_GEM or settings.debg:
			ne='gem_ptf'
			s.is_enabled=True
			if settings.debg:
				t=0
		super().__init__(model=omf+'ev/'+ne+'/'+ne+'.ply',texture=omf+'ev/'+ne+'/'+ne+'.tga',rotation_x=-90,scale=.001,position=pos,color=LC.GMC[t],unlit=False)
		del pos,t
		if s.is_enabled:
			HitBox(pos=(s.x,s.y-.15,s.z),sca=(.6,.4,.6))
			return
		s.alpha=.5

#############
## Switches #
class LevelFinish(Entity):## finish level
	def __init__(self,p):
		s=self
		trpv=omf+'ev/teleport/warp_effect'
		super().__init__(model='sphere',name='lvfi',collider=b,scale=1,position=p,visible=False)
		ef.WarpVortex(pos=(s.x,s.y+.1,s.z),col=color.yellow,sca=.6,drc=1)
		ef.WarpVortex(pos=(s.x,s.y+.3,s.z),col=color.orange,sca=.7,drc=0)
		ef.WarpVortex(pos=(s.x,s.y+.5,s.z),col=color.yellow,sca=.8,drc=1)
		ef.WarpVortex(pos=(s.x,s.y+.7,s.z),col=color.orange,sca=.7,drc=0)
		s.w_audio=Audio('res/snd/misc/portal.wav',volume=0,loop=True)
		s.refr=.3
		del p
	def update(self):
		s=self
		if st.pause:
			s.w_audio.volume=0
			return
		s.refr=max(s.refr-time.dt,0)
		if s.refr <= 0:
			s.refr=.3
			if s.intersects(LC.ACTOR):
				cc.jmp_lv_fin()
				return
			if (distance(s,LC.ACTOR) < 10):
				nvv=max(0,1-(distance(s,LC.ACTOR)/10))
				s.w_audio.volume=min(1,nvv*settings.SFX_VOLUME)
				return
			s.w_audio.volume=0

class IndoorZone(Entity):## disable rain
	def __init__(self,pos,sca):
		super().__init__(model='cube',name='indz',scale=sca,position=pos,collider=b,visible=False)
		del pos,sca
	def update(self):
		if self.intersects(LC.ACTOR):
			LC.ACTOR.CMS=3.2
			LC.ACTOR.indoor=.3

###################
## global objects #
mpk={1:omf+'l1/block/block',
	2:omf+'l2/block/block',
	3:omf+'l3/tile/tile',
	4:omf+'l4/swr_tile/swr_tile',
	5:omf+'l5/block/block'}
class FloorBlock(Entity):
	def __init__(self,pos,ID,sca=0,ro_y=0,typ=0,EMD=False):
		s=self
		s.vnum=ID
		super().__init__(model=mpk[ID]+'.obj',texture=mpk[ID]+'.png',name='block',position=pos,scale=sca,rotation_y=ro_y,collider=b)
		s.double_sided=(ID in {4,5})
		if EMD:
			s.collider=None
			del pos,sca,ro_y,typ,ID,EMD
			return
		if ID == 2:
			s.rotation_y=180
			s.collider=BoxCollider(self,size=Vec3(2,4,2))
		if ID == 3:
			s.scale=.35
			s.collider=BoxCollider(s,center=Vec3(0,-.1,0),size=Vec3(2.4,1,2.4))
		if ID == 4:
			s.scale=.02
			s.collider=BoxCollider(s,size=Vec3(25,4,25))
			s.matr='metal'
		if ID == 5:
			s.scale=.03
			s.rotation_y=-90
			s.collider=BoxCollider(s,center=Vec3(0,-7.5,0),size=(25,15,25))
		del pos,sca,ro_y,typ,ID

class HitBox(Entity):
	def __init__(self,pos,sca):
		super().__init__(model=wfc,position=pos,scale=sca,collider=b,name='htbx',visible=False)
		del pos,sca

class LightArea(SpotLight):
	def __init__(self,pos):
		super().__init__(position=pos,color=color.white)
		self.ta=LC.ACTOR
		del pos
	def update(self):
		if not st.gproc():
			self.position=(self.ta.x+.5,self.ta.y+1.5,self.ta.z+1)

class InvWall(Entity):
	def __init__(self,pos,sca):
		super().__init__(model=wfc,position=pos,scale=sca,visible=False,collider=b)
		del pos,sca

wtfc=omf+'ev/water/water_'
class Water(Entity):
	def __init__(self,pos,sca,c,a):
		s=self
		super().__init__(model='plane',texture=wtfc+'0.tga',position=pos,scale=(sca[0],.1,sca[1]),color=c,alpha=a)
		WaterHit(p=(pos[0],pos[1]-.1,pos[2]),sc=sca)
		s.texture_scale=(sca[0]/3,sca[1]/3)
		s.org_height=s.y
		s.frm=0
		del pos,sca,c,a
	def update(self):
		if st.gproc():
			return
		if (self.y < -15 and not st.bonus_round) or (self.x > 175 and not st.death_route):
			return
		if st.level_index != 2:
			s=self
			if wtr_dist(w=s,p=LC.ACTOR):
				s.frm=min(s.frm+time.dt*15,57.999)
				if s.frm > 57.99:
					s.frm=0
				s.texture=wtfc+f'{int(s.frm)}.tga'