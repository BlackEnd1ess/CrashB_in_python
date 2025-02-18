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
	LC.FOG_L_COLOR=color.azure
	LC.FOG_B_COLOR=color.azure
	LC.SKY_BG_COLOR=color.black
	LC.AMB_M_COLOR=color.rgb32(150,150,190)
	LC.LV_DST=(140,160)
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
	o.spw_block(ID=1,p=(7,-.5,1.5),vx=[5,9],ro_y=180)
	o.spw_block(ID=1,p=(9,0,6),vx=[1,1],ro_y=180)

def load_crate():
	mt.crate_wall(ID=11,POS=(8,.66+.32*4,8),CNT=[1,1])
	mt.crate_wall(ID=12,POS=(8,.66,8),CNT=[1,4])

def load_npc():
	return

def load_wumpa():
	return

def bonus_zone():
	return