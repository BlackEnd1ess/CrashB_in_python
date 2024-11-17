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
b='box'

def wtr_dist(w,p):
	return ((p.z < w.z+(w.scale_z/2)+4) and (p.z > w.z-(w.scale_z/2)-4) and (p.x < w.x+(w.scale_x/2)+2) and (p.x > w.x-w.scale_x/2-2))

#lv1
def gr_block(p,vx,sca=.5):
	for gbx in range(vx[0]):
		for gbz in range(vx[1]):
			GrassBlock(pos=(p[0]+gbx,p[1],p[2]+gbz),sca=sca)
	del p,vx,sca,gbx

#lv2
def plank_bridge(pos,typ,cnt,ro_y,DST):
	for wP in range(cnt):
		plNK={90:lambda:Plank(pos=(pos[0]+wP*DST,pos[1],pos[2]),ro_y=ro_y,typ=typ),
			0:lambda:Plank(pos=(pos[0],pos[1],pos[2]+wP*DST),ro_y=ro_y,typ=typ)}
		plNK[ro_y]()

def sn_block(p,vx,sca=.5):
	for gbx in range(vx[0]):
		for gbz in range(vx[1]):
			SnowBlock(pos=(p[0]+gbx/1.02,p[1],p[2]+gbz),sca=sca)
	del p,vx,sca

def pillar_twin(p):
	Pillar(pos=(p[0],p[1],p[2]))
	Pillar(pos=(p[0]+1.5,p[1],p[2]))

def spawn_ice_wall(pos,cnt,d):
	ws={0:90,1:-90}
	for icew in range(cnt):
		SnowHill(pos=(pos[0],pos[1],pos[2]+icew*16.4),ro_y=ws[d])

#lv3
def multi_tile(p,cnt):#usage [x,y]
	for _tlx in range(cnt[0]):
		for _tly in range(cnt[1]):
			StoneTile(pos=(p[0]+.85*_tlx,p[1],p[2]+.85*_tly))

#lv 4
def swr_multi_ptf(p,cnt):#usage [x,y]
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

## Pseudo CrashB
class PseudoCrash(Entity):
	def __init__(self):
		MVP=omf+'l1/p_moss/moss'
		rp='res/pc/crash'
		super().__init__(model=rp+'.ply',texture=rp+'.tga',scale=.1/20,rotation=(-90,30,0),position=(9,-4,0),unlit=False)
		Entity(model=MVP+'.obj',texture=MVP+'.tga',scale=.75/30,position=(self.x,self.y,self.z),double_sided=True)
		self.idfr=0
	def update(self):
		animation.idle(self,sp=16)

####################
## level 1 objects #
MVP=omf+'l1/p_moss/moss'
class MossPlatform(Entity):
	def __init__(self,p,ptm,pts=.5,ptw=3):
		s=self
		super().__init__(model=MVP+'.obj',name='mptf',texture=MVP+'.tga',scale=.0085,position=(p[0],p[1]+.475,p[2]),enabled=False,double_sided=True,collider=b)
		s.spawn_pos=p
		s.ptm=ptm
		s.pts=pts
		s.turn=0
		if ptm == 1:
			s.is_sfc=True
			Sequence(s.dive,Wait(ptw),loop=True)()
		if ptm > 1:
			ca='x'
			if ptm == 3:
				ca='z'
			Sequence(lambda:s.ptf_move(di=ca),loop=True)()
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
		if not st.gproc():
			s=self
			if s.is_sfc:
				s.is_sfc=False
				s.animate_y(s.y-1,duration=.3)
				if distance(s,LC.ACTOR) < 6:
					sn.obj_audio(ID=6)
				return
			s.is_sfc=True
			s.animate_y(s.spawn_pos[1],duration=.3)

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
		super().__init__(model=gr+'.ply',texture=gr+'.jpg',name='grsi',position=pos,scale=(1,2,1.4),rotation_x=-90,enabled=False)
		if m:
			self.scale_x=-1
		del pos,m

btt=omf+'l1/bush/bush1.png'
class Bush(Entity):
	def __init__(self,pos,sca,ro_y=0):
		super().__init__(model='quad',texture=btt,position=pos,scale=sca,rotation_y=ro_y,color=color.rgb32(0,170,0),enabled=False)
		del pos,sca,ro_y

tvx=omf+'l1/block/block'
class GrassBlock(Entity):
	def __init__(self,pos,sca):
		super().__init__(model=tvx+'.obj',name='mblo',texture=tvx+'.jpg',position=pos,scale=sca,collider=b)
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

class Ropes(Entity):
	def __init__(self,pos,le):
		s=self
		rpt=omf+'l2/rope/rope_pce.jpg'
		super().__init__(model='cube',scale=(.03,.03,le),name='snrp',texture=rpt,position=pos,texture_scale=(1,le*8),origin_z=-.5)
		s.dup=Entity(model='cube',scale=s.scale,name=s.name,position=(s.x+.95,s.y,s.z),texture=rpt,texture_scale=(1,le*8),origin_z=s.origin_z)
		del pos,le

class Pillar(Entity):
	def __init__(self,pos):
		ppt=omf+'l2/pillar/s_pillar'
		super().__init__(model=ppt+'.ply',texture=ppt+'_0.jpg',name='pilr',scale=.2,rotation=(-90,45,0),position=pos,color=color.cyan,collider=b)
		IceCrystal(pos=(self.x,self.y+1.1,self.z+.075))
		del pos

class SnowWall(Entity):
	def __init__(self,pos):
		s=self
		swbo='l2/snow_wall/snow_bonus'
		super().__init__(model=omf+swbo+'.ply',texture=omf+swbo+'.tga',scale=.02,name='snwa',position=pos,rotation=(-90,-90,0))
		del pos

class IceCrystal(Entity):
	def __init__(self,pos):
		super().__init__(model=omf+'l2/ice_crystal/ice_crystal.ply',name='icec',texture=omf+'l2/ice_crystal/snow_2.tga',scale=(.025,.02,.03),position=pos,rotation=(-90,45,0),color=color.cyan)
		del pos

class WoodLog(Entity):
	def __init__(self,pos):
		s=self
		inp=omf+'l2/wood_log/wood_log'
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
				cc.get_damage(LC.ACTOR,rsn=1)
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

class IceChunk(Entity):
	def __init__(self,pos,rot,typ):
		ice_ch=omf+'l2/ice_pce/ice_pce'
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
				cc.get_damage(LC.ACTOR,rsn=1)
			s.roll_wait=max(s.roll_wait-time.dt,0)
			if s.roll_wait <= 0:
				s.is_rolling=True
				s.danger=True
				rdi={0:s.roll_right,1:s.roll_left}
				rdi[s.direc]()
				return
			s.is_rolling=False
			s.danger=False

sbl=omf+'l2/block/block'
class SnowBlock(Entity):
	def __init__(self,pos,sca):
		super().__init__(model=sbl+'.obj',texture=sbl+'.jpg',rotation_y=180,position=pos,scale=sca)
		self.collider=BoxCollider(self,size=Vec3(2,4,2))
		del pos,sca


####################
## level 3 objects #
class WaterFlow(Entity):
	def __init__(self,pos,sca):
		s=self
		s.wtr_t=omf+'l3/water_flow/'
		super().__init__(model='plane',texture=s.wtr_t+'water_flow0.tga',name='wafl',scale=(sca[0],.1,sca[1]),texture_scale=(1,11),position=pos,color=color.rgb32(170,170,170),alpha=.8)
		s.cbst=Entity(model='cube',texture='res/terrain/l3/cobble_stone.png',name=s.name,position=(pos[0],pos[1]-.7,pos[2]+.05),scale=(10,.1,sca[1]),texture_scale=(10,sca[1]))
		WaterHit(p=(pos[0],pos[1]-.1,pos[2]),sc=sca)
		s.frm=0
	def update(self):
		if not st.gproc():
			s=self
			if wtr_dist(w=s,p=LC.ACTOR):
				s.frm=min(s.frm+time.dt*10,3.999)
				if s.frm > 3.99:
					s.frm=0
				s.texture=s.wtr_t+'water_flow'+str(int(s.frm))+'.tga'

class WaterFall(Entity):
	def __init__(self,pos):
		s=self
		s.pa=omf+'l3/water_fall/waterf'
		super().__init__(model='quad',name='wtfa',texture=s.pa+'0.png',position=pos,scale=(5,1),texture_scale=(10,1),color=color.rgb32(240,255,240))
		Entity(model='plane',color=color.black,scale=(12,1,20),position=(s.x,s.y-.7,s.z+1.3))
		s.frm=0
		Foam(pos=(s.x,s.y-.49,s.z-.5),t=0)
		Foam(pos=(s.x,s.y+.501,s.z+.49),t=1)
	def update(self):
		if not st.gproc():
			s=self
			s.frm=min(s.frm+time.dt*7,31.99)
			if s.frm > 31.98:
				s.frm=0
			s.texture=s.pa+str(int(s.frm))+'.png'

class SceneWall(Entity):
	def __init__(self,pos,typ):
		s=self
		sWCN=omf+'l3/scn_w/'
		super().__init__(model=sWCN+'side'+str(typ)+'.ply',texture=sWCN+'water2_scn.tga',name='scwa',position=pos,scale=.04,rotation_x=-90)
		roTY={1:91,2:90}
		s.rotation_y=roTY[typ]

trw=omf+'l3/temple_wall/tm_wall'
class TempleWall(Entity):
	def __init__(self,pos,sd):
		kq=.025
		if sd == 2:
			kq=-.025
		super().__init__(model=trw+'.ply',texture=trw+'.tga',name='tmpw',position=pos,scale=(.025,kq,.025),rotation=(-90,90,0),collider=b)

class WoodStage(Entity):
	def __init__(self,pos):
		s=self
		wdStg=omf+'l3/wood_stage/w_stage'
		super().__init__(model=wdStg+'.ply',texture=omf+'l3/wood_stage/stage_z.tga',name='wdst',position=pos,scale=.03,rotation=(-90,90,0),color=color.rgb32(100,100,0))
		Entity(model=wfc,position=(s.x,s.y-.46,s.z-1.5),scale=(4.2,1,1.2),name=s.name,collider=b,visible=False)
		Entity(model=wfc,position=(s.x,s.y-.46,s.z+.2),scale=(1.2,1,2.3),name=s.name,collider=b,visible=False)

tlX=omf+'l3/tile/tile'
class StoneTile(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=tlX+'.obj',name='tile',texture=tlX+'.jpg',position=pos,scale=.35)
		s.collider=BoxCollider(s,center=Vec3(0,-.1,0),size=Vec3(2.4,1,2.4))

lbP=omf+'l3/mtree_scn/'
class MushroomTree(Entity):
	def __init__(self,pos,typ):
		s=self
		if typ == 1:
			super().__init__(model=lbP+'BTree0.ply',name='mtbt',texture=lbP+'tm_scn.tga',position=pos,scale=.03,color=color.rgb32(180,180,180),rotation=(-90,90,0))
			Entity(model=wfc,name=s.name,scale=(1.3,.5,.5),position=(s.x-.1,s.y+2.15,s.z-1.1),collider=b,visible=False)
			Entity(model=wfc,name=s.name,position=(s.x,s.y+3,s.z-.6),scale=(1,7,.5),collider=b,visible=False)
			return
		super().__init__(model=lbP+'BTree1.ply',name='mtbt',texture=lbP+'tm_scn.tga',position=pos,scale=.06,rotation=(-90,90,0))
		s.gnd=Entity(model='cube',name=s.name,scale=(.65,.5,.6),position=(s.x,s.y-.1,s.z),collider=b,visible=False)
		s.gnd=Entity(model='cube',name=s.name,position=(s.x,s.y+1.5,s.z+.5),scale=(1,3,.5),collider=b,visible=False)

class Foam(Entity):
	def __init__(self,pos,t):
		s=self
		rrfm={0:0,1:180}
		s.t=omf+'l3/foam/'
		super().__init__(model='quad',texture=s.t+'0.png',position=pos,scale=(5,1),texture_scale=(10,1),rotation=(90,rrfm[t],0))
		s.typ=t
		s.frm=0
		if t == 1:
			s.color=color.rgb32(210,210,210)
			s.frm=15.99
	def flow_normal(self):
		s=self
		s.frm+=time.dt*6
		if s.frm > 15.9:
			s.frm=0
		s.texture=s.t+str(int(s.frm))+'.png'
	def flow_reverse(self):
		s=self
		s.frm-=time.dt*6
		if s.frm <= 0:
			s.frm=15.99
		s.texture=s.t+str(int(s.frm))+'.png'
	def update(self):
		if not st.gproc():
			s=self
			if s.typ == 1:
				s.flow_reverse()
				return
			s.flow_normal()

class BonusBackground(Entity):
	def __init__(self,pos,sca):
		super().__init__(model='quad',texture='res/background/bonus_1.jpg',name='bbgn',scale=sca,texture_scale=(1,1),position=pos,color=color.rgb32(100,60,80),unlit=False,shader=unlit_shader)

class BonusScene(Entity):
	def __init__(self,pos):
		bcnn=omf+'l3/mtree_scn/'
		super().__init__(model=bcnn+'wtr_bSCN.ply',texture=bcnn+'tm_scn.tga',name='bnsc',position=pos,scale=.035,rotation=(-90,90,0))


####################
## level 4 objects #
class SewerTunnel(Entity):
	def __init__(self,pos,c=color.white):
		s=self
		_sPA=omf+'l4/scn/'
		super().__init__(model=_sPA+'tunnel.ply',texture=_sPA+'sewer2.tga',name='swtu',position=pos,color=c,scale=(.032,.034,.03),rotation=(-90,90,0))
		Entity(model=wfc,position=(s.x-3,s.y+2,s.z-3),name=s.name,scale=(1,6,10),collider=b,visible=False)
		Entity(model=wfc,position=(s.x+3,s.y+2,s.z-3),name=s.name,scale=(1,6,10),collider=b,visible=False)

class SewerEscape(Entity):
	def __init__(self,pos,typ=None,c=color.white):
		s=self
		_SE=omf+'l4/scn/'
		super().__init__(model=_SE+'pipe_1.ply',texture=_SE+'sewers.tga',name='swec',position=pos,scale=.048,color=c,rotation=(-90,90,0))
		Entity(model=wfc,scale=(.3,8,11),name=s.name,position=(s.x-1.5,s.y+3,s.z+2),collider=b,visible=False)
		Entity(model=wfc,scale=(.3,8,11),name=s.name,position=(s.x+1.8,s.y+3,s.z+2),collider=b,visible=False)
		if typ == 1:
			s.color=color.rgb32(255,50,0)
			s.unlit=False

class SewerPlatform(Entity):
	def __init__(self,pos):
		s=self
		pPF=omf+'l4/scn/'
		super().__init__(model=wfc,name='swpl',scale=(.5,.2,.5),collider=b,position=pos,visible=False)
		s.vis=Entity(model=pPF+'ptf.ply',texture=pPF+'swr_ptf.tga',name=s.name,position=(s.x,s.y+.05,s.z),scale=.02,rotation_x=-90)
		s.matr='metal'

class SewerWall(Entity):
	def __init__(self,pos):
		s=self
		mo=omf+'l4/scn/sewer_wall_b'
		super().__init__(model=mo+'.ply',texture=mo+'.tga',name='ssww',position=pos,scale=.0175,rotation=(-90,90,0))
		s.bgw=Entity(model='cube',name=s.name,color=color.black,scale=(5,8,.1),position=(s.x,s.y,s.z+1))
		s.color=color.rgb(.6,.5,.4)

class SwimPlatform(Entity):
	def __init__(self,pos):
		s=self
		swmi=omf+'l4/swr_swim/swr_swim'
		super().__init__(model=wfc,name='swpt',color=color.white,collider=b,position=pos,scale=(.5,.3,.5),visible=False)
		s.opt=Entity(model=swmi+'.ply',texture=swmi+'.tga',name=s.name,scale=.1/200,rotation_x=-90,position=(s.x,s.y+.06,s.z))
		s.active=False
		s.matr='metal'
		s.spawn_y=s.y
		s.f_time=0
	def sink(self):
		s=self
		s.y-=time.dt
		s.opt.y-=time.dt
		if s.y <= s.spawn_y-.3:
			sn.pc_audio(ID=10)
			s.collider=None
			s.active=False
			s.f_time=0
			invoke(lambda:setattr(s,'y',s.spawn_y),delay=5)
			invoke(lambda:setattr(s,'collider',b),delay=5)
			invoke(lambda:setattr(s.opt,'y',s.spawn_y),delay=5)
	def update(self):
		if not st.gproc():
			s=self
			if s.active:
				s.f_time+=time.dt
				if s.f_time >= .5:
					s.sink()

class SewerEntrance(Entity):
	def __init__(self,pos):
		swn=omf+'l4/swr_entrance/swr_entrance'
		super().__init__(model=swn+'.ply',texture=swn+'.jpg',name='swri',position=pos,rotation_y=90,scale=2)

class SewerPipe(Entity):## danger
	def __init__(self,pos,typ):
		s=self
		swrp=omf+'l4/pipe/pipe_'
		swu=str(typ)
		ro_y={0:-90,1:-90,2:90,3:90}
		super().__init__(model=swrp+swu+'.ply',texture=swrp+swu+'.png',name='swpi',position=pos,scale=.75,rotation=(-90,ro_y[typ],0))
		s.danger=(typ == 3)
		s.typ=typ
		if typ == 0:
			Entity(model=Circle(16,thickness=1,radius=.6),name=s.name,color=color.black,position=(s.x,s.y,s.z+.2))
			has_drips=random.randint(0,1)
			if has_drips == 1:
				DrippingWater(pos=(s.x,s.y-.75,s.z-.25),sca=(.9,.4))
		if typ == 2:
			Entity(model=Circle(16,thickness=1,radius=.5),color=color.black,name=s.name,position=(s.x,s.y+.8,s.z-.7),rotation_x=-30)
			DrippingWater(pos=(s.x,s.y-.2,s.z-.5),sca=(.9,.4))
		if typ == 3:
			s.collider=BoxCollider(s,size=Vec3(.5,.5,5))
			s.rotation_x=0
			s.color=color.red
			s.unlit=False
	def update(self):
		s=self
		if not st.gproc() and s.typ == 3:
			if s.intersects(LC.ACTOR):
				cc.get_damage(LC.ACTOR,rsn=3)

class EletricWater(Entity):
	def __init__(self,pos,sca):
		s=self
		self.wtt=omf+'l4/wtr/'
		super().__init__(model='cube',texture=s.wtt+'0.png',name='elwt',position=pos,scale=(sca[0],.1,sca[1]),texture_scale=(sca[0],sca[1]),color=color.rgb32(0,180,180),alpha=.9,collider=b)
		s.tx=(sca[0],sca[1])
		s.electric=False
		s.nr=False
		s.splash=0
		s.frm=0
		s.tme=8
		if s.x > 150:
			s.tme=random.uniform(.1,.2)
	def wtr_anim(self):
		s=self
		s.frm=min(s.frm+time.dt*8,31.999)
		if s.frm > 31.99:
			s.frm=0
		s.texture=s.wtt+f'{int(s.frm)}.png'
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
		s.electric=False
		s.color=color.rgb32(0,125,125)
		s.unlit=True
		s.alpha=.9
	def check_p(self):
		s=self
		ta=LC.ACTOR
		if ta.in_water <= 0:
			s.splash=max(s.splash-time.dt,0)
		if s.intersects(ta):
			ta.in_water=.3
			if s.electric:
				cc.get_damage(ta,rsn=4)
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
				if s.x > 150:
					s.tme=8
				else:
					s.tme=8
				s.wtr_danger()

class DrippingWater(Entity):
	def __init__(self,pos,sca):
		s=self
		s.dpw=omf+'l4/drips/'
		super().__init__(model='quad',texture=s.dpw+'0.png',name='drpw',position=pos,scale=sca,rotation_z=90)
		s.frm=0
	def update(self):
		s=self
		if st.gproc() or (distance(s,LC.ACTOR) > 8):
			return
		s.frm=min(s.frm+(time.dt*10),7.999)
		if s.frm > 7.99:
			s.frm=0
		s.texture=s.dpw+f'{int(s.frm)}.png'


####################
## level 5 objects #
class RuinsPlatform(Entity):##big platform
	def __init__(self,pos,m):
		s=self
		rnp=omf+'l5/ruins_scn/'
		msc={True:-.03,False:.03}
		msv={True:-.9,False:.9}
		super().__init__(model=wfc,collider=b,scale=(1.7,1,1.5),name='rnsp',position=pos,visible=False)
		s.opt_model=Entity(model=rnp+'ruins_ptf1.ply',texture=rnp+'ruins_scn.tga',name=s.name,position=(s.x,s.y+.5,s.z),scale=(.03,msc[m],.03),rotation=(-90,90,0))
		s.rail0=Entity(model=wfc,scale=(1.7,.5,.3),name=s.name,collider=b,position=(s.x,s.y+.8,s.z+.9),visible=False)
		s.rail0=Entity(model=wfc,scale=(.3,.5,1.7),name=s.name,collider=b,position=(s.x+msv[m],s.y+.8,s.z),visible=False)

class RuinsBlock(Entity):## small platform
	def __init__(self,pos):
		s=self
		rnb=omf+'l5/ruins_scn/'
		super().__init__(model=wfc,collider=b,scale=(.75,1,.75),name='rubl',position=pos,visible=False)
		s.opt_model=Entity(model=rnb+'ruins_ptf02.ply',name=s.name,texture=rnb+'ruins_scn.tga',position=(s.x,s.y+.5,s.z-.025),scale=.03,rotation=(-90,90,0))

class RuinsCorridor(Entity):## corridor
	def __init__(self,pos):
		s=self
		rco=omf+'l5/ruins_scn/'
		super().__init__(model=wfc,position=pos,scale=(3,1,3),name='rncr',collider=b,visible=False)
		s.opt_model=Entity(model=rco+'ruins_cor.ply',texture=rco+'ruins_scn.tga',name=s.name,position=(s.x,s.y+.5,s.z),scale=.03,rotation=(-90,90,0))
		s.cor_w0=Entity(model=wfc,position=(s.x-1.4,s.y+1.7,s.z),name=s.name,scale=(.5,2,3),collider=b,visible=False)
		s.cor_w1=Entity(model=wfc,position=(s.x+1.4,s.y+1.7,s.z),name=s.name,scale=(.5,2,3),collider=b,visible=False)
		IndoorZone(pos=(s.x,s.y+2.55,s.z),sca=3)

class MonkeySculpture(Entity):
	def __init__(self,pos,r,d,ro_y=90):
		s=self
		rmsc=omf+'l5/m_sculpt/m_sculpt'
		super().__init__(model=rmsc+'.ply',texture=rmsc+'.tga',name='mnks',position=pos,scale=.003,rotation=(-90,ro_y,0),unlit=False)
		s.podium=Entity(model='cube',texture='res/terrain/l5/moss.png',name=s.name,scale=(.5,1,.5),texture_scale=(1,2),position=(s.x,s.y-.5,s.z))
		s.f_pause=False
		s.s_audio=False
		s.f_cnt=0
		s.danger=d
		s.rot=r
		if s.danger:
			Sequence(s.fire_throw,Wait(.08),loop=True)()
		if s.rot:
			Sequence(s.rot_to_crash,loop=True)()
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

class LoosePlatform(Entity):
	def __init__(self,pos,t):
		s=self
		s.lpp=omf+'l5/loose_ptf'+str(t)+'/'
		super().__init__(model=wfc,position=pos,scale=(.7,.5,.6),name='loos',collider=b,visible=False)
		s.opt_model=Entity(model=s.lpp+'loose_ptf'+str(t)+'.ply',texture=s.lpp+'loose_ptf'+str(t)+'.tga',name=s.name,scale=.01/15,position=(s.x,s.y+.25,s.z),rotation=(-90,-90,0))
		s.active=False
		s.typ=t
		s.frm=0
		if s.typ == 2:
			s.f_time=0
			s.scale=(.55,.2,.55)
			s.opt_model.position=(s.x-.275,s.y+.1,s.z+.25)
			s.spawn_h=s.y
	def respawn(self):
		s=self
		s.collider=b
		s.frm=0
		s.opt_model.model=s.lpp+'0.ply'
	def fall(self):
		s=self
		s.y-=time.dt*3
		s.opt_model.y-=time.dt*3
		if s.y <= s.spawn_h-1:
			s.active=False
			s.collider=None
			s.f_time=0
			invoke(lambda:setattr(s,'y',s.spawn_h),delay=5)
			invoke(lambda:setattr(s.opt_model,'y',s.spawn_h),delay=5)
			invoke(lambda:setattr(s,'collider',b),delay=5)
	def collapse(self):
		s=self
		s.frm=min(s.frm+(time.dt*18),32.99)
		if s.frm > 26:
			s.collider=None
			if s.frm > 32.98:
				sn.obj_audio(ID=9,pit=1)
				s.active=False
				invoke(s.respawn,delay=7)
				return
		s.opt_model.model=s.lpp+str(int(s.frm))+'.ply'
	def update(self):
		s=self
		if not s.active:
			return
		if s.typ != 2:
			s.collapse()
			return
		s.f_time=max(s.ftime+time.dt,.5)
		if s.f_time >= .5:
			s.fall()

class RuinRuins(Entity):
	def __init__(self,pos,typ,ro_y):
		rrn=omf+'l5/ruins_bgo/'
		if typ == 3:
			super().__init__(model=rrn+'ruin_bg'+str(typ)+'.ply',name='rrrr',texture=rrn+'ruin_scene.tga',position=pos,scale=.08,rotation=(-90,ro_y,0),unlit=False)
			return
		super().__init__(model=rrn+'ruin_bg'+str(typ)+'.ply',name='rrrr',texture=rrn+'ruin.tga',position=pos,scale=.03,rotation=(-90,ro_y,0),unlit=False)

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
					cc.get_damage(LC.ACTOR,rsn=1)

##################
## logic objects #
class FallingZone(Entity):## falling
	def __init__(self,pos,s):
		super().__init__(model='cube',name='fllz',collider=b,scale=s,position=pos,color=color.rgb32(0,0,0))
		if st.level_index != 5:
			self.visible=False
		Sequence(self.refr_p,Wait(.2),loop=True)()
	def refr_p(self):
		ac=LC.ACTOR
		if self.intersects(ac):
			cc.dth_event(ac,rsn=0)

class WaterHit(Entity):## collider for water
	def __init__(self,p,sc):
		super().__init__(model=wfc,name='wtrh',collider=b,position=p,scale=(sc[0],.2,sc[1]),visible=False)

class CrateScore(Entity):## level reward
	def __init__(self,pos):
		s=self
		ev='res/crate/'
		super().__init__(model=ev+'cr_t0.ply',name='ctsc',texture=ev+'1.tga',alpha=.4,scale=.18,position=pos,origin_y=.5)
		s.cc_text=Text(parent=scene,position=(s.x-.2,s.y,s.z),name=s.name,text=None,font=ui._fnt,color=color.rgb32(255,255,100),scale=10)
		if settings.debg:
			print(f'crates total: {st.crates_in_level}')
	def update(self):
		if st.gproc():
			return
		s=self
		dv=(LC.C_GEM and distance(s,LC.C_GEM) < .5)
		s.cc_text.visible=not(dv)
		s.visible=not(dv)
		if s.visible:
			s.cc_text.text=f'{st.crate_count}/{st.crates_in_level}'
			s.rotation_y-=120*time.dt
		if (st.crate_count >= st.crates_in_level):
			item.GemStone(pos=(s.x,s.y-.3,s.z),c=0)
			sn.ui_audio(ID=4)
			cc.purge_instance(s.cc_text)
			cc.purge_instance(s)

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
		if st.crates_in_level > 0:
			if s.x < 180:# pos_x 190 is death zone in lv 5
				CrateScore(pos=(s.x-1.1,s.y-.7,s.z))
		if st.level_index == 1 and not 4 in st.COLOR_GEM:
			item.GemStone(pos=(s.x-1.1,s.y-.9,s.z),c=4)
		if st.level_index == 2 and not 1 in st.COLOR_GEM:
			item.GemStone(pos=(s.x-1.1,s.y-.9,s.z),c=1)
		del pos,c

class RoomDoor(Entity):## door for start and end room
	def __init__(self,pos):
		s=self
		s.dPA=omf+'ev/door/'
		super().__init__(model=s.dPA+'u0.ply',texture=s.dPA+'u_door.tga',name='rmdr',position=pos,scale=.001,rotation_x=90,collider=b)
		s.door_part=Entity(model=s.dPA+'d0.ply',name=s.name,texture=s.dPA+'d_door.tga',position=(s.x,s.y+.1,s.z),scale=.001,rotation_x=90,collider=b)
		s.d_opn=False
		s.d_frm=0
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
		super().__init__(model=omf+sIN+'.ply',texture=omf+sIN+'.tga',name='bnpt',collider=b,scale=-.001,rotation_x=90,position=pos,unlit=False)
		s.start_y=s.y
	def update(self):
		if st.bonus_solved:
			cc.purge_instance(self)

class GemPlatform(Entity):## gem platform
	def __init__(self,pos,t):
		s=self
		ne='gem_ptf_e'
		s.is_enabled=False
		if t in st.COLOR_GEM:
			ne='gem_ptf'
			s.is_enabled=True
		if settings.debg:
			ne='gem_ptf'
			s.is_enabled=True
			t=0
		L=180
		GMC={0:color.rgb32(130,130,140),1:color.rgb32(L+20,0,0),2:color.rgb32(0,L,0),3:color.rgb32(L-50,0,L-50),4:color.rgb32(0,0,L+40),5:color.rgb32(L-30,L-30,0)}
		super().__init__(model=wfc,name='gmpt',color=color.green,scale=(.6,.4,.6),position=pos,collider=b,visible=False)
		s.opt_model=Entity(model=omf+'ev/'+ne+'/'+ne+'.ply',name=s.name,texture=omf+'ev/'+ne+'/'+ne+'.tga',rotation_x=-90,scale=.001,position=pos,color=GMC[t],unlit=False)
		s.bg_darkness=Entity(model=Circle(16,mode='ngon',thickness=.1),name=s.name,position=(s.x,s.y-.011,s.z),rotation_x=90,color=color.black,scale=.7,alpha=.98)
		s.org_color=s.color
		s.start_y=s.y
		s.typ=t
		if not s.is_enabled:
			s.unlit=False
			s.collider=None
			s.bg_darkness.hide()
			s.alpha=.6
	def update(self):
		if not st.gproc():
			s=self
			if st.gem_path_solved:
				cc.purge_instance(s.bg_darkness)
				cc.purge_instance(s.opt_model)
				cc.purge_instance(s)
				return
			s.opt_model.position=(s.x,s.y+.15,s.z)
			s.bg_darkness.position=(s.opt_model.x,s.opt_model.y-.01,s.opt_model.z)
			if s.is_enabled and not LC.ACTOR.freezed:
				s.opt_model.rotation_y+=time.dt*20

class PseudoGemPlatform(Entity):
	def __init__(self,pos,t):
		s=self
		ne='gem_ptf_e'
		s.is_enabled=False
		if t in st.COLOR_GEM:
			ne='gem_ptf'
			s.is_enabled=True
		if settings.debg:
			ne='gem_ptf'
			s.is_enabled=True
			t=0
		L=180
		GMC={0:color.rgb32(130,130,140),1:color.rgb32(L,0,0),2:color.rgb32(0,L,0),3:color.rgb32(L-50,0,L-50),4:color.rgb32(0,0,L+40),5:color.rgb32(L-30,L-30,0)}
		super().__init__(model=omf+'ev/'+ne+'/'+ne+'.ply',texture=omf+'ev/'+ne+'/'+ne+'.tga',rotation_x=-90,scale=.001,position=pos,color=GMC[t],unlit=False)
		s.bg_darkness=Entity(model=Circle(16,mode='ngon',thickness=.1),position=(s.x,s.y-.01,s.z),rotation_x=90,color=color.black,scale=.7,alpha=.98)
		if s.is_enabled:
			HitBox(pos=(s.x,s.y-.15,s.z),sca=(.6,.4,.6))
			return
		s.unlit=False
		s.bg_darkness.hide()
		s.alpha=.5

#############
## Switches #
class LevelFinish(Entity):## finish level
	def __init__(self,p):
		s=self
		trpv=omf+'ev/teleport/warp_effect'
		super().__init__(model='sphere',name='lvfi',collider=b,scale=1,position=p,visible=False)
		ef.WarpVortex(pos=(s.x,s.y,s.z),col=color.yellow,sca=.6,drc=1)
		ef.WarpVortex(pos=(s.x,s.y+.2,s.z),col=color.orange,sca=.7,drc=0)
		ef.WarpVortex(pos=(s.x,s.y+.4,s.z),col=color.yellow,sca=.8,drc=1)
		ef.WarpVortex(pos=(s.x,s.y+.6,s.z),col=color.orange,sca=.7,drc=0)
		ef.WarpVortex(pos=(s.x,s.y+.8,s.z),col=color.yellow,sca=.6,drc=1)
		s.w_audio=Audio('res/snd/misc/portal.wav',volume=0,loop=True)
	def update(self):
		if not st.gproc():
			s=self
			if s.intersects(LC.ACTOR):
				cc.jmp_lv_fin()
				return
			if (distance(s,LC.ACTOR) < 6):
				s.w_audio.volume=settings.SFX_VOLUME
				return
			s.w_audio.volume=0

class IndoorZone(Entity):## disable rain
	def __init__(self,pos,sca):
		super().__init__(model='cube',name='indz',scale=sca,position=pos,collider=b,visible=False)
	def update(self):
		if self.intersects(LC.ACTOR):
			LC.ACTOR.CMS=3.2
			LC.ACTOR.indoor=.3

###################
## global objects #
class HitBox(Entity):
	def __init__(self,pos,sca):
		super().__init__(model=wfc,position=pos,scale=sca,collider=b,name='htbx',visible=False,enabled=True)
		del pos,sca

class LevelScene(Entity):
	def __init__(self,pos,sca):
		s=self
		s.vpa='res/background/'
		super().__init__(model='quad',texture=None,scale=sca,position=pos,texture_scale=(sca[0]/50,1))
		if st.level_index == 1:
			s.texture=s.vpa+'bg_woods.png'
			s.unlit=True
			return
		if st.level_index == 5:
			s.texture=s.vpa+'bg_ruins.jpg'
			s.color=color.rgb32(150,150,160)
			s.shader=unlit_shader
			s.orginal_tsc=s.texture_scale
			s.orginal_x=s.x
			s.orginal_y=s.y
			s.bonus_y=-70
			s.bonus_x=170
			_loc.bgT=s
	def update(self):
		if st.level_index == 5:
			s=self
			xp={True:lambda:setattr(s,'x',s.bonus_x),False:lambda:setattr(s,'x',s.orginal_x)}
			yp={True:lambda:setattr(s,'y',s.bonus_y),False:lambda:setattr(s,'y',s.orginal_y)}
			xp[st.death_route]()
			yp[st.bonus_round]()

class LightArea(SpotLight):
	def __init__(self,pos):
		super().__init__(position=pos,color=color.white)
		self.ta=LC.ACTOR
	def update(self):
		if not st.gproc():
			self.position=(self.ta.x+.5,self.ta.y+1.5,self.ta.z+1)

class InvWall(Entity):
	def __init__(self,pos,sca):
		super().__init__(model=wfc,position=pos,scale=sca,visible=False,collider=b,color=color.blue)

wtfc=omf+'ev/water/wtr_srfc/water_'
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
