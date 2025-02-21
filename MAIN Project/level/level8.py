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
	LC.AMB_M_COLOR=color.rgb32(210,225,225)
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
	o.EndRoom(pos=(10,2,16),c=color.gray)
	#skybox
	o.ObjType_Background(ID=4,pos=(8,0,300),sca=(400,300),txa=(1,1),col=color.cyan,UL=True)
	#wall
	o.ObjType_Wall(ID=7,pos=(6,0,10),ro_y=180,sca=.5,col=color.dark_gray)
	o.ObjType_Wall(ID=7,pos=(10.5,0,6),ro_y=0,sca=.5,col=color.dark_gray)
	#water
	Entity(model='plane',scale=(256,.19,256),color=color.black,position=(8,.1,-16))
	o.ObjType_Water(ID=5,pos=(8,.2,-16),sca=(32,128),al=1,rot=(0,0,0),col=color.rgb32(0,160,160),frames=0,spd=0,UL=True)
	
	#blocks
	o.spw_block(ID=1,p=(7,-.5,1.5),vx=[5,5],ro_y=180)
	o.spw_block(ID=1,p=(7,-.5,7.5),vx=[5,5],ro_y=180)

def load_crate():
	c.place_crate(ID=1,p=(8,.66,8))
	c.place_crate(ID=2,p=(9,.66,10))

def load_npc():
	n.Firefly(pos=(11,1,8))

def load_wumpa():
	return

def bonus_zone():
	return