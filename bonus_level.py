import crate,item,status,_core,objects,environment,map_tools
from ursina import *

MT=map_tools
o=objects
c=crate
U=-3
def load_bonus_level(idx):
	lv_lst={1:bonus1,2:bonus2,3:bonus3,4:bonus4}
	lv_lst[idx]()

def bonus1():
	o.BonusPlatform(pos=(11.5,-37,U))
	o.Water(pos=(0,-39,0),s=(60,60),c=color.rgb(100,110,110),a=.9)
	for w in range(2):
		o.BackgroundWall(p=(0+w*14,-37,2))
	for bc0 in range(6):
		c.place_crate(ID=0,p=(0+bc0/3.1,-37,U))
		c.place_crate(ID=0,p=(3+bc0/3.1,-37,U))
		c.place_crate(ID=0,p=(6+bc0/3.1,-37,U))
		c.place_crate(ID=0,p=(9+bc0/3.1,-37,U))
	c.place_crate(ID=8,p=(4,-36.66,U))
	MT.crate_row(ID=1,POS=(4,-35,U),WAY=2,CNT=4)
	MT.crate_wall(ID=1,POS=(1,-36.66,U),CNT=3)
	MT.crate_wall(ID=2,POS=(6,-36.66,U),CNT=2)
	c.place_crate(ID=4,p=(9,-36.66,U))
	MT.wumpa_row(POS=(9,-36,U),CNT=4,WAY=2)
	MT.wumpa_row(POS=(9.4,-36.6,U),CNT=4,WAY=0)
	MT.wumpa_row(POS=(1.6,-36,U),CNT=4,WAY=0)
	#for bc1 in range(20):
	#	c.place_crate(ID=3,p=(0+bc1/3.1,-25.5,-3))
	#	c.place_crate(ID=1,p=(0+bc1/3.1,-24,-3))

def bonus2():
	o.FallingZone(pos=(0,-40,0),s=(64,1,64))
	for sw in range(20):
		o.SnowWall(pos=(0+sw*7,-37,-2.5))
		o.SnowWall(pos=(0+sw*7,-33,-2.5))
	o.mBlock(pos=(0,-37,U),sca=(3,.5,.5))
	o.mBlock(pos=(4,-37,U),sca=(3,.5,.5))
	o.mBlock(pos=(8,-37,U),sca=(3,.5,.5))
	o.mBlock(pos=(14,-37,U),sca=(3,.5,.5))
	MT.crate_row(ID=0,POS=(3.8,-35,U),WAY=0,CNT=8)
	MT.crate_wall(ID=2,POS=(4,-34.68,U),CNT=2)
	c.place_crate(ID=1,p=(8.3,-36.68,U))
	c.place_crate(ID=1,p=(7.5,-36,U))
	c.place_crate(ID=1,p=(7,-35.5,U))
	c.place_crate(ID=9,p=(15,-36.68,U),m=1)
	c.place_crate(ID=13,p=(4,-36.68,U),m=1,l=2)
	MT.crate_row(ID=1,POS=(10,-37,U),WAY=0,CNT=7)
	MT.crate_row(ID=3,POS=(10.32,-37.32,U),WAY=0,CNT=5)
	MT.wumpa_row(POS=(-.5,-36.9,U),CNT=4,WAY=0)
	MT.wumpa_row(POS=(10,-36.4,U),CNT=7,WAY=0)
	MT.wumpa_row(POS=(10,-36,U),CNT=7,WAY=0)
	MT.wumpa_row(POS=(10,-35.6,U),CNT=7,WAY=0)
	MT.wumpa_row(POS=(2.8,-36.9,U),CNT=8,WAY=0)
	MT.wumpa_row(POS=(7,-36.9,U),CNT=5,WAY=0)
	o.BonusPlatform(pos=(16,-37,U-.3))

def bonus3():
	Entity(model='plane',texture='res/ui/background/bonus_1.jpg',scale=(90,1,20),position=(0,-40,14),rotation_x=-90,texture_scale=(3,1),unlit=False)
	o.FallingZone(pos=(0,-40,0),s=(64,1,64))
	o.MushroomTree(pos=(2,-39,U+1),typ=1)
	o.MushroomTree(pos=(4,-39,U+1),typ=1)
	o.MushroomTree(pos=(6,-38.5,U+1),typ=1)
	MT.crate_row(ID=0,POS=(-1,-37,U),WAY=0,CNT=7)
	MT.bounce_twin(POS=(7.2,-36.32,U),CNT=5)
	o.MushroomTree(pos=(9.5,-38.5,U+1),typ=1)
	o.MushroomTree(pos=(10.5,-38,U+1),typ=1)
	o.MushroomTree(pos=(11.5,-38,U+1),typ=1)
	c.place_crate(ID=11,p=(12.5,-36.5,U))
	MT.crate_row(ID=12,POS=(12.82,-36.5,U),WAY=0,CNT=7)
	MT.crate_row(ID=1,POS=(12.82,-36.18,U),WAY=0,CNT=7)
	o.MushroomTree(pos=(16,-38,U+1),typ=1)
	o.MushroomTree(pos=(18,-38,U+1),typ=1)
	o.BonusPlatform(pos=(19.3,-35.7,U))

def bonus4():
	return
## gem route
def gem_route1():
	o.FallingZone(pos=(200,-4,0),s=(40,1,32))
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
	MT.crate_wall(ID=1,POS=(203.8,-.68,U),CNT=2)
	o.GemPlatform(pos=(212,3.5,U),t=4)