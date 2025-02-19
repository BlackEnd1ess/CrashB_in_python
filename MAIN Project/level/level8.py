import objects,map_tools,crate,npc,item,sys,os,_loc,status,danger
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ursina import *

mt=map_tools
st=status
dg=danger
o=objects
LC=_loc
c=crate
n=npc

def map_setting():
	LC.FOG_L_COLOR=color.black
	LC.FOG_B_COLOR=color.black
	LC.SKY_BG_COLOR=color.black
	LC.AMB_M_COLOR=color.rgb32(30,30,30)
	LC.LV_DST=(14,16)
	LC.BN_DST=(10,14)
	st.toggle_thunder=False
	st.toggle_rain=False

def start_load():
	bonus_zone()
	load_crate()
	load_object()
	load_wumpa()
	load_npc()
	map_setting()

def load_object():
	o.StartRoom(pos=(8,.5,-1))
	o.EndRoom(pos=(48,2,120),c=color.gray)
	o.spw_block(ID=0,p=(7,0,1.5),vx=[5,8],ro_y=180)
	n.Firefly(pos=(11,1,8))

def load_crate():
	return

def load_npc():
	return

def load_wumpa():
	return

def bonus_zone():
	return