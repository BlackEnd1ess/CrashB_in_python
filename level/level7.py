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
def load_crate():
	return
def load_wumpa():
	return
def load_npc():
	return

## bonus level / gem path
def bonus_zone():
	return
def gem_zone():
	return