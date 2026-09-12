import objects,map_tools,crate,status,npc,sys,os,_loc,danger,effect,random,settings
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from ursina import Entity,color

mt=map_tools
o=objects
dg=danger
st=status
LC=_loc
c=crate
n=npc
U=-3

SKULL_PTF=False
GEM_VNUM=2

def map_setting():
	LC.FOG_L_COLOR=color.white
	LC.FOG_B_COLOR=color.white
	LC.SKY_BG_COLOR=color.white
	LC.AMB_M_COLOR=color.rgb32(200,160,210)
	LC.LV_DST=(3,12)
	LC.BN_DST=(4,4.5)
	LC.RCZ=30
	LC.RCX=12
	LC.RCB=14
	st.toggle_thunder=False
	st.toggle_rain=False

def start_load():
	load_crate()
	bonus_zone()
	if GEM_VNUM in st.COLOR_GEM or settings.debg:
		gem_zone()
	load_object()
	load_wumpa()
	load_npc()
	map_setting()

def load_object():
	o.StartRoom(pos=(0,1,-64.2))
	o.BonusPlatform(pos=(20.8,5.6,7))
	o.GemPlatform(pos=(1.1,1.1,-22.2),t=GEM_VNUM)
	o.spawn_ice_wall(pos=(-2.3,-.5,-50),cnt=4,d=0)
	o.spawn_ice_wall(pos=(2.3,-.5,-56),cnt=3,d=1)
	o.spawn_ice_wall(pos=(20,4,15.5),cnt=2,d=0)
	o.spawn_ice_wall(pos=(26,4,10),cnt=1,d=1)
	o.spawn_ice_wall(pos=(44,4,29),cnt=1,d=1)
	o.ObjType_Water(pos=(12,-.5,-32),sca=(32,128),al=1,rot=(0,0,0),txs=(32*2,64*2),col=color.cyan,spd=0)
	o.ObjType_Water(pos=(51,4.5,23.5),sca=(64,40),al=1,rot=(0,0,0),txs=(64*2,40*2),col=color.cyan,spd=0)
	Entity(model='quad',scale=(256,128,1),color=color.white,z=64)
	effect.WeatherSnow(p_count=340,p_speed=2.5)
	#iceicle
	dg.IceIcle(pos=(4,3.1,2.5),fall_speed=3)
	dg.IceIcle(pos=(6.2,3.8,2.5),fall_speed=3)
	dg.IceIcle(pos=(13.1,4.2,2.5),fall_speed=3)
	dg.IceIcle(pos=(15.7,4.2,2.5),fall_speed=3)
	dg.IceIcle(pos=(18.4,4.2,2.5),fall_speed=3)
	#ice ceiling
	cblu=color.rgb32(180,180,200)
	o.ObjType_Deco(ID=17,sca=.4,pos=(-.5,3.75,2),rot=(-90,-90,0),col=cblu)
	o.ObjType_Deco(ID=17,sca=.4,pos=(4.2,4.9,2),rot=(-90,-90,0),col=cblu)
	o.ObjType_Deco(ID=17,sca=.4,pos=(8.3,4.9,2),rot=(-90,-90,0),col=cblu)
	o.ObjType_Deco(ID=17,sca=.4,pos=(12.4,5.2,2),rot=(-90,-90,0),col=cblu)
	o.ObjType_Deco(ID=17,sca=.4,pos=(16.5,5.2,2),rot=(-90,-90,0),col=cblu)
	o.ObjType_Deco(ID=17,sca=.6,pos=(16,.5,3),rot=(-90,-90,0))
	#invisible walls
	o.InvWall(pos=(-2.3,3,-30),sca=(1,10,70))
	o.InvWall(pos=(2.3,3,-30),sca=(1,10,60))
	o.InvWall(pos=(44,5,30),sca=(.5,15,40))
	o.InvWall(pos=(21,5,3),sca=(3,5,.5))
	o.InvWall(pos=(25,5,3),sca=(3,5,.5))
	o.InvWall(pos=(40,-.1,3),sca=(100,11,.5))
	#ice chunk
	for icj in range(5):
		o.ObjType_Deco(ID=4,sca=.6,pos=(13.5+icj*1.5,1.5,2.3),rot=(-90,-90,0))
	del icj
	o.ObjType_Deco(ID=4,sca=.6,pos=(21.2,1.2,2.3),rot=(-90,-90,0))
	o.ObjType_Deco(ID=4,sca=.6,pos=(22.4,2.25,2.4),rot=(90,-90,0))
	o.ObjType_Deco(ID=4,sca=.5,pos=(4.4,1.65,3),rot=(-90,-90,0))
	o.ObjType_Deco(ID=4,sca=.3,pos=(8,2.1,3),rot=(-90,-90,0))
	o.ObjType_Deco(ID=4,sca=.6,pos=(11.3,2,3),rot=(-90,-90,0))
	o.ObjType_Deco(ID=4,sca=.3,pos=(22,5.4,4.9),rot=(-90,-90,0))
	o.ObjType_Deco(ID=4,sca=.3,pos=(24,5.4,4.9),rot=(-90,-90,0))
	o.ObjType_Deco(ID=4,sca=.3,pos=(40.5,5.9,32.55),rot=(-90,-90,0))
	o.ObjType_Deco(ID=4,sca=.3,pos=(42.5,5.9,32.55),rot=(-90,-90,0))
	o.ObjType_Deco(ID=4,sca=.8,pos=(21.7,6,2.6),rot=(-180,-90,0))
	o.ObjType_Deco(ID=4,sca=.8,pos=(24.4,6,2.6),rot=(0,-90,0))
	o.ObjType_Deco(ID=4,sca=.8,pos=(21.2,5.3,3.2),rot=(260,-90,0))
	o.ObjType_Deco(ID=4,sca=.8,pos=(24.8,5.3,3.2),rot=(-80,-90,0))
	o.ObjType_Deco(ID=4,sca=.8,pos=(28,5.35,28.1),rot=(-180,-90,0))
	o.ObjType_Deco(ID=4,sca=.8,pos=(28,7.8,28),rot=(-180,-90,0))
	o.ObjType_Deco(ID=4,sca=.8,pos=(0,3.3,-60.4),rot=(90,-90,0))
	o.ObjType_Deco(ID=4,sca=.8,pos=(1.4,2.5,-60.6),rot=(0,-90,0))
	o.ObjType_Deco(ID=4,sca=.8,pos=(-1.3,2.3,-60.6),rot=(180,-90,0))
	o.ObjType_Deco(ID=4,sca=.8,pos=(41.7,8.5,38.3),rot=(90,-90,0))
	for ict in range(4):
		o.ObjType_Deco(ID=4,sca=.8,pos=(33+ict*2.5,4.5,43.6),rot=(-90,-90,0))
		o.ObjType_Deco(ID=4,sca=.8,pos=(33.5+ict*2.5,4.8,44.3),rot=(-90,-90,0))
	del ict
	#dangers
	wlO=3.8
	dg.DeathSmasher(pos=(10,wlO,2.45),typ=1,turn=1,speed=2)
	dg.DeathSmasher(pos=(11,wlO,2.45),typ=1,speed=2)
	dg.DeathSmasher(pos=(8,wlO,2.45),typ=0,speed=2)
	dg.Role(pos=(41.5,6.8,33.2),di=1)
	#first pass
	phg=-.065
	o.spw_block(ro_y=180,p=(0,phg,-61),vx=[1,2],ID=1)
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
	o.plank_bridge(pos=(24.7,5.3,27),ro_y=-90,typ=1,cnt=4,DST=.46)
	o.plank_bridge(pos=(28,5.3,27),ro_y=-90,typ=1,cnt=3,DST=.46)
	#ptf object
	for ptf1 in range(4):
		for ptf2 in range(3):
			o.ObjType_Movable(ID=1,pos=(34+ptf1*1.5,5.8,27+ptf2*1.5),ptm=0)
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
	del sna,snz
	o.EndRoom(pos=(43,8,44),c=color.rgb32(160,160,180))
def load_crate():
	h1=.75+.16
	h2=.925+.16
	h3=5.375+.16
	mt.crate_plane(ID=2,POS=(-.7,h2,-57),CNT=[1,2])
	mt.crate_wall(ID=12,POS=(-.3,h2,-18.6),CNT=[3,2])
	c.spawn(ID=1,p=(0,h1,-54))
	c.spawn(ID=3,p=(0,h1,-51))
	c.spawn(ID=2,p=(-.2,h1,-48))
	c.spawn(ID=5,p=(-1.1,h2,-43.2))
	c.spawn(ID=11,p=(.8,h2,-18.6))
	c.spawn(ID=12,p=(.2,h2,-15))
	c.spawn(ID=12,p=(0,h1,-13))
	c.spawn(ID=12,p=(-.3,h1,-10))
	c.spawn(ID=12,p=(0,h1,-8))
	c.spawn(ID=12,p=(-.2,h1,-6))
	c.spawn(ID=12,p=(0,h1,-4))
	mt.crate_row(ID=2,POS=(18,2.55+.16,2.5),CNT=3,WAY=0)
	c.spawn(ID=8,p=(23,4.2+.16,2.55))
	c.spawn(ID=8,p=(22,3.2+.16,2.5))
	mt.crate_plane(ID=1,POS=(22,h3,5.5),CNT=[1,2])
	c.spawn(ID=3,p=(23.2,5.45+.16,13))
	c.spawn(ID=5,p=(5.3,2.2+.16,2.5))
	c.spawn(ID=5,p=(23.9,h3,6.8))
	if not st.level_index in st.COLOR_GEM:
		c.spawn(ID=16,p=(.75,.925+.16,-56.7))
	#checkpoints
	c.spawn(ID=6,p=(0,h2,-41))
	c.spawn(ID=6,p=(3.2,1.23+.16,2.5))
	c.spawn(ID=6,p=(23,h3,4.2))
	c.spawn(ID=6,p=(23.4,h3,26.6))
	mt.box_wall_mixxed(POS=(0,.925+.16,-42.9),ID=(1,2))
	mt.box_wall_mixxed(POS=(-1,.925+.16,-22.1),ID=(2,1))
	mt.box_quad_mixxed(POS=(-.15,.7+.16,-32),ID=(1,12))
	mt.crate_wall(ID=14,POS=(-1,1.23+.16,2.5),CNT=[1,2])
	mt.crate_wall(ID=14,POS=(12,2.79,2.5),CNT=[1,1])
	mt.crate_plane(ID=14,POS=(22.7,5.54,21.1),CNT=[2,2])
	mt.crate_wall(ID=4,POS=(37,5.96,27),CNT=[1,1])
	mt.crate_wall(ID=1,POS=(38.4,5.96,30),CNT=[1,1])
	mt.crate_plane(ID=1,POS=(42.8,6+.16,29.9),CNT=[2,1])
	mt.box_wall_mixxed(POS=(40.7,6.4+.16,37),ID=(2,1))
	mt.box_wall_mixxed(POS=(42.8,6.4+.16,38.4),ID=(1,11))
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
	mt.wumpa_row(POS=(41.5,6.1,33.8),CNT=6,WAY=1)
def load_npc():
	n.spawn(ID=4,POS=(23,5.375,24),RNG=.3)
	n.spawn(ID=5,POS=(0,.92,1),DRC=2)
	n.spawn(ID=6,POS=(14.5,2.65,2.4))
	n.spawn(ID=5,POS=(30.5,5.35,26.9),RNG=.5)
	n.spawn(ID=6,POS=(42,6.4,37.6),RNG=1)

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
	c.spawn(ID=4,p=(5.3,-34.68,U))
	c.spawn(ID=1,p=(8.3,-36.78,U))
	c.spawn(ID=1,p=(7.5,-36.1,U))
	c.spawn(ID=1,p=(7,-35.6,U))
	c.spawn(ID=9,p=(14.5,-37,U),m=1)
	c.spawn(ID=13,p=(4,-37,U),m=1,l=2)
	mt.crate_row(ID=1,POS=(10,-37.32,U),WAY=0,CNT=7)
	mt.crate_row(ID=3,POS=(10.32,-37.64,U),WAY=0,CNT=5)
	mt.wumpa_double_row(POS=(-.5,-37,U),CNT=3)
	mt.wumpa_double_row(POS=(10,-36.9,U),CNT=7)
	mt.wumpa_double_row(POS=(2.8,-37,U),CNT=3)
	mt.wumpa_double_row(POS=(7,-37,U),CNT=3)
	o.BonusPlatform(pos=(16,-37.1,U))

def gem_zone():
	cblu=color.rgb32(180,180,200)
	o.ObjType_Deco(ID=17,sca=.5,pos=(199,2,-2.1),rot=(90,-90,0),col=cblu)
	o.ObjType_Deco(ID=17,sca=.5,pos=(204.85,2,-2.1),rot=(90,-90,0),col=cblu)
	o.ObjType_Deco(ID=17,sca=.5,pos=(204.85+5.85,2,-2.1),rot=(90,-90,0),col=cblu)
	o.ObjType_Water(pos=(220,.65,40),sca=(64,100),al=1,rot=(0,0,0),txs=(64,100),col=color.cyan,spd=0)
	o.GemPlatform(pos=(214.4,2.7,37.2),t=GEM_VNUM)
	for wce in range(9):
		o.ObjType_Deco(ID=17,sca=.5,pos=(213.3,5.2,.85+5.85*wce),rot=(90,180,0),col=cblu)
		o.ObjType_Deco(ID=17,sca=.5,pos=(215.5,5.2,-.75+5.85*wce),rot=(90,0,0),col=cblu)
		o.ObjType_Deco(ID=17,sca=.5,pos=(213.3,2.5,.85+5.85*wce),rot=(90,180,0),col=cblu)
		o.ObjType_Deco(ID=17,sca=.5,pos=(215.5,2.5,-.75+5.85*wce),rot=(90,0,0),col=cblu)
		o.ObjType_Deco(ID=17,sca=.5,pos=(213.3,-.2,.85+5.85*wce),rot=(90,180,0),col=cblu)
		o.ObjType_Deco(ID=17,sca=.5,pos=(215.5,-.2,-.75+5.85*wce),rot=(90,0,0),col=cblu)
	del wce
	o.ObjType_Deco(ID=17,sca=.5,pos=(213,3,38),rot=(90,-90,0),col=cblu)
	#inv wall
	o.InvWall(pos=(200,3.5,-2.5),sca=(8,20,.4))
	o.InvWall(pos=(205,4,-2.5),sca=(5,20,.4))
	o.InvWall(pos=(209,4.7,-2.5),sca=(8,20,.4))
	o.InvWall(pos=(213.3,4.7,17.5),sca=(.8,20,40))
	o.InvWall(pos=(215.3,4.7,15),sca=(.3,20,40))
	o.InvWall(pos=(213,4.7,38),sca=(10,20,.3))
	#blocks
	o.spw_block(ID=1,ro_y=180,p=(200,0,U),vx=[1,1])
	o.multi_ice_floor(pos=(201,0,U),cnt=[3,1])
	o.multi_ice_floor(pos=(204.5,.3,U),cnt=[1,1])
	o.multi_ice_floor(pos=(206.5,.6,U),cnt=[1,1])
	o.multi_ice_floor(pos=(208,.6,U),cnt=[8,1])
	o.multi_ice_floor(pos=(214,.6,-2),cnt=[2,4])
	o.ObjType_Movable(ID=1,pos=(214.3,1.5,2.5),ptm=0)
	o.ObjType_Movable(ID=1,pos=(214.3,1.5,4),ptm=0)
	o.multi_ice_floor(pos=(214,.6,5.5),cnt=[2,2])
	o.multi_ice_floor(pos=(214,.6,8.5),cnt=[1,5])
	o.multi_ice_floor(pos=(214,.6,14),cnt=[2,2])
	o.multi_ice_floor(pos=(214.5,.9,17),cnt=[1,4])
	o.multi_ice_floor(pos=(214.5,1.5,20.5),cnt=[1,8])
	o.spw_block(ID=1,ro_y=180,p=(214.5,1.5,28.5),vx=[1,2])
	o.spw_block(ID=1,ro_y=180,p=(214,1.5,34.5),vx=[2,4])
	#danger
	dg.DeathSmasher(pos=(207.9,1.6+1.65,-3.15),typ=1,turn=1,speed=3,wait=.5)
	dg.DeathSmasher(pos=(209.5,1.6+1.65,-3.15),typ=1,turn=1,speed=3,wait=.5)
	dg.DeathSmasher(pos=(212.8,1.6+1.65,-3.15),typ=0,turn=1,speed=4,wait=.3)
	#crates
	c.spawn(ID=3,p=(201.3,1+.16,U))
	c.spawn(ID=5,p=(201.3,2.5,U))
	c.spawn(ID=2,p=(204.2,1.3+.16,U))
	c.spawn(ID=11,p=(206.7,1.6+.16,U))
	c.spawn(ID=5,p=(214.5,1.6+.16,-1.8))
	c.spawn(ID=3,p=(214.6,1.6+.16,.9))
	c.spawn(ID=4,p=(214.2,1.6+.16,12.6))
	c.spawn(ID=9,p=(214.5,2.5+.16,28.5),m=27)
	mt.crate_row(ID=13,POS=(214.5,2.5,30.4),CNT=10,WAY=1,l=1,m=27)
	mt.crate_row(ID=13,POS=(214.5,2.5-.32,30.4),CNT=10,WAY=1,l=12,m=27)
	mt.box_quad_mixxed(POS=(202,1.16,-3.2),ID=(2,3))
	mt.crate_row(ID=12,POS=(214,1.6+.16,-.6),CNT=5,WAY=0)
	mt.crate_row(ID=1,POS=(214.7,1.6+.16,5.4),CNT=3,WAY=1)
	c.spawn(ID=12,p=(214.7,1.6+.16,6.7))
	c.spawn(ID=12,p=(214.2,1.6+.16,10))
	c.spawn(ID=12,p=(214.7,1.6+.16,13.9))
	c.spawn(ID=12,p=(214,1.6+.16,15.2))
	mt.crate_row(ID=12,POS=(214.1,1.9+.16,19.8),CNT=4,WAY=0)
	mt.crate_row(ID=12,POS=(214,2.5+.16,20.7),CNT=8,WAY=1)
	mt.crate_row(ID=12,POS=(215,2.5+.16,20.7),CNT=8,WAY=1)
	mt.crate_row(ID=3,POS=(214.3,2.5+.16,25),CNT=4,WAY=1)
	mt.crate_row(ID=3,POS=(214.3,4.3,25),CNT=4,WAY=1)
	mt.crate_row(ID=1,POS=(214.5,2.5+.16,21),CNT=5,WAY=1)
	mt.box_quad_mixxed(POS=(214.3,1.6+.16,-.2),ID=(1,2))
	mt.box_wall_mixxed(POS=(214.5,2.5+.16,36.2),ID=(1,4))
	c.spawn(ID=10,p=(214.7,2.5+.16,35.3))
	#wumpa
	mt.wumpa_row(POS=(202.7,1.25,U),CNT=3,WAY=0)
	mt.wumpa_row(POS=(210.1,1.8,U),CNT=8,WAY=0)
	mt.wumpa_row(POS=(214.1,1.8,.1),CNT=5,WAY=1)
	mt.wumpa_row(POS=(214.1,1.8,5.4),CNT=5,WAY=1)
	mt.wumpa_row(POS=(214.1,1.8,8.3),CNT=4,WAY=1)
	mt.wumpa_row(POS=(214.1,1.8,10.7),CNT=4,WAY=1)
	mt.wumpa_row(POS=(214.5,2.1,17),CNT=8,WAY=1)
	mt.wumpa_row(POS=(214.5,2.1,26.4),CNT=8,WAY=1)
	#npc
	n.spawn(ID=6,POS=(214.1,1.6,-3.1),RNG=.5,DRC=0)
	n.spawn(ID=6,POS=(214.7,2.5,25.6),RNG=1,DRC=2)