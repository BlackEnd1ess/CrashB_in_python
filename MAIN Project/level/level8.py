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
U=-3

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
	o.EndRoom(pos=(61.5,2,153),c=color.gray)
	o.BonusPlatform(pos=(35,4.3,61))
	o.GemPlatform(pos=(61.8,2,111.5),t=3)
	#skybox
	o.ObjType_Background(ID=4,pos=(8,10,300),sca=(400,300),txa=(1,1),col=color.cyan,UL=True)
	#wall
	o.ObjType_Wall(ID=7,pos=(6,0,10),ro_y=180,sca=.5,col=color.dark_gray)
	o.ObjType_Wall(ID=7,pos=(10.5,0,6),ro_y=0,sca=.5,col=color.dark_gray)
	o.ObjType_Wall(ID=7,pos=(19,0,44),ro_y=180,sca=.5,col=color.dark_gray)
	o.ObjType_Wall(ID=7,pos=(24.5,0,40),ro_y=0,sca=.5,col=color.dark_gray)
	o.ObjType_Wall(ID=7,pos=(19,0,54),ro_y=180,sca=.5,col=color.dark_gray)
	o.ObjType_Wall(ID=7,pos=(24.5,0,50),ro_y=0,sca=.5,col=color.dark_gray)
	o.ObjType_Wall(ID=7,pos=(15,0,64),ro_y=-90,sca=.5,col=color.dark_gray)
	o.ObjType_Wall(ID=7,pos=(28,0,64),ro_y=-90,sca=.5,col=color.dark_gray)
	o.ObjType_Wall(ID=7,pos=(43,0,65),ro_y=-90,sca=.5,col=color.dark_gray)
	o.ObjType_Wall(ID=7,pos=(54,0,65),ro_y=-90,sca=.5,col=color.dark_gray)
	o.ObjType_Wall(ID=7,pos=(34,0,71),ro_y=-90,sca=.5,col=color.dark_gray)
	o.ObjType_Wall(ID=7,pos=(45,0,71),ro_y=-90,sca=.5,col=color.dark_gray)
	o.ObjType_Wall(ID=7,pos=(56,0,113),ro_y=-90,sca=.5,col=color.dark_gray)
	o.ObjType_Wall(ID=7,pos=(70,0,113),ro_y=-90,sca=.5,col=color.dark_gray)
	o.ObjType_Wall(ID=7,pos=(84,0,113.5),ro_y=-90,sca=.5,col=color.dark_gray)
	#dangers
	dg.Role(pos=(52.5,2.5+.75,84),di=0)
	dg.Role(pos=(52.5,2.5+.75,86),di=1)
	#water
	o.ObjType_Water(ID=5,pos=(8,.2,32),sca=(128,256),al=.96,rot=(0,0,0),col=color.rgb32(0,70,70),frames=0,spd=0,UL=True)
	#ice floor
	icv=color.rgb32(0,140,200)
	o.ObjType_Floor(ID=0,pos=(8,-.5,17),sca=(6,1.9,10),txa=(6,10),col=icv,al=1)
	o.ObjType_Floor(ID=0,pos=(22,-.5,45.5),sca=(6,2,20),txa=(6,20),col=icv,al=1)
	o.ObjType_Floor(ID=0,pos=(38,1.5,67),sca=(7,2,1),txa=(10,1),col=icv,al=1)
	o.ObjType_Floor(ID=0,pos=(47,1.5,67),sca=(10,2,1),txa=(10,1),col=icv,al=1)
	o.ObjType_Floor(ID=0,pos=(52.5,1.5,71.5),sca=(1,2,10),txa=(1,10),col=icv,al=1)
	o.ObjType_Floor(ID=0,pos=(51.5,1.5,92.5),sca=(1,2,1),txa=(1,1),col=icv,al=1)
	o.ObjType_Floor(ID=0,pos=(51.5,1.5,94),sca=(1,2,1),txa=(1,1),col=icv,al=1)
	o.ObjType_Floor(ID=0,pos=(53,1.5,94),sca=(1,2,1),txa=(1,1),col=icv,al=1)
	o.ObjType_Floor(ID=0,pos=(53,1.5,95.5),sca=(1,2,1),txa=(1,1),col=icv,al=1)
	o.ObjType_Floor(ID=0,pos=(53,1.5,97),sca=(.5,2,.5),txa=(1,1),col=icv,al=1)
	o.ObjType_Floor(ID=0,pos=(60.5,-.5,129),sca=(6,1.9,10),txa=(6,10),col=icv,al=1)
	o.ObjType_Floor(ID=0,pos=(60.5,-.5,139),sca=(6,1.9,2),txa=(6,2),col=icv,al=1)
	o.ObjType_Floor(ID=0,pos=(60.5,-.5,144),sca=(1,1.9,8),txa=(1,8),col=icv,al=1)
	o.ObjType_Floor(ID=0,pos=(61.5,-.5,146),sca=(1,1.9,1),txa=(1,1),col=icv,al=1)
	del icv
	#snow ptf
	o.SnowPlatform(pos=(53,1.5,107))
	o.SnowPlatform(pos=(53.4,1.5,108.5))
	o.SnowPlatform(pos=(53,1.5,110))
	o.SnowPlatform(pos=(60.5,.5,135))
	o.SnowPlatform(pos=(60.5,.5,136.5))
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
	o.spw_block(ID=1,p=(34,2,66),vx=[1,2],ro_y=180)
	o.spw_block(ID=1,p=(35,1.75,66.99),vx=[1,1],ro_y=180)
	o.spw_block(ID=1,p=(52.5,1.5,77),vx=[1,2],ro_y=180)
	o.spw_block(ID=1,p=(50.5,1.5,79),vx=[5,4],ro_y=180)
	o.spw_block(ID=1,p=(50.5,1.5,84),vx=[5,1],ro_y=180)
	o.spw_block(ID=1,p=(50.5,1.5,86),vx=[5,1],ro_y=180)
	o.spw_block(ID=1,p=(50.5,1.5,88),vx=[5,3],ro_y=180)
	o.spw_block(ID=1,p=(53,1.5,98.5),vx=[1,3],ro_y=180)
	o.spw_block(ID=1,p=(53,1,101.5),vx=[1,2],ro_y=180)
	o.spw_block(ID=1,p=(53,.5,103.5),vx=[1,3],ro_y=180)
	o.spw_block(ID=1,p=(53,.5,111.5),vx=[4,1],ro_y=180)
	o.spw_block(ID=1,p=(57,0,111.5),vx=[2,1],ro_y=180)
	o.spw_block(ID=1,p=(59,1,111.5),vx=[3,1],ro_y=180)
	o.spw_block(ID=1,p=(60.5,1,112.5),vx=[1,3],ro_y=180)
	o.spw_block(ID=1,p=(60.5,-.5,123),vx=[1,2],ro_y=180)

def load_crate():
	c.place_crate(ID=10,p=(61.6,.45+.16,146.1))
	c.place_crate(ID=8,p=(23.1,1.16,57.1))
	c.place_crate(ID=8,p=(20,2.5+.16,58.1))
	c.place_crate(ID=4,p=(60.5,2,116))
	c.place_crate(ID=2,p=(60.5,1.6,118))
	c.place_crate(ID=1,p=(60.5,1.2,120))
	c.place_crate(ID=1,p=(60.5,.8,122))

def load_npc():
	n.Firefly(pos=(9,1,8))

def load_wumpa():
	return

def bonus_zone():
	o.spw_block(ID=1,p=(-1,-38,U),vx=[3,1],ro_y=180)
	o.spw_block(ID=1,p=(3,-37.5,U),vx=[2,1],ro_y=180)
	o.spw_block(ID=1,p=(7,-41,U),vx=[2,1],ro_y=180)