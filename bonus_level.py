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
	o.BonusPlatform(pos=(11.5,-27,U))
	o.Water(pos=(0,-29,0),s=(60,60),c=color.rgb(100,110,110),a=.9)
	for w in range(2):
		o.BackgroundWall(p=(0+w*14,-27,2))
	for bc0 in range(6):
		c.place_crate(ID=0,p=(0+bc0/3.1,-27,U))
		c.place_crate(ID=0,p=(3+bc0/3.1,-27,U))
		c.place_crate(ID=0,p=(6+bc0/3.1,-27,U))
		c.place_crate(ID=0,p=(9+bc0/3.1,-27,U))
	c.place_crate(ID=8,p=(4,-26.66,U))
	MT.crate_row(ID=1,POS=(4,-25,U),WAY=2,CNT=4)
	MT.crate_wall(ID=1,POS=(1,-26.66,U),CNT=3)
	MT.crate_wall(ID=2,POS=(6,-26.66,U),CNT=2)
	c.place_crate(ID=4,p=(9,-26.66,U))
	#for bc1 in range(20):
	#	c.place_crate(ID=3,p=(0+bc1/3.1,-25.5,-3))
	#	c.place_crate(ID=1,p=(0+bc1/3.1,-24,-3))

def bonus2():
	return