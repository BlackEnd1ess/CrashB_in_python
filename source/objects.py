from ursina import Entity,color,time,distance,distance_xz,invoke,BoxCollider,Vec2,Vec3,SpotLight,camera,Audio,Text,scene,load_texture
import _core,status,item,sound,animation,player,_loc,settings,npc,ui,danger,random
from effect import WarpVortex,WaterDrips
from ursina.ursinastuff import destroy
from ursina.shaders import *

an=animation
dg=danger
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

block_sca_level={0:.5,1:.5,2:.35,3:.02,4:.03,5:(.5,.8,.5)}
trhs={0:1,1:.985,2:.85,3:.501,4:.75,5:1}
def spw_block(ID,p,vx,ro_y=0,typ=0,sca=None):
	kg=block_sca_level[ID] if not sca else sca
	for gbx in range(vx[0]):
		for gbz in range(vx[1]):
			ObjType_Block(ID=ID,pos=(p[0]+trhs[ID]*gbx,p[1],p[2]+trhs[ID]*gbz),sca=kg,ro_y=ro_y,typ=typ)
	del p,vx,ID,gbx,gbz,ro_y,typ,kg

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
		s.double_sided=ID in (1,3,4)
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
		if ID in (3,5):
			s.matr='metal'
		del pos,sca,ro_y,typ,ID,bl_c,s


##platforms with dyncamic move func
mpt={0:'l1/p_moss/moss',
	1:'l2/snow_platform/snow_platform',
	2:'l7/space_ptf/space_ptf'}
class ObjType_Movable(Entity):
	def __init__(self,pos,ptm,ID,pts=.5,ptw=3,rng=1,tu=0,col=color.light_gray,UL=False):
		s=self
		s.vnum=ID
		super().__init__(model=wfc,collider=b,position=pos,scale=(.75,1,.75),name='mptf',visible=False)
		s.opt_model=Entity(model=omf+mpt[ID]+'.ply',texture=omf+mpt[ID]+'.png',color=col,position=(pos[0],pos[1]+(.46 if ID == 0 else +.5),pos[2]),rotation_x=-90,scale=(.0075 if ID == 1 else .001))
		s.spawn_pos=pos
		s.ptf_speed=pts
		s.ptf_range=rng
		s.ptf_wait=ptw if pts != 1 else 0
		s.is_sfc=False
		s.ptf_slp=ptw
		s.ptf_mv=ptm
		s.turn=tu
		s.mv_drc='z' if ptm == 3 else 'x'
		if UL:
			s.opt_model.unlit=False
		if ID == 2:
			scale=.1/120
			s.matr='metal'
		del pos,ptm,ID,pts,ptw,rng,tu,col,UL,s
	def ptf_move(self):
		s=self
		pdv={2:s.spawn_pos[0],3:s.spawn_pos[2]}
		kv=getattr(s,s.mv_drc)
		{0:lambda:setattr(s,s.mv_drc,kv+time.dt*s.ptf_speed),1:lambda:setattr(s,s.mv_drc,kv-time.dt*s.ptf_speed)}[s.turn]()
		if (s.turn == 0 and kv >= pdv[s.ptf_mv]+s.ptf_range):
			s.ptf_wait=s.ptf_slp
			s.turn=1
		if (s.turn == 1 and kv <= pdv[s.ptf_mv]-s.ptf_range):
			s.ptf_wait=s.ptf_slp
			s.turn=0
		del kv,pdv
	def mv_player(self):
		if self.ptf_mv < 2:
			return
		LC.ACTOR.position=(self.x,LC.ACTOR.y,self.z)
	def dive(self):
		s=self
		if s.is_sfc:
			s.y-=time.dt*4
			if s.y <= s.spawn_pos[1]-.5:
				s.y=s.spawn_pos[1]-.5
				s.is_sfc=False
				s.ptf_wait=s.ptf_slp
				if distance(s,LC.ACTOR) < 6 and s.vnum == 0:
					sn.obj_audio(ID=6)
			return
		s.y+=time.dt*4
		if s.y >= s.spawn_pos[1]:
			s.y=s.spawn_pos[1]
			s.is_sfc=True
			s.ptf_wait=s.ptf_slp
			if distance(s,LC.ACTOR) < 6 and s.vnum == 0:
				sn.pc_audio(ID=10)
	def update(self):
		if st.gproc():
			return
		s=self
		if s.ptf_mv == 1:
			s.opt_model.y=s.y+.46 if s.vnum == 0 else s.y+.5
			s.ptf_wait=max(s.ptf_wait-time.dt,0)
			if s.ptf_wait <= 0:
				s.dive()
			return
		if s.ptf_mv > 1:
			s.opt_model.x=s.x
			s.opt_model.z=s.z
			s.ptf_wait=max(s.ptf_wait-time.dt,0)
			if s.ptf_wait <= 0:
				s.ptf_move()


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
		del pos,sca,ID,ro_y,col,typ,s
	def check_obj(self):
		s=self
		if s.vnum in (3,10,11):
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
	6:'l7/lab_bgs/lab_bgs',
	7:'l8/polar_hills/polar_hills'}
class ObjType_Wall(Entity):
	def __init__(self,ID,pos,sca,ro_y=0,col=color.white):
		s=self
		s.vnum=ID
		super().__init__(model=omf+smd[ID]+'.ply',texture=omf+smd[ID]+'.png',position=pos,scale=sca,rotation=(-90,ro_y,0),color=col,double_sided=True)
		if ID == 0 and pos[0] > 190:
			s.color=color.rgb32(0,140,160)
		if ID in (2,4):
			s.collider=b
		if ID == 7:
			s.unlit=False
			if ro_y in (180,0):
				s.collider=BoxCollider(s,center=Vec3(-1,-4,5),size=Vec3(2,24,20))
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
	12:'l7/boiler/boiler',
	13:'l8/polar_sky/polar_sky'}
class ObjType_Deco(Entity):#UL=unlit Flag, htb=HitBox
	def __init__(self,ID,pos,sca,rot,col=color.white,UL=False,htb=False):
		s=self
		s.vnum=ID
		super().__init__(model=None,texture=f'{omf}{dms[ID]}.png',position=pos,scale=sca,rotation=rot,color=col)
		s.model='quad' if ID == 0 else f'{omf}{dms[ID]}.ply'
		if ID == 1:
			HitBox(pos=pos,sca=(1,5,1))
		if ID == 2:
			ObjType_Deco(ID=3,pos=(s.x,s.y+1.1,s.z+.075),sca=(.025,.02,.03),rot=(-90,45,0),col=col)
			HitBox(pos=(pos[0],pos[1]+4.9,pos[2]),sca=(.5,10,.5))
		if ID in (8,9):
			WaterDrips(pos=(s.x,s.y-{8:1,9:.2}[ID],s.z-{8:.25,9:.5}[ID]),sca=(.9,.4),rot=(0,0,90))
		if ID == 13:
			s.shader=unlit_shader
		if UL:
			s.unlit=False
		if htb:
			s.collider=b
		del ID,pos,sca,rot,col,htb


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
		del ID,pos,rot,s
	def check_model(self):
		s=self
		if s.vnum == 0:
			s.scale=.1
			HitBox(sca=(3,3,2.2),pos=(s.x+2.3,s.y,s.z))
			HitBox(sca=(3,3,2.2),pos=(s.x-2.3,s.y,s.z))
			HitBox(sca=(3,3,2.2),pos=(s.x,s.y+3,s.z))
			IndoorZone(pos=(s.x,s.y+1.6,s.z),sca=3)
			if st.level_index == 8:
				s.color=color.rgb32(0,100,160)
				s.unlit=False
			return
		if s.vnum == 1:
			s.model=wfc
			s.scale=(3,1,3)
			s.collider=b
			Entity(model=omf+cor[s.vnum]+'.ply',texture=omf+cor[s.vnum]+'.png',position=(s.x,s.y+.5,s.z),scale=.03,rotation=(-90,90,0))
			s.visible=False
			dg.FireTrap(pos=(s.x-1.34,s.y+1.58,s.z+.675))
			dg.FireTrap(pos=(s.x+1.225,s.y+1.58,s.z+.675))
			for pvb in ((s.x-1.4,s.y+1.7,s.z),(s.x+1.4,s.y+1.7,s.z)):
				HitBox(pos=pvb,sca=(.5,2,3))
			del pvb
			IndoorZone(pos=(s.x,s.y+2.55,s.z),sca=3)


#################
##level Grounds##
def multi_ice_floor(pos,cnt):
	for ifx in range(cnt[0]):
		for ifz in range(cnt[1]):
			ObjType_Floor(ID=0,pos=(pos[0]+ifx,pos[1],pos[2]+ifz),sca=(1,2,1),txa=(1,1),col=color.rgb32(0,140,200),al=1)
	del pos,cnt,ifx,ifz

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
	def __init__(self,ID,pos,sca,rot=(0,0,0),txa=(1,1),al=1,col=color.white):
		s=self
		s.vnum=ID
		super().__init__(position=pos,scale=sca,rotation=rot,color=col)
		s.set_model(txa)
		if ID == 0:
			s.alpha=al
			s.texture_scale=txa
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
			#s.name='befl'
		s.set_collider()
		del ID,pos,sca,rot,col,al,txa,s
	def set_model(self,txa):
		s=self
		if s.vnum in (0,8):
			s.model='cube'
			s.texture=trn+trx[s.vnum]
			return
		if s.vnum in (2,4,5,6,7,9):
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
	3:'ruin.jpg',
	4:'polar.jpg'}
class ObjType_Background(Entity):
	def __init__(self,ID,pos,sca,txa,col=color.white,UL=False):
		s=self
		s.vnum=ID
		super().__init__(model='quad',texture=bgg+bpb[ID],position=pos,scale=sca,color=col)
		if ID == 3:
			s.texture_scale=txa
			s.orginal_x,s.orginal_y=s.x,s.y
			s.spawn_y=s.y
			s.bonus_y=-70
		if UL:
			s.unlit=False
			s.shader=unlit_shader
			s.texture_scale=txa
		del ID,pos,sca,col,txa,UL,s
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
class ObjType_Water(Entity):
	def __init__(self,pos,sca,spd,rot,al=0,txs=(1,1),col=color.white,rev=False,UL=False):
		s=self
		super().__init__(model='plane',texture=LC.wtr_texture[0],texture_scale=txs,position=pos,scale=(sca[0],.1,sca[1]),rotation=rot,color=col,alpha=al)
		dg.WaterHit(p=(s.x,s.y-.1,s.z),sc=sca)
		s.max_frm=int(len(LC.wtr_texture))-1+.99
		s.frm=a.max_frm+.999 if rev else 0
		s.reverse=rev
		s.speed=spd
		s.frozen=bool(s.max_frm == 0 or spd == 0)
		if UL:
			s.unlit=False
		del pos,sca,spd,rot,al,txs,col,rev,UL
	def refr_texture(self):
		s=self
		s.texture=LC.wtr_texture[int(s.frm)]
		if s.reverse:
			s.frm=max(s.frm-time.dt*s.speed,0)
			if s.frm <= 0:
				s.frm=s.max_frm
			return
		cc.incr_frm(s,s.speed)
	def update(self):
		s=self
		if st.gproc() or s.frozen or (s.y < -15 and not st.bonus_round) or (s.x > 190 and not st.death_route):
			return
		if st.wtr_dist(s,LC.ACTOR):
			s.refr_texture()


#####################
## level 2 objects ##
def plank_bridge(pos,typ,cnt,ro_y,DST):
	for wP in range(cnt):
		plNK={90:lambda:Plank(pos=(pos[0]+wP*DST,pos[1],pos[2]),ro_y=ro_y,typ=typ),
			0:lambda:Plank(pos=(pos[0],pos[1],pos[2]+wP*DST),ro_y=ro_y,typ=typ)}
		plNK[ro_y]()
	del pos,typ,cnt,ro_y,DST,wP

plob=f'{omf}l2/plank/plank'
class Plank(Entity):
	def __init__(self,pos,typ,ro_y):
		s=self
		super().__init__(model=f'{plob}.ply',texture=f'{plob}.png',name='plnk',scale=(.0012,.001,.0012),position=pos,collider=b,rotation=(-90,ro_y+90,0),color=color.orange)
		s.spawn_pos=s.position
		s.typ=typ
		if typ == 1:
			s.color=color.rgb32(200,255,255)
			s.is_touched=False
			s.is_reset=False
			s.falling=False
			s.tme=0
		del pos,typ,ro_y,s
	def reset_status(self):
		s=self
		s.is_touched=False
		s.is_reset=False
		s.falling=False
		s.visible=True
		s.position=s.spawn_pos
		s.collider=b
	def pl_touch(self):
		if not self.is_touched:
			self.is_touched=True
	def refr_function(self):
		s=self
		s.tme+=time.dt
		if s.tme > 1.5:
			s.tme=0
			s.falling=True
			s.collider=None
			sn.crate_audio(ID=2,pit=.8)
	def fall_down(self):
		s=self
		if s.y > s.spawn_pos[1]-3:
			s.y-=time.dt*4
			return
		s.visible=False
		s.is_reset=True
	def update(self):
		if st.gproc() or self.typ == 0:
			return
		s=self
		if s.is_reset:
			s.tme+=time.dt
			if s.tme > 5:
				s.tme=0
				s.reset_status()
			return
		if s.falling:
			s.fall_down()
		if s.is_touched:
			s.refr_function()

rpt=f'{omf}l2/rope/rope_pce.jpg'
class Ropes(Entity):
	def __init__(self,pos,le):
		s=self
		super().__init__(model='cube',scale=(.03,.03,le),name='snrp',texture=rpt,position=pos,texture_scale=(1,le*8),origin_z=-.5)
		s.dup=Entity(model='cube',scale=s.scale,name=s.name,position=(s.x+.95,s.y,s.z),texture=rpt,texture_scale=(1,le*8),origin_z=s.origin_z)
		del pos,le,s

#####################
## leve 3 objects ###
class WaterFlow(Entity):
	def __init__(self,pos,sca):
		s=self
		super().__init__(model='plane',texture=f'{omf}l3/water_flow/water_flow.png',position=pos,scale=(sca[0],0,sca[1]),color=color.white,alpha=.75)
		dg.WaterHit(p=(s.x,s.y-.1,s.z),sc=sca)
		s.texture_scale=(1,sca[1]/16)
		s.speed=.1
	def update(self):
		if st.gproc():
			return
		self.texture_offset+=Vec2(0,time.dt*self.speed)

class Waterfall(Entity):
	def __init__(self,pos,sca):
		s=self
		if len(LC.wtf_texture) <= 0:
			LC.wtf_texture=[load_texture(f'res/objects/l3/water_fall/waterf{cbx}.png') for cbx in range(31+1)]
		super().__init__(model='quad',texture=LC.wtf_texture[0],position=pos,scale=(sca[0],sca[1]),texture_scale=(sca[0],1))
		WaterFoam(pos=(s.x,s.y-.49,s.z-.5),sc_x=5)
		WaterFoam(pos=(s.x,s.y+.501,s.z+.49),sc_x=5,rev=True)
		s.max_frm=len(LC.wtf_texture)-1+.99
		s.spd=10
		s.frm=0
		del pos,sca,s
	def update(self):
		if st.gproc():
			return
		s=self
		cc.incr_frm(s,s.spd)
		if s.texture != LC.wtf_texture[int(s.frm)]:
			s.texture=LC.wtf_texture[int(s.frm)]

class WaterFoam(Entity):
	def __init__(self,pos,sc_x,al=1,rev=False):
		s=self
		if len(LC.wff_texture) <= 0:#water foam l3
			LC.wff_texture=[load_texture(f'res/objects/l3/water_foam/foam{cbx}.png') for cbx in range(15+1)]
		super().__init__(model='plane',texture=LC.wff_texture[0],position=pos,rotation=(0,0,0),scale=(sc_x,1),texture_scale=(sc_x,1),alpha=al)
		s.max_frm=len(LC.wff_texture)-1+.99
		s.frm=s.max_frm if rev else 0
		s.reverse=rev
		s.spd=6
		if rev:
			s.color=color.rgb32(210,210,210)
			s.rotation=(0,180,0)
		del pos,sc_x,al,rev,s
	def decrase_frame(self):
		s=self
		s.frm-=time.dt*s.spd
		if s.frm <= 0:
			s.frm=s.max_frm
	def refr_texture(self):
		s=self
		if s.texture != LC.wff_texture[int(s.frm)]:
			s.texture=LC.wff_texture[int(s.frm)]
	def update(self):
		if st.gproc():
			return
		s=self
		s.refr_texture()
		if s.reverse:
			s.decrase_frame()
			return
		cc.incr_frm(s,s.spd)


#####################
## level 4 objects ##
swmi=f'{omf}l4/swr_swim/swr_swim'
class SwimPlatform(Entity):##box collider
	def __init__(self,pos):
		s=self
		super().__init__(model=f'{swmi}.obj',texture=f'{swmi}.png',name='swpt',scale=.00625,position=pos,color=color.rgb32(120,200,200),double_sided=True)
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
lpp=f'{omf}l5/loose_ptf/'
class LoosePlatform(Entity):
	def __init__(self,pos,t):
		s=self
		super().__init__(model=f'{lpp}{t}/lpf.obj',texture=f'{lpp}{t}/0.png',name='loos',scale=.01/15,position=pos,rotation_y=90,double_sided=True)
		s.collider=BoxCollider(s,center=Vec3(0,-.5,0),size=(100*10,100,100*10))
		s.collapsed=False
		s.active=False
		s.tme=0
		s.typ=t
		del pos,t
	def reset(self):
		s=self
		s.collapsed=False
		s.collision=True
		s.visible=True
	def action(self):
		s=self
		s.tme+=time.dt
		if s.tme > 1:
			s.tme=0
			sn.obj_audio(ID=20)
			s.collision=False
			s.collapsed=True
			s.active=False
	def pl_touch(self):
		s=self
		if not s.active:
			s.active=True
			s.visible=False
			an.CollapseFloor(t=s.typ,pos=s.position)
			sn.obj_audio(ID=19)
	def update(self):
		if st.gproc():
			return
		s=self
		if s.collapsed:
			s.tme+=time.dt
			if s.tme > 8:
				s.tme=0
				s.reset()
			return
		if s.active:
			s.action()


#####################
## level 7 objects ##
lbff=f'{omf}l7/piston_ptf/piston_ptf'
class PistonPlatform(Entity):
	def __init__(self,pos,spd,pa):
		s=self
		super().__init__(model=f'{lbff}.obj',texture=f'{lbff}.png',name='pipf',position=pos,scale=.1/100,double_sided=True)
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
			sn.obj_audio(ID=11,pit=.5)
	def mv_up(self):
		s=self
		if s.y < s.spw_y:
			s.y+=time.dt*s.mvsp
			return
		s.wait=s.wt*2
		s.stat=0
		if distance(s,LC.ACTOR) < 8:
			sn.obj_audio(ID=11,pit=.8)
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

###################
## logic objects ##
ev='res/crate/'
class CrateScore(Entity):## level reward
	def __init__(self,pos):
		s=self
		super().__init__(model=f'{ev}cr_t0.obj',texture=f'{ev}1.png',scale=.18,position=pos,origin_y=.5,unlit=False,color=color.light_gray,alpha=.4)
		s.cc_text=Text(parent=scene,position=(s.x-.2,s.y,s.z),name=s.name,text=None,font=ui._fnt,color=color.rgb32(255,255,100),scale=10,unlit=False)
		del pos,s
	def refr_function(self):
		self.cc_text.text=f'{st.crate_count}/{st.crates_in_level}'
		self.rotation_y-=120*time.dt
	def spawn_gemstone(self):
		s=self
		item.GemStone(pos=(s.x,s.y-.3,s.z),c=0)
		sn.ui_audio(ID=4)
		destroy(s.cc_text)
		destroy(s)
	def update(self):
		if st.gproc():
			return
		s=self
		if st.crate_count >= st.crates_in_level:
			s.spawn_gemstone()
			return
		dv=LC.C_GEM and distance(s,LC.C_GEM) < .5
		s.cc_text.visible=not(dv or st.relic_challange)
		s.visible=not(dv or st.relic_challange)
		if s.visible:
			s.refr_function()

rmp=f'{omf}ev/s_room/room'
class StartRoom(Entity):## game spawn point
	def __init__(self,pos):
		s=self
		super().__init__(model=f'{rmp}.ply',texture=f'{rmp}.png',name='strm',position=pos,scale=(.07,.07,.08),rotation=(270,90),color=color.white)
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
		if st.level_index == 5:
			s.color=color.rgb32(120,120,120)
			s.unlit=False
		if st.level_index == 8:
			s.color=color.rgb32(60,60,60)
			s.unlit=False
		del pos,s

eR=f'{omf}ev/e_room/e_room'
class EndRoom(Entity):## finish level
	def __init__(self,pos,c):
		s=self
		super().__init__(model=f'{eR}.ply',texture=f'{eR}.png',scale=.025,name='enrm',rotation=(-90,90,0),position=pos,color=c,unlit=False)
		Entity(model='plane',name=s.name,color=color.black,scale=(4,1,16),position=(s.x-1,s.y-1.8,s.z+3))#curtain
		HitBox(sca=(4,1,16),pos=(s.x-1,s.y-2,s.z+3))#floor
		HitBox(sca=(1,3,16),pos=(s.x-2.2,s.y,s.z+3))#wall left
		HitBox(sca=(1,3,16),pos=(s.x,s.y,s.z+3))#wall right
		HitBox(sca=(5,3,16),pos=(s.x-1,s.y+1.4,s.z+3))#ceiling
		HitBox(sca=(6,4,2),pos=(s.x,s.y,s.z+9))#back
		HitBox(sca=(6,1,2.5),pos=(s.x-1,s.y-1.85,s.z+.45))#pod1
		HitBox(sca=(.85,1,.85),pos=(s.x-1.1,s.y-1.6,s.z+.3))#pod2
		HitBox(sca=(1.6,1,1),pos=(s.x-1.1,s.y-1.51,s.z+6.5))#pod3
		IndoorZone(pos=(s.x-1,s.y-.15,s.z+1),sca=(5,2,12))
		LevelFinish(p=(s.x-1.1,s.y-1.1,s.z+7))
		RoomDoor(pos=(s.x-1.1,s.y+.25,s.z-4.78))
		if s.x < 180:
			LC.gem_pod_position=(s.x-1.1,s.y-.9,s.z)
		if st.level_index != 5:
			Entity(model='cube',scale=(20,10,.1),name=s.name,position=(s.x,s.y-5,s.z+16),color=color.black)
		if st.crates_in_level > 0 and not st.level_index in st.CLEAR_GEM:
			if s.x < 180:# pos_x 190 is death zone in lv 5
				CrateScore(pos=(s.x-1.1,s.y-.7,s.z))
		if st.level_index == 8:
			s.unlit=False
		del pos,c

class RoomDoor(Entity):## door for start and end room
	def __init__(self,pos):
		s=self
		s.dPA=f'{omf}ev/door/'
		s.idf='mo'
		super().__init__(model=f'{s.dPA}u0.ply',texture=f'{s.dPA}u_door.png',name='rmdr',position=pos,scale=.001,rotation_x=90,collider=b)
		s.door_part=Entity(model=f'{s.dPA}d0.ply',name=s.name,texture=f'{s.dPA}d_door.png',position=(s.x,s.y+.1,s.z),scale=.001,rotation_x=90,collider=b)
		s.active=False
		s.d_opn=False
		s.d_frm=0
		if st.level_index in (5,8):
			s.door_part.color=color.rgb32(60,60,60) if st.level_index == 8 else color.rgb32(120,120,120)
			s.color=color.rgb32(60,60,60) if st.level_index == 8 else color.rgb32(120,120,120)
			s.door_part.unlit=False
			s.unlit=False
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
	def __init__(self,pos,ID=0):
		s=self
		k=bool(st.level_index == 7 or ID == 1)
		sIN=f'{omf}ev/bonus/bonus_e' if k else f'{omf}ev/bonus/bonus'
		s.matr='metal' if k else None
		super().__init__(model=f'{sIN}.ply',texture=f'{sIN}.png',name='bnpt',collider=b,scale=-.001,rotation_x=90,position=pos,unlit=False)
		s.fixx_y=s.y+.25
		s.start_y=s.y
		s.w_time=0
		del pos,k,sIN,ID
	def refr(self):
		s=self
		s.w_time+=time.dt
		if s.w_time > .5:
			s.w_time=0
			LC.ACTOR.y=s.fixx_y
			LC.ACTOR.freezed=False
	def update(self):
		if st.gproc() or st.death_event:
			return
		s=self
		s.collider=None if (st.relic_challange) else b
		s.visible=not(st.relic_challange)
		if st.bonus_solved:
			destroy(s)
			return
		if LC.ACTOR.freezed and LC.ACTOR.y < s.fixx_y and distance_xz(LC.ACTOR,s) < .3:
			s.refr()

class GemPlatform(Entity):## gem platform
	def __init__(self,pos,t):
		s=self
		physical=bool(t in st.COLOR_GEM or settings.debg)
		ne='gem_ptf' if physical else 'gem_ptf_e'
		s.is_enabled=physical
		super().__init__(model=wfc,name='gmpt',scale=(.6,.4,.6),position=pos,visible=False)
		s.opt_model=Entity(model=f'{omf}ev/{ne}/{ne}.ply',name=s.name,texture=f'{omf}ev/{ne}/{ne}.png',rotation_x=-90,scale=.001,position=pos,color=LC.GEM_PLATFORM_COLOR[t],unlit=False)
		s.alpha=1 if physical else .5
		s.org_color=s.color
		s.start_y=s.y
		s.typ=t
		del pos,t,physical
	def check_collider(self):
		s=self
		if st.relic_challange:
			if s.collider:
				s.collider=None
			return
		if s.is_enabled:
			if not s.collider:
				s.collider=b
	def update(self):
		if st.gproc():
			return
		s=self
		s.check_collider()
		s.opt_model.visible=not(st.relic_challange)
		if st.gem_path_solved or st.relic_challange:
			destroy(s.opt_model)
			cc.destroy_entity(s)
			return
		s.opt_model.position=(s.x,s.y+.15,s.z)
		if s.is_enabled and not LC.ACTOR.freezed:
			s.opt_model.rotation_y+=time.dt*20

class PseudoGemPlatform(Entity):
	def __init__(self,pos,t):
		s=self
		physical=bool(t in st.COLOR_GEM or settings.debg)
		ne='gem_ptf' if physical else 'gem_ptf_e'
		s.is_enabled=physical
		super().__init__(model=f'{omf}ev/{ne}/{ne}.ply',texture=f'{omf}ev/{ne}/{ne}.png',rotation_x=-90,scale=.001,position=pos,color=LC.GEM_PLATFORM_COLOR[t],unlit=False)
		del pos,t
		if s.is_enabled:
			HitBox(pos=(s.x,s.y-.15,s.z),sca=(.6,.4,.6))
			return
		s.alpha=.5
	def update(self):
		if st.gproc():
			return
		self.visible=not(st.relic_challange)

##############
## Switches ##
class LevelFinish(Entity):## finish level
	def __init__(self,p):
		s=self
		super().__init__(model='sphere',name='lvfi',collider=b,scale=1,position=p,visible=False)
		WarpVortex(pos=(s.x,s.y+.1,s.z),col=color.yellow,sca=.6,drc=1)
		WarpVortex(pos=(s.x,s.y+.3,s.z),col=color.orange,sca=.7,drc=0)
		WarpVortex(pos=(s.x,s.y+.5,s.z),col=color.yellow,sca=.8,drc=1)
		WarpVortex(pos=(s.x,s.y+.7,s.z),col=color.orange,sca=.7,drc=0)
		s.w_audio=Audio('res/snd/obj_portal.wav',volume=0,loop=True)
		LC.lv_fin_pos=(p[0],p[1]+.3,p[2])
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
		##visible for development
		#self.model='cube'
		#self.visible=True
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
class PseudoCrash(Entity):
	def __init__(self):
		s=self
		super().__init__(model=f'{LC.ctx}.ply',texture=f'{LC.ctx}.png',scale=.1/20,rotation=(-90,30,0),position=(9,-4,0),unlit=False)
		Entity(model=f'{mpt[0]}.ply',texture=f'{mpt[0]}.png',scale=.00275,position=(s.x,s.y,s.z),double_sided=True,color=color.rgb32(170,190,180),rotation_x=-90,unlit=False)
		s.new_anim_idx=0
		s.anim_idx=0
		s.frm=0
		del s
	def update(self):
		animation.c_animation(self,0)