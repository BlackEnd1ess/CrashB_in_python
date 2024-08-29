import crate,item,status,_core,objects,environment,map_tools,npc
from ursina import *

MT=map_tools
o=objects
c=crate
N=npc
U=-3
def load_bonus_level(idx):
	lv_lst={1:bonus1,2:bonus2,3:bonus3,4:bonus4,5:bonus5,6:bonus1}
	lv_lst[idx]()

def bonus1():
	o.BonusPlatform(pos=(11.5,-37,U))
	o.Water(pos=(0,-39,0),s=(60,60),c=color.rgb32(100,110,110),a=.9)
	for w in range(2):
		o.BackgroundWall(p=(0+w*14,-37,2))
	for bc0 in range(6):
		c.place_crate(ID=0,p=(0+bc0/3.1,-37,U))
		c.place_crate(ID=0,p=(3+bc0/3.1,-37,U))
		c.place_crate(ID=0,p=(6+bc0/3.1,-37,U))
		c.place_crate(ID=0,p=(9+bc0/3.1,-37,U))
	c.place_crate(ID=8,p=(4,-36.66,U))
	MT.crate_row(ID=1,POS=(4,-35,U),WAY=2,CNT=4)
	MT.crate_wall(ID=1,POS=(1,-36.66,U),CNT=[3,3])
	MT.crate_wall(ID=2,POS=(6,-36.66,U),CNT=[2,2])
	c.place_crate(ID=4,p=(9,-36.66,U))
	MT.wumpa_row(POS=(9,-36,U),CNT=4,WAY=2)
	MT.wumpa_row(POS=(9.4,-36.6,U),CNT=4,WAY=0)
	MT.wumpa_row(POS=(1.6,-36,U),CNT=4,WAY=0)

def bonus2():
	o.FallingZone(pos=(0,-40,0),s=(64,1,64))
	for sw in range(5):
		o.SnowWall(pos=(-4+sw*5.4,-33.9,-2.5))
		o.SnowWall(pos=(-4+sw*5.4,-37,-2.5))
		o.SnowWall(pos=(-4+sw*5.4,-40.1,-2.5))
	o.mBlock(pos=(0,-37.4,U),sca=(3,.5,.5))
	o.mBlock(pos=(4,-37.4,U),sca=(3,.5,.5))
	o.mBlock(pos=(8,-37.4,U),sca=(3,.5,.5))
	o.mBlock(pos=(14,-37.4,U),sca=(3,.5,.5))
	MT.crate_row(ID=0,POS=(3.8,-35,U),WAY=0,CNT=8)
	MT.crate_wall(ID=2,POS=(4,-34.68,U),CNT=[2,2])
	c.place_crate(ID=4,p=(5.3,-34.68,U))
	c.place_crate(ID=1,p=(8.3,-36.68,U))
	c.place_crate(ID=1,p=(7.5,-36,U))
	c.place_crate(ID=1,p=(7,-35.5,U))
	c.place_crate(ID=9,p=(15,-37,U),m=1)
	c.place_crate(ID=13,p=(4,-37,U),m=1,l=2)
	MT.crate_row(ID=1,POS=(10,-37.32,U),WAY=0,CNT=7)
	MT.crate_row(ID=3,POS=(10.32,-37.64,U),WAY=0,CNT=5)
	MT.wumpa_double_row(POS=(-.5,-37.1,U),CNT=5)
	MT.wumpa_double_row(POS=(10,-36.3,U),CNT=7)
	MT.wumpa_double_row(POS=(10,-36.9,U),CNT=7)
	MT.wumpa_double_row(POS=(2.8,-37.1,U),CNT=8)
	MT.wumpa_double_row(POS=(7,-37.1,U),CNT=8)
	o.BonusPlatform(pos=(16,-37.1,U))

def bonus3():
	Entity(model='plane',texture='res/ui/background/bonus_1.jpg',scale=(60,1,30),position=(10,-40,15),rotation_x=-90,unlit=False)
	MT.wumpa_double_row(POS=(12.8,-35,U),CNT=6)
	MT.wumpa_double_row(POS=(-.5,-36.5,U),CNT=4)
	MT.wumpa_row(POS=(1.5,-36.35,U),CNT=3,WAY=0)
	MT.wumpa_row(POS=(3.5,-35.35,U),CNT=3,WAY=0)
	MT.wumpa_row(POS=(5.5,-34.85,U),CNT=3,WAY=0)
	MT.wumpa_row(POS=(17.5,-35.35,U),CNT=3,WAY=0)
	o.FallingZone(pos=(0,-40,0),s=(64,1,64))
	o.MushroomTree(pos=(2,-39,U+1.2),typ=1)
	o.MushroomTree(pos=(4,-39,U+1.2),typ=1)
	o.MushroomTree(pos=(6,-38.5,U+1.2),typ=1)
	MT.crate_row(ID=0,POS=(-1,-37,U),WAY=0,CNT=7)
	MT.bounce_twin(POS=(7.2,-36.16,U),CNT=5)
	o.MushroomTree(pos=(9.5,-38.5,U+1.2),typ=1)
	o.MushroomTree(pos=(10.5,-38,U+1.2),typ=1)
	o.MushroomTree(pos=(11.5,-38,U+1.2),typ=1)
	c.place_crate(ID=11,p=(12.5,-36,U))
	MT.crate_row(ID=12,POS=(12.82,-36,U),WAY=0,CNT=7)
	MT.crate_row(ID=1,POS=(12.82,-35.68,U),WAY=0,CNT=7)
	o.MushroomTree(pos=(16,-38,U+1.2),typ=1)
	o.MushroomTree(pos=(18,-38,U+1.2),typ=1)
	MT.crate_wall(ID=1,POS=(16,-35.65+.16,U+.1),CNT=[2,2])
	c.place_crate(ID=2,p=(4,-36.65+.16,U+.1))
	c.place_crate(ID=4,p=(5.8,-35.1,U))
	MT.crate_row(ID=2,POS=(10.4,-35.65+.16,U+.1),CNT=4,WAY=0)
	o.BonusPlatform(pos=(19.3,-35.7,U))

def bonus4():
	o.FallingZone(pos=(0,-42,0),s=(64,1,64))
	#bg walls
	Entity(model='quad',texture='res/terrain/l4/sewer_tiles.jpg',scale=(60,20),texture_scale=(30,10),position=(0,-35,1),color=color.rgb32(160,150,150))
	#pipes
	o.SewerPipe(pos=(8.3,-36.4,U),typ=3)
	for swp in range(3):
		o.SewerPipe(pos=(2+swp*13,-34,.6),typ=2)
		o.SewerPipe(pos=(4.5+swp*13,-34,.6),typ=2)
		o.SewerPipe(pos=(7+swp*13,-34,.6),typ=2)
		o.SewerPipe(pos=(3+swp*13,-36,.6),typ=0)
		o.SewerPipe(pos=(6+swp*13,-36,.6),typ=0)
	#
	for swl in range(3):
		o.SewerWall(pos=(-2+swl*13,-38,0))
		o.SewerWall(pos=(-2+swl*13,-30.8,0))
	#platform
	o.swr_multi_ptf(p=(0,-36.5,U),cnt=[3,1])
	o.swr_multi_ptf(p=(2,-36,U),cnt=[1,1])
	o.swr_multi_ptf(p=(3,-35.5,U),cnt=[4,1])
	o.swr_multi_ptf(p=(5,-34,U),cnt=[7,1])
	o.swr_multi_ptf(p=(9,-34,U),cnt=[3,1])
	
	o.swr_multi_ptf(p=(8.5,-36,U),cnt=[5,1])
	o.swr_multi_ptf(p=(12,-36,U),cnt=[3,1])
	o.swr_multi_ptf(p=(14,-35.5,U),cnt=[1,1])
	o.swr_multi_ptf(p=(15,-35,U),cnt=[1,1])
	o.swr_multi_ptf(p=(16,-34.5,U),cnt=[1,1])
	o.swr_multi_ptf(p=(17,-34.5,U),cnt=[4,1])
	o.swr_multi_ptf(p=(20,-34.5,U),cnt=[4,1])
	#crate
	c.place_crate(ID=4,p=(2,-35.9+.16,U))
	c.place_crate(ID=1,p=(2,-35.9+.48,U))
	c.place_crate(ID=7,p=(4.4,-35.4+.16,U))
	c.place_crate(ID=11,p=(4.4-.32,-35.4+.16,U))
	c.place_crate(ID=12,p=(5.57,-33.74,U))
	c.place_crate(ID=12,p=(6.49,-33.74,U))
	c.place_crate(ID=12,p=(7.45,-33.74,U))
	c.place_crate(ID=9,p=(10,-33.7,U),m=2)
	MT.crate_row(ID=13,POS=(6.1,-36,U),CNT=7,WAY=0,m=2,l=3)
	MT.crate_row(ID=2,POS=(12.5,-35.74,U),CNT=3,WAY=2)
	MT.crate_wall(ID=2,POS=(17.47,-34.24,U),CNT=[3,2])
	c.place_crate(ID=11,p=(21.2,-34.24,U))
	c.place_crate(ID=12,p=(12.97,-35.74,U))
	c.place_crate(ID=1,p=(12.97,-35.74+.32,U))
	c.place_crate(ID=12,p=(14.12,-35.24,U))
	c.place_crate(ID=2,p=(14.12,-35.24+.32,U))
	c.place_crate(ID=12,p=(14.97,-34.74,U))
	c.place_crate(ID=1,p=(14.97,-34.74+.32,U))
	c.place_crate(ID=12,p=(15.98,-34.24,U))
	c.place_crate(ID=1,p=(15.98,-34.24+.32,U))
	c.place_crate(ID=12,p=(16.97,-34.24,U))
	c.place_crate(ID=1,p=(16.97,-34.24+.32,U))
	#wumpa fruits
	MT.wumpa_double_row(POS=(.4,-36.24,U),CNT=3)
	MT.wumpa_double_row(POS=(3,-35.24,U),CNT=3)
	MT.wumpa_double_row(POS=(8.48,-35.74,U),CNT=7)
	MT.wumpa_double_row(POS=(20.02,-34.24,U),CNT=3)
	MT.wumpa_row(POS=(4.5,-34.6,U),CNT=4,WAY=2)
	MT.wumpa_row(POS=(12,-35.74,U),CNT=4,WAY=2)
	MT.wumpa_row(POS=(8.48,-35.3,U),CNT=8,WAY=2)
	o.BonusPlatform(pos=(22.3,-34.2,U))

def bonus5():
	o.FallingZone(pos=(0,-42,0),s=(128,.3,32))
	o.spw_ruin_ptf(p=(-1,-37,U),cnt=4,way=0)
	o.spw_ruin_ptf(p=(2,-36.5,U),cnt=2,way=0)
	o.spw_ruin_ptf(p=(4.5,-36.5,U),cnt=3,way=0)
	o.spw_ruin_ptf(p=(6.75,-36,U),cnt=4,way=0)
	o.LoosePlatform(pos=(10,-35.8,U),t=1)
	o.LoosePlatform(pos=(11.5,-36,U),t=1)
	o.LoosePlatform(pos=(13,-36.5,U),t=1)
	o.spw_ruin_ptf(p=(14,-36.7,U),cnt=8,way=0)
	o.spw_ruin_ptf(p=(21,-36.7,U),cnt=1,way=0)
	o.spw_ruin_ptf(p=(21.75,-36.2,U),cnt=1,way=0)
	o.spw_ruin_ptf(p=(24,-36.2,U),cnt=1,way=0)
	o.spw_ruin_ptf(p=(24.75,-36.7,U),cnt=3,way=0)
	o.spw_ruin_ptf(p=(32.15,-36.7,U),cnt=5,way=0)
	#crate
	MT.crate_stair(ID=1,POS=(26.8,-36.3,U),CNT=4,WAY=0)
	MT.crate_row(ID=1,POS=(26.8+.32*4,-36.3+.32*3,U),CNT=8,WAY=0)
	MT.crate_stair(ID=1,POS=(26.8+.32*12,-36.3+.32*3,U),CNT=4,WAY=1)
	MT.bounce_twin(POS=(26.8+.32*4,-36.3+.32*4,U),CNT=7)
	o.BonusPlatform(pos=(36,-36,U))
## gem route
def gem_route1():
	o.FallingZone(pos=(200,-4,0),s=(40,1,32))
	wtw='res/objects/l1/bush/bush1.png'
	Entity(model='quad',texture=wtw,scale=12,color=color.rgb32(0,50,0),position=(175,0,128.1))
	Entity(model='quad',texture=wtw,scale=12,color=color.rgb32(0,50,0),position=(175,-6,128.2))
	Entity(model='quad',texture=wtw,scale=12,color=color.rgb32(0,50,0),position=(175,-12,128.3))
	Entity(model='quad',texture=wtw,scale=12,color=color.rgb32(0,50,0),position=(175,-18,128.4))
	Entity(model='quad',texture=wtw,scale=12,color=color.rgb32(0,50,0),position=(175,-24,128.5))
	Entity(model='quad',texture='res/background/bg_woods.png',scale=(90,20,1),position=(210,-15,25),texture_scale=(4,1),unlit=False)
	Entity(model='quad',texture='res/background/bg_woods.png',color=color.rgb32(50,120,50),scale=(90,20,1),position=(210,-6,27),texture_scale=(4,1),unlit=False)
	MT.crate_row(ID=0,POS=(200,-2,U),WAY=0,CNT=7)
	MT.crate_row(ID=0,POS=(203,-1,U),WAY=0,CNT=7)
	c.place_crate(ID=8,p=(206,0,U))
	c.place_crate(ID=8,p=(207,1,U))
	c.place_crate(ID=8,p=(206,2,U))
	c.place_crate(ID=8,p=(207,3,U))
	MT.bounce_twin(POS=(201.6,-1.68,U),CNT=2)
	c.place_crate(ID=1,p=(202.5,-1.3,U))
	MT.crate_row(ID=0,POS=(208,3,U),WAY=0,CNT=12)
	MT.crate_row(ID=2,POS=(209,3.32,U),WAY=0,CNT=4)
	MT.crate_row(ID=1,POS=(209,4.8,U),WAY=0,CNT=4)
	MT.crate_wall(ID=1,POS=(203.8,-.68,U),CNT=[2,2])
	o.GemPlatform(pos=(212.2,3.1,U),t=4)

def gem_route4():
	Entity(model='cube',scale=(16,1,96),position=(200,-1.2,-16),collider='box',color=color.black)
	o.swr_multi_ptf(p=(199.75,-.4,-3.25),cnt=[2,2])
	o.EletricWater(pos=(200,-.5,22),sca=(8,64),ID=3)
	o.SewerTunnel(pos=(200,-.3,5),c=color.rgb32(0,200,180))
	o.SewerTunnel(pos=(200,-.3,15),c=color.rgb32(0,200,180))
	o.SewerTunnel(pos=(200,-.3,25),c=color.rgb32(0,200,180))
	o.SewerEntrance(pos=(200,1,-3))
	o.SwimPlatform(pos=(200,-.45,-.7))
	o.SwimPlatform(pos=(200-.3,-.45,.7))
	c.place_crate(ID=0,p=(200,-.5,-2))
	c.place_crate(ID=0,p=(200,-.5,2))
	c.place_crate(ID=9,p=(200,-.5,3),m=101)
	c.place_crate(ID=13,p=(200,-.5,4),l=8,m=101)
	c.place_crate(ID=9,p=(200,-.5,6),m=102)
	MT.crate_row(ID=13,POS=(200,-.5,6.32),CNT=8,WAY=1,l=0,m=102)
	MT.crate_row(ID=13,POS=(200,-.5,6+.32*9),CNT=3,WAY=0,l=0,m=102)
	MT.crate_row(ID=13,POS=(200+.32*2,-.5,6+.32*10),CNT=5,WAY=1,l=0,m=102)
	o.SwimPlatform(pos=(200+.3,-.45,11.8))
	o.SwimPlatform(pos=(200,-.45,12.8))
	o.SwimPlatform(pos=(200-.3,-.45,13.8))
	MT.crate_row(ID=13,POS=(200-.32*2,-.5,14.5),CNT=5,WAY=1,l=0,m=102)
	MT.crate_row(ID=13,POS=(200-.32*2,-.5,14.5+.32*5),CNT=4,WAY=0,l=0,m=102)
	MT.crate_row(ID=13,POS=(200+.32*2,-.5,14.5+.32*5),CNT=7,WAY=1,l=0,m=102)
	o.SwimPlatform(pos=(200+.3,-.45,18.7))
	o.SwimPlatform(pos=(200,-.45,19.7))
	o.SwimPlatform(pos=(200-.3,-.45,20.7))
	MT.crate_row(ID=13,POS=(200-.32,-.5,21.5),CNT=7,WAY=1,l=0,m=102)
	MT.crate_row(ID=13,POS=(200-.32,-.5,21.5+.32*7),CNT=4,WAY=0,l=0,m=102)
	MT.crate_row(ID=13,POS=(200-.32+.32*3,-.5,21.5+.32*8),CNT=8,WAY=1,l=0,m=102)
	N.spawn(pos=(200,0,5),mID=13,mDirec=1,mTurn=0)
	N.spawn(pos=(200,0,16),mID=13,mDirec=1,mTurn=0)
	N.spawn(pos=(200,0,19.7),mID=13,mDirec=1,mTurn=0)
	N.spawn(pos=(200,0,23.7),mID=13,mDirec=1,mTurn=0)
	o.SewerEscape(pos=(200,-1,30),c=color.rgb32(0,200,180))
	o.SewerEntrance(pos=(200,1,27))
	Entity(model='cube',scale=(4,.5,7),position=(200,-.5,31),texture_scale=(4,5),collider='box',texture='res/terrain/l4/metal_01.jpg')
	N.spawn(pos=(200,-.25,29),mID=11,mDirec=0,mTurn=0,ro_mode=1)
	o.SewerWall(pos=(200,-1.7,33))
	item.GemStone(c=2,pos=(200,0,28.9))
	o.GemPlatform(pos=(200,0,31.9),t=5)