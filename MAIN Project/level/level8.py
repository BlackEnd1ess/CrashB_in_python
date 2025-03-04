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
	LC.AMB_M_COLOR=color.rgb32(10,20,20)
	LC.LV_DST=(14,16)
	LC.BN_DST=(10,14)
	LC.RCX=12
	LC.RCB=8
	LC.RCZ=25
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
	o.EndRoom(pos=(61.5,2,153),c=color.light_gray)
	o.BonusPlatform(pos=(35,4.3,61))
	o.GemPlatform(pos=(61.8,2,111.5),t=3)
	#skybox
	o.ObjType_Background(ID=4,pos=(8,10,200),sca=(400,300),txa=(1,1),col=color.rgb32(50,100,100),UL=True)
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
	o.ObjType_Wall(ID=7,pos=(49.5,1.8,86.5),ro_y=180,sca=.5,col=color.dark_gray)
	o.ObjType_Wall(ID=7,pos=(55.5,1.8,82.5),ro_y=0,sca=.5,col=color.dark_gray)
	o.ObjType_Wall(ID=7,pos=(57,-.5,131.5),ro_y=180,sca=.5,col=color.dark_gray)
	o.ObjType_Wall(ID=7,pos=(64,-.5,127.5),ro_y=0,sca=.5,col=color.dark_gray)
	#dangers
	dg.Role(pos=(52.5,2.5+.75,84),di=0)
	dg.Role(pos=(52.5,2.5+.75,86),di=1)
	#water
	o.ObjType_Water(ID=5,pos=(8,.2,90),sca=(128,180),al=.96,rot=(0,0,0),col=color.rgb32(0,65,65),frames=0,spd=0,UL=True)
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
	mt.crate_row(ID=12,POS=(7.0,0.61,12.6),WAY=0,CNT=4)
	mt.crate_row(ID=12,POS=(9.5,0.61,17.3),WAY=0,CNT=4)
	mt.crate_row(ID=12,POS=(20.0,0.66,40.7),WAY=0,CNT=4)
	mt.crate_row(ID=12,POS=(22.0,0.66,44.6),WAY=0,CNT=4)
	mt.crate_row(ID=12,POS=(20.1,0.66,48.3),WAY=0,CNT=4)
	mt.crate_row(ID=12,POS=(22.0,0.66,52.5),WAY=0,CNT=4)
	c.place_crate(ID=12,p=(12.8,1.16,22.2))
	c.place_crate(ID=12,p=(13.7,1.16,21.7))
	c.place_crate(ID=12,p=(16.6,1.16,22.2))
	c.place_crate(ID=12,p=(36.7,2.66,66.8))
	c.place_crate(ID=12,p=(38.8,2.66,67.4))
	c.place_crate(ID=12,p=(40.7,2.66,66.8))
	c.place_crate(ID=12,p=(44.0,2.66,66.8))
	c.place_crate(ID=12,p=(51.1,2.66,66.8))
	c.place_crate(ID=12,p=(52.3,2.66,69.1))
	c.place_crate(ID=12,p=(52.7,2.66,72.7))
	c.place_crate(ID=12,p=(52.3,2.66,75.7))
	c.place_crate(ID=12,p=(42.2,2.66,67.3))
	c.place_crate(ID=12,p=(53.3,2.66,93.7))
	c.place_crate(ID=12,p=(51.1,2.66,94.3))
	c.place_crate(ID=12,p=(60.3,0.61,142.3))
	c.place_crate(ID=12,p=(60.7,0.61,142.3))
	#checkp
	c.place_crate(ID=6,p=(22.0,1.16,34.7))
	c.place_crate(ID=6,p=(34.0,3.16,67.0))
	c.place_crate(ID=6,p=(53.3,2.66,79.5))
	c.place_crate(ID=6,p=(53.0,1.66,105.3))
	c.place_crate(ID=6,p=(60.5,2.16,111.5))
	#aku
	c.place_crate(ID=5,p=(7.9,0.66,11.3))
	c.place_crate(ID=5,p=(21.3,0.66,40.1))
	c.place_crate(ID=5,p=(51.2,2.66,81.5))

def load_npc():
	n.Firefly(pos=(9,1,8))
	n.Firefly(pos=(18,1.50,26.0))
	n.Firefly(pos=(21.1,1,44.3))
	n.Firefly(pos=(32,4,59))
	#enemies
	n.spawn(ID=4,POS=(8.2,0.50,9.4),DRC=0,RNG=1)
	n.spawn(ID=4,POS=(19.5,2.00,25.9),DRC=0,RNG=1)
	n.spawn(ID=5,POS=(21.6,0.50,42.3),DRC=0,RNG=1)
	n.spawn(ID=4,POS=(21.8,0.50,46.5),DRC=0,RNG=1)
	n.spawn(ID=6,POS=(21.7,0.50,50.4),DRC=0,RNG=1)
	n.spawn(ID=4,POS=(21.7,1.00,56.4),DRC=0,RNG=1)
	n.spawn(ID=6,POS=(28.4,4.00,59.1),DRC=0,RNG=1)
	n.spawn(ID=4,POS=(47.9,2.50,67.1),DRC=0,RNG=1)
	n.spawn(ID=5,POS=(52.6,2.50,89.0),DRC=0,RNG=1)
	n.spawn(ID=4,POS=(60.5,0.45,127.2),DRC=0,RNG=1)
	n.spawn(ID=5,POS=(60.5,0.45,129.4),DRC=0,RNG=1)
	n.spawn(ID=4,POS=(60.5,0.45,131.9),DRC=0,RNG=1)
	n.spawn(ID=4,POS=(60.5,0.45,139.5),DRC=0,RNG=1)
	n.spawn(ID=5,POS=(17.0,1.00,24.8),DRC=2,RNG=1)
	n.spawn(ID=5,POS=(22.0,2.00,27.0),DRC=2,RNG=1)

def load_wumpa():
	return

def bonus_zone():
	o.ObjType_Wall(ID=7,pos=(0,-38,0),ro_y=-90,sca=.5,col=color.dark_gray)
	o.ObjType_Wall(ID=7,pos=(11,-38,0),ro_y=-90,sca=.5,col=color.dark_gray)
	o.spw_block(ID=1,p=(-1,-38,U),vx=[3,1],ro_y=180)
	o.spw_block(ID=1,p=(3,-37.5,U),vx=[2,1],ro_y=180)
	o.spw_block(ID=1,p=(7,-41,U),vx=[2,1],ro_y=180)
	o.spw_block(ID=1,p=(10,-40,U),vx=[3,1],ro_y=180)