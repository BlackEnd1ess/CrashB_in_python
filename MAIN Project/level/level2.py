import objects,map_tools,crate,status,npc,sys,os,_loc,danger
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from ursina import *

mt=map_tools
o=objects
dg=danger
st=status
LC=_loc
r=random
c=crate
n=npc
U=-3

def map_setting():
	LC.FOG_L_COLOR=color.white
	LC.FOG_B_COLOR=color.white
	LC.SKY_BG_COLOR=color.white
	LC.AMB_M_COLOR=color.rgb32(200,160,210)
	LC.LV_DST=(3,12)
	LC.BN_DST=(4,4.5)
	LC.RCX=12
	LC.RCB=6
	LC.RCZ=28
	st.toggle_thunder=False
	st.toggle_rain=False

def start_load():
	load_crate()
	bonus_zone()
	load_object()
	load_wumpa()
	load_npc()
	map_setting()

def load_object():
	o.StartRoom(pos=(0,1,-64.2))
	o.BonusPlatform(pos=(20.8,5.6,7))
	o.spawn_ice_wall(pos=(-2.3,-.5,-50),cnt=4,d=0)
	o.spawn_ice_wall(pos=(2.3,-.5,-56),cnt=3,d=1)
	o.spawn_ice_wall(pos=(20,4,15.5),cnt=2,d=0)
	o.spawn_ice_wall(pos=(26,4,10),cnt=1,d=1)
	o.spawn_ice_wall(pos=(44,4,29),cnt=1,d=1)
	o.ObjType_Water(ID=0,pos=(12,-.5,-32),sca=(32,128),al=1,rot=(0,0,0),col=color.cyan,frames=0,spd=0)
	o.ObjType_Water(ID=0,pos=(51,4.5,23.5),sca=(64,40),al=1,rot=(0,0,0),col=color.cyan,frames=0,spd=0)
	Entity(model='quad',scale=(256,128,1),color=color.white,z=64)
	#invisible walls
	o.InvWall(pos=(-2.3,3,-30),sca=(1,10,70))
	o.InvWall(pos=(2.3,3,-30),sca=(1,10,60))
	o.InvWall(pos=(44,5,30),sca=(.5,15,40))
	o.InvWall(pos=(21,5,3),sca=(3,5,.5))
	o.InvWall(pos=(25,5,3),sca=(3,5,.5))
	o.InvWall(pos=(40,-.1,3),sca=(100,11,.5))
	#ice chunk
	o.ObjType_Deco(ID=4,sca=.8,pos=(21.7,6,2.6),rot=(-180,-90,0))
	o.ObjType_Deco(ID=4,sca=.8,pos=(24.4,6,2.6),rot=(0,-90,0))
	o.ObjType_Deco(ID=4,sca=.8,pos=(21.2,5.3,3.2),rot=(260,-90,0))
	o.ObjType_Deco(ID=4,sca=.8,pos=(24.8,5.3,3.2),rot=(-80,-90,0))
	o.ObjType_Deco(ID=4,sca=.8,pos=(28,5.35,28.1),rot=(-180,-90,0))
	o.ObjType_Deco(ID=4,sca=.8,pos=(28,7.8,28),rot=(-180,-90,0))
	o.ObjType_Deco(ID=4,sca=.8,pos=(0,3.3,-60.4),rot=(90,-90,0))
	o.ObjType_Deco(ID=4,sca=.8,pos=(41.7,8.5,38.3),rot=(90,-90,0))
	for ict in range(4):
		o.ObjType_Deco(ID=4,sca=.8,pos=(33+ict*2.5,4.5,43.6),rot=(-90,-90,0))
		o.ObjType_Deco(ID=4,sca=.8,pos=(33.5+ict*2.5,4.8,44.3),rot=(-90,-90,0))
	del ict
	#dangers
	wlO=3.7
	dg.WoodLog(pos=(10.5,wlO,2.45))
	dg.WoodLog(pos=(8.2,wlO,2.45))
	dg.Role(pos=(41.5,6.8,33.2),di=1)
	#first pass
	phg=-.065
	o.spw_block(ro_y=180,p=(0,phg,-60.5),vx=[1,2],ID=1)
	o.spw_block(ro_y=180,p=(-1,phg,-57.5),vx=[3,2],ID=1)
	o.spw_block(ro_y=180,p=(-1,phg,-43),vx=[3,1],ID=1)
	o.spw_block(ro_y=180,p=(0,phg,-42),vx=[1,3],ID=1)
	o.spw_block(ro_y=180,p=(-1,phg,-22),vx=[3,1],ID=1)
	o.spw_block(ro_y=180,p=(0,phg,-21),vx=[1,2],ID=1)
	o.spw_block(ro_y=180,p=(0,phg,-19),vx=[2,1],ID=1)
	o.spw_block(ro_y=180,p=(-1,phg,-1),vx=[3,1],ID=1)
	o.spw_block(ro_y=180,p=(0,phg,0),vx=[1,3],ID=1)
	#2d area
	bz=2.7
	nh=.25
	nv=1.2
	nf=5
	o.spw_block(ID=1,ro_y=180,p=(-1,nh,bz),vx=[3,1])
	o.spw_block(ID=1,ro_y=180,p=(3,nh,bz),vx=[1,1])
	o.spw_block(ID=1,ro_y=180,p=(4,.75,bz),vx=[1,1])
	o.spw_block(ID=1,ro_y=180,p=(5,nv,bz),vx=[2,1])
	o.spw_block(ID=1,ro_y=180,p=(8,nv,bz),vx=[1,1])
	o.spw_block(ID=1,ro_y=180,p=(10,nv,bz),vx=[2,1])
	o.spw_block(ID=1,ro_y=180,p=(12,nv+.4,bz),vx=[2,1])
	o.ObjType_Floor(ID=0,pos=(16.4,2.05,bz+.1),sca=(6,1),txa=(6,1))
	o.spw_block(ID=1,ro_y=180,p=(19.8,nv+.4,bz),vx=[2,1])
	o.spw_block(ID=1,ro_y=180,p=(21.8,nv+1,bz),vx=[1,1])
	o.spw_block(ID=1,ro_y=180,p=(22.8,nv+2,bz),vx=[1,1])
	# final area
	o.spw_block(ID=1,ro_y=180,p=(23,nv+3.2,3.3),vx=[1,2])
	o.spw_block(ID=1,ro_y=180,p=(22,nv+3.2,5.3),vx=[3,3])
	o.spw_block(ID=1,ro_y=180,p=(22,nv+3.2,20),vx=[3,1])
	o.spw_block(ID=1,ro_y=180,p=(23,nv+3.2,21),vx=[1,2])
	o.spw_block(ID=1,ro_y=180,p=(23,nv+3.2,24),vx=[1,1])
	o.spw_block(ID=1,ro_y=180,p=(23,nv+3.2,26),vx=[2,2])
	o.spw_block(ID=1,ro_y=180,p=(30.1,nv+3.2,26.7),vx=[2,1])
	o.spw_block(ID=1,ro_y=180,p=(32.1,nv+3.8,26.7),vx=[1,1])
	# room area
	o.spw_block(ID=1,ro_y=180,p=(40,nf,30),vx=[4,1])
	o.spw_block(ID=1,ro_y=180,p=(41.5,nf,31),vx=[1,2])
	o.spw_block(ID=1,ro_y=180,p=(40.5,nf,33),vx=[3,1])
	o.spw_block(ID=1,ro_y=180,p=(41.5,nf,34),vx=[1,3])
	o.spw_block(ID=1,ro_y=180,p=(40.5,nf+.4,37),vx=[4,3])
	#pillar
	phe=1.1
	o.pillar_twin(p=(-.75,phe,-56))
	o.pillar_twin(p=(-.75,phe,-42.6))
	o.pillar_twin(p=(-.75,phe,-21.65))
	o.pillar_twin(p=(-.75,phe,-1))
	o.pillar_twin(p=(22.25,5.35,7.5))
	o.pillar_twin(p=(22.25,5.35,19.85))
	o.Ropes(pos=(-.475,.7,-56),le=55)
	o.Ropes(pos=(22.5,5.3,7),le=13)
	o.ObjType_Deco(ID=2,pos=(40.25,6.55,38.7),sca=.2,rot=(-90,45,0),col=color.cyan)
	o.ObjType_Deco(ID=2,pos=(43.75,6.55,38.7),sca=.2,rot=(-90,45,0),col=color.cyan)
	#planks
	_pl=.7
	#bridge1
	o.plank_bridge(pos=(0,_pl,-55),ro_y=0,typ=0,cnt=3,DST=1)
	o.plank_bridge(pos=(0,_pl,-50),ro_y=0,typ=1,cnt=4,DST=1.5)
	#bridge2
	o.plank_bridge(pos=(0,_pl,-38),ro_y=0,typ=0,cnt=1,DST=1)
	o.plank_bridge(pos=(0,_pl,-36),ro_y=0,typ=1,cnt=2,DST=.5)
	o.plank_bridge(pos=(0,_pl,-34),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(0,_pl,-32),ro_y=0,typ=1,cnt=2,DST=.5)
	o.plank_bridge(pos=(0,_pl,-30),ro_y=0,typ=0,cnt=2,DST=.5)
	o.plank_bridge(pos=(0,_pl,-28),ro_y=0,typ=0,cnt=2,DST=.5)
	o.plank_bridge(pos=(0,_pl,-26),ro_y=0,typ=0,cnt=4,DST=.5)
	o.plank_bridge(pos=(0,_pl,-18),ro_y=0,typ=1,cnt=2,DST=.5)
	o.plank_bridge(pos=(0,_pl,-16),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(0,_pl,-14),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(0,_pl,-12),ro_y=0,typ=1,cnt=4,DST=.5)
	o.plank_bridge(pos=(0,_pl,-10),ro_y=0,typ=0,cnt=2,DST=.5)
	o.plank_bridge(pos=(0,_pl,-8),ro_y=0,typ=1,cnt=2,DST=.5)
	o.plank_bridge(pos=(0,_pl,-6),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(0,_pl,-4),ro_y=0,typ=1,cnt=2,DST=.5)
	o.plank_bridge(pos=(0,_pl,-3),ro_y=0,typ=0,cnt=1,DST=.5)
	#bridge 3
	o.plank_bridge(pos=(23-.025,5.35,8.3),ro_y=0,typ=0,cnt=2,DST=.5)
	o.plank_bridge(pos=(23-.025,5.35,11),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(23-.025,5.35,13),ro_y=0,typ=1,cnt=2,DST=.5)
	o.plank_bridge(pos=(23-.025,5.35,15),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(23-.025,5.35,16),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(23-.025,5.35,17),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(23-.025,5.35,18),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(23-.025,5.35,19),ro_y=0,typ=0,cnt=1,DST=.5)
	#bridge 4
	o.plank_bridge(pos=(24.7,5.3,26.75),ro_y=90,typ=1,cnt=4,DST=.44)
	o.plank_bridge(pos=(28,5.3,26.75),ro_y=90,typ=1,cnt=3,DST=.44)
	#ptf object
	for ptf1 in range(4):
		for ptf2 in range(3):
			o.SnowPlatform(pos=(34+ptf1*1.5,5.8,27+ptf2*1.5))
	del ptf1,ptf2
	#walls
	snz=3
	for snw in range(7):
		o.ObjType_Wall(ID=1,pos=(-5+snw*5.4,.1,snz),sca=.02,ro_y=90)
		o.ObjType_Wall(ID=1,pos=(-5+snw*5.4,3.2,snz),sca=.02,ro_y=90)
	del snw
	o.ObjType_Wall(ID=1,pos=(19,6.3,snz),sca=.02,ro_y=90)
	o.ObjType_Wall(ID=1,pos=(27,6.3,snz),sca=.02,ro_y=90)
	o.ObjType_Wall(ID=1,pos=(30,2,38),sca=.02,ro_y=90)
	for sna in range(2):
		o.ObjType_Wall(ID=1,pos=(20+sna*5.4,5,28),sca=.02,ro_y=90)
		o.ObjType_Wall(ID=1,pos=(20+sna*5.4,8.2,28),sca=.02,ro_y=90)
	del sna
	o.EndRoom(pos=(43,8,44),c=color.rgb32(160,160,180))
def load_crate():
	h1=.75+.16
	h2=.925+.16
	h3=5.375+.16
	mt.crate_plane(ID=2,POS=(-.7,h2,-57),CNT=[1,2])
	mt.crate_wall(ID=12,POS=(-.3,h2,-18.6),CNT=[3,2])
	c.place_crate(ID=1,p=(0,h1,-54))
	c.place_crate(ID=3,p=(0,h1,-51))
	c.place_crate(ID=2,p=(-.2,h1,-48))
	c.place_crate(ID=5,p=(-1.1,h2,-43.2))
	c.place_crate(ID=11,p=(.8,h2,-18.6))
	c.place_crate(ID=12,p=(.2,h2,-15))
	c.place_crate(ID=12,p=(0,h1,-13))
	c.place_crate(ID=12,p=(-.3,h1,-10))
	c.place_crate(ID=12,p=(0,h1,-8))
	c.place_crate(ID=12,p=(-.2,h1,-6))
	c.place_crate(ID=12,p=(0,h1,-4))
	mt.crate_row(ID=2,POS=(18,2.55+.16,2.5),CNT=3,WAY=0)
	c.place_crate(ID=8,p=(23,4.2+.16,2.55))
	c.place_crate(ID=8,p=(22,3.2+.16,2.5))
	mt.crate_plane(ID=1,POS=(22,h3,5.5),CNT=[1,2])
	c.place_crate(ID=3,p=(23.2,5.45+.16,13))
	c.place_crate(ID=10,p=(42.8,6.4+.16,37.7))
	c.place_crate(ID=5,p=(5.3,2.2+.16,2.5))
	c.place_crate(ID=5,p=(23.9,h3,6.8))
	if not 1 in status.COLOR_GEM:
		c.place_crate(ID=16,p=(.75,.925+.16,-56.7))
	#checkpoints
	c.place_crate(ID=6,p=(0,h2,-41))
	c.place_crate(ID=6,p=(3.2,1.23+.16,2.5))
	c.place_crate(ID=6,p=(23,h3,4.2))
	c.place_crate(ID=6,p=(23.4,h3,26.6))
	mt.crate_wall(ID=14,POS=(-1,1.23+.16,2.5),CNT=[1,2])
	mt.crate_wall(ID=14,POS=(12,2.79,2.5),CNT=[1,1])
	mt.crate_plane(ID=14,POS=(22.7,5.54,21.1),CNT=[2,2])
	mt.crate_wall(ID=4,POS=(37,5.96,27),CNT=[1,1])
	mt.crate_wall(ID=1,POS=(38.4,5.96,30),CNT=[1,1])
	mt.crate_plane(ID=1,POS=(42.8,6+.16,29.9),CNT=[2,1])
def load_wumpa():
	whl=1.2
	mt.wumpa_wall(POS=(-.2,.95,-53),CNT=[2,1])
	mt.wumpa_plane(POS=(0,.95,-30),CNT=[1,3])
	mt.wumpa_plane(POS=(0,.95,-28),CNT=[1,2])
	mt.wumpa_plane(POS=(0,.95,-26),CNT=[1,5])
	mt.wumpa_double_row(POS=(0,1.4,2.5),CNT=3)
	mt.wumpa_double_row(POS=(5.7,2.4,2.5),CNT=2)
	mt.wumpa_double_row(POS=(14,2.85,2.5),CNT=4)
	mt.wumpa_double_row(POS=(26,5.6,27),CNT=5)
	mt.wumpa_wall(POS=(22.7,5.55,18.9),CNT=[2,2])
def load_npc():
	n.spawn(ID=4,POS=(23,5.375,24),RNG=.3)
	n.spawn(ID=5,POS=(0,.92,1),DRC=2)
	n.spawn(ID=6,POS=(14.5,2.65,2.4))
	n.spawn(ID=5,POS=(30.5,5.35,26.9),RNG=.5)

## bonus level / gem path
def bonus_zone():
	dg.FallingZone(pos=(0,-40,0),s=(64,1,64))
	o.spw_block(p=(0,-38.5,U),ro_y=180,vx=[1,1],ID=1)
	o.spw_block(p=(2,-38.2,U),ro_y=180,vx=[4,1],ID=1)
	o.spw_block(p=(7,-38.2,U),ro_y=180,vx=[3,1],ID=1)
	o.spw_block(p=(12.8,-38.2,U),ro_y=180,vx=[3,1],ID=1)
	for sw in range(5):
		o.ObjType_Wall(ID=1,pos=(-4+sw*5.4,-33.9,-2.5),sca=.02,ro_y=90)
		o.ObjType_Wall(ID=1,pos=(-4+sw*5.4,-37,-2.5),sca=.02,ro_y=90)
		o.ObjType_Wall(ID=1,pos=(-4+sw*5.4,-40.1,-2.5),sca=.02,ro_y=90)
	del sw
	mt.crate_row(ID=0,POS=(3.8,-35,U),WAY=0,CNT=8)
	mt.crate_wall(ID=2,POS=(4,-34.68,U),CNT=[2,2])
	c.place_crate(ID=4,p=(5.3,-34.68,U))
	c.place_crate(ID=1,p=(8.3,-36.78,U))
	c.place_crate(ID=1,p=(7.5,-36.1,U))
	c.place_crate(ID=1,p=(7,-35.6,U))
	c.place_crate(ID=9,p=(14.5,-37,U),m=1)
	c.place_crate(ID=13,p=(4,-37,U),m=1,l=2)
	mt.crate_row(ID=1,POS=(10,-37.32,U),WAY=0,CNT=7)
	mt.crate_row(ID=3,POS=(10.32,-37.64,U),WAY=0,CNT=5)
	mt.wumpa_double_row(POS=(-.5,-37,U),CNT=3)
	mt.wumpa_double_row(POS=(10,-36.9,U),CNT=7)
	mt.wumpa_double_row(POS=(2.8,-37,U),CNT=3)
	mt.wumpa_double_row(POS=(7,-37,U),CNT=3)
	o.BonusPlatform(pos=(16,-37.1,U))