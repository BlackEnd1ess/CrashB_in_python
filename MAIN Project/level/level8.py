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
	#o.EndRoom(pos=(10,2,16),c=color.gray)
	o.BonusPlatform(pos=(35,4.3,61))
	#skybox
	o.ObjType_Background(ID=4,pos=(8,10,300),sca=(400,300),txa=(1,1),col=color.cyan,UL=True)
	#wall
	o.ObjType_Wall(ID=7,pos=(6,0,10),ro_y=180,sca=.5,col=color.dark_gray)
	o.ObjType_Wall(ID=7,pos=(10.5,0,6),ro_y=0,sca=.5,col=color.dark_gray)
	o.ObjType_Wall(ID=7,pos=(19,0,44),ro_y=180,sca=.5,col=color.dark_gray)
	o.ObjType_Wall(ID=7,pos=(24.5,0,40),ro_y=0,sca=.5,col=color.dark_gray)
	o.ObjType_Wall(ID=7,pos=(19,0,54),ro_y=180,sca=.5,col=color.dark_gray)
	o.ObjType_Wall(ID=7,pos=(24.5,0,50),ro_y=0,sca=.5,col=color.dark_gray)
	#water
	#Entity(model='plane',scale=(256,.19,256),color=color.black,position=(8,.1,-16))
	o.ObjType_Water(ID=5,pos=(8,.2,32),sca=(128,256),al=.96,rot=(0,0,0),col=color.rgb32(0,160,160),frames=0,spd=0,UL=True)
	#ice floor
	o.ObjType_Floor(ID=0,pos=(8,-.5,17),sca=(6,1.9,10),txa=(6,10),col=color.rgb32(0,140,200),al=1)
	o.ObjType_Floor(ID=0,pos=(22,-.5,45.5),sca=(6,2,20),txa=(6,20),col=color.rgb32(0,140,200),al=1)
	o.ObjType_Floor(ID=0,pos=(36,2,67),sca=(10,2,1),txa=(10,1),col=color.rgb32(0,140,200),al=1)
	o.ObjType_Floor(ID=0,pos=(47,2,67),sca=(10,2,1),txa=(10,1),col=color.rgb32(0,140,200),al=1)
	
	o.ObjType_Floor(ID=0,pos=(52.5,2,71.5),sca=(1,2,10),txa=(1,10),col=color.rgb32(0,140,200),al=1)
	#blocks
	o.spw_block(ID=1,p=(7,-.5,1.5),vx=[5,5],ro_y=180)
	o.spw_block(ID=1,p=(7,-.5,7.5),vx=[5,5],ro_y=180)
	o.spw_block(ID=1,p=(11,0,22),vx=[1,1],ro_y=180)
	o.spw_block(ID=1,p=(11,-.25,21),vx=[1,1],ro_y=180)
	o.spw_block(ID=1,p=(13,0,22),vx=[2,1],ro_y=180)
	o.spw_block(ID=1,p=(16,0,22),vx=[2,1],ro_y=180)
	o.spw_block(ID=1,p=(17,0,24),vx=[1,3],ro_y=180)
	o.spw_block(ID=1,p=(18,.5,26),vx=[1,1],ro_y=180)
	o.spw_block(ID=1,p=(19,1,26),vx=[2,1],ro_y=180)
	o.spw_block(ID=1,p=(22,1,26),vx=[1,3],ro_y=180)
	o.spw_block(ID=1,p=(22,.5,30),vx=[1,1],ro_y=180)
	o.spw_block(ID=1,p=(22,0,32),vx=[1,4],ro_y=180)
	o.spw_block(ID=1,p=(20,0,56),vx=[5,2],ro_y=180)
	o.spw_block(ID=1,p=(19,1.5,58),vx=[7,1],ro_y=180)
	o.spw_block(ID=1,p=(19,3,59),vx=[7,1],ro_y=180)
	
	o.spw_block(ID=1,p=(27,3,59),vx=[4,1],ro_y=180)
	o.spw_block(ID=1,p=(32,3,59),vx=[1,1],ro_y=180)
	o.spw_block(ID=1,p=(34,3,59),vx=[1,1],ro_y=180)
	
	o.spw_block(ID=1,p=(34,3,60),vx=[1,3],ro_y=180)
	o.spw_block(ID=1,p=(34,2.5,64),vx=[1,1],ro_y=180)
	o.spw_block(ID=1,p=(34,2,66),vx=[1,1],ro_y=180)
	
	o.spw_block(ID=1,p=(52.5,3.5,77),vx=[1,1],ro_y=180)

def load_crate():
	c.place_crate(ID=8,p=(23.1,1.16,57.1))
	c.place_crate(ID=8,p=(20,2.5+.16,58.1))

def load_npc():
	n.Firefly(pos=(11,1,8))

def load_wumpa():
	return

def bonus_zone():
	return