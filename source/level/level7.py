import objects,map_tools,crate,npc,item,status,sys,os,_loc,danger
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
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
	LC.AMB_M_COLOR=color.rgb32(140,140,200)
	LC.LV_DST=(14,16)
	LC.BN_DST=(10,14)
	LC.RCX=12
	LC.RCZ=26
	LC.RCB=6
	st.toggle_thunder=False
	st.toggle_rain=False

def start_load():
	load_crate()
	load_object()
	load_wumpa()
	load_npc()
	bonus_zone()
	map_setting()

def load_object():
	o.StartRoom(pos=(0,0,-65))
	dg.FallingZone(pos=(0,-2,0),s=(300,.3,128))
	o.BonusPlatform(pos=(26,3.2,-37))
	#pipes scene
	o.ObjType_Deco(ID=11,pos=(25,2,-36),sca=.05,rot=(-90,90,0))
	o.ObjType_Deco(ID=11,pos=(1,-1,-57),sca=.05,rot=(-90,90,0))
	o.ObjType_Deco(ID=11,pos=(5,-1,-57),sca=.05,rot=(-90,90,0))
	o.ObjType_Deco(ID=11,pos=(7,-.6,-46),sca=.05,rot=(-90,90,0))
	o.ObjType_Deco(ID=11,pos=(11,.1,-46),sca=.05,rot=(-90,90,0))
	o.ObjType_Deco(ID=11,pos=(20.5,1.1,-36),sca=.05,rot=(-90,90,0))
	o.ObjType_Deco(ID=11,pos=(33.9,2.1,-36),sca=.05,rot=(-90,90,0))
	o.ObjType_Deco(ID=11,pos=(71,2.4,1),sca=.05,rot=(-90,90,0))
	o.ObjType_Deco(ID=11,pos=(81,2.4,1),sca=.05,rot=(-90,90,0))
	o.ObjType_Deco(ID=11,pos=(85,2.4,1),sca=.05,rot=(-90,90,0))
	o.ObjType_Deco(ID=11,pos=(87.6,3.7,1),sca=.05,rot=(-90,90,0))
	o.ObjType_Deco(ID=11,pos=(92,3.7,1),sca=.05,rot=(-90,90,0))
	o.ObjType_Deco(ID=11,pos=(96,3.7,1),sca=.05,rot=(-90,90,0))
	o.ObjType_Deco(ID=11,pos=(99,3.7,1),sca=.05,rot=(-90,90,0))
	#scene
	o.ObjType_Deco(ID=12,pos=(-1.5,0,-58),sca=.04,rot=(-90,75,0))
	o.ObjType_Deco(ID=12,pos=(4.5,0,-53),sca=.04,rot=(-90,75,0))
	o.ObjType_Deco(ID=12,pos=(4.5,0,-50),sca=.04,rot=(-90,75,0))
	o.ObjType_Deco(ID=12,pos=(4.5,0,-47),sca=.04,rot=(-90,75,0))
	o.ObjType_Deco(ID=12,pos=(7.5,0,-53),sca=.04,rot=(-90,105,0))
	o.ObjType_Deco(ID=12,pos=(7.5,0,-50),sca=.04,rot=(-90,105,0))
	o.ObjType_Deco(ID=12,pos=(14,2,-42),sca=.04,rot=(-90,90,0))
	o.ObjType_Deco(ID=12,pos=(16,2,-42),sca=.04,rot=(-90,90,0))
	o.ObjType_Deco(ID=12,pos=(18,2,-42),sca=.04,rot=(-90,90,0))
	o.ObjType_Deco(ID=12,pos=(18,2,-38),sca=.04,rot=(-90,90,0))
	o.ObjType_Deco(ID=12,pos=(21,2,-42),sca=.04,rot=(-90,90,0))
	o.ObjType_Deco(ID=12,pos=(38.5,3,-36),sca=.04,rot=(-90,90,0))
	o.ObjType_Deco(ID=12,pos=(38.5,3,-33),sca=.04,rot=(-90,90,0))
	o.ObjType_Deco(ID=12,pos=(35.5,3,-33),sca=.04,rot=(-90,90,0))
	o.ObjType_Deco(ID=12,pos=(53.5,3,-31),sca=.04,rot=(-90,90,0))
	o.ObjType_Deco(ID=12,pos=(53.5,3,-29),sca=.04,rot=(-90,90,0))
	o.ObjType_Deco(ID=12,pos=(53.5,3,-26),sca=.04,rot=(-90,90,0))
	o.ObjType_Deco(ID=12,pos=(53.5,3,-23),sca=.04,rot=(-90,90,0))
	o.ObjType_Deco(ID=12,pos=(53.5,3,-20),sca=.04,rot=(-90,90,0))
	o.ObjType_Deco(ID=12,pos=(47,3,-25),sca=.04,rot=(-90,90,0))
	o.ObjType_Deco(ID=12,pos=(67.5,2,-6),sca=.04,rot=(-90,90,0))
	o.ObjType_Deco(ID=12,pos=(70.6,2,-6),sca=.04,rot=(-90,90,0))
	o.ObjType_Deco(ID=12,pos=(67.5,2,-3),sca=.04,rot=(-90,90,0))
	o.ObjType_Deco(ID=12,pos=(70.6,2,-3),sca=.04,rot=(-90,90,0))
	o.ObjType_Deco(ID=12,pos=(67.5,2,0),sca=.04,rot=(-90,90,0))
	o.ObjType_Deco(ID=12,pos=(98,4.4,3),sca=.04,rot=(-90,90,0))
	o.ObjType_Deco(ID=12,pos=(102,4.4,3),sca=.04,rot=(-90,90,0))
	o.ObjType_Deco(ID=12,pos=(98.5,4.4,6.4),sca=.04,rot=(-90,90,0))
	o.ObjType_Deco(ID=12,pos=(101.5,4.4,6.4),sca=.04,rot=(-90,90,0))
	o.ObjType_Deco(ID=12,pos=(101.5,4.4,0),sca=.04,rot=(-90,90,0))
	o.ObjType_Wall(ID=6,pos=(0,0,-54.5),sca=.015,ro_y=90)
	o.ObjType_Wall(ID=6,pos=(9,0,-54.5),sca=.015,ro_y=90)
	o.ObjType_Wall(ID=6,pos=(4.4,0,-43),sca=.015,ro_y=90)
	o.ObjType_Wall(ID=6,pos=(10,.3,-43),sca=.015,ro_y=90)
	o.ObjType_Wall(ID=6,pos=(19,2,-33),sca=.015,ro_y=90)
	o.ObjType_Wall(ID=6,pos=(25,2.4,-33),sca=.015,ro_y=90)
	o.ObjType_Wall(ID=6,pos=(31,2.4,-33),sca=.015,ro_y=90)
	o.ObjType_Wall(ID=6,pos=(38.5,3,-17.5),sca=.015,ro_y=90)
	o.ObjType_Wall(ID=6,pos=(44.5,3,-17.5),sca=.015,ro_y=90)
	o.ObjType_Wall(ID=6,pos=(37,3,-27),sca=.015,ro_y=90)
	o.ObjType_Wall(ID=6,pos=(50,3,-11),sca=.015,ro_y=90)
	o.ObjType_Wall(ID=6,pos=(56,3,-11),sca=.015,ro_y=90)
	o.ObjType_Wall(ID=6,pos=(63,2.4,-6),sca=.015,ro_y=90)
	o.ObjType_Wall(ID=6,pos=(72,2.4,-6),sca=.015,ro_y=90)
	o.ObjType_Wall(ID=6,pos=(68,3.2,3.3),sca=.015,ro_y=90)
	o.ObjType_Wall(ID=6,pos=(74,3.2,3.3),sca=.015,ro_y=90)
	o.ObjType_Wall(ID=6,pos=(80,3.2,3.3),sca=.015,ro_y=90)
	o.ObjType_Wall(ID=6,pos=(86,3.2,3.3),sca=.015,ro_y=90)
	o.ObjType_Wall(ID=6,pos=(92,4,3.3),sca=.015,ro_y=90)
	#floating platform
	o.ObjType_Movable(ID=2,pos=(71,2,-9),ptm=2,ptw=1.5)
	o.ObjType_Movable(ID=2,pos=(75,2,-9),ptm=2,ptw=1.5)
	#pistons
	o.ObjType_Block(ID=5,pos=(20.5,2,-36),sca=(.5,.8,.5),typ=1,ro_y=90)
	dg.Piston(pos=(20.5,2.05+4.2,-36),typ=0,spd=2)
	o.ObjType_Block(ID=5,pos=(29,3,-36),sca=(.5,.8,.5),typ=1,ro_y=90)
	dg.Piston(pos=(29,3.05+4.2,-36),typ=0,spd=2)
	o.ObjType_Block(ID=5,pos=(33,3,-36),sca=(.5,.8,.5),typ=1,ro_y=90)
	dg.Piston(pos=(33,3.05+4.2,-36),typ=0,spd=2)
	o.ObjType_Block(ID=5,pos=(59,3.6,-13),sca=(.5,.8,.5),typ=1,ro_y=90)
	dg.Piston(pos=(59,3.65+4.2,-13),typ=0,spd=3)
	o.ObjType_Block(ID=5,pos=(60,3.6,-13),sca=(.5,.8,.5),typ=1,ro_y=90)
	dg.Piston(pos=(60,3.65+4.2,-13),typ=0,spd=3)
	o.ObjType_Block(ID=5,pos=(95,4.5,1),sca=(.5,1.2,.5),typ=1,ro_y=90)
	dg.Piston(pos=(95,4.65+4.2,1),typ=0,spd=4)
	o.ObjType_Block(ID=5,pos=(96,4.5,1),sca=(.5,1.2,.5),typ=1,ro_y=90)
	dg.Piston(pos=(96,4.65+4.2,1),typ=0,spd=4)
	#e pads
	
	dg.LabPad(pos=(74,3.4,1),ID=142)
	dg.LabPad(pos=(75,3.4,1),ID=143)
	dg.LabPad(pos=(77,3.4,1),ID=144)
	dg.LabPad(pos=(78,3.4,1),ID=145)
	dg.LabPad(pos=(91,4.7,1),ID=146)
	dg.LabPad(pos=(93,4.7,1),ID=148)
	#e1
	o.spw_block(ID=5,p=(0,0,-62),vx=[1,4],ro_y=90)
	o.spw_block(ID=5,p=(0,0,-57),vx=[3,1],ro_y=0)
	o.spw_block(ID=5,p=(4,0,-57),vx=[1,1],ro_y=0)
	dg.multi_heat_tile(p=(8,.45,-57),typ=0,ro_y=0,sca=(.5,.8,.5),CNT=[1,1])
	o.spw_block(ID=5,p=(5,.45,-57),vx=[2,1],ro_y=0)
	o.spw_block(ID=5,p=(6,.45,-55),vx=[1,3],ro_y=90)
	dg.multi_heat_tile(p=(6,.45,-51),typ=0,ro_y=90,sca=(.5,.8,.5),CNT=[1,1])
	o.spw_block(ID=5,p=(6,.45,-50),vx=[1,4],ro_y=90)
	o.spw_block(ID=5,p=(6,.45,-46),vx=[3,1],ro_y=0)
	dg.multi_heat_tile(p=(10,1,-46),typ=1,ro_y=0,sca=(.5,.8,.5),CNT=[3,1])
	o.spw_block(ID=5,p=(13,1.5,-46),vx=[1,1],ro_y=0)
	o.spw_block(ID=5,p=(14,2,-46),vx=[1,1],ro_y=0)
	for lab_x in range(3):
		for lab_z in range(2):
			o.spw_block(ID=5,p=(15.5+lab_x*2,2,-46+lab_z*2),vx=[1,1],ro_y=0)
	o.spw_block(ID=5,p=(19.5,2,-42),vx=[1,7],ro_y=90)
	o.spw_block(ID=5,p=(21.5,2,-36),vx=[1,1],ro_y=0)
	o.spw_block(ID=5,p=(23,2.5,-36),vx=[1,1],ro_y=0)
	o.spw_block(ID=5,p=(24,3,-36),vx=[4,1],ro_y=0)
	o.spw_block(ID=5,p=(31,3,-36),vx=[1,1],ro_y=0)
	o.spw_block(ID=5,p=(34,3,-36),vx=[2,1],ro_y=0)
	o.spw_block(ID=5,p=(37,3,-36),vx=[1,3],ro_y=90)
	o.spw_block(ID=5,p=(37,3,-31),vx=[1,2],ro_y=90)
	o.spw_block(ID=5,p=(42,3,-28),vx=[1,1],ro_y=90)
	o.spw_block(ID=5,p=(42,3,-26),vx=[1,1],ro_y=90)
	o.spw_block(ID=5,p=(42,3,-24),vx=[1,1],ro_y=90)
	o.spw_block(ID=5,p=(38,3,-30),vx=[5,1],ro_y=0)
	o.spw_block(ID=5,p=(44,3,-30),vx=[4,1],ro_y=0)
	o.spw_block(ID=5,p=(49,3,-30),vx=[1,1],ro_y=0)
	o.spw_block(ID=5,p=(47,3,-29),vx=[1,4],ro_y=90)
	o.spw_block(ID=5,p=(50,3,-30),vx=[2,2],ro_y=0)
	o.spw_block(ID=5,p=(51,3,-28),vx=[1,6],ro_y=90)
	o.spw_block(ID=5,p=(42,3,-22),vx=[3,3],ro_y=0)
	dg.multi_heat_tile(p=(51,3,-21),typ=1,ro_y=90,sca=(.5,.8,.5),CNT=[1,1])
	o.spw_block(ID=5,p=(47,3,-29),vx=[1,4],ro_y=90)
	o.spw_block(ID=5,p=(51,3.3,-19),vx=[1,1],ro_y=90)
	o.spw_block(ID=5,p=(51,3.6,-18),vx=[1,5],ro_y=90)
	dg.multi_heat_tile(p=(51,3.6,-13),typ=1,ro_y=0,sca=(.5,.8,.5),CNT=[3,1])
	o.spw_block(ID=5,p=(54,3.6,-13),vx=[1,1],ro_y=0)
	dg.multi_heat_tile(p=(55,3.6,-13),typ=1,ro_y=0,sca=(.5,.8,.5),CNT=[4,1])
	o.spw_block(ID=5,p=(61,3.6,-13),vx=[1,1],ro_y=0)
	o.spw_block(ID=5,p=(62,3.6,-13),vx=[1,3],ro_y=90)
	o.spw_block(ID=5,p=(62,3.6,-9),vx=[2,1],ro_y=0)
	o.spw_block(ID=5,p=(63,2,-9),vx=[6,1],ro_y=0)
	o.spw_block(ID=5,p=(69,2,-9),vx=[1,6],ro_y=90)
	o.spw_block(ID=5,p=(73,2,-9),vx=[1,1],ro_y=0)
	o.spw_block(ID=5,p=(77,2,-9),vx=[3,1],ro_y=0)
	o.spw_block(ID=5,p=(77,2,-8),vx=[3,1],ro_y=0)
	o.spw_block(ID=5,p=(77,2,-10),vx=[3,1],ro_y=0)
	o.spw_block(ID=5,p=(69,2.4,-3),vx=[1,2],ro_y=90)
	o.spw_block(ID=5,p=(69,2.9,-1),vx=[1,2],ro_y=90)
	o.spw_block(ID=5,p=(69,3.3,1),vx=[5,1],ro_y=0)
	o.spw_block(ID=5,p=(80,3.3,1),vx=[3,1],ro_y=0)
	o.spw_block(ID=5,p=(84,3.3,1),vx=[3,1],ro_y=0)
	o.spw_block(ID=5,p=(87,4.5,1),vx=[3,1],ro_y=0,typ=2)
	o.spw_block(ID=5,p=(92,4.5,1),vx=[1,1],ro_y=0,typ=2)
	o.spw_block(ID=5,p=(97,4.5,1),vx=[3,1],ro_y=0,typ=2)
	o.spw_block(ID=5,p=(100,4.5,1),vx=[1,6],ro_y=90,typ=2)
	o.spw_block(ID=5,p=(101,4.5,5),vx=[1,1],ro_y=0,typ=2)
	o.EndRoom(pos=(101,6.3,11.5),c=color.rgb32(140,210,230))
def load_crate():
	#iron
	c.place_crate(ID=0,p=(6,.6+.16,-51.3))
	#checkp
	c.place_crate(ID=6,p=(14.2,2.27,-46.1))
	c.place_crate(ID=6,p=(25.0,3.27,-36.0))
	c.place_crate(ID=6,p=(51.0,3.87,-14.1))
	c.place_crate(ID=6,p=(63.0,3.87,-9.1))
	c.place_crate(ID=6,p=(82.1,3.57,1.0))
	#akuaku
	c.place_crate(ID=5,p=(6.1,.72,-57.1))
	c.place_crate(ID=5,p=(35,3.27,-36.1))
	c.place_crate(ID=5,p=(54.2,3.87,-13.0))
	c.place_crate(ID=5,p=(89.1,4.83,.9))
	c.place_crate(ID=10,p=(101,4.83,4.9))
	#default
	c.place_crate(ID=1,p=(89.1,4.83+.32,.9))
	c.place_crate(ID=4,p=(8.9,.8,-46))
	c.place_crate(ID=13,p=(18.3,2.1+.16,-36),m=71,l=2)
	c.place_crate(ID=9,p=(37,2.52+.16,-37),m=71)
	c.place_crate(ID=7,p=(8,.6+.16,-57))
	c.place_crate(ID=11,p=(8-.32,.6+.16,-57))
	mt.crate_row(ID=3,POS=(8,2.5,-57),CNT=2,WAY=2)
	mt.crate_wall(ID=1,POS=(-.1,.27,-58.7),CNT=[1,2])
	mt.crate_wall(ID=2,POS=(-.1+.32,.27,-58.7),CNT=[1,2])
	mt.crate_wall(ID=1,POS=(2.8,-.05,-57),CNT=[2,1])
	mt.crate_wall(ID=14,POS=(17.5,2.27,-46),CNT=[1,2])
	mt.crate_wall(ID=2,POS=(21.8,2.27,-36),CNT=[1,3])
	mt.crate_wall(ID=2,POS=(27.2,3.27,-36),CNT=[1,2])
	mt.crate_wall(ID=2,POS=(36.8,3.27,-29.7),CNT=[1,1])
	mt.crate_wall(ID=2,POS=(46.8,3.27,-25.9),CNT=[1,2])
	mt.crate_wall(ID=2,POS=(42.1,3.27,-20.2),CNT=[1,1])
	mt.crate_wall(ID=2,POS=(62.2,3.87,-13.2),CNT=[1,2])
	mt.crate_wall(ID=1,POS=(62.8,2.27,-9),CNT=[2,2])
	mt.crate_wall(ID=1,POS=(77,2.27,-8.1),CNT=[4,2])
	c.place_crate(ID=8,p=(86,3.4+.16,1))
	mt.crate_wall(ID=1,POS=(100.0,4.83,2.1),CNT=[2,3])
	mt.crate_plane(ID=1,POS=(6.7,.72,-48.5),CNT=[1,3])
	mt.crate_plane(ID=2,POS=(47.2,3.27,-28.4),CNT=[1,3])
	mt.crate_plane(ID=14,POS=(49.8,3.27,-29.2),CNT=[2,2])
	mt.crate_plane(ID=1,POS=(43.4,3.27,-21.9),CNT=[3,2])
	mt.crate_plane(ID=2,POS=(78.0,2.27,-10.0),CNT=[3,3])
	mt.bounce_twin(POS=(19.8,2.27,-44),CNT=1)
	c.place_crate(ID=3,p=(22.9,3.6,-36))
	mt.crate_wall(ID=1,POS=(22.9,5.2,-36),CNT=[1,2])
	mt.bounce_twin(POS=(51.3,3.27,-30.1),CNT=1)
	mt.bounce_twin(POS=(65,3.9,-9),CNT=3)
	mt.crate_block(ID=11,POS=(43.5,3.27,-20.3),CNT=[2,2,2])
	#nitro
	mt.crate_wall(ID=12,POS=(5.6,.72,-54.),CNT=[1,1])
	mt.crate_wall(ID=12,POS=(5.7,.72,-50.1),CNT=[3,1])
	mt.crate_wall(ID=12,POS=(19.5,2.27,-41.6),CNT=[1,1])
	mt.crate_wall(ID=12,POS=(19.7,2.27,-37),CNT=[1,1])
	mt.crate_plane(ID=12,POS=(31.,3.27,-36.3),CNT=[1,2])
	#bridge crates
	c.place_crate(ID=1,p=(37,3.1-.16,-33.3))
	c.place_crate(ID=12,p=(37,3.1-.16,-33.3+.32))
	c.place_crate(ID=3,p=(37,3.1-.16,-33.3+.64))
	c.place_crate(ID=12,p=(37,3.1-.16,-33.3+.96))
	c.place_crate(ID=2,p=(37,3.1-.16,-33.3+1.28))
	c.place_crate(ID=12,p=(37,3.1-.16,-33.3+1.6))
def load_wumpa():
	mt.wumpa_row(POS=(4.8,0.76,-57),CNT=4,WAY=0)
	mt.wumpa_row(POS=(6.1,0.76,-46),CNT=4,WAY=0)
	mt.wumpa_row(POS=(10.1,1.31,-46),CNT=4,WAY=0)
	mt.wumpa_row(POS=(23.7,3.31,-36),CNT=4,WAY=0)
	mt.wumpa_row(POS=(25.4,3.31,-36),CNT=4,WAY=0)
	mt.wumpa_row(POS=(38.0,3.31,-30),CNT=4,WAY=0)
	mt.wumpa_row(POS=(45.0,3.31,-30),CNT=4,WAY=0)
	mt.wumpa_row(POS=(63.9,2.31,-9),CNT=4,WAY=0)
	mt.wumpa_row(POS=(67.0,2.31,-9),CNT=4,WAY=0)
	mt.wumpa_row(POS=(69.0,3.61,1),CNT=4,WAY=0)
	mt.wumpa_row(POS=(71.9,3.61,1),CNT=4,WAY=0)
	mt.wumpa_row(POS=(80.0,3.61,1),CNT=4,WAY=0)
	mt.wumpa_row(POS=(87.0,4.87,1),CNT=4,WAY=0)
	mt.wumpa_row(POS=(91.6,4.87,1),CNT=3,WAY=0)
	mt.wumpa_row(POS=(96.8,4.87,1),CNT=4,WAY=0)
	mt.wumpa_row(POS=(6.0,0.76,-55.1),CNT=4,WAY=1)
	mt.wumpa_row(POS=(6.0,0.76,-49.1),CNT=4,WAY=1)
	mt.wumpa_row(POS=(19.5,2.31,-40.9),CNT=4,WAY=1)
	mt.wumpa_row(POS=(37.0,3.31,-35.9),CNT=4,WAY=1)
	mt.wumpa_row(POS=(51.0,3.31,-28.1),CNT=4,WAY=1)
	mt.wumpa_row(POS=(51.0,3.91,-17.9),CNT=4,WAY=1)
	mt.wumpa_row(POS=(62.0,3.91,-12.6),CNT=4,WAY=1)
	mt.wumpa_row(POS=(69.0,2.31,-7.1),CNT=4,WAY=1)
	mt.wumpa_row(POS=(69.0,2.71,-3.3),CNT=4,WAY=1)
	mt.wumpa_row(POS=(100.0,4.87,3.4),CNT=4,WAY=1)
def load_npc():
	n.spawn(ID=17,POS=(1,.1,-57),DRC=0,RNG=1)
	n.spawn(ID=19,POS=(7,.6,-46),DRC=0,RNG=1)
	n.spawn(ID=19,POS=(19.5,2.1,-39),DRC=2,RNG=1.6)
	n.spawn(ID=17,POS=(51,3.1,-25.6),DRC=2,RNG=3)
	n.spawn(ID=20,POS=(44,3.1,-30),DRC=0)
	n.spawn(ID=20,POS=(49,3.1,-30),DRC=0)

## bonus level / gem path
def bonus_zone():
	dg.FallingZone(pos=(0,-40,0),s=(64,.3,64))
	mt.crate_plane(ID=12,POS=(2.4,-36.93,U-.32),CNT=[1,3])
	mt.crate_plane(ID=12,POS=(5.0,-36.43,U-.32),CNT=[1,3])
	mt.crate_wall(ID=12,POS=(18.5,-35.93,U),CNT=[4,1])
	mt.crate_wall(ID=2,POS=(18.5,-35.93+.32,U),CNT=[4,1])
	mt.crate_wall(ID=12,POS=(21.7,-34.16,U),CNT=[5,1])
	mt.crate_wall(ID=12,POS=(24.4,-34.20,U),CNT=[5,1])
	mt.crate_plane(ID=12,POS=(13.0,-36.93,U-.32),CNT=[1,3])
	mt.crate_plane(ID=12,POS=(35.0,-35.93,U-.32),CNT=[1,3])
	c.place_crate(ID=7,p=(.7,-36.93,U))
	mt.crate_wall(ID=1,POS=(.7,-34.8,U),CNT=[1,3])
	c.place_crate(ID=1,p=(11.6,-36.93,U))
	c.place_crate(ID=2,p=(14.4,-36.93,U))
	c.place_crate(ID=3,p=(27.4,-35.93,U))
	c.place_crate(ID=13,p=(29.6,-34.19,U),m=129,l=2)
	c.place_crate(ID=13,p=(31.9,-34.19,U),m=129,l=4)
	c.place_crate(ID=9,p=(34.5,-35.93,U),m=129)
	c.place_crate(ID=2,p=(34.5,-34.7,U))
	mt.crate_wall(ID=1,POS=(36.0,-35.93,U),CNT=[1,3])
	o.ObjType_Wall(ID=6,pos=(-2,-38,0),sca=.015,ro_y=90)
	o.ObjType_Wall(ID=6,pos=(4,-38,0),sca=.015,ro_y=90)
	o.ObjType_Wall(ID=6,pos=(10,-38,0),sca=.015,ro_y=90)
	o.ObjType_Wall(ID=6,pos=(16,-38,0),sca=.015,ro_y=90)
	o.ObjType_Wall(ID=6,pos=(22,-37.5,0),sca=.015,ro_y=90)
	o.ObjType_Wall(ID=6,pos=(28,-37.5,0),sca=.015,ro_y=90)
	o.ObjType_Wall(ID=6,pos=(34,-37.5,0),sca=.015,ro_y=90)
	o.ObjType_Wall(ID=6,pos=(40,-37.5,0),sca=.015,ro_y=90)
	o.spw_block(ID=5,p=(0,-37.2,U),vx=[3,1],ro_y=0)
	o.spw_block(ID=5,p=(5,-36.7,U),vx=[1,1],ro_y=0)
	dg.multi_heat_tile(p=(8,-36.7,U),typ=1,ro_y=0,sca=(.5,.8,.5),CNT=[1,1])
	dg.multi_heat_tile(p=(10,-36.7,U),typ=1,ro_y=0,sca=(.5,.8,.5),CNT=[1,1])
	dg.multi_heat_tile(p=(11,-37.2,U),typ=0,ro_y=0,sca=(.5,.8,.5),CNT=[2,1])
	o.spw_block(ID=5,p=(13,-37.2,U),vx=[1,1],ro_y=0)
	dg.multi_heat_tile(p=(14,-37.2,U),typ=0,ro_y=0,sca=(.5,.8,.5),CNT=[2,1])
	o.spw_block(ID=5,p=(16,-37.2,U),vx=[1,1],ro_y=0)
	o.spw_block(ID=5,p=(18,-36.2,U),vx=[4,1],ro_y=0)
	o.ObjType_Block(ID=5,pos=(4,-36.7,U),sca=(.5,.8,.5),typ=1,ro_y=90)
	dg.Piston(pos=(4,-36.65+4.2,U),typ=0,spd=3)
	o.ObjType_Block(ID=5,pos=(6,-36.7,U),sca=(.5,.8,.5),typ=1,ro_y=90)
	dg.Piston(pos=(6,-36.65+4.2,U),typ=0,spd=3)
	o.ObjType_Block(ID=5,pos=(17,-36.7,U),sca=(.5,.8,.5),typ=1,ro_y=90)
	dg.Piston(pos=(17,-36.65+4.2,U),typ=0,spd=3)
	o.PistonPlatform(pos=(21.9,-36.4,U),spd=3,pa=1.5)
	o.PistonPlatform(pos=(22.7,-36.4,U),spd=3,pa=1.5)
	o.spw_block(ID=5,p=(23.65,-36.2,U),vx=[1,1],ro_y=0)
	o.PistonPlatform(pos=(24.6,-36.4,U),spd=3,pa=.75)
	o.PistonPlatform(pos=(25.4,-36.4,U),spd=3,pa=.75)
	dg.multi_heat_tile(p=(26.3,-36.2,U),typ=0,ro_y=0,sca=(.5,.8,.5),CNT=[1,1])
	o.spw_block(ID=5,p=(27.3,-36.2,U),vx=[1,1],ro_y=0)
	dg.multi_heat_tile(p=(28.3,-36.2,U),typ=0,ro_y=0,sca=(.5,.8,.5),CNT=[1,1])
	o.PistonPlatform(pos=(29.6,-36.4,U),spd=3,pa=.75)
	o.PistonPlatform(pos=(31.9,-36.4,U),spd=3,pa=.75)
	o.spw_block(ID=5,p=(33,-36.2,U),vx=[4,1],ro_y=0)
	#wumpa
	mt.wumpa_row(POS=(1.1,-36.89,U),CNT=4,WAY=0)
	mt.wumpa_row(POS=(16.0,-36.89,U),CNT=4,WAY=0)
	mt.wumpa_row(POS=(17.9,-35.89,U),CNT=4,WAY=2)
	mt.wumpa_row(POS=(20.0,-35.89,U),CNT=4,WAY=2)
	mt.wumpa_row(POS=(23.6,-35.89,U),CNT=4,WAY=2)
	mt.wumpa_row(POS=(27.3,-35.3,U),CNT=4,WAY=2)
	mt.wumpa_row(POS=(33.0,-35.89,U),CNT=4,WAY=2)
	o.BonusPlatform(pos=(37,-36,U))
def gem_zone():
	return