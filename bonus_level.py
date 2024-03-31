import crate,item,status,_core,objects,environment,map_tools
from ursina import *

MT=map_tools
o=objects
c=crate
U=-3
def load_bonus_level(idx):
	lv_lst={1:bonus1,2:bonus2}
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
	#for bc1 in range(20):
	#	c.place_crate(ID=3,p=(0+bc1/3.1,-25.5,-3))
	#	c.place_crate(ID=1,p=(0+bc1/3.1,-24,-3))

def bonus2():
	return

## gem route
def gem_route1():
	MT.crate_row(ID=0,POS=(200,-2,U),WAY=0,CNT=7)
	MT.crate_row(ID=0,POS=(203,-1,U),WAY=0,CNT=7)
	c.place_crate(ID=8,p=(206,0,U))
	c.place_crate(ID=8,p=(207,1,U))
	c.place_crate(ID=8,p=(206,2,U))
	c.place_crate(ID=8,p=(207,3,U))
	MT.crate_row(ID=0,POS=(208,3,U),WAY=0,CNT=12)
	o.GemPlatform(pos=(212,3.5,U),t=4)