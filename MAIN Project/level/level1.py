import settings,objects,map_tools,crate,npc,status,_loc,sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ursina import *

st=status
mt=map_tools
o=objects
LC=_loc
c=crate
n=npc
U=-3

def map_setting():
	LC.LV_DST=(10,15)
	LC.BN_DST=(6,12)
	window.color=color.rgb32(0,60,80)
	scene.fog_density=(10,15)
	scene.fog_color=color.rgb32(20,70,50)
	LC.AMBIENT_LIGHT.color=color.rgb32(140,140,140)
	st.toggle_thunder=False
	st.toggle_rain=True

def start_load():
	load_crate()
	bonus_zone()
	if 4 in st.COLOR_GEM or settings.debg:
		gem_zone()
	load_object()
	load_wumpa()
	load_npc()
	map_setting()

def load_object():
	o.StartRoom(pos=(-.3,1,-66.5))
	TS=16
	cG=color.green
	o.Water(pos=(0,.6,-16),sca=(10,96),c=color.rgb32(70,90,100),a=1)
	o.InvWall(pos=(-5,.5,-32),sca=(5.,10,128))
	o.InvWall(pos=(5.3,.5,-32),sca=(5.,10,128))
	o.BonusPlatform(pos=(1.1,1.2,-6))
	o.GemPlatform(pos=(-.3,1.2,-18),t=4)
	gs=1.6
	o.GrassSide(pos=(-4,gs,-47),m=False)
	o.GrassSide(pos=(-4,gs,-16),m=False)
	o.GrassSide(pos=(-4,gs,15),m=False)
	o.GrassSide(pos=(-4,gs,46),m=False)
	o.GrassSide(pos=(4,gs,-47),m=True)
	o.GrassSide(pos=(4,gs,-16),m=True)
	o.GrassSide(pos=(4,gs,15),m=True)
	o.GrassSide(pos=(4,gs,46),m=True)
	o.WoodScene(pos=(0,0,128))
	o.WoodScene(pos=(0,-20,127))
	#plants
	Entity(model='cube',texture='res/terrain/l1/bricks.png',scale=(9,2,.3),position=(0,-.2,-64.5),texture_scale=(9,2))
	o.TreeScene(pos=(-1.2,1.2,-46),sca=.0175)
	o.TreeScene(pos=(0,1.7,-26.4),sca=.0175)
	for trw in range(8):
		o.TreeRow(pos=(-4.3,1.2,-60+trw*12),sca=(.15,.16,.18))
		o.TreeRow(pos=(4.3,1.2,-60+trw*12),sca=(.15,.16,.18))
	del trw
	o.TreeScene(pos=(-1.5,1.2,20.3),sca=.0175)
	o.TreeScene(pos=(1.2,1.2,20.3),sca=.0175)
	o.TreeScene(pos=(1.1,1.5,11),sca=.0175)
	o.TreeScene(pos=(.5,1.3,2.5),sca=.0175)
	o.TreeScene(pos=(0,1,-2),sca=.013)
	o.TreeScene(pos=(0,1,6),sca=.013)
	o.TreeScene(pos=(1,1.6,-34.6),sca=.02)
	o.TreeScene(pos=(-1.8,1.5,-21.5),sca=.02)
	o.TreeScene(pos=(-1.5,1.2,-62.5),sca=.02)
	o.TreeScene(pos=(1.1,1.5,-53),sca=.02)
	#platform
	dz=-64
	dy=.5
	o.spw_block(ID=1,p=(-.25,dy,dz),vx=[1,6])
	o.spw_block(ID=1,p=(-1,dy,dz+7),vx=[2,2])
	o.spw_block(ID=1,p=(0,dy,dz+10),vx=[1,1])
	o.spw_block(ID=1,p=(-1,dy,dz+12),vx=[3,1])
	o.spw_block(ID=1,p=(0,dy,dz+14),vx=[1,5])
	o.spw_block(ID=1,p=(0,dy,dz+26),vx=[1,5])
	o.spw_block(ID=1,p=(0,dy,dz+32),vx=[1,1])
	o.spw_block(ID=1,p=(0,dy,dz+34),vx=[1,1])
	o.spw_block(ID=1,p=(0,dy,dz+36),vx=[1,2])
	o.spw_block(ID=1,p=(-2,dy,dz+36.5),vx=[1,6])
	o.spw_block(ID=1,p=(.7,dy,dz+41),vx=[1,6])
	o.spw_block(ID=1,p=(-1,dy,dz+48),vx=[3,5])
	o.spw_block(ID=1,p=(0,dy,dz+53),vx=[1,7])
	o.spw_block(ID=1,p=(-2,dy,dz+60),vx=[5,1])
	o.spw_block(ID=1,p=(-2,dy,dz+61),vx=[1,5])
	o.spw_block(ID=1,p=(-2,dy,dz+68),vx=[1,4])
	o.spw_block(ID=1,p=(+2,dy,dz+61),vx=[1,4])
	o.spw_block(ID=1,p=(+2,dy,dz+68+.32),vx=[1,2])
	o.spw_block(ID=1,p=(+2,dy,dz+72),vx=[1,1])
	o.spw_block(ID=1,p=(-2,dy,dz+73),vx=[5,1])
	o.spw_block(ID=1,p=(0,dy,dz+74),vx=[1,2])
	o.spw_block(ID=1,p=(0,dy,dz+81),vx=[1,2])
	o.spw_block(ID=1,p=(0,dy,dz+83),vx=[1,3])
	o.MossPlatform(p=(0,.5,-44),ptm=0)
	o.MossPlatform(p=(0,.5,-42),ptm=0)
	o.MossPlatform(p=(0,.5,-40),ptm=0)
	o.MossPlatform(p=(-2,.5,-6),ptm=0)
	o.MossPlatform(p=(0,.5,13.5),ptm=0)
	o.MossPlatform(p=(0,.5,15),ptm=0)
	o.Corridor(pos=(0,1,-13))
	o.Bush(pos=(-1.3,1.2,-14.2),sca=(2,1))
	o.Bush(pos=(1.3,1.2,-14.2),sca=(2,1))
	o.EndRoom(pos=(1,2.4,26.2),c=color.rgb32(160,180,160))
def load_crate():
	CRP=1.16
	if not 4 in st.COLOR_GEM:
		c.place_crate(ID=16,p=(-1.1,CRP,-57))
	mt.crate_plane(ID=2,POS=(-1.8,CRP,3.3),CNT=[2,1])
	mt.crate_wall(ID=14,POS=(-1.3,1.14,8.8),CNT=[2,2])
	mt.crate_plane(ID=1,POS=(-1.5,CRP,-2.5),CNT=[1,3])
	mt.crate_wall(ID=14,POS=(-.7,CRP,-56.1),CNT=[1,2])
	mt.crate_wall(ID=1,POS=(-1,CRP,-49),CNT=[2,1])
	c.place_crate(ID=5,p=(0,CRP,-54))
	mt.bounce_twin(POS=(1,CRP,-36),CNT=1)
	mt.crate_row(ID=1,POS=(-1.3,.9,-22.3),CNT=5,WAY=0)
	c.place_crate(ID=9,m=1,l=0,p=(-1.3,.9,-22.82))
	for aE in range(4):
		c.place_crate(ID=13,m=1,l=0,p=(-.98+.32*aE,.9,-22.82))
	del aE
	mt.crate_row(ID=1,POS=(-1.3,.9,-27.5),CNT=3,WAY=0)
	mt.crate_row(ID=1,POS=(2.1,.8,1.1-.32),CNT=10,WAY=1)
	c.place_crate(ID=4,p=(.9,CRP,-3.9))
	c.place_crate(ID=3,m=1,l=0,p=(-2,CRP,-6))
	mt.crate_wall(ID=1,POS=(-1.09,CRP,17),CNT=[1,2])
	mt.bounce_twin(POS=(1.1,CRP,18),CNT=1)
	#checkpoints
	c.place_crate(ID=6,p=(0,CRP,-46))
	c.place_crate(ID=6,p=(.6,CRP,-17.8))
	c.place_crate(ID=6,p=(0,CRP,11.1))
	#crates gem route
	c.place_crate(ID=11,p=(208.7,1.4,-2))
	c.place_crate(ID=7,p=(209.02,1.4,-2))
	c.place_crate(ID=3,p=(215,2,-2))
	c.place_crate(ID=3,p=(216,1.7,-2))
	c.place_crate(ID=3,p=(217,1.4,-2))
	c.place_crate(ID=11,p=(222,2,-2))
	c.place_crate(ID=2,p=(223,2,-2))
	c.place_crate(ID=1,p=(224,2,-2))
	c.place_crate(ID=4,p=(225,2,-2))
	c.place_crate(ID=1,p=(226,2,-2))
	c.place_crate(ID=2,p=(227,2.5,-2))
	c.place_crate(ID=3,p=(228,2.3,-2))
	c.place_crate(ID=11,p=(229,2.1,-2))
	c.place_crate(ID=1,p=(230,1.9,-2))
	mt.crate_row(ID=14,POS=(199.3,.66,-2),CNT=2,WAY=2)
	mt.crate_row(ID=2,POS=(202.2,1.16,-2),CNT=1,WAY=0)
	mt.crate_row(ID=4,POS=(208,2.9,-2),CNT=1,WAY=0)
	mt.crate_row(ID=1,POS=(213,2.3,-2),CNT=1,WAY=0)
	mt.crate_row(ID=13,POS=(211,2.88,-2),CNT=4,WAY=0,m=124,l=4)
	c.place_crate(ID=9,p=(220.4,2.415,-2),m=124)
	c.place_crate(ID=2,p=(231.9,2.7,-2))
	mt.crate_wall(ID=1,POS=(236.8,3.66,-2),CNT=[2,2])
	mt.bounce_twin(POS=(235.2,3.66,-2),CNT=1)
def load_wumpa():
	wu_h=1.3
	mt.wumpa_row(POS=(-.2,wu_h,-57),CNT=2,WAY=2)
	mt.wumpa_plane(POS=(0,wu_h,-50),CNT=[1,2])
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

## bonus level / gem path
def bonus_zone():
	o.BonusPlatform(pos=(12,-36.2,U))
	o.Water(pos=(0,-37.5,0),sca=(48,32),c=color.rgb32(80,80,120),a=1)
	o.TreeScene(pos=(.3,-36.6,-1.5),sca=.018)
	o.TreeScene(pos=(3.5,-36.5,-1.5),sca=.017)
	o.TreeScene(pos=(6.6,-36.6,-1.5),sca=.018)
	o.TreeScene(pos=(10.5,-36.5,-1.5),sca=.017)
	for w in range(2):
		o.BackgroundWall(p=(0+w*14,-37,2))
	del w
	bnh=-37
	o.spw_block(p=(.35,bnh,U),vx=[2,1],sca=(.5,.75,.1),ID=1)
	o.spw_block(p=(3,bnh,U),vx=[2,1],sca=(.5,.75,.1),ID=1)
	o.spw_block(p=(6,bnh,U),vx=[2,1],sca=(.5,.75,.1),ID=1)
	o.spw_block(p=(9,bnh,U),vx=[3,1],sca=(.5,.75,.1),ID=1)
	c.place_crate(ID=8,p=(4,-36.5+.16,U))
	mt.crate_row(ID=1,POS=(4,-34,U),WAY=2,CNT=4)
	mt.crate_wall(ID=1,POS=(1,-36.5+.16,U),CNT=[1,3])
	mt.crate_wall(ID=2,POS=(6,-36.5+.16,U),CNT=[2,2])
	mt.bounce_twin(POS=(10.9,-36.5+.16,U),CNT=1)
	c.place_crate(ID=4,p=(9,-36.5+.16,U))
	del bnh
	mt.wumpa_row(POS=(9,-36,U),CNT=4,WAY=2)
	mt.wumpa_row(POS=(9.4,-36.72,U),CNT=4,WAY=0)
	mt.wumpa_row(POS=(2,-36,U),CNT=3,WAY=0)
def gem_zone():
	o.Water(pos=(220,-1,0),sca=(50,12),c=color.rgb32(70,70,100),a=1)
	for w in range(4):
		o.BackgroundWall(p=(195+w*14,1,1.5))
	del w
	o.spw_block(ID=1,p=(199.5,0,-3),vx=[2,2],sca=(.5,.5,.3))
	o.spw_block(ID=1,p=(202,.5,-2),vx=[1,1],sca=(.5,.5,.3))
	o.spw_block(ID=1,p=(204,.5,-2),vx=[3,1],sca=(.5,.5,.3))
	o.spw_block(ID=1,p=(208,1,-2),vx=[1,1],sca=(.5,.5,.3))
	o.spw_block(ID=1,p=(210,2.2,-2),vx=[3,1],sca=(.5,.5,.3))
	o.spw_block(ID=1,p=(214,1.7,-2),vx=[1,1],sca=(.5,.5,.3))
	o.spw_block(ID=1,p=(218,1.75,-2),vx=[4,1],sca=(.5,.5,.3))
	o.spw_block(ID=1,p=(231,2,-2),vx=[1,1],sca=(.5,.5,.3))
	o.spw_block(ID=1,p=(233,2.5,-2),vx=[1,1],sca=(.5,.5,.3))
	o.spw_block(ID=1,p=(234,3,-2),vx=[4,1],sca=(.5,.5,.3))
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
	o.GemPlatform(pos=(237.8,3.75,-2),t=4)