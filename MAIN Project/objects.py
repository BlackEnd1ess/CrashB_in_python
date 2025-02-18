from ursina import Entity,color,time,distance,invoke,BoxCollider,Vec3,SpotLight,camera,Audio,Text,scene
import _core,status,item,sound,animation,player,_loc,settings,effect,npc,ui,danger,random
from ursina.ursinastuff import destroy
from ursina.shaders import *

an=animation
dg=danger
ef=effect
st=status
sn=sound
cc=_core
LC=_loc

wfc='wireframe_cube'
trn='res/terrain/'
omf='res/objects/'
bgg='res/background/'
b='box'

### OBJECT TYPES #########
##level block platforms ##

block_sca={0:.5,1:.5,2:.35,3:.02,4:.03,5:(.5,.8,.5)}
trhs={0:1,1:.985,2:.85,3:.501,4:.75,5:1}
def spw_block(ID,p,vx,sca=0,ro_y=0,typ=0):
	for gbx in range(vx[0]):
		for gbz in range(vx[1]):
			ObjType_Block(ID=ID,pos=(p[0]+trhs[ID]*gbx,p[1],p[2]+trhs[ID]*gbz),sca=block_sca[ID],ro_y=ro_y,typ=typ)
	del p,vx,ID,sca,gbx,gbz,ro_y,typ

mpk={0:'l1/block/block',
	1:'l2/block/block',
	2:'l3/tile/tile',
	3:'l4/swr_tile/swr_tile',
	4:'l5/block/block',
	5:'l7/lab_ptf/lab_ptf'}
class ObjType_Block(Entity):
	def __init__(self,pos,ID,sca=0,ro_y=0,typ=0):
		s=self
		s.vnum=ID
		super().__init__(model=omf+mpk[ID]+'.obj',texture=mpk[ID]+'.png',position=pos,rotation_y=ro_y,scale=sca)
		s.double_sided=ID in {1,3,4}
		bl_c={0:lambda:setattr(s,'collider',b),
			1:lambda:setattr(s,'collider',BoxCollider(s,size=Vec3(2,4,2))),
			2:lambda:setattr(s,'collider',BoxCollider(s,size=Vec3(2.4,1,2.4),center=Vec3(0,-.1,0))),
			3:lambda:setattr(s,'collider',BoxCollider(s,size=Vec3(25,4,25))),
			4:lambda:setattr(s,'collider',BoxCollider(s,center=Vec3(0,-7.5,0),size=(25,15,25))),
			5:lambda:setattr(s,'collider',b)}
		bl_c[ID]()
		if ID == 0 and typ == 1:
			s.scale=(.5,.5,.3)
		if ID == 5:
			if typ == 1:
				s.texture=omf+mpk[ID]+'_e.png'
			#temp collision landing fixx
			if st.level_index == 7 and s.y > 4:
				s.scale_y=1.2
		if ID in {3,5}:
			s.matr='metal'
		del pos,sca,ro_y,typ,ID,bl_c

###########################
##level side wall scenes ##
def spawn_ice_wall(pos,cnt,d):
	for icew in range(cnt):
		ObjType_Scene(ID=2,pos=(pos[0],pos[1],pos[2]+icew*16.4),ro_y={0:90,1:-90}[d],sca=(.6,.5,.4),col=color.white)
	del pos,cnt,d,icew

sds={0:'l1/grass_side/grass_sd',
	1:'l1/tree/multi_tree',
	2:'l2/snw_hill/sn_hill',
	3:'l3/s_wall/s_wall',
	4:'l3/t_wall/t_wall',
	5:'l3/bonus_scn/bonus_scn',
	6:'l4/tunnel/tunnel',
	7:'l4/escape/escape',
	8:'l4/swr_ring/swr_ring',
	9:'l5/ruins_scn/ruins_scn',
	10:'l6/wall_side/wall_side',
	11:'l6/tree_side/tree_side'}
class ObjType_Scene(Entity):
	def __init__(self,pos,sca,ID,ro_y=0,typ=0,col=color.gray):
		s=self
		s.vnum=ID
		super().__init__(texture=omf+sds[ID]+'.png',position=pos,scale=sca,rotation_y=ro_y,double_sided=True,color=col)
		if ID == 7 and typ == 1:
			dg.SewerGlowIron(pos=(s.x,s.y+.2,s.z+2.5),sca=(10,.01,10))
			s.color=color.rgb32(255,50,0)
			s.unlit=False
		s.check_obj()
		del pos,sca,ID,ro_y,col,typ
	def check_obj(self):
		s=self
		if s.vnum in {3,10,11}:
			s.model=omf+sds[s.vnum]+'.obj'
			return
		s.model=omf+sds[s.vnum]+'.ply'
		s.rotation_x=-90

######################
##level front walls ##
smd={0:'l1/turtle_wall/turtle_wall',
	1:'l2/snow_wall/snow_wall',
	2:'l4/swr_wall/swr_wall',
	3:'l5/broken_wall/broken_wall',
	4:'l6/stone_wall/stone_wall',
	5:'l6/bonus_wall/bonus_wall',
	6:'l7/lab_bgs/lab_bgs'}
class ObjType_Wall(Entity):
	def __init__(self,ID,pos,sca,ro_y=0,col=color.white):
		s=self
		s.vnum=ID
		super().__init__(model=omf+smd[ID]+'.ply',texture=omf+smd[ID]+'.png',position=pos,scale=sca,rotation=(-90,ro_y,0),color=col,double_sided=True)
		if ID == 0 and pos[0] > 190:
			s.color=color.rgb32(0,140,160)
		if ID == 2:
			s.collider='box'
		del ID,pos,sca,ro_y,col

######################
##level decorations ##
def pillar_twin(p):
	ObjType_Deco(ID=2,sca=.2,col=color.cyan,rot=(-90,45,0),pos=(p[0],p[1],p[2]))
	ObjType_Deco(ID=2,sca=.2,col=color.cyan,rot=(-90,45,0),pos=(p[0]+1.5,p[1],p[2]))
	del p

dms={0:'l1/bush/bush',
	1:'l1/tree_s/tree_s',
	2:'l2/pillar/pillar',
	3:'l2/ice_cry/ice_cry',
	4:'l2/ice_pce/ice_pce',
	5:'l2/ice_shard/ice_shard',
	6:'l3/cobble_stone/cobble_stone',
	7:'l4/swr_dmg_pipe/swr_dmg_pipe',
	8:'l4/swr_drain/swr_drain',
	9:'l4/swr_drain_big/swr_drain_big',
	10:'l6/stone_board/stone_board',
	11:'l7/lab_pipe/lab_pipe',
	12:'l7/boiler/boiler'}
#dm_sca={0:,1:,2:,3:,4:,5}
class ObjType_Deco(Entity):
	def __init__(self,ID,pos,sca,rot,col=color.white):
		s=self
		s.vnum=ID
		super().__init__(model=None,texture=omf+dms[ID]+'.png',position=pos,scale=sca,rotation=rot,color=col)
		s.check_model()
		if ID == 1:
			HitBox(pos=pos,sca=(1,5,1))
		if ID == 2:
			ObjType_Deco(ID=3,pos=(s.x,s.y+1.1,s.z+.075),sca=(.025,.02,.03),rot=(-90,45,0),col=col)
		if ID == 8:
			vvf=random.randint(0,1)
			if vvf == 0:
				ObjType_Water(ID=4,pos=(s.x,s.y-.2,s.z-.5),sca=(.9,.4),rot=(0,0,90),frames=7,spd=10,al=1)
		del ID,pos,sca,rot,col
	def check_model(self):
		s=self
		if s.vnum == 0:
			s.model='quad'
			return
		s.model=omf+dms[s.vnum]+'.ply'

####################
##level corridors ##
cor={0:'l1/turtle_corridor/turtle_corridor',
	1:'l5/ruin_corridor/ruin_corridor'}
class ObjType_Corridor(Entity):
	def __init__(self,ID,pos,rot=(-90,90,0)):
		s=self
		s.vnum=ID
		super().__init__(model=omf+cor[ID]+'.ply',texture=omf+cor[ID]+'.png',position=pos,rotation=rot)
		s.check_model()
		del ID,pos,rot
	def check_model(self):
		s=self
		if s.vnum == 0:
			s.scale=.1
			HitBox(sca=(3,3,2.2),pos=(s.x+2.3,s.y,s.z))
			HitBox(sca=(3,3,2.2),pos=(s.x-2.3,s.y,s.z))
			HitBox(sca=(3,3,2.2),pos=(s.x,s.y+3,s.z))
			IndoorZone(pos=(s.x,s.y+1.6,s.z),sca=3)
			return
		if s.vnum == 1:
			s.model=wfc
			s.scale=(3,1,3)
			s.collider=b
			Entity(model=omf+cor[s.vnum]+'.ply',texture=omf+cor[s.vnum]+'.png',position=(s.x,s.y+.5,s.z),scale=.03,rotation=(-90,90,0))
			s.visible=False
			HitBox(pos=(s.x-1.4,s.y+1.7,s.z),sca=(.5,2,3))
			HitBox(pos=(s.x+1.4,s.y+1.7,s.z),sca=(.5,2,3))
			IndoorZone(pos=(s.x,s.y+2.55,s.z),sca=3)

#################
##level Grounds##
flr={0:None,
	1:'l3/wood_stage/wood_stage',
	2:'l3/big_tile/big_tile',
	3:'l3/wt_tree/wt_tree',#sca=.03,col=color.rgb32(180,180,180),rot=rotation=(-90,90,0),
	4:'l4/floor/swr_floor',#sca=.5
	5:'l5/ruin_tower/ruin_tower',#sca=.03,ro_y=-90
	6:'l6/frozen_floor/frozen_floor',#
	7:'l6/dirt_floor/dirt_floor',
	8:None,
	9:'l6/stone_ground/stone_ground'}
trx={0:'ice_ground.png',8:'bee_terra.png'}
class ObjType_Floor(Entity):
	def __init__(self,ID,pos,sca,rot=(0,0,0),col=color.white):
		s=self
		s.vnum=ID
		super().__init__(position=pos,scale=sca,rotation=rot,color=col)
		s.set_model()
		if ID == 0:
			s.texture_scale=(sca[0],sca[1])
			s.name='iceg'
			s.alpha=.9
		if ID == 1:
			HitBox(pos=(s.x,s.y-.46,s.z-1.5),sca=(4.2,1,1.2))
			HitBox(pos=(s.x,s.y-.46,s.z+.2),sca=(1.2,1,2.3))
		if ID == 3:
			HitBox(pos=(s.x-.1,s.y+2.15,s.z-1.1),sca=(1.3,.5,.5))
			HitBox(pos=(s.x,s.y+3,s.z-.6),sca=(1,7,.5))
		if ID == 4:
			s.matr='metal'
		if ID == 5:
			HitBox(pos=(s.x,s.y+.4,s.z+.9),sca=(1.7,.5,.3))
			if sca[2] < 0:
				HitBox(pos=(s.x+.9,s.y+.4,s.z),sca=(.3,.5,1.7))
			else:
				HitBox(pos=(s.x-.9,s.y+.4,s.z),sca=(.3,.5,1.7))
		if ID == 8:
			s.texture_scale=(sca[0],sca[2])
			s.name='befl'
		s.set_collider()
		del ID,pos,sca,rot,col
	def set_model(self):
		s=self
		if s.vnum in {0,8}:
			s.model='cube'
			s.texture=trn+trx[s.vnum]
			return
		if s.vnum in {2,4,5,6,7,9}:
			s.model=omf+flr[s.vnum]+'.obj'
			s.double_sided=True
		else:
			s.model=omf+flr[s.vnum]+'.ply'
		s.texture=omf+flr[s.vnum]+'.png'
	def set_collider(self):
		s=self
		cdl={0:lambda:setattr(s,'collider',b),
			2:lambda:setattr(s,'collider',BoxCollider(s,center=Vec3(0,-.1,0),size=(7.3,1,7.3))),
			4:lambda:setattr(s,'collider',BoxCollider(s,center=Vec3(0,-.5,0),size=(5,1.2,9.5))),
			5:lambda:setattr(s,'collider',BoxCollider(s,center=Vec3(0,-5,0),size=(55,10,55))),
			6:lambda:setattr(s,'collider',BoxCollider(s,size=Vec3(4,6,4))),
			7:lambda:setattr(s,'collider',BoxCollider(s,size=Vec3(4,6,4))),
			8:lambda:setattr(s,'collider',b),
			9:lambda:setattr(s,'collider',b)}
		if s.vnum in cdl:
			cdl[s.vnum]()
		del cdl

#####################
##level background ##
bpb={0:'warp_room.png',
	1:'jungle.png',
	2:'island.jpg',
	3:'ruin.jpg'}
class ObjType_Background(Entity):
	def __init__(self,ID,pos,sca,txa,col=color.white,UL=False):
		s=self
		s.vnum=ID
		super().__init__(model='quad',texture=bgg+bpb[ID],position=pos,scale=sca,color=col)
		if ID == 3:
			s.texture_scale=txa
			s.orginal_x,s.orginal_y=s.x,s.y
			s.orginal_tsc=s.texture_scale
			s.spawn_y=s.y
			s.bonus_y=-70
			LC.bgT=s
		if UL:
			s.unlit=False
			s.shader=unlit_shader
			s.texture_scale=txa
		del ID,pos,sca,col,txa,UL
	def update(self):
		s=self
		if s.vnum != 3:
			return
		if st.bonus_round:
			s.y=s.bonus_y
			return
		if s.y != s.spawn_y:
			s.y=s.spawn_y

################
##level water ##
wtr={0:'ev/water/water_',
	1:'l3/water_flow/water_flow',
	2:'l3/water_fall/waterf',
	3:'l3/foam/foam',
	4:'l4/drips/'}#frames 7
class ObjType_Water(Entity):
	def __init__(self,ID,pos,frames,spd,sca,rot,al=0,col=color.white,rev=False):
		s=self
		s.vnum=ID
		super().__init__(texture=omf+wtr[s.vnum]+'0.png',position=pos,rotation=rot,color=col)
		if ID in {0,1}:
			s.model='plane'
			s.scale=(sca[0],.1,sca[1])
			s.texture_scale=(sca[0]/3,sca[1]/3)
			if ID == 1:
				s.texture_scale=(1,12)
			dg.WaterHit(p=(pos[0],pos[1]-.1,pos[2]),sc=sca)
		else:
			s.model='quad'
			s.scale=(sca[0],sca[1])
			s.texture_scale=(s.scale_x,1)
			if ID == 2:
				ObjType_Water(ID=3,pos=(s.x,s.y-.49,s.z-.5),sca=(5,1),rot=(90,0,0),frames=15,spd=6,al=1)
				ObjType_Water(ID=3,pos=(s.x,s.y+.501,s.z+.49),sca=(5,1),rot=(90,180,0),frames=15,spd=6,col=color.rgb32(210,210,210),rev=True,al=1)
		if rev:
			s.frm=frames+.999
		else:
			s.frm=0
		s.frames=frames
		s.reverse=rev
		s.speed=spd
		s.alpha=al
		del ID,pos,frames,spd,sca,rot,al,col,rev
	def flow_reverse(self):
		s=self
		s.frm-=time.dt*s.speed
		if s.frm <= 0:
			s.frm=s.frames+.999
	def flow_normal(self):
		s=self
		s.frm=min(s.frm+time.dt*s.speed,s.frames+.999)
		if s.frm > s.frames+.99:
			s.frm=0
	def update(self):
		s=self
		if st.gproc() or (0 in {s.speed,s.frames}) or (s.y < -15 and not st.bonus_round):
			return
		if st.wtr_dist(s,LC.ACTOR):
			s.texture=omf+wtr[s.vnum]+f'{int(s.frm)}.png'
			if s.reverse:
				s.flow_reverse()
				return
			s.flow_normal()

#####################
## level 1 objects ##
MVP=omf+'l1/p_moss/moss'
class MossPlatform(Entity):
	def __init__(self,p,ptm,pts=.5,ptw=3):
		s=self
		super().__init__(model=MVP+'.obj',name='mptf',texture=MVP+'.png',scale=.0085,position=(p[0],p[1]+.475,p[2]),double_sided=True,collider=b)
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

#####################
## level 2 objects ##
def plank_bridge(pos,typ,cnt,ro_y,DST):
	for wP in range(cnt):
		plNK={90:lambda:Plank(pos=(pos[0]+wP*DST,pos[1],pos[2]),ro_y=ro_y,typ=typ),
			0:lambda:Plank(pos=(pos[0],pos[1],pos[2]+wP*DST),ro_y=ro_y,typ=typ)}
		plNK[ro_y]()
	del pos,typ,cnt,ro_y,DST

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

snPL=omf+'l2/snow_platform/snow_platform'
class SnowPlatform(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=snPL+'.ply',texture=snPL+'.png',name='sngg',position=pos,scale=.0075,rotation_x=-90)
		s.co=Entity(model=wfc,scale=(.85,1,.85),name=s.name,position=(s.x,s.y-.5,s.z),collider=b,visible=False)
		del pos

#####################
## level 3 objects ##
cbls=omf+''
class CobbleStone(Entity):
	def __init__(self,pos):
		super().__init__(model=cbls+'.ply',texture=cbls+'.png',position=pos,)
		del pos

#####################
## level 4 objects ##
swmi=omf+'l4/swr_swim/swr_swim'
class SwimPlatform(Entity):##box collider
	def __init__(self,pos):
		s=self
		super().__init__(model=swmi+'.obj',texture=swmi+'.png',name='swpt',scale=.00625,position=pos,color=color.rgb32(120,200,200),double_sided=True)
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

#####################
## level 5 objects ##
lpp=omf+'l5/loose_ptf/'
class LoosePlatform(Entity):
	def __init__(self,pos,t):
		s=self
		super().__init__(model=lpp+f'{t}/'+'lpf.obj',texture=lpp+f'{t}/'+'0.png',name='loos',scale=.01/15,position=pos,rotation_y=90,double_sided=True)
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

#####################
## level 7 objects ##
lbff=omf+'l7/piston_ptf/piston_ptf'
class PistonPlatform(Entity):
	def __init__(self,pos,spd,pa):
		s=self
		super().__init__(model=lbff+'.obj',texture=lbff+'.png',name='pipf',position=pos,scale=.1/100,double_sided=True)
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

llpt=omf+'l7/space_ptf/space_ptf'
class LabPlatform(Entity):
	def __init__(self,pos,drc,spd,rng):
		s=self
		super().__init__(model=llpt+'.ply',texture=llpt+'.png',name='lbbt',position=pos,scale=.1/120,rotation_x=-90,unlit=False,collider=b)
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
	def mv_player(self):
		s=self
		LC.ACTOR.x=s.x
		LC.ACTOR.z=s.z
	def update(self):
		if st.gproc():
			return
		s=self
		svd={0:lambda:s.ptf_sd(),1:lambda:s.ptf_fwd(),2:lambda:s.ptf_up()}
		svd[s.direc]()
		del svd

###################
## logic objects ##
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
		an.CrateBreak(pos=(0,-5,-10),col=color.white)
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
		if st.level_index in {6,7,8} and not st.level_index in st.COLOR_GEM:
			item.GemStone(c=st.level_index,pos=(s.x-1.1,s.y-.9,s.z))
		del pos,c

class RoomDoor(Entity):## door for start and end room
	def __init__(self,pos):
		s=self
		s.dPA=omf+'ev/door/'
		s.idf='mo'
		super().__init__(model=s.dPA+'u0.ply',texture=s.dPA+'u_door.tga',name='rmdr',position=pos,scale=.001,rotation_x=90,collider=b)
		s.door_part=Entity(model=s.dPA+'d0.ply',name=s.name,texture=s.dPA+'d_door.tga',position=(s.x,s.y+.1,s.z),scale=.001,rotation_x=90,collider=b)
		s.active=False
		s.d_opn=False
		s.d_frm=0
		del pos
	def update(self):
		if st.gproc():
			return
		s=self
		fvd=distance(s,LC.ACTOR)
		if fvd > 4:
			s.active=False
		if fvd < 2.4:
			s.active=True
		if s.active:
			if not s.d_opn:
				an.door_open(s)
			return
		if s.d_opn:
			an.door_close(s)

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

##############
## Switches ##
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

####################
## global objects ##
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

## Pseudo CrashB in Warp Room
rp='res/pc/crash'
class PseudoCrash(Entity):
	def __init__(self):
		s=self
		super().__init__(model=rp+'.ply',texture=rp+'.tga',scale=.1/20,rotation=(-90,30,0),position=(9,-4,0),unlit=False)
		Entity(model=MVP+'.obj',texture=MVP+'.png',scale=.75/30,position=(s.x,s.y,s.z),double_sided=True,color=color.rgb32(170,190,180))
		s.idfr=0
	def update(self):
		animation.idle(self)