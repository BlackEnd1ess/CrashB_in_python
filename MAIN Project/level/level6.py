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
	o.LandMine(pos=(0,0,-56.4))
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
	#e2
	o.FrontStoneWall(pos=(-4.6,1,-6.1))
	o.FrontStoneWall(pos=(4.6,1,-6.1))
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
	o.FrontStoneWall(pos=(-.6,1.5,23))
	o.FrontStoneWall(pos=(4.1,1.5,23))
	o.FrontStoneWall(pos=(14,1.5,23))
	o.BeeBigGround(pos=(9,1.91,32),sca=(4,1,16))
	o.EndRoom(pos=(1.75,5.7,48),c=color.rgb32(180,160,160))

def load_crate():
	return
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