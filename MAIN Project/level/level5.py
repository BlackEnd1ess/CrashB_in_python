import settings,objects,map_tools,crate,npc,status,item,random,_loc,sys,os,danger
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from ursina import *

mt=map_tools
st=status
dg=danger
o=objects
LC=_loc
r=random
c=crate
n=npc
U=-3

def map_setting():
	LC.FOG_L_COLOR=color.black
	LC.FOG_B_COLOR=color.black
	LC.SKY_BG_COLOR=color.black
	LC.AMB_M_COLOR=color.rgb32(140,140,160)
	LC.LV_DST=(8,15)
	LC.BN_DST=(10,20)
	st.toggle_thunder=True
	st.toggle_rain=True

def start_load():
	load_crate()
	bonus_zone()
	if 5 in st.COLOR_GEM or settings.debg:
		gem_zone()
	load_object()
	load_wumpa()
	load_npc()
	map_setting()

def load_object():
	blh=.2
	o.StartRoom(pos=(0,0,-64.2))
	o.BonusPlatform(pos=(9+.75*6,.5,-22))
	o.GemPlatform(pos=(16.9,.4,-.1),t=2)
	dg.FallingZone(pos=(0,-2,0),s=(150,.3,128))
	o.ObjType_Background(ID=3,sca=(800,120),pos=(50,-38,128),col=color.rgb32(160,160,170),txa=(2,1),UL=True)
	o.ObjType_Floor(ID=5,pos=(0,blh,-56),sca=(.03,.03,.03),rot=(0,-90,0))
	o.ObjType_Floor(ID=5,pos=(5.4,blh,-56),sca=(.03,.03,-.03),rot=(0,-90,0))
	o.spw_block(ID=4,p=(0,blh,-61),vx=[1,3])
	o.spw_block(ID=4,p=(0,blh,-61+.75*5),vx=[1,1])
	o.spw_block(ID=4,p=(1.2,blh,-56),vx=[1,1])
	o.spw_block(ID=4,p=(1.2+.75*2,blh,-56),vx=[1,1])
	o.spw_block(ID=4,p=(1.2+.75*4,blh,-56),vx=[1,1])
	o.spw_block(ID=4,p=(1.2+.75*2,blh,-55.25),vx=[1,2])
	o.spw_block(ID=4,p=(1.2+.75*2,blh,-55.25+.75*4),vx=[1,1])
	o.spw_block(ID=4,p=(1.2+.75*2,blh,-50.5),vx=[1,1])
	o.ObjType_Corridor(ID=1,pos=(2.7,blh-.5,-47),rot=(0,0,0))
	o.spw_block(ID=4,p=(1.2+.75*2,blh,-44),vx=[1,1])
	o.spw_block(ID=4,p=(1.2+.75*2,blh,-44+.75*2),vx=[1,1])
	o.spw_block(ID=4,p=(1.2+.75*2,blh,-44+.75*4),vx=[1,1])
	o.spw_block(ID=4,p=(1.2+.75*2,blh,-44+.75*6),vx=[1,1])
	o.spw_block(ID=4,p=(1.2+.75*1,blh,-44+.75*7),vx=[3,1])
	o.spw_block(ID=4,p=(1.2+.75*2,blh,-44+.75*9),vx=[1,1])
	o.spw_block(ID=4,p=(1.2+.75*2,blh,-44+.75*11),vx=[1,1])
	o.ObjType_Floor(ID=5,pos=(2.7,blh,-33),sca=(.03,.03,.03),rot=(0,-90,0))
	o.LoosePlatform(pos=(5,.2,-33),t=0)
	o.LoosePlatform(pos=(6.5,.2,-33),t=0)
	o.LoosePlatform(pos=(8,.2,-33),t=0)
	o.spw_block(ID=4,p=(9,blh,-33),vx=[2,1])
	o.spw_block(ID=4,p=(9+.75*4,blh,-33),vx=[1,3])
	o.ObjType_Corridor(ID=1,pos=(12,blh-.5,-28.5),rot=(0,0,0))
	o.spw_block(ID=4,p=(9+.75*4,blh,-25),vx=[1,1])
	o.spw_block(ID=4,p=(9+.75*4,blh,-23.5),vx=[1,1])
	o.spw_block(ID=4,p=(9+.75*4,blh,-22),vx=[3,1])
	o.spw_block(ID=4,p=(9+.75*4,blh,-20.5),vx=[1,1])
	o.LoosePlatform(pos=(9+.75*4,.2,-19),t=0)
	o.LoosePlatform(pos=(9+.75*4,.2,-17.5),t=0)
	o.LoosePlatform(pos=(9+.75*4,.2,-16),t=0)
	o.ObjType_Corridor(ID=1,pos=(12,blh-.5,-13),rot=(0,0,0))
	o.ObjType_Corridor(ID=1,pos=(12,blh-.5,-10),rot=(0,0,0))
	o.spw_block(ID=4,p=(9+.75*4,blh,-8.1),vx=[1,1])
	o.ObjType_Floor(ID=5,pos=(12,blh,-6.9),sca=(.03,.03,.03),rot=(0,-90,0))
	o.spw_block(ID=4,p=(13.2,blh,-7),vx=[1,4])
	o.spw_block(ID=4,p=(13.2,blh,-7+.75*5.5),vx=[1,1])
	o.spw_block(ID=4,p=(13.2,blh,-7+.75*8),vx=[1,1])
	o.spw_block(ID=4,p=(14.7,blh,-7+.75*8),vx=[2,1])
	o.spw_block(ID=4,p=(14.7+.75*3,blh,-7+.75*8),vx=[2,1])
	o.LoosePlatform(pos=(19,.2,-1),t=0)
	o.LoosePlatform(pos=(20.5,.2,-1),t=0)
	o.spw_block(ID=4,p=(22,blh,-7+.75*8),vx=[4,1])
	o.spw_block(ID=4,p=(22+.75*4,blh,-7+.75*8),vx=[1,2])
	o.spw_block(ID=4,p=(22+.75*4,blh,-7+.75*11),vx=[1,1])
	o.spw_block(ID=4,p=(22+.75*4,blh,-7+.75*13),vx=[1,1])
	o.spw_block(ID=4,p=(22+.75*6,blh,-7+.75*8),vx=[1,1])
	o.spw_block(ID=4,p=(22+.75*8,blh,-7+.75*8),vx=[1,1])
	o.ObjType_Floor(ID=5,pos=(25,blh,4.65),sca=(.03,.03,.03),rot=(0,-90,0))
	o.ObjType_Floor(ID=5,pos=(29.95,blh,-7+.75*8),sca=(.03,.03,-.03),rot=(0,-90,0))
	for lp0 in range(3):
		o.LoosePlatform(pos=(26.6+lp0,.3+lp0/3,4.7),t=1)
	blk=1.1
	o.spw_block(ID=4,p=(30,blk,4.7),vx=[1,1])
	o.spw_block(ID=4,p=(30+.75*2,blk,4.7),vx=[1,1])
	o.spw_block(ID=4,p=(30+.75*4,blk,4.7),vx=[1,1])
	o.spw_block(ID=4,p=(30+.75*6,blk,4.7),vx=[1,1])
	o.spw_block(ID=4,p=(30+.75*6,blk,4.7+.75*2),vx=[1,1])
	o.spw_block(ID=4,p=(30+.75*6,blk,4.7+.75*4),vx=[1,1])
	o.spw_block(ID=4,p=(30+.75*6,blk,4.7+.75*5),vx=[2,1])
	o.spw_block(ID=4,p=(30+.75*10,blk,4.7+.75*5),vx=[3,1])
	o.spw_block(ID=4,p=(30+.75*12,blk,4.7),vx=[1,1])
	o.spw_block(ID=4,p=(30+.75*12,blk,4.7+.75*2),vx=[1,1])
	o.spw_block(ID=4,p=(30+.75*12,blk,4.7+.75*4),vx=[1,1])
	o.spw_block(ID=4,p=(30+.75*14,-.2+.5,4.7),vx=[1,1])
	o.spw_block(ID=4,p=(30+.75*16,-1+.5,4.7),vx=[1,1])
	o.spw_block(ID=4,p=(30+.75*18,-1+.5,4.7),vx=[1,1])
	o.spw_block(ID=4,p=(30+.75*20,-1+.5,4.7),vx=[1,1])
	o.spw_block(ID=4,p=(30+.75*22,-1+.5,4.7),vx=[1,1])
	o.spw_block(ID=4,p=(30+.75*24,-.6+.5,4.7),vx=[1,1])
	o.spw_block(ID=4,p=(30+.75*25,-.2+.5,4.7),vx=[1,1])
	o.spw_block(ID=4,p=(30+.75*25,.2+.5,4.7+.75),vx=[1,1])
	o.spw_block(ID=4,p=(30+.75*26,blk,4.7+.75),vx=[1,1])
	o.spw_block(ID=4,p=(30+.75*28,blk,4.7+.75),vx=[1,1])
	o.spw_block(ID=4,p=(30+.75*30,blk,4.7+.75),vx=[1,1])
	o.ObjType_Floor(ID=5,pos=(35.5,blk,9.6),sca=(.03,.03,.03),rot=(0,-90,0))
	o.ObjType_Floor(ID=5,pos=(37.175,blk-.001,9.6),sca=(.03,.03,-.03),rot=(0,-90,0))
	o.spw_block(ID=4,p=(30+.75*31,blk,4.7+.75),vx=[1,1])
	o.spw_block(ID=4,p=(30+.75*31,blk,4.7+.75*3),vx=[1,1])
	o.spw_block(ID=4,p=(30+.75*31,blk,4.7+.75*5),vx=[1,1])
	o.LoosePlatform(pos=(53.2,1,9.6),t=0)
	o.LoosePlatform(pos=(53.2,1,11.1),t=0)
	o.LoosePlatform(pos=(53.2,1,12.6),t=0)
	o.LoosePlatform(pos=(53.2,1,14.1),t=0)
	o.spw_block(ID=4,p=(52.45,blk,15.75),vx=[3,2])
	o.spw_block(ID=4,p=(53.2-.75,blk,15+.75*3),vx=[1,1])
	o.spw_block(ID=4,p=(53.2-.75,blk,15+.75*5),vx=[1,1])
	o.spw_block(ID=4,p=(53.2-.75,blk,15+.75*7),vx=[1,1])
	o.spw_block(ID=4,p=(53.2-.75,blk,15+.75*8),vx=[1,1])
	o.spw_block(ID=4,p=(53.2-.75+.75*2,blk,15+.75*8),vx=[1,1])
	o.spw_block(ID=4,p=(53.2-.75+.75*4,blk,15+.75*8),vx=[1,1])
	o.spw_block(ID=4,p=(53.2+.75*3,blk,15+.75*8),vx=[1,1])
	o.spw_block(ID=4,p=(53.2+.75*3,blk,15+.75*10),vx=[1,1])
	o.spw_block(ID=4,p=(53.2+.75*3,blk,15+.75*12),vx=[1,4])
	o.spw_block(ID=4,p=(53.2+.75*4,blk,15+.75*13),vx=[1,1])
	#red gem path
	o.spw_block(ID=4,p=(42.75,-.5,-1.4),vx=[3,3])
	#all gem path
	o.spw_block(ID=4,p=(59.5,blk,15.75),vx=[3,2])
	#sculpts
	dg.MonkeySculpture(pos=(3.8,.2,-55),r=True,d=False)
	dg.MonkeySculpture(pos=(1.7,.3,-42.4),r=False,d=True,ro_y=-90)
	dg.MonkeySculpture(pos=(4,.3,-41.4),r=False,d=True,ro_y=90)
	dg.MonkeySculpture(pos=(9.7,.3,-32),r=False,d=True,ro_y=0)
	dg.MonkeySculpture(pos=(11,.3,-25),r=False,d=True,ro_y=-90)
	dg.MonkeySculpture(pos=(26.5,.3,0),r=False,d=True,ro_y=0)
	dg.MonkeySculpture(pos=(28,.3,0),r=False,d=True,ro_y=0)
	dg.MonkeySculpture(pos=(42.7,-.5,5.5),r=False,d=True,ro_y=0)
	dg.MonkeySculpture(pos=(44.2,-.5,5.5),r=False,d=True,ro_y=0)
	dg.MonkeySculpture(pos=(45.7,-.5,5.5),r=False,d=True,ro_y=0)
	dg.MonkeySculpture(pos=(47.2,-.5,5.5),r=False,d=True,ro_y=0)
	dg.MonkeySculpture(pos=(51.4,1.1,17.2),r=False,d=True,ro_y=-90)
	dg.MonkeySculpture(pos=(53.4,1.1,18.7),r=False,d=True,ro_y=90)
	dg.MonkeySculpture(pos=(51.4,1.1,20.2),r=False,d=True,ro_y=-90)
	#pseudo gem pltf
	o.PseudoGemPlatform(pos=(43.5,-.52,3.5),t=1)
	o.PseudoGemPlatform(pos=(43.5,-.52,2),t=1)
	o.PseudoGemPlatform(pos=(55.1,1.1,15.7),t=3)
	o.PseudoGemPlatform(pos=(56.6,1.1,15.7),t=3)
	o.PseudoGemPlatform(pos=(58.1,1.1,15.7),t=3)
	# background objects
	ccw=color.white
	sk=.03
	o.ObjType_Wall(ID=3,pos=(-3,-1,-58),ro_y=30,sca=sk)
	o.ObjType_Wall(ID=3,pos=(5,-1,-52),ro_y=40,sca=sk)
	o.ObjType_Wall(ID=3,pos=(0,-1,-52),ro_y=0,sca=sk)
	o.ObjType_Wall(ID=3,pos=(0,-1,-50),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(.5,-.8,-43),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(0,-1,-41),ro_y=0,sca=sk)
	o.ObjType_Wall(ID=3,pos=(0,-1,-38),ro_y=0,sca=sk)
	o.ObjType_Wall(ID=3,pos=(4.7,-.8,-42),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(4.5,-1,-40),ro_y=180,sca=sk)
	o.ObjType_Wall(ID=3,pos=(4,-1,-38),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(5,-1,-35),ro_y=180,sca=sk)
	o.ObjType_Wall(ID=3,pos=(.5,-.8,-35),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(0,-1,-32),ro_y=0,sca=sk)
	o.ObjType_Wall(ID=3,pos=(0,-1,-29),ro_y=0,sca=sk)
	o.ObjType_Wall(ID=3,pos=(2,-.8,-29),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(5,-.7,-31),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(10,-.7,-20),ro_y=0,sca=sk)
	o.ObjType_Wall(ID=3,pos=(8,-.8,-29),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(11,-1,-31),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(10,-.8,-12),ro_y=0,sca=sk)
	o.ObjType_Wall(ID=3,pos=(9.5,-.8,-6),ro_y=0,sca=sk)
	o.ObjType_Wall(ID=3,pos=(11,-.8,0),ro_y=0,sca=sk)
	o.ObjType_Wall(ID=3,pos=(11.5,-.8,4),ro_y=0,sca=sk)
	o.ObjType_Wall(ID=3,pos=(13,-.8,2),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(16,-.7,4),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(19,-.8,2),ro_y=90,sca=sk)
	o.ObjType_Scene(ID=9,pos=(23,-1,7),ro_y=-70,sca=.08)
	o.ObjType_Wall(ID=3,pos=(26,-.7,8),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(29,-.7,10),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(31,0,9),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(32,0,8),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(33,.3,12),ro_y=0,sca=sk)
	o.ObjType_Wall(ID=3,pos=(36,-.5,7.3),ro_y=90,sca=sk)
	####o.RuinRuins(pos=(37.5,-.6,7),ro_y=45,typ=1)
	o.ObjType_Scene(ID=9,pos=(48,-.8,-4),ro_y=100,sca=.08)
	o.ObjType_Scene(ID=9,pos=(40,-.8,-3.5),ro_y=-100,sca=.08)
	o.ObjType_Wall(ID=3,pos=(36,.6,12),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(39,.6,14),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(42,.6,10),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(41,-.6,7),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(44,-.7,9),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(47,-.3,7),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(52,0,24),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(53.5,.4,26),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(57,.45,26),ro_y=90,sca=sk)
	o.ObjType_Scene(ID=9,pos=(50,0,16),ro_y=-90,sca=.08,col=ccw)
	o.ObjType_Scene(ID=9,pos=(51,.4,31),ro_y=-70,sca=.08,col=ccw)
	o.ObjType_Scene(ID=9,pos=(56,0,9),ro_y=90,sca=.08,col=ccw)
	o.ObjType_Scene(ID=9,pos=(58,0,24),ro_y=90,sca=.08,col=ccw)
	o.ObjType_Scene(ID=9,pos=(-3.5,-1,-54),ro_y=-90,sca=.08,col=ccw)
	o.ObjType_Scene(ID=9,pos=(8.5,-.6,-53),ro_y=70,sca=.08,col=ccw)
	o.ObjType_Scene(ID=9,pos=(-1,-1,-40),ro_y=90,sca=.08,col=ccw)
	o.ObjType_Scene(ID=9,pos=(9,-.8,-24),ro_y=-90,sca=.08,col=ccw)
	o.ObjType_Scene(ID=9,pos=(16,-.8,-24),ro_y=90,sca=.08,col=ccw)
	o.ObjType_Scene(ID=9,pos=(16,-.8,-9),ro_y=90,sca=.08,col=ccw)
	o.ObjType_Scene(ID=9,pos=(9,-1,-9),ro_y=90,sca=.08,col=ccw)
	o.EndRoom(pos=(56.5,2.8,31.6),c=color.rgb32(180,200,200))
	del sk
def load_crate():
	mt.crate_row(ID=4,POS=(5.3+.32,.36,-56),CNT=1,WAY=2)
	mt.crate_wall(ID=1,POS=(.3,.36,-55.6),CNT=[2,1])
	mt.crate_wall(ID=1,POS=(3.2,.36,-46.0),CNT=[1,2])
	mt.crate_wall(ID=1,POS=(11.4,.36,-27.4),CNT=[1,2])
	mt.crate_wall(ID=1,POS=(11.2,.36,-11.9),CNT=[2,2])
	mt.crate_wall(ID=1,POS=(12.6,.36,-9.1),CNT=[1,2])
	mt.crate_wall(ID=1,POS=(24.6,.36,5),CNT=[1,2])
	c.place_crate(ID=12,p=(-.2,.36,-55.6))
	c.place_crate(ID=12,p=(3.5,.36,-55.9))
	c.place_crate(ID=12,p=(3.3,.36,-47.5))
	c.place_crate(ID=12,p=(1.9,.36,-47.5))
	c.place_crate(ID=12,p=(1.9,.36,-46))
	c.place_crate(ID=12,p=(5.6,.36,-33.1))
	c.place_crate(ID=12,p=(2.5,.36,-37.2))
	c.place_crate(ID=12,p=(7.5,.36,-33))
	c.place_crate(ID=12,p=(11.3,.36,-11.5))
	c.place_crate(ID=12,p=(11.1,.36,-13.7))
	c.place_crate(ID=12,p=(12.6,.36,-13.7))
	c.place_crate(ID=12,p=(15.4,.36,-1))
	c.place_crate(ID=10,p=(56.2,1.26,24.7))
	mt.crate_plane(ID=1,POS=(1.6,0,-35.7),CNT=[2,2])
	mt.crate_plane(ID=2,POS=(35.6,1.26,9.5),CNT=[2,2])
	mt.crate_row(ID=1,POS=(52.4,1.26,15.7),CNT=3,WAY=0)
	mt.crate_block(ID=2,POS=(29.8,.36,-1),CNT=[2,2,1])
	mt.crate_wall(ID=14,POS=(37.1,1.26,9.6),CNT=[1,3])
	mt.crate_wall(ID=1,POS=(43.5,-.34,4.7),CNT=[1,2])
	c.place_crate(ID=4,p=(11.6,.36,-33.1))
	mt.bounce_twin(POS=(2.3,.36,-33.1),CNT=1)
	mt.bounce_twin(POS=(38.3,1.26,8.4),CNT=1)
	mt.bounce_twin(POS=(53.9,1.26,16.5),CNT=1)
	c.place_crate(ID=3,p=(11.4,.36,-20.6))
	c.place_crate(ID=3,p=(19.7,.36,-1))
	c.place_crate(ID=11,p=(52.5,1.26,5.4))
	c.place_crate(ID=11,p=(27.7,.84,4.6))
	c.place_crate(ID=11,p=(26.6,.3+.16,4.6))
	c.place_crate(ID=7,p=(43,-.5+.16,-1))
	c.place_crate(ID=9,p=(43,1.6,-1),m=102)
	for ffc_x in range(5):
		for ffc_z in range(2):
			c.place_crate(ID=13,p=(59.6+.32*ffc_x,1.1+.16,16+.32*ffc_z),m=102,l=r.choice([1,2,7]))
	mt.crate_plane(ID=2,POS=(44,-.5+.16,-1.5),CNT=[2,2])
	#aku
	c.place_crate(ID=5,p=(4.8,.36,-56))
	c.place_crate(ID=5,p=(13.1,.36,-5.5))
	#checkpoints
	c.place_crate(ID=6,p=(11.9,.36,-28.6))
	c.place_crate(ID=6,p=(25.4,.36,4.5))
	c.place_crate(ID=6,p=(40.5,.3+.16,4.6))
	if not 3 in status.COLOR_GEM:
		c.place_crate(ID=16,p=(-.4,.36,-56.4))
def load_wumpa():
	mt.wumpa_row(POS=(0,.5,-60.3),CNT=3,WAY=1)
	mt.wumpa_row(POS=(2.7,.5,-55.3),CNT=3,WAY=1)
	mt.wumpa_row(POS=(2.7,.5,-44),CNT=3,WAY=1)
	mt.wumpa_row(POS=(12,.5,-32.3),CNT=3,WAY=1)
	mt.wumpa_row(POS=(25,.5,-0.4),CNT=3,WAY=1)
	mt.wumpa_row(POS=(34.5,1.4,5.3),CNT=3,WAY=1)
	mt.wumpa_row(POS=(39,1.4,4.7),CNT=3,WAY=1)
	mt.wumpa_row(POS=(53.2,1.4,5.4),CNT=3,WAY=1)
	mt.wumpa_row(POS=(52.4,1.4,16.6),CNT=3,WAY=1)
	mt.wumpa_row(POS=(55.4,1.4,21.7),CNT=3,WAY=1)
	mt.wumpa_row(POS=(1.2,.5,-56),CNT=2,WAY=0)
	mt.wumpa_row(POS=(9,.5,-33),CNT=3,WAY=0)
	mt.wumpa_row(POS=(12,.5,-22),CNT=2,WAY=0)
	mt.wumpa_row(POS=(15.9,.5,-1.1),CNT=3,WAY=0)
	mt.wumpa_row(POS=(22,.5,-1.1),CNT=3,WAY=0)
	mt.wumpa_row(POS=(30,1.4,4.7),CNT=3,WAY=0)
	mt.wumpa_row(POS=(35.2,1.4,8.4),CNT=3,WAY=0)
	mt.wumpa_row(POS=(49.4,1.4,5.5),CNT=3,WAY=0)
	mt.wumpa_row(POS=(52.4,1.4,21),CNT=3,WAY=0)
def load_npc():
	n.spawn(ID=8,POS=(2.7,.2,-50.5),CMV=False)
	n.spawn(ID=8,POS=(2.7,.2,-35.7),CMV=False)
	n.spawn(ID=8,POS=(6.5,.25,-32.9),CMV=False)
	n.spawn(ID=8,POS=(11.9,.2,-23.5),CMV=False)
	n.spawn(ID=9,POS=(2.7,.2,-38.8))
	n.spawn(ID=8,POS=(24.2,.2,-1),DRC=0,CMV=True)
	n.spawn(ID=8,POS=(13.1,.2,-1),CMV=False)
	n.spawn(ID=9,POS=(34.9,1.1,8.6),DRC=0,RNG=.6)
	n.spawn(ID=8,POS=(53.2,1.1,8.3),CMV=False)
	n.spawn(ID=8,POS=(55.4,1.1,25.2),DRC=2,RNG=.6,CMV=True)

## bonus level / gem path
def bonus_zone():
	dg.FallingZone(pos=(0,-42,0),s=(128,.3,32))
	o.spw_block(ID=4,p=(-1,-36.5,U),vx=[4,1])
	o.spw_block(ID=4,p=(2,-36,U),vx=[2,1])
	o.spw_block(ID=4,p=(4.5,-36,U),vx=[3,1])
	o.spw_block(ID=4,p=(6.75,-35.5,U),vx=[4,1])
	o.LoosePlatform(pos=(10,-35.5,U),t=1)
	o.LoosePlatform(pos=(11.5,-35.8,U),t=1)
	o.LoosePlatform(pos=(13,-36.1,U),t=1)
	o.spw_block(ID=4,p=(14,-36.2,U),vx=[8,1])
	o.spw_block(ID=4,p=(21,-36.2,U),vx=[1,1])
	o.spw_block(ID=4,p=(21.75,-35.7,U),vx=[1,1])
	o.spw_block(ID=4,p=(24,-35.7,U),vx=[1,1])
	o.spw_block(ID=4,p=(24.75,-36.2,U),vx=[3,1])
	o.spw_block(ID=4,p=(31.17,-36.2,U),vx=[6,1])
	#crate
	mt.crate_stair(ID=1,POS=(26.8,-36.3,U),CNT=4,WAY=0)
	mt.crate_row(ID=1,POS=(26.8+.32*4,-36.3+.32*3,U),CNT=5,WAY=0)
	mt.crate_stair(ID=1,POS=(26.8+.32*9,-36.3+.32*3,U),CNT=4,WAY=1)
	mt.bounce_twin(POS=(26.8+.32*4,-36.3+.32*4,U),CNT=5)
	#
	mt.crate_wall(ID=14,POS=(8.2,-35.34,U),CNT=[1,3])
	c.place_crate(ID=12,p=(4.4,-35.84,U))
	c.place_crate(ID=12,p=(16.3,-36,U))
	c.place_crate(ID=12,p=(17.7,-36,U))
	c.place_crate(ID=9,p=(35,-36,U),m=103)
	mt.crate_row(ID=13,POS=(22.42,-35.86,U),CNT=4,m=103,l=1,WAY=0)
	mt.crate_row(ID=13,POS=(22.42,-35.86-.32,U),CNT=4,m=103,l=2,WAY=0)
	mt.crate_row(ID=13,POS=(22.42,-35.86-.64,U),CNT=4,m=103,l=3,WAY=0)
	mt.crate_row(ID=13,POS=(22.42,-35.86-.96,U),CNT=4,m=103,l=11,WAY=0)
	c.place_crate(ID=4,p=(21.7,-35.54,U))
	#wumpa
	mt.wumpa_double_row(POS=(.5,-36.2,U),CNT=2)
	mt.wumpa_double_row(POS=(1.9,-35.7,U),CNT=2)
	mt.wumpa_double_row(POS=(4.9,-35.7,U),CNT=2)
	mt.wumpa_double_row(POS=(6.7,-35.2,U),CNT=2)
	mt.wumpa_double_row(POS=(33.4,-35.9,U),CNT=2)
	mt.wumpa_double_row(POS=(18.2,-35.9,U),CNT=2)
	mt.wumpa_row(POS=(9.9,-35.25,U),CNT=2,WAY=2)
	mt.wumpa_row(POS=(11.5,-35.45,U),CNT=2,WAY=2)
	mt.wumpa_row(POS=(13,-35.95,U),CNT=2,WAY=2)
	mt.wumpa_row(POS=(21,-35.90,U),CNT=2,WAY=2)
	mt.wumpa_row(POS=(23.9,-35.40,U),CNT=2,WAY=2)
	#stair left
	mt.wumpa_row(POS=(26.8,-35.9,U),CNT=2,WAY=2)
	mt.wumpa_row(POS=(26.8+.32,-35.9+.32,U),CNT=2,WAY=2)
	mt.wumpa_row(POS=(26.8+.32*2,-35.9+.32*2,U),CNT=2,WAY=2)
	mt.wumpa_row(POS=(26.8+.32*3,-35.9+.32*3,U),CNT=2,WAY=2)
	#stair right
	mt.wumpa_row(POS=(26.8+.32*9,-35.9+.32*3,U),CNT=2,WAY=2)
	mt.wumpa_row(POS=(26.8+.32*10,-35.9+.32*2,U),CNT=2,WAY=2)
	mt.wumpa_row(POS=(26.8+.32*11,-35.9+.32,U),CNT=2,WAY=2)
	mt.wumpa_row(POS=(26.8+.32*12,-35.9,U),CNT=2,WAY=2)
	#background
	sk=.03
	o.ObjType_Wall(ID=3,pos=(-2.5,-37,U+1),ro_y=45,sca=sk)
	o.ObjType_Wall(ID=3,pos=(0,-37,U+2),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(3,-36.8,U+2),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(6,-36.6,U+2),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(9,-36.8,U+2),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(12,-36.6,U+2),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(15,-36.8,U+2),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(18,-36.6,U+2),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(21,-36.8,U+2),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(24,-36.6,U+2),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(27,-36.8,U+2),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(30,-36.6,U+2),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(33,-36.8,U+2),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(36,-36.6,U+2),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(39,-36.8,U+2),ro_y=90,sca=sk)
	o.BonusPlatform(pos=(36,-36,U))
	del sk
def gem_zone():
	bnh=-2.5
	sk=.03
	dg.FallingZone(pos=(200,-5,0),s=(40,1,80))
	o.spw_block(ID=4,p=(200,bnh,U),vx=[1,1])
	o.spw_block(ID=4,p=(200,bnh,U+1.5),vx=[2,1])
	for rn_a in range(3):
		o.spw_block(ID=4,p=(200+(.75*3+rn_a*1.5),bnh,U+1.5),vx=[1,1])
	del rn_a
	o.spw_block(ID=4,p=(206.5,bnh,U+1.5),vx=[2,1])
	for rn_b in range(5):
		o.spw_block(ID=4,p=(200.5+.75*8,bnh,U+(.75*3+rn_b*1.5)),vx=[1,1])
	del rn_b
	o.spw_block(ID=4,p=(206.4-.75,bnh,6.8),vx=[2,1])
	for rn_c in range(7):
		o.spw_block(ID=4,p=(202+(.75*3-rn_c*1.5),bnh,U+.75*13),vx=[1,1])
	del rn_c
	o.spw_block(ID=4,p=(194,bnh,U+.75*13),vx=[1,3])
	for rn_dx in range(1):
		for rn_dz in range(4):
			o.spw_block(ID=4,p=(189.5+.75*6+(rn_dx*1.5),bnh,U+(.75*17)+(rn_dz*1.3)),vx=[1,1])
	del rn_dx,rn_dz
	o.spw_block(ID=4,p=(194,bnh,15.5),vx=[1,5])
	for llpf in range(8):
		o.LoosePlatform(pos=(194,-2.6,19.5+llpf*1.5),t=0)
	del llpf
	o.spw_block(ID=4,p=(193.25,bnh,31.6),vx=[4,2])
	dg.MonkeySculpture(pos=(194-1,-2.6,21),r=False,d=True,ro_y=-90)
	dg.MonkeySculpture(pos=(194+1,-2.6,24),r=False,d=True,ro_y=90)
	dg.MonkeySculpture(pos=(194-1,-2.6,27),r=False,d=True,ro_y=-90)
	# npc
	n.spawn(ID=14,POS=(206.4,-2.5,7.1),DRC=0)
	n.spawn(ID=14,POS=(195.2,-2.5,6.75),DRC=3)
	n.spawn(ID=14,POS=(206.75,-2.5,-1.5),DRC=1)
	n.spawn(ID=14,POS=(194,-2.5,15.6),DRC=0)
	#background
	o.ObjType_Scene(ID=9,pos=(197.5,-4,0),ro_y=-60,sca=.08)
	o.ObjType_Scene(ID=9,pos=(209,-4,2),ro_y=90,sca=.08)
	o.ObjType_Wall(ID=3,pos=(202,-3,4),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(204,-3.2,3),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(199,-3,5),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(196,-3,5.3),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(196.5,-2.4,8.2),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(199,-2.5,9.2),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(201.5,-2.6,8.2),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(204,-2.3,9.2),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(206.5,-2.4,8.2),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(209,-2.6,9.2),ro_y=90,sca=sk)
	o.ObjType_Wall(ID=3,pos=(192.3,-2.9,7.6),ro_y=0,sca=sk)
	o.ObjType_Scene(ID=9,pos=(197,-4,16),ro_y=90,sca=.08)
	o.ObjType_Scene(ID=9,pos=(191,-4,16),ro_y=-90,sca=.08)
	o.ObjType_Scene(ID=9,pos=(198,-4,32),ro_y=90,sca=.08)
	o.ObjType_Scene(ID=9,pos=(191,-4,32),ro_y=-90,sca=.08)
	if not 3 in st.COLOR_GEM:
		item.GemStone(c=3,pos=(194.4,-2,37.7))
	o.EndRoom(pos=(195.5,-1.01,37.7),c=color.rgb32(220,100,220))
	del sk