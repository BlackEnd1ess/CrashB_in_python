import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import objects,map_tools,crate,status,npc
from ursina import *

mt=map_tools
o=objects
r=random
c=crate
n=npc
U=-3

def start_load():
	load_crate()
	bonus_zone()
	load_object()
	load_wumpa()
	load_npc()

def load_object():
	o.StartRoom(pos=(0,1,-64.2))
	o.BonusPlatform(pos=(21.4,5.6,7.7))
	o.spawn_ice_wall(pos=(-2.3,-.5,-58.6),cnt=8,d=0)
	o.spawn_ice_wall(pos=(2.3,-.5,-58.6),cnt=7,d=1)
	o.spawn_ice_wall(pos=(20,4,8),cnt=4,d=0)
	o.spawn_ice_wall(pos=(26,4,8),cnt=2,d=1)
	o.spawn_ice_wall(pos=(45,4,28),cnt=3,d=1)
	o.Water(pos=(12,-.5,-32),sca=(32,128),c=color.cyan,a=1)
	o.Water(pos=(51,4.5,23.5),sca=(64,40),c=color.cyan,a=1)
	Entity(model='quad',scale=(512,512,1),color=color.white,z=64)
	#invisible walls
	o.InvWall(pos=(16.5,9,1.75),sca=(30,15,.5))
	for i_ch in range(50):
		o.IceChunk(pos=(-4-r.uniform(-.5,-1),1.8,-63+i_ch*1.5),rot=(-90,30,0),typ=1)
		if i_ch < 38:
			o.IceChunk(pos=(2.9+r.uniform(.5,1),1.8,-63+i_ch*1.5),rot=(-90,-30,0),typ=1)
	for u_ch in range(20):
		o.IceChunk(pos=(18.2-r.uniform(-.5,-1),6.3,3.7+u_ch*1.5),rot=(-90,30,0),typ=1)
		if u_ch < 11:
			o.IceChunk(pos=(26.5+r.uniform(.5,1),6.3,3.7+u_ch*1.5),rot=(-90,-30,0),typ=1)
	for e_ch in range(20):
		o.IceChunk(pos=(45.4+r.uniform(.5,1),6.3,26+e_ch*1.5),rot=(-90,-30,0),typ=1)
	o.IceChunk(pos=(21.7,6,2.6),typ=1,rot=(-180,-90,0))
	o.IceChunk(pos=(24.4,6,2.6),typ=1,rot=(0,-90,0))
	o.IceChunk(pos=(21.2,5.3,3.2),typ=1,rot=(260,-90,0))
	o.IceChunk(pos=(24.8,5.3,3.2),typ=1,rot=(-80,-90,0))
	o.IceChunk(pos=(28,5.35,28.1),typ=1,rot=(-180,-90,0))
	o.IceChunk(pos=(28,7.8,28),typ=1,rot=(-180,-90,0))
	o.IceChunk(pos=(0,3.3,-60.4),typ=1,rot=(90,-90,0))
	o.IceChunk(pos=(41.7,8.5,38.3),typ=1,rot=(90,-90,0))
	for ict in range(12):
		o.IceChunk(pos=(17+ict*2.5,4.5,43.6),typ=1,rot=(-90,-90,0))
		o.IceChunk(pos=(17.5+ict*2.5,4.7,44.3),typ=1,rot=(-90,-90,0))
		o.IceChunk(pos=(17+ict*2.5,4.9,45.3),typ=1,rot=(-90,-90,0))
	#dangers
	wlO=3.7
	o.WoodLog(pos=(10.5,wlO,2.2))
	o.WoodLog(pos=(8.2,wlO,2.2))
	o.Role(pos=(42.2,6.6,31),di=1)
	o.Role(pos=(42.2,6.6,32),di=0)
	#first pass
	o.mBlock(pos=(0,.8,-59),sca=(3,6))
	o.mBlock(pos=(0,.8,-41),sca=(3,4))
	o.mBlock(pos=(0,.8,-20),sca=(3,4))
	o.mBlock(pos=(0,.8,0),sca=(3,4))
	#2d area
	bz=2.5
	o.mBlock(pos=(1.5,1.2,bz),sca=(6,1))
	o.mBlock(pos=(6,1.5,bz),sca=(1,1))
	o.mBlock(pos=(7.5,2,bz),sca=(2,1))
	o.mBlock(pos=(10.5,2,bz),sca=(2,1))
	o.mBlock(pos=(12,2.5,bz),sca=(1,1))
	o.IceGround(pos=(15,2.125,bz),sca=(5,1))
	o.mBlock(pos=(19,2.5,bz),sca=(3,1))
	o.mBlock(pos=(23,2.5,bz),sca=(2,1))
	o.mBlock(pos=(23,5.25,2.2),sca=(1,1.75))
	o.mBlock(pos=(24.5,3,bz),sca=(1,1))
	o.mBlock(pos=(23,5.25,5.2),sca=(4,4))
	o.mBlock(pos=(23,5.25,23),sca=(2,7))
	o.mBlock(pos=(23.5,5.25,27),sca=(3,1))
	o.mBlock(pos=(31.8,5.248,26.98),sca=(3,1))
	o.mBlock(pos=(42,5.6,32),sca=(4,8))
	o.mBlock(pos=(42,6.2,38),sca=(4,4))
	#pillar
	phe=1.1
	o.pillar_twin(p=(-.75,phe,-56))
	o.pillar_twin(p=(-.75,phe,-42.6))
	o.pillar_twin(p=(-.75,phe,-39))
	o.pillar_twin(p=(-.75,phe,-21.65))
	o.pillar_twin(p=(-.75,phe,-18))
	o.pillar_twin(p=(-.75,phe,-1.8))
	o.pillar_twin(p=(22.25,5.35,7))
	o.pillar_twin(p=(22.25,5.35,19.85))
	o.pillar_twin(p=(22.25,5.35,26.3))
	o.Ropes(pos=(-.5,.7,-56),le=55)
	o.Ropes(pos=(22.5,5.3,7),le=16)
	o.Pillar(pos=(40.25,6.55,38.7))
	o.Pillar(pos=(43.75,6.55,38.7))
	#planks
	_pl=.7
	#bridge1
	o.plank_bridge(pos=(0,_pl,-55),ro_y=0,typ=0,cnt=4,DST=1)
	o.plank_bridge(pos=(0,_pl,-50),ro_y=0,typ=1,cnt=5,DST=1.5)
	#bridge2
	o.plank_bridge(pos=(0,_pl,-38),ro_y=0,typ=0,cnt=2,DST=1)
	o.plank_bridge(pos=(0,_pl,-36),ro_y=0,typ=1,cnt=2,DST=.5)
	o.plank_bridge(pos=(0,_pl,-34),ro_y=0,typ=1,cnt=2,DST=.5)
	o.plank_bridge(pos=(0,_pl,-32),ro_y=0,typ=1,cnt=2,DST=.5)
	o.plank_bridge(pos=(0,_pl,-30),ro_y=0,typ=0,cnt=3,DST=.5)
	o.plank_bridge(pos=(0,_pl,-28),ro_y=0,typ=0,cnt=2,DST=.5)
	o.plank_bridge(pos=(0,_pl,-26),ro_y=0,typ=0,cnt=6,DST=.5)
	o.plank_bridge(pos=(0,_pl,-18),ro_y=0,typ=1,cnt=2,DST=.5)
	o.plank_bridge(pos=(0,_pl,-16),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(0,_pl,-14),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(0,_pl,-12),ro_y=0,typ=1,cnt=4,DST=.5)
	o.plank_bridge(pos=(0,_pl,-10),ro_y=0,typ=0,cnt=3,DST=.5)
	o.plank_bridge(pos=(0,_pl,-8),ro_y=0,typ=1,cnt=2,DST=.5)
	o.plank_bridge(pos=(0,_pl,-6),ro_y=0,typ=1,cnt=2,DST=.5)
	o.plank_bridge(pos=(0,_pl,-4),ro_y=0,typ=1,cnt=2,DST=.5)
	o.plank_bridge(pos=(0,_pl,-3),ro_y=0,typ=0,cnt=1,DST=.5)
	o.plank_bridge(pos=(23,5.3,8.3),ro_y=0,typ=0,cnt=3,DST=.5)
	o.plank_bridge(pos=(23,5.3,11),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(23,5.3,13),ro_y=0,typ=1,cnt=2,DST=.5)
	o.plank_bridge(pos=(23,5.3,15),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(23,5.3,16),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(23,5.3,17),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(23,5.3,18),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(23,5.3,19),ro_y=0,typ=0,cnt=1,DST=.5)
	o.plank_bridge(pos=(25.2,5.3,27),ro_y=90,typ=1,cnt=12,DST=.45)
	#ptf object
	for ptf1 in range(4):
		for ptf2 in range(3):
			o.SnowPlatform(pos=(34+ptf1*1.5,5.8,27+ptf2*1.5))
	#walls
	snz=3
	for snw in range(7):
		o.SnowWall(pos=(-5+snw*5.4,.1,snz))
		o.SnowWall(pos=(-5+snw*5.4,3.2,snz))
	o.SnowWall(pos=(19,6.3,snz))
	o.SnowWall(pos=(27,6.3,snz))
	o.SnowWall(pos=(30,2,38))
	for sna in range(2):
		o.SnowWall(pos=(20+sna*5.4,5,28))
		o.SnowWall(pos=(20+sna*5.4,8.2,28))
	o.EndRoom(pos=(43,8,44),c=color.rgb32(160,160,180))
def load_crate():
	h1=.75+.16
	h2=.925+.16
	h3=5.375+.16
	mt.crate_plane(ID=1,POS=(.5,h2,-58),CNT=[1,2])
	mt.crate_plane(ID=2,POS=(-.7,h2,-57),CNT=[2,2])
	mt.crate_wall(ID=12,POS=(-.3,h2,-18.6),CNT=[3,2])
	c.place_crate(ID=1,p=(0,h1,-54))
	c.place_crate(ID=3,p=(0,h1,-51))
	c.place_crate(ID=2,p=(-.2,h1,-48))
	c.place_crate(ID=5,p=(-.7,h2,-42.1))
	c.place_crate(ID=11,p=(.8,h2,-18.6))
	c.place_crate(ID=12,p=(.2,h2,-15))
	c.place_crate(ID=12,p=(0,h1,-13))
	c.place_crate(ID=12,p=(-.3,h1,-10))
	c.place_crate(ID=12,p=(0,h1,-8))
	c.place_crate(ID=12,p=(-.2,h1,-6))
	c.place_crate(ID=12,p=(0,h1,-4))
	mt.crate_row(ID=2,POS=(18,2.625+.16,2.5),CNT=4,WAY=0)
	mt.crate_row(ID=3,POS=(21,2.6,2.5),CNT=3,WAY=0)
	c.place_crate(ID=8,p=(24.5,3.3,2.5))
	c.place_crate(ID=8,p=(23.7,4.2,2.5))
	mt.crate_plane(ID=1,POS=(21.6,h3,5.4),CNT=[1,3])
	c.place_crate(ID=3,p=(23.2,5.45+.16,13))
	c.place_crate(ID=10,p=(37,h3+.48,30.4))
	c.place_crate(ID=5,p=(7.2,2.125+.16,2.5))
	c.place_crate(ID=5,p=(24.3,h3,5))
	mt.bounce_twin(POS=(24.5,h3,6),CNT=1)
	if not 1 in status.COLOR_GEM:
		c.place_crate(ID=16,p=(.75,.925+.16,-56.7))
	#checkpoints
	c.place_crate(ID=6,p=(-.2,h2,-40))
	c.place_crate(ID=6,p=(3.2,1.325+.16,2.5))
	c.place_crate(ID=6,p=(23,h3,4.2))
	c.place_crate(ID=6,p=(24.4,h3,27))
	mt.crate_wall(ID=14,POS=(-1,1.49,2.5),CNT=[1,2])
	mt.crate_wall(ID=14,POS=(12,2.79,2.5),CNT=[1,1])
	mt.crate_plane(ID=14,POS=(22.7,5.54,21.1),CNT=[2,2])
	mt.crate_wall(ID=4,POS=(37,5.96,27),CNT=[1,1])
	mt.crate_wall(ID=1,POS=(38.4,5.96,30),CNT=[1,1])
	mt.crate_block(ID=1,POS=(42.6,5.88,28.9),CNT=[2,2,2])
def load_wumpa():
	whl=1.2
	mt.wumpa_wall(POS=(0,1.13,-58.7),CNT=[3,2])
	mt.wumpa_wall(POS=(-.2,.95,-53),CNT=[2,1])
	mt.wumpa_wall(POS=(-.2,.95,-44),CNT=[2,1])
	mt.wumpa_wall(POS=(-.2,.95,-37),CNT=[2,1])
	mt.wumpa_plane(POS=(0,.95,-30),CNT=[1,3])
	mt.wumpa_plane(POS=(0,.95,-28),CNT=[1,2])
	mt.wumpa_plane(POS=(0,.95,-26),CNT=[1,5])
	mt.wumpa_double_row(POS=(-.2,1.5,2.5),CNT=3)
	mt.wumpa_double_row(POS=(5.7,1.8,2.5),CNT=2)
	mt.wumpa_double_row(POS=(14,2.85,2.5),CNT=4)
	mt.wumpa_double_row(POS=(22.4,2.85,2.5),CNT=2)
	mt.wumpa_double_row(POS=(26,5.6,27),CNT=5)
	mt.wumpa_wall(POS=(22.7,5.55,18.9),CNT=[2,2])
def load_npc():
	n.spawn(ID=4,POS=(23,5.375,24.3),DRC=2)
	n.spawn(ID=5,POS=(0,.92,1))
	n.spawn(ID=6,POS=(14.5,2.65,2.4))
	n.spawn(ID=5,POS=(31.7,5.35,26.9))

## bonus level / gem path
def bonus_zone():
	o.FallingZone(pos=(0,-40,0),s=(64,1,64))
	for sw in range(5):
		o.SnowWall(pos=(-4+sw*5.4,-33.9,-2.5))
		o.SnowWall(pos=(-4+sw*5.4,-37,-2.5))
		o.SnowWall(pos=(-4+sw*5.4,-40.1,-2.5))
	o.mBlock(pos=(0,-37.4,U),sca=(3,.5,.5))
	o.mBlock(pos=(4,-37.4,U),sca=(3,.5,.5))
	o.mBlock(pos=(8,-37.4,U),sca=(3,.5,.5))
	o.mBlock(pos=(14,-37.4,U),sca=(3,.5,.5))
	mt.crate_row(ID=0,POS=(3.8,-35,U),WAY=0,CNT=8)
	mt.crate_wall(ID=2,POS=(4,-34.68,U),CNT=[2,2])
	c.place_crate(ID=4,p=(5.3,-34.68,U))
	c.place_crate(ID=1,p=(8.3,-36.78,U))
	c.place_crate(ID=1,p=(7.5,-36.1,U))
	c.place_crate(ID=1,p=(7,-35.6,U))
	c.place_crate(ID=9,p=(15,-37,U),m=1)
	c.place_crate(ID=13,p=(4,-37,U),m=1,l=2)
	mt.crate_row(ID=1,POS=(10,-37.32,U),WAY=0,CNT=7)
	mt.crate_row(ID=3,POS=(10.32,-37.64,U),WAY=0,CNT=5)
	mt.wumpa_double_row(POS=(-.5,-37.1,U),CNT=3)
	mt.wumpa_double_row(POS=(10,-36.9,U),CNT=7)
	mt.wumpa_double_row(POS=(2.8,-37.1,U),CNT=3)
	mt.wumpa_double_row(POS=(7,-37.1,U),CNT=3)
	o.BonusPlatform(pos=(16,-37.1,U))