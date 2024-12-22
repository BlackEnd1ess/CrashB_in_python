import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import objects,map_tools,crate,npc,item
from ursina import *

mt=map_tools
o=objects
c=crate
n=npc
U=-3

def start_load():
	load_crate()
	bonus_zone()
	load_object()
	load_wumpa()
	load_npc()

def load_object():
	o.StartRoom(pos=(0,0,-65))
	o.BonusPlatform(pos=(-.5,2,7.7))
	o.GemPlatform(pos=(4,1,-7.9),t=2)
	o.FallingZone(pos=(0,-1.4,-40),s=(5,.1,60),v=True)
	#e0
	o.BeeSideTree(pos=(1.7,.4,-60))
	o.BeeSideTree(pos=(-1.7,.4,-60),m=True)
	o.BeeSideTree(pos=(1.7,.4,-56.3))
	o.BeeSideTree(pos=(-1.7,.4,-56.3),m=True)
	o.BeeSideWall(pos=(-.5,.8,-45),t=0)
	o.BeeFloor(pos=(0,-1.8,-61.5),t=0)
	o.SnowPlatform(pos=(0,0,-58.5))
	o.SnowPlatform(pos=(0,0,-56.4))
	#o.LandMine(pos=(0,0,-56.4))
	o.BeeFloor(pos=(0,-1.8,-54),t=0)
	o.BeeFloor(pos=(1,-1.8,-50),t=0)
	o.BeeFloor(pos=(-1,-1.8,-44),t=0)
	o.BeeFloor(pos=(0,-1.6,-41),t=0)
	o.SnowPlatform(pos=(0,0,-47))
	#o.TikkiSculpture(pos=(0,0,-52.2),spd=3,rng=.8)
	#e1
	o.BeeFloor(pos=(0,-1.2,-38.5),t=0)
	o.BeeFloor(pos=(0,-.8,-35.9),t=0)
	o.BeeFloor(pos=(0,-.8,-31.9),t=0)
	o.BeeSideWall(pos=(-.51,.7,-34),t=0)
	o.BeeBigGround(pos=(0,.2,-25),sca=(4,1,12))
	for stt1 in range(4):
		o.BeeSideTree(pos=(1.7,1,-30+stt1*3.7))
		o.BeeSideTree(pos=(-1.7,1,-30+stt1*3.7),m=True)
	o.BeeSideTree(pos=(1.7,1,-12.4))
	o.BeeSideTree(pos=(-1.7,1,-12.4),m=True)
	o.BeeSideTree(pos=(5.5,1,-8))
	o.BeeSideTree(pos=(-5.5,1,-8),m=True)
	o.BeeSideWall(pos=(-.5,2.6,3.2),t=0)
	o.BeeSideWall(pos=(-.5,2.6,14),t=0)
	#e2
	o.FrontStoneWall(pos=(-4.4,1,-6.1))
	o.FrontStoneWall(pos=(4.4,1,-6.1))
	o.BeeFloor(pos=(-2.2,1,-16),t=0)
	o.BeeFloor(pos=(2.2,1,-16),t=0)
	o.BeeFloor(pos=(0,-1,-15.8),t=0)
	o.BeeFloor(pos=(0,-1,-11.8),t=0)
	o.BeeFloor(pos=(0,-1,-7.8),t=0)
	o.BeeFloor(pos=(-4,-1,-7.8),t=0)
	o.BeeFloor(pos=(4,-1,-7.8),t=0)
	o.BeeFloor(pos=(0,-.7,-4.8),t=1)
	o.BeeFloor(pos=(0,-.3,-2.8),t=1)
	o.BeeFloor(pos=(0,.1,-.8),t=1)
	o.BeeBigGround(pos=(0,1.3,8),sca=(4,1,16))
	o.BeeFloor(pos=(0,.1,17),t=0)
	o.BeeFloor(pos=(0,.4,19),t=0)
	o.BeeFloor(pos=(0,.7,21),t=0)
	o.BeeFloor(pos=(3,.7,21),t=1)
	o.BeeFloor(pos=(6,.7,21),t=1)
	o.BeeFloor(pos=(9,.7,21),t=1)
	o.BeeFloor(pos=(9,.7,24),t=1)
	#e3
	o.BeeSideTree(pos=(-1.8,2.7,19),m=True)
	o.BeeSideTree(pos=(11,2.7,21))
	o.BeeSideWall(pos=(8.5,3.4,32.1),t=0)
	o.BeeSideTree(pos=(7.4,3,36.5),m=True)
	o.BeeSideTree(pos=(10.6,3,36.5))
	o.FrontStoneWall(pos=(-1,1.5,22.8))
	o.FrontStoneWall(pos=(4.3,1.5,23))
	o.FrontStoneWall(pos=(13.7,1.5,23))
	o.BeeBigGround(pos=(9,1.91,32),sca=(4,1,16))
	o.EndRoom(pos=(10.1,4.2,43.5),c=color.rgb32(180,160,160))

def load_crate():
	#normals
	mt.crate_wall(ID=2,POS=(-0.7,0.16,-60.8),CNT=[1,2])
	mt.crate_wall(ID=1,POS=(-0.7,0.96,-11.9),CNT=[1,2])
	mt.crate_wall(ID=2,POS=(3.4,0.96,-7.2),CNT=[1,2])
	mt.crate_wall(ID=1,POS=(0.4,1.96,12.3),CNT=[1,2])
	mt.crate_wall(ID=2,POS=(-0.7,1.96,14.5),CNT=[1,2])
	mt.crate_wall(ID=1,POS=(9.8,2.66,21.5),CNT=[1,2])
	#nitro
	c.place_crate(ID=10,p=(8.5,2.57,36.4))
	c.place_crate(ID=12,p=(0.1,0.16,-50.9))
	c.place_crate(ID=12,p=(-0.3,0.16,-47.0))
	c.place_crate(ID=12,p=(-0.5,0.36,-40.3))
	c.place_crate(ID=12,p=(0.6,0.36,-41.8))
	c.place_crate(ID=12,p=(-0.5,0.86,-27.3))
	c.place_crate(ID=12,p=(0.6,0.86,-23.9))
	c.place_crate(ID=12,p=(-0.5,0.86,-19.8))
	c.place_crate(ID=12,p=(0.0,1.26,-5.8))
	c.place_crate(ID=12,p=(-0.6,2.36,18.3))
	c.place_crate(ID=12,p=(0.7,2.66,20.9))
	c.place_crate(ID=12,p=(3.6,2.66,21.5))
	c.place_crate(ID=12,p=(5.8,2.66,20.3))
	c.place_crate(ID=12,p=(9.8,2.66,21.1))
	c.place_crate(ID=12,p=(9.4,2.57,33.2))
	#aku
	c.place_crate(ID=5,p=(0.7,0.16,-61.0))
	c.place_crate(ID=5,p=(-0.5,1.16,-35.6))
	c.place_crate(ID=5,p=(0.0,2.06,16.7))
	#checkpoints
	c.place_crate(ID=6,p=(0.0,1.16,-31.5))
	c.place_crate(ID=6,p=(0.0,0.96,-7.9))
	c.place_crate(ID=6,p=(9.0,2.66,21.1))
def load_wumpa():
	return
def load_npc():
	return
	n.spawn(ID=16,POS=(0,0,-57.4))
	n.spawn(ID=16,POS=(0,1.2,-4.3))

## bonus level / gem path
def bonus_zone():
	o.BonusBeeWall(pos=(0,-40,0))
	o.BonusBeeWall(pos=(20,-40,0))
	o.StoneWall(pos=(0,-37.5,U))
	o.StoneWall(pos=(-3,-37,U))
	o.StoneWall(pos=(3,-37.5,U))
	o.StoneWall(pos=(6,-38,U))
	o.StoneWall(pos=(9,-38,U))
	o.BonusPlatform(pos=(10.7,-36.9,U))
def gem_zone():
	return