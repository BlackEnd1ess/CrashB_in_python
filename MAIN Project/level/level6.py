import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import objects,map_tools,crate,npc,item
from ursina import *

mt=map_tools
o=objects
c=crate
n=npc

def start_load():
	load_crate()
	load_object()
	load_wumpa()
	load_npc()

def load_object():
	o.StartRoom(pos=(0,0,-65))
	o.FallingZone(pos=(0,-1.4,-40),s=(5,.1,60),v=True)
	bte='res/terrain/l6/bee_terra.png'
	#e0
	o.BeeSideWall(pos=(.5,.8,-54),t=0)
	o.BeeSideWall(pos=(.5,.8,-48),t=0)
	o.BeeSideTree(pos=(1.7,.2,-43.3))
	o.BeeSideTree(pos=(-1.7,.2,-43.3),m=True)
	o.BeeFloor(pos=(0,-1.8,-61.5),t=0)
	o.BeeFloor(pos=(0,-1.8,-58),t=0)
	o.SnowPlatform(pos=(0,0,-56))
	o.SnowPlatform(pos=(0,0,-54.5))
	o.BeeFloor(pos=(0,-1.8,-52),t=0)
	o.BeeFloor(pos=(1,-1.8,-48),t=0)
	o.BeeFloor(pos=(-1,-1.8,-44),t=0)
	o.BrickWall(pos=(-1.2,-2.5,-40),sca=(45,0,5))
	o.BrickWall(pos=(1.2,-2.5,-40),sca=(45,0,5))
	o.SnowPlatform(pos=(0,0,-41))
	o.TikkiSculpture(pos=(0,0,-52.2),spd=3,rng=.8)
	#e1
	o.BeeFloor(pos=(0,-1.8,-38.5),t=0)
	o.BeeFloor(pos=(0,-.8,-35.9),t=0)
	o.BeeFloor(pos=(0,-.8,-31.9),t=0)
	o.BeeSideWall(pos=(.5,.8,-33),t=0)
	o.BeeSideTree(pos=(1.7,1.2,-29))
	o.BeeSideTree(pos=(-1.7,1.2,-29),m=True)
	o.BeeSideTree(pos=(1.7,1.2,-25.2))
	o.BeeSideTree(pos=(-1.7,1.2,-25.2),m=True)
	o.SnowPlatform(pos=(0,1,-29))
	o.BeeFloor(pos=(1,-.8,-26),t=0)
	o.BeeFloor(pos=(-2.3,2,-23),t=0)
	o.BeeFloor(pos=(2.3,2,-23),t=0)
	o.BeeFloor(pos=(0,-.5,-23.1),t=0)
	o.BeeBigGround(pos=(0,.2,-12),sca=(4,2,20))
	o.TikkiSculpture(pos=(0,1,-32.1),spd=5,rng=.8)
	o.BeeSideWall(pos=(.5,1.3,-16),t=0)
	o.BeeSideWall(pos=(.5,1.3,-12),t=0)
	o.Hive(pos=(.6,1.3,-22.6),bID=21,bMAX=3)


def load_crate():
	return
def load_wumpa():
	return
def load_npc():
	n.spawn(ID=16,POS=(0,0,-57.4))
	n.spawn(ID=16,POS=(0,1.2,-4.3))

## bonus level / gem path
def bonus_zone():
	return
def gem_zone():
	return