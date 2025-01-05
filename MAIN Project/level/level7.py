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
	o.BonusPlatform(pos=(26,3.5,-37))
	#scene
	o.LabScene(pos=(0,0,-55))
	o.LabScene(pos=(9,0,-54.5))
	o.LabScene(pos=(5,0,-43))
	o.LabScene(pos=(10,.3,-43))
	#e1
	o.spw_lab_tile(p=(0,0,-62),cnt=4,way=1,typ=0)
	o.spw_lab_tile(p=(0,0,-57),cnt=5,way=0,typ=0)
	o.spw_lab_tile(p=(5,.46,-57),cnt=2,way=0,typ=0)
	o.spw_lab_tile(p=(6,.46,-55),cnt=3,way=1,typ=0)
	o.spw_lab_tile(p=(6,.46,-51),cnt=1,way=1,typ=1)
	o.spw_lab_tile(p=(6,.46,-50),cnt=4,way=1,typ=0)
	o.spw_lab_tile(p=(6,.46,-46),cnt=3,way=0,typ=0)
	o.spw_lab_tile(p=(10,.925,-46),cnt=3,way=0,typ=2)
	o.spw_lab_tile(p=(13,1.45,-46),cnt=1,way=0,typ=0)
	o.spw_lab_tile(p=(14,2.03,-46),cnt=1,way=0,typ=0)
	for lab_x in range(4):
		for lab_z in range(3):
			o.spw_lab_tile(p=(15.5+lab_x*2,2.03,-48+lab_z*2),cnt=1,way=0,typ=2)
	o.spw_lab_tile(p=(19.5,2.03,-42),cnt=6,way=1,typ=0)
	o.spw_lab_tile(p=(19.5,2.03,-36),cnt=3,way=0,typ=0)
	o.spw_lab_tile(p=(23,2.5,-36),cnt=1,way=0,typ=0)
	o.spw_lab_tile(p=(24,3.33,-36),cnt=4,way=0,typ=0)
def load_crate():
	return
def load_wumpa():
	return
def load_npc():
	n.spawn(ID=18,POS=(2,.1,-57),DRC=0,RNG=2)

## bonus level / gem path
def bonus_zone():
	return
def gem_zone():
	return