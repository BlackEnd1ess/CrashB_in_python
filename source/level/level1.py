import settings,objects,map_tools,crate,npc,status,_loc,sys,os
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from ursina import Entity,color

mt=map_tools
st=status
o=objects
LC=_loc
c=crate
n=npc
U=-3

SKULL_PTF=False
GEM_VNUM=1

def map_setting():
	LC.FOG_L_COLOR=color.rgb32(20,70,50)
	LC.FOG_B_COLOR=color.rgb32(20,70,50)
	LC.AMB_M_COLOR=color.rgb32(140,140,140)
	LC.SKY_BG_COLOR=color.rgb32(0,60,80)
	st.toggle_thunder=False
	st.toggle_rain=True
	LC.LV_DST=(10,15)
	LC.BN_DST=(6,12)
	LC.RCZ=30
	LC.RCX=16
	LC.RCB=6

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
	o.StartRoom(pos=(-.3,1,-66.5))
	cG=color.green
	o.ObjType_Water(pos=(0,.6,-16),sca=(10,96),al=1,col=color.rgb32(190,190,190),spd=8,rot=(0,0,0),txs=(10*2,96*2))
	o.InvWall(pos=(-5,.5,-32),sca=(5.,10,128))
	o.InvWall(pos=(5.3,.5,-32),sca=(5.,10,128))
	o.BonusPlatform(pos=(1.1,1.2,-6))
	o.GemPlatform(pos=(-.3,1.2,-18),t=GEM_VNUM)
	gt=(1,2,1.4)
	gs=1.6
	fgg=color.rgb32(190,200,190)
	o.ObjType_Scene(ID=0,pos=(-4,gs,-47),ro_y=0,sca=gt,col=fgg)
	o.ObjType_Scene(ID=0,pos=(4,gs,-47),ro_y=180,sca=gt,col=fgg)
	o.ObjType_Scene(ID=0,pos=(-4,gs,-16),ro_y=0,sca=gt,col=fgg)
	o.ObjType_Scene(ID=0,pos=(4,gs,-16),ro_y=180,sca=gt,col=fgg)
	o.ObjType_Scene(ID=0,pos=(-4,gs,15),ro_y=0,sca=gt,col=fgg)
	o.ObjType_Scene(ID=0,pos=(4,gs,15),ro_y=180,sca=gt,col=fgg)
	o.ObjType_Scene(ID=0,pos=(-4,gs,46),ro_y=0,sca=gt,col=fgg)
	o.ObjType_Scene(ID=0,pos=(4,gs,46),ro_y=180,sca=gt,col=fgg)
	o.ObjType_Background(ID=1,pos=(0,0,128),sca=(250,40),txa=(5,1))
	o.ObjType_Background(ID=1,pos=(0,-20,127),sca=(250,40),txa=(5,1))
	del gt,gs,fgg
	#cobblestone underwater
	for cbb in range(3):
		o.ObjType_Deco(ID=6,pos=(0,.6-cbb/7,-64+cbb*44.4),sca=(2,3,.75),rot=(-90,0,0))
	del cbb
	#plants
	Entity(model='cube',texture='res/terrain/bricks.png',scale=(9,2,.3),position=(0,-.2,-64.5),texture_scale=(9,2))
	o.ObjType_Deco(ID=1,pos=(-1.2,1.2,-46),sca=.0175,rot=(-90,0,0))
	o.ObjType_Deco(ID=1,pos=(0,1.4,-26.4),sca=.013,rot=(-90,0,0))
	for trw in range(8):
		o.ObjType_Scene(ID=1,pos=(-4.3,1.2,-60+trw*12),sca=(.15,.16,.18),col=color.rgb32(180,190,180))
		o.ObjType_Scene(ID=1,pos=(4.3,1.2,-60+trw*12),sca=(.15,.16,.18),col=color.rgb32(180,190,180))
	del trw
	o.ObjType_Deco(ID=1,pos=(-1.5,1.2,20.3),sca=.0175,rot=(-90,0,0))
	o.ObjType_Deco(ID=1,pos=(1.2,1.2,20.3),sca=.0175,rot=(-90,0,0))
	o.ObjType_Deco(ID=1,pos=(1.1,1.5,10),sca=.0175,rot=(-90,0,0))
	o.ObjType_Deco(ID=1,pos=(-1.8,1.5,13.3),sca=.0175,rot=(-90,0,0))
	o.ObjType_Deco(ID=1,pos=(.5,1.3,2.5),sca=.0175,rot=(-90,0,0))
	o.ObjType_Deco(ID=1,pos=(0,1,-2),sca=.016,rot=(-90,0,0))
	o.ObjType_Deco(ID=1,pos=(0,1,6),sca=.015,rot=(-90,0,0))
	o.ObjType_Deco(ID=1,pos=(-1.7,1.3,-35),sca=.013,rot=(-90,0,0))
	o.ObjType_Deco(ID=1,pos=(-1.5,1.1,-31),sca=.015,rot=(-90,0,0))
	o.ObjType_Deco(ID=1,pos=(1.4,1.2,-29),sca=.014,rot=(-90,0,0))
	o.ObjType_Deco(ID=1,pos=(1,1.6,-34.6),sca=.02,rot=(-90,0,0))
	o.ObjType_Deco(ID=1,pos=(-1.8,1.5,-21.5),sca=.02,rot=(-90,0,0))
	o.ObjType_Deco(ID=1,pos=(1.75,1.5,-18.2),sca=.02,rot=(-90,0,0))
	o.ObjType_Deco(ID=1,pos=(-1.4,1.5,-8.1),sca=.02,rot=(-90,0,0))
	o.ObjType_Deco(ID=1,pos=(-1.5,1.2,-62.5),sca=.02,rot=(-90,0,0))
	o.ObjType_Deco(ID=1,pos=(1.1,1.5,-53),sca=.02,rot=(-90,0,0))
	o.ObjType_Deco(ID=1,pos=(-1.5,1.5,-54),sca=.02,rot=(-90,0,0))
	#mushroom
	o.ObjType_Deco(ID=15,pos=(.12,1,-63.2),col=color.white,sca=.085,rot=(-90,45,0))
	o.ObjType_Deco(ID=14,pos=(-1.2,1,-55.9),col=color.white,sca=.085,rot=(-90,45,0))
	o.ObjType_Deco(ID=15,pos=(-.9,1,-14.4),col=color.white,sca=.085,rot=(-90,45,0))
	o.ObjType_Deco(ID=14,pos=(1.2,1,-15.6),col=color.white,sca=.085,rot=(-90,45,0))
	#jungle bush 3d
	o.ObjType_Deco(ID=16,pos=(-2.1,1,-14),sca=.0006,rot=(-90,0,-10),col=color.white,UL=True)
	o.ObjType_Deco(ID=16,pos=(2.3,1,-14),sca=.0006,rot=(-90,0,-10),col=color.white,UL=True)
	o.ObjType_Deco(ID=16,pos=(-2.1,1.75,-14),sca=.0006,rot=(-90,0,-10),col=color.white,UL=True)
	o.ObjType_Deco(ID=16,pos=(2.3,1.75,-14),sca=.0006,rot=(-90,0,-10),col=color.white,UL=True)
	o.ObjType_Deco(ID=16,pos=(-2.1,2.5,-14),sca=.0006,rot=(-90,0,-10),col=color.white,UL=True)
	o.ObjType_Deco(ID=16,pos=(2.3,2.5,-14),sca=.0006,rot=(-90,0,-10),col=color.white,UL=True)
	#pillar
	plc=color.rgb32(200,230,140)
	o.ObjType_Deco(ID=2,pos=(.7,.5,-60.5),sca=.2,rot=(-90,45,0),col=plc,htb=False)
	o.ObjType_Deco(ID=2,pos=(.8,.5,-56.8),sca=.2,rot=(-90,45,0),col=plc,htb=False)
	o.ObjType_Deco(ID=2,pos=(1.2,.5,-50),sca=.2,rot=(-90,45,0),col=plc,htb=False)
	o.ObjType_Deco(ID=2,pos=(-1,.5,-47),sca=.2,rot=(-90,45,0),col=plc,htb=False)
	o.ObjType_Deco(ID=2,pos=(1.1,.5,-44),sca=.2,rot=(-90,45,0),col=plc,htb=False)
	o.ObjType_Deco(ID=2,pos=(-1.2,.5,-42),sca=.2,rot=(-90,45,0),col=plc,htb=False)
	o.ObjType_Deco(ID=2,pos=(1.2,.5,-41),sca=.2,rot=(-90,45,0),col=plc,htb=False)
	o.ObjType_Deco(ID=2,pos=(-1.2,.5,-39),sca=.2,rot=(-90,45,0),col=plc,htb=False)
	o.ObjType_Deco(ID=2,pos=(.8,.5,-31.7),sca=.2,rot=(-90,45,0),col=plc,htb=False)
	o.ObjType_Deco(ID=2,pos=(1.5,.5,-21),sca=.2,rot=(-90,45,0),col=plc,htb=False)
	o.ObjType_Deco(ID=2,pos=(-.3,.5,-19),sca=.2,rot=(-90,45,0),col=plc,htb=False)
	o.ObjType_Deco(ID=2,pos=(.8,.5,-8),sca=.2,rot=(-90,45,0),col=plc,htb=False)
	o.ObjType_Deco(ID=2,pos=(-.9,.5,-3.1),sca=.2,rot=(-90,45,0),col=plc,htb=False)
	o.ObjType_Deco(ID=2,pos=(-1,.5,18.5),sca=.2,rot=(-90,45,0),col=plc,htb=False)
	o.ObjType_Deco(ID=2,pos=(1,.5,17),sca=.2,rot=(-90,45,0),col=plc,htb=False)
	del plc
	#platform
	dz=-64
	dy=.5
	o.spw_block(ID=0,p=(-1.5,dy,dz+27),vx=[1,2])
	o.spw_block(ID=0,p=(-.25,dy,dz),vx=[1,6])
	o.spw_block(ID=0,p=(-1,dy,dz+7),vx=[2,2])
	o.spw_block(ID=0,p=(0,dy,dz+10),vx=[1,1])
	o.spw_block(ID=0,p=(-1,dy,dz+12),vx=[3,1])
	o.spw_block(ID=0,p=(0,dy,dz+14),vx=[1,5])
	o.spw_block(ID=0,p=(0,dy,dz+26),vx=[1,5])
	o.spw_block(ID=0,p=(0,dy,dz+32),vx=[1,1])
	o.spw_block(ID=0,p=(0,dy,dz+34),vx=[1,1])
	o.spw_block(ID=0,p=(0,dy,dz+36),vx=[1,3])
	o.spw_block(ID=0,p=(-2,dy,dz+36.5),vx=[1,6])
	o.spw_block(ID=0,p=(.7,dy,dz+41),vx=[1,6])
	o.spw_block(ID=0,p=(-1,dy,dz+48),vx=[3,5])
	o.spw_block(ID=0,p=(0,dy,dz+53),vx=[1,7])
	o.spw_block(ID=0,p=(-2,dy,dz+60),vx=[5,1])
	o.spw_block(ID=0,p=(-2,dy,dz+61),vx=[1,5])
	o.spw_block(ID=0,p=(-2,dy,dz+68),vx=[1,4])
	o.spw_block(ID=0,p=(+2,dy,dz+61),vx=[1,4])
	o.spw_block(ID=0,p=(+2,dy,dz+68+.32),vx=[1,2])
	o.spw_block(ID=0,p=(+2,dy,dz+72),vx=[1,1])
	o.spw_block(ID=0,p=(-2,dy,dz+73),vx=[5,1])
	o.spw_block(ID=0,p=(0,dy,dz+74),vx=[1,2])
	o.spw_block(ID=0,p=(0,dy,dz+81),vx=[1,2])
	o.spw_block(ID=0,p=(0,dy,dz+83),vx=[1,3])
	o.ObjType_Movable(ID=0,pos=(1.3,1,-54),ptm=0)
	o.ObjType_Movable(ID=0,pos=(1.4,1,-47.8),ptm=0)
	o.ObjType_Movable(ID=0,pos=(1.5,1,-46.8),ptm=0)
	o.ObjType_Movable(ID=0,pos=(1.2,1,-42.5),ptm=0)
	o.ObjType_Movable(ID=0,pos=(1,1,-36),ptm=0)
	o.ObjType_Movable(ID=0,pos=(0,1,-42),ptm=2,drc=1,rng=2.4,pts=1,ptw=2)
	o.ObjType_Movable(ID=0,pos=(-2,1,-6),ptm=0)
	o.ObjType_Movable(ID=0,pos=(0,1,14),ptm=2,drc=1,rng=2,pts=1,ptw=2)
	o.ObjType_Corridor(ID=0,pos=(0,1,-13))
	o.ObjType_Deco(ID=0,pos=(-1.1,1.2,-11.9),sca=(2,1),rot=(0,0,0),col=color.rgb32(0,170,0))
	o.ObjType_Deco(ID=0,pos=(1.1,1.2,-11.9),sca=(2,1),rot=(0,0,0),col=color.rgb32(0,170,0))
	o.ObjType_Deco(ID=0,pos=(-1.1,1.2,-14.2),sca=(2,1),rot=(0,0,0),col=color.rgb32(0,170,0))
	o.ObjType_Deco(ID=0,pos=(1.1,1.2,-14.2),sca=(2,1),rot=(0,0,0),col=color.rgb32(0,170,0))
	o.EndRoom(pos=(1,2.4,26.2),c=color.rgb32(160,180,160))
def load_crate():
	CRP=1.16
	if not st.level_index in st.COLOR_GEM:
		c.spawn(ID=16,p=(-1.1,CRP,-57))
	mt.crate_plane(ID=2,POS=(-1.8,CRP,3.3),CNT=[2,1])
	mt.crate_wall(ID=14,POS=(-1.3,1.14,8.8),CNT=[2,2])
	mt.crate_plane(ID=1,POS=(-1.5,CRP,-2.5),CNT=[1,3])
	mt.crate_wall(ID=14,POS=(-.7,CRP,-56.1),CNT=[1,2])
	mt.crate_wall(ID=1,POS=(-1,CRP,-49),CNT=[2,1])
	c.spawn(ID=5,p=(0,CRP,-54))
	c.spawn(ID=1,m=1,l=0,p=(.85,CRP,-52.2))
	c.spawn(ID=1,m=1,l=0,p=(-1.8,CRP,-35.7))
	c.spawn(ID=9,m=4,l=0,p=(1.2,CRP,-42.5))
	c.spawn(ID=13,m=4,l=2,p=(2.1,CRP,9))
	mt.bounce_twin(POS=(1,CRP,-36),CNT=1)
	mt.crate_row(ID=1,POS=(-1.3,.9,-22.3),CNT=5,WAY=0)
	c.spawn(ID=9,m=1,l=0,p=(-1.3,.9,-22.82))
	for aE in range(4):
		c.spawn(ID=13,m=1,l=0,p=(-.98+.32*aE,.9,-22.82))
	del aE
	mt.crate_row(ID=1,POS=(-1.3,.9,-27.5),CNT=3,WAY=0)
	mt.crate_row(ID=1,POS=(2.1,.8,1.1-.32),CNT=10,WAY=1)
	c.spawn(ID=4,p=(.9,CRP,-3.9))
	c.spawn(ID=3,m=1,l=0,p=(-2,CRP,-6))
	mt.crate_wall(ID=1,POS=(-1.09,CRP,17),CNT=[1,2])
	mt.bounce_twin(POS=(1.1,CRP,18),CNT=1)
	#checkpoints
	c.spawn(ID=6,p=(0,CRP,-46))
	c.spawn(ID=6,p=(.6,CRP,-17.8))
	c.spawn(ID=6,p=(0,CRP,11.1))
	#crates gem route
	c.spawn(ID=11,p=(208.7,1.4,-2))
	c.spawn(ID=7,p=(209.02,1.4,-2))
	c.spawn(ID=3,p=(215,2,-2))
	c.spawn(ID=3,p=(216,1.7,-2))
	c.spawn(ID=3,p=(217,1.4,-2))
	c.spawn(ID=11,p=(222,2,-2))
	c.spawn(ID=2,p=(223,2,-2))
	c.spawn(ID=1,p=(224,2,-2))
	c.spawn(ID=4,p=(225,2,-2))
	c.spawn(ID=1,p=(226,2,-2))
	c.spawn(ID=2,p=(227,2.5,-2))
	c.spawn(ID=3,p=(228,2.3,-2))
	c.spawn(ID=11,p=(229,2.1,-2))
	c.spawn(ID=1,p=(230,1.9,-2))
	mt.crate_row(ID=14,POS=(199.3,.66,-2),CNT=2,WAY=2)
	mt.crate_row(ID=2,POS=(202.2,1.16,-2),CNT=1,WAY=0)
	mt.crate_row(ID=4,POS=(208,2.9,-2),CNT=1,WAY=0)
	mt.crate_row(ID=1,POS=(213,2.3,-2),CNT=1,WAY=0)
	mt.crate_row(ID=13,POS=(211,2.88,-2),CNT=4,WAY=0,m=124,l=4)
	c.spawn(ID=9,p=(220.4,2.415,-2),m=124)
	c.spawn(ID=2,p=(231.9,2.7,-2))
	mt.crate_wall(ID=1,POS=(236.8,3.66,-2),CNT=[2,2])
	mt.bounce_twin(POS=(235.2,3.66,-2),CNT=1)
def load_wumpa():
	wu_h=1.3
	mt.wumpa_row(POS=(-.3,wu_h,-62.3),CNT=8,WAY=1)
	mt.wumpa_row(POS=(-.2,wu_h,-57),CNT=2,WAY=2)
	mt.wumpa_row(POS=(1.3,wu_h,-54),CNT=3,WAY=2)
	mt.wumpa_plane(POS=(0,wu_h,-50),CNT=[1,2])
	mt.wumpa_row(POS=(1.4,wu_h,-47.8),CNT=3,WAY=2)
	mt.wumpa_row(POS=(1.5,wu_h,-46.8),CNT=3,WAY=2)
	mt.wumpa_row(POS=(1.2,wu_h+.4,-42.5),CNT=3,WAY=2)
	mt.wumpa_row(POS=(0,wu_h,-44),CNT=2,WAY=2)
	mt.wumpa_row(POS=(0,wu_h,-40),CNT=2,WAY=2)
	mt.wumpa_plane(POS=(0,wu_h,-36.5),CNT=[1,2])
	mt.wumpa_row(POS=(-2,wu_h,-27),CNT=3,WAY=1)
	mt.wumpa_row(POS=(.6,wu_h,-22),CNT=3,WAY=1)
	mt.wumpa_plane(POS=(0,wu_h,-9),CNT=[1,2])
	mt.wumpa_plane(POS=(0,wu_h,-6),CNT=[1,2])
	mt.wumpa_plane(POS=(2,wu_h,-1.5),CNT=[1,2])
	mt.wumpa_plane(POS=(0,wu_h,16.7),CNT=[1,2])
def load_npc():
	n.spawn(ID=0,POS=(0,1.1,-52))
	n.spawn(ID=1,POS=(0,1.1,-36.3),DRC=2)
	n.spawn(ID=2,POS=(0,1.1,-15))
	
	bdh=1.2
	n.Bird(pos=(-.2,bdh,-57.1))
	n.Bird(pos=(-.6,bdh+.32,-48.7))
	n.Bird(pos=(-.12,bdh,-32))
	n.Bird(pos=(.1,bdh,-30))
	n.Bird(pos=(-2,bdh,-23.7))
	n.Bird(pos=(.6,bdh,-15.8))
	n.Bird(pos=(.1,bdh,-8.1))
	n.Bird(pos=(2.2,bdh,-2.1))
	n.Bird(pos=(1.1,bdh,8.9))
	n.Bird(pos=(-.3,bdh,18.8))
	n.Bird(pos=(.2,bdh,18.8))
	n.Bird(pos=(0,bdh,19.2))
	n.Bird(pos=(0,bdh,19.7))
	
	n.Butterfly(pos=(-.3,1,-59.1),typ=1,rng=1)
	n.Butterfly(pos=(-2,1.6,-26.6),typ=3,rng=1)
	n.Butterfly(pos=(-2,1.6,-.2),typ=5,rng=1)
	n.Butterfly(pos=(200,.8,-2.5),typ=4,rng=1)
	n.Butterfly(pos=(0,1.6,-4),typ=2,rng=1)
	n.spawn(ID=20,POS=(-1.8,1,.9),PTH=[(-2.2,1,.9),(-1.8,1,0),(-2.2,1,-.9),(-1.8,1,-1.8),(-2.2,1,-2.7),(-2,1,-3.6)])
	n.spawn(ID=20,POS=(-1.5,1,-36.1),PTH=[(-1.5,1,-36),(-1.5,1,-37)])

## bonus level / gem path
def bonus_zone():
	o.BonusPlatform(pos=(12,-36.2,U))
	o.ObjType_Water(pos=(0,-37.5,0),sca=(48,32),txs=(48*2,32*2),al=1,col=color.rgb32(180,180,180),rot=(0,0,0),spd=8)
	o.ObjType_Deco(ID=1,pos=(.3,-36.6,-1.75),sca=.018,rot=(-90,0,0))
	o.ObjType_Deco(ID=1,pos=(3.5,-36.5,-1.75),sca=.017,rot=(-90,0,0))
	o.ObjType_Deco(ID=1,pos=(6.6,-36.6,-1.75),sca=.018,rot=(-90,0,0))
	o.ObjType_Deco(ID=1,pos=(10.5,-36.5,-1.75),sca=.017,rot=(-90,0,0))
	for w in range(2):
		o.ObjType_Wall(ID=0,pos=(0+w*14,-37,2),ro_y=90,sca=.02,col=color.rgb32(160,190,160))
	del w
	for bbss in range(12):
		o.ObjType_Deco(ID=16,pos=(-1+bbss*1.6,-34.1,-2.8),sca=.001,rot=(-90,0,0),col=color.white,UL=True)
	bnh=-37
	o.spw_block(p=(.35,bnh,U),vx=[2,1],ID=0,sca=(.5,.5,.2))
	o.spw_block(p=(3,bnh,U),vx=[2,1],ID=0,sca=(.5,.5,.2))
	o.spw_block(p=(6,bnh,U),vx=[2,1],ID=0,sca=(.5,.5,.2))
	o.spw_block(p=(9,bnh,U),vx=[3,1],ID=0,sca=(.5,.5,.2))
	c.spawn(ID=8,p=(4,-36.5+.16,U))
	mt.crate_row(ID=1,POS=(4,-34,U),WAY=2,CNT=4)
	mt.crate_wall(ID=1,POS=(1,-36.5+.16,U),CNT=[1,3])
	mt.crate_wall(ID=2,POS=(6,-36.5+.16,U),CNT=[2,2])
	mt.bounce_twin(POS=(10.9,-36.5+.16,U),CNT=1)
	c.spawn(ID=4,p=(9,-36.5+.16,U))
	del bnh
	mt.wumpa_row(POS=(9,-36,U),CNT=4,WAY=2)
	mt.wumpa_row(POS=(9.4,-36.72,U),CNT=4,WAY=0)
	mt.wumpa_row(POS=(2,-36,U),CNT=3,WAY=0)
def gem_zone():
	o.ObjType_Water(pos=(220,-1,0),sca=(50,12),txs=(50*2,12*2),al=1,col=color.rgb32(190,190,190),rot=(0,0,0),spd=8)
	for w in range(4):
		o.ObjType_Wall(ID=0,pos=(195+w*14,1,1.5),ro_y=90,sca=.02)
	del w
	o.spw_block(ID=0,p=(199.5,0,-3),vx=[2,2])
	o.spw_block(ID=0,p=(202,.5,-2),vx=[1,1])
	o.spw_block(ID=0,p=(202,-.5,-2),vx=[1,1])
	o.spw_block(ID=0,p=(204,.5,-2),vx=[3,1])
	o.spw_block(ID=0,p=(204,-.5,-2),vx=[3,1])
	o.spw_block(ID=0,p=(208,1,-2),vx=[1,1])
	o.spw_block(ID=0,p=(208,0,-2),vx=[1,1])
	o.spw_block(ID=0,p=(210,2.2,-2),vx=[3,1])
	o.spw_block(ID=0,p=(210,1.2,-2),vx=[3,1])
	o.spw_block(ID=0,p=(210,0.2,-2),vx=[3,1])
	o.spw_block(ID=0,p=(214,1.7,-2),vx=[1,1])
	o.spw_block(ID=0,p=(214,0.7,-2),vx=[1,1])
	o.spw_block(ID=0,p=(218,1.75,-2),vx=[4,1])
	o.spw_block(ID=0,p=(218,0.75,-2),vx=[4,1])
	o.spw_block(ID=0,p=(231,2,-2),vx=[1,1])
	o.spw_block(ID=0,p=(231,1,-2),vx=[1,1])
	o.spw_block(ID=0,p=(231,0,-2),vx=[1,1])
	o.spw_block(ID=0,p=(233,2.5,-2),vx=[1,1])
	o.spw_block(ID=0,p=(233,1.5,-2),vx=[1,1])
	o.spw_block(ID=0,p=(233,0.5,-2),vx=[1,1])
	o.spw_block(ID=0,p=(234,3,-2),vx=[4,1])
	o.spw_block(ID=0,p=(234,2,-2),vx=[4,1])
	o.spw_block(ID=0,p=(234,1,-2),vx=[4,1])
	#deco
	o.ObjType_Deco(ID=14,pos=(200.7,.5,-3.3),col=color.white,sca=.085,rot=(-90,45,0))
	o.ObjType_Deco(ID=15,pos=(205,1,-1.7),col=color.white,sca=.085,rot=(-90,45,0))
	o.ObjType_Deco(ID=15,pos=(234,3.5,-1.7),col=color.white,sca=.085,rot=(-90,45,0))
	o.ObjType_Deco(ID=14,pos=(235,3.5,-1.7),col=color.white,sca=.085,rot=(-90,45,0))
	o.ObjType_Deco(ID=1,pos=(210.6,2.8,-1),sca=.0175,rot=(-90,0,0))
	o.ObjType_Deco(ID=1,pos=(219.2,2.3,-1),sca=.0175,rot=(-90,0,0))
	o.ObjType_Deco(ID=1,pos=(236.2,3.8,-1),sca=.0175,rot=(-90,0,0))
	#npc
	n.spawn(ID=0,POS=(204.9,1,-2))
	n.spawn(ID=0,POS=(214,2.2,-2),RNG=.2)
	n.spawn(ID=2,POS=(218.9,2.3,-2),RNG=.5)
	n.spawn(ID=2,POS=(233,3,-2),RNG=.4)
	#wumpa
	mt.wumpa_row(POS=(199.8,.70,-2),CNT=4,WAY=0)
	mt.wumpa_row(POS=(209,1.8,-2),CNT=4,WAY=2)
	mt.wumpa_row(POS=(230.6,2.7,-2),CNT=3,WAY=0)
	mt.wumpa_row(POS=(233.7,3.7,-2),CNT=4,WAY=0)
	o.GemPlatform(pos=(237.8,3.75,-2),t=GEM_VNUM)