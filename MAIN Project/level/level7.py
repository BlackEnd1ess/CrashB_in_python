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
	load_object()
	load_wumpa()
	load_npc()
	bonus_zone()

def load_object():
	o.StartRoom(pos=(0,0,-65))
	o.FallingZone(pos=(0,-2,0),s=(128,.3,128))
	o.BonusPlatform(pos=(26,3.2,-37))
	#scene
	o.LabScene(pos=(0,0,-54.5))
	o.LabScene(pos=(9,0,-54.5))
	o.LabScene(pos=(5,0,-43))
	o.LabScene(pos=(10,.3,-43))
	o.LabScene(pos=(19,2,-33))
	o.LabScene(pos=(25,2.4,-33))
	o.LabScene(pos=(31,2.4,-33))
	o.LabScene(pos=(38.5,3,-17.5))
	o.LabScene(pos=(44.5,3,-17.5))
	o.LabScene(pos=(37,3,-27))
	#pistons
	o.Piston(pos=(20.5,2.1+4.2,-36),typ=0,spd=2)
	o.Piston(pos=(29,3.1+4.2,-36),typ=0,spd=2)
	o.Piston(pos=(33,3.1+4.2,-36),typ=0,spd=2)
	#e1
	o.spw_lab_tile(p=(0,0,-62),cnt=4,way=1,typ=0)
	o.spw_lab_tile(p=(0,0,-57),cnt=5,way=0,typ=0)
	o.spw_lab_tile(p=(8,.45,-57),cnt=1,way=0,typ=1)
	o.spw_lab_tile(p=(5,.45,-57),cnt=2,way=0,typ=0)
	o.spw_lab_tile(p=(6,.45,-55),cnt=3,way=1,typ=0)
	o.spw_lab_tile(p=(6,.45,-51),cnt=1,way=1,typ=1)
	o.spw_lab_tile(p=(6,.45,-50),cnt=4,way=1,typ=0)
	o.spw_lab_tile(p=(6,.45,-46),cnt=3,way=0,typ=0)
	o.spw_lab_tile(p=(10,1,-46),cnt=3,way=0,typ=2)
	o.spw_lab_tile(p=(13,1.5,-46),cnt=1,way=0,typ=0)
	o.spw_lab_tile(p=(14,2,-46),cnt=1,way=0,typ=0)
	for lab_x in range(4):
		for lab_z in range(3):
			o.spw_lab_tile(p=(15.5+lab_x*2,2,-48+lab_z*2),cnt=1,way=0,typ=2)
	o.spw_lab_tile(p=(19.5,2,-42),cnt=6,way=1,typ=0)
	o.spw_lab_tile(p=(19.5,2,-36),cnt=3,way=0,typ=0)
	o.spw_lab_tile(p=(23,2.5,-36),cnt=1,way=0,typ=0)
	o.spw_lab_tile(p=(24,3,-36),cnt=4,way=0,typ=0)
	o.spw_lab_tile(p=(29,3,-36),cnt=1,way=0,typ=0)
	o.spw_lab_tile(p=(31,3,-36),cnt=1,way=0,typ=0)
	o.spw_lab_tile(p=(33,3,-36),cnt=3,way=0,typ=0)
	o.spw_lab_tile(p=(37,3,-36),cnt=7,way=1,typ=0)
	o.spw_lab_tile(p=(38,3,-30),cnt=4,way=0,typ=0)
	o.spw_multi_lab_tile(p=(42,3,-31),cnt=[3,3],typ=0,way=0)
	o.spw_lab_tile(p=(43,3,-28),cnt=6,way=1,typ=0)
	o.spw_lab_tile(p=(45,3,-30),cnt=5,way=0,typ=0)
	o.spw_multi_lab_tile(p=(50,3,-31),cnt=[3,3],typ=0,way=0)
	o.spw_lab_tile(p=(51,3,-28),cnt=6,way=1,typ=0)
	o.spw_multi_lab_tile(p=(42,3,-22),cnt=[3,3],typ=0,way=0)
	o.spw_lab_tile(p=(45,3,-21),cnt=5,way=0,typ=0)
	o.spw_multi_lab_tile(p=(50,3,-22),cnt=[3,3],typ=0,way=0)
	o.spw_lab_tile(p=(50,3.3,-19),cnt=3,way=0,typ=0)
	o.spw_lab_tile(p=(50,3.6,-18),cnt=3,way=0,typ=0)
	o.spw_lab_tile(p=(51,3.6,-17),cnt=4,way=1,typ=0)
	o.EndRoom(pos=(52.1,5.3,-8.6),c=color.rgb32(255,100,0))
def load_crate():
	return
def load_wumpa():
	return
def load_npc():
	n.spawn(ID=17,POS=(2,.1,-57),DRC=0,RNG=2)
	n.spawn(ID=19,POS=(7,.6,-46),DRC=0,RNG=1)
	n.spawn(ID=19,POS=(19.5,2.1,-39),DRC=2,RNG=2)
	n.spawn(ID=19,POS=(47,3.1,-21),DRC=0,RNG=3)
	n.spawn(ID=19,POS=(47,3.1,-30),DRC=0,RNG=3)
	n.spawn(ID=17,POS=(43,3.1,-25.6),DRC=2,RNG=3)
	n.spawn(ID=17,POS=(51,3.1,-25.6),DRC=2,RNG=3)

## bonus level / gem path
def bonus_zone():
	o.LabScene(pos=(-2,-38,0))
	o.LabScene(pos=(4,-38,0))
	o.LabScene(pos=(10,-38,0))
	o.LabScene(pos=(16,-38,0))
	o.LabScene(pos=(22,-37.5,0))
	o.LabScene(pos=(28,-37.5,0))
	o.FallingZone(pos=(0,-40,0),s=(64,.3,64))
	o.spw_lab_tile(p=(0,-37.2,U),cnt=3,way=0,typ=0)
	o.spw_lab_tile(p=(4,-36.7,U),cnt=3,way=0,typ=0)
	o.spw_lab_tile(p=(8,-36.7,U),cnt=1,way=0,typ=2)
	o.spw_lab_tile(p=(10,-36.7,U),cnt=1,way=0,typ=2)
	o.spw_lab_tile(p=(11,-37.2,U),cnt=2,way=0,typ=1)
	o.spw_lab_tile(p=(13,-37.2,U),cnt=1,way=0,typ=0)
	o.spw_lab_tile(p=(14,-37.2,U),cnt=2,way=0,typ=1)
	o.spw_lab_tile(p=(16,-37.2,U),cnt=1,way=0,typ=0)
	o.spw_lab_tile(p=(17,-36.7,U),cnt=1,way=0,typ=0)
	o.spw_lab_tile(p=(18,-36.2,U),cnt=4,way=0,typ=0)
	o.BonusPlatform(pos=(22,-36,U))
	o.Piston(pos=(4,-36.6+4.2,U),typ=0,spd=3)
	o.Piston(pos=(6,-36.6+4.2,U),typ=0,spd=3)
	o.Piston(pos=(17,-36.6+4.2,U),typ=0,spd=3)
def gem_zone():
	return