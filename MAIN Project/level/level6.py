import objects,map_tools,crate,npc,item,sys,os,_loc,status
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ursina import *

mt=map_tools

st=status
o=objects
LC=_loc
c=crate
n=npc
U=-3

def map_setting():
	LC.LV_DST=(15,20)
	LC.BN_DST=(15,18)
	window.color=color.orange
	scene.fog_density=(15,20)
	scene.fog_color=color.orange
	LC.AMBIENT_LIGHT.color=color.rgb32(190,190,190)
	st.toggle_thunder=False
	st.toggle_rain=False

def start_load():
	load_crate()
	bonus_zone()
	load_object()
	load_wumpa()
	load_npc()
	map_setting()

def load_object():
	o.StartRoom(pos=(0,0,-65))
	o.BonusPlatform(pos=(9,2.7,19.25))
	if not 6 in status.COLOR_GEM:
		item.GemStone(c=6,pos=(0,2.1,-.8))
	o.FallingZone(pos=(0,-1,-40),s=(32,.1,300),v=True)
	#tikki sculpt
	o.TikkiSculpture(pos=(0,0,-54),spd=2,rng=.8)
	o.TikkiSculpture(pos=(0,1.8,7.35),spd=3,rng=.8)
	o.TikkiSculpture(pos=(9,2.5,23.9),spd=4,rng=1)
	#invisible wall
	o.HitBox(pos=(-1.3,0,-39.5),sca=(.3,10,60))
	o.HitBox(pos=(1.3,0,-39.5),sca=(.3,10,60))
	o.HitBox(pos=(-5.1,0,-8),sca=(.3,10,7))
	o.HitBox(pos=(5.1,0,-8),sca=(.3,10,7))
	o.HitBox(pos=(-1.3,0,14.5),sca=(.3,10,40))
	o.HitBox(pos=(1.3,0,7),sca=(.3,10,25))
	o.HitBox(pos=(10.2,0,30),sca=(.3,10,24))
	o.HitBox(pos=(7.8,0,32),sca=(.3,10,18))
	#hives
	o.Hive(pos=(.5,.7,-29.7),bID=21,bMAX=2)
	o.Hive(pos=(.5,1.8,1),bID=22,bMAX=3)
	o.Hive(pos=(9.6,2.4,25.8),bID=23,bMAX=4)
	#mines
	o.LandMine(pos=(0,0,-56.3813))
	o.LandMine(pos=(-.45,.2,-41.7))
	o.LandMine(pos=(0,.7,-28.8))
	o.LandMine(pos=(0.56,.7,-25.9))
	o.LandMine(pos=(-.32,.7,-24.3))
	o.LandMine(pos=(.6,.7,-21.8))
	o.LandMine(pos=(.1,.8,-16.3))
	o.LandMine(pos=(0,.8,-7))
	o.LandMine(pos=(-.2,1.8,2.4))
	o.LandMine(pos=(.5,1.8,3.6))
	o.LandMine(pos=(-.2,1.8,5))
	o.LandMine(pos=(.4,1.8,6.37))
	o.LandMine(pos=(-.1,1.8,9))
	o.LandMine(pos=(.45,1.8,10.69))
	o.LandMine(pos=(-.5,1.8,11.41))
	o.LandMine(pos=(0,1.8,13.33))
	o.LandMine(pos=(0,2.2,19))
	o.LandMine(pos=(9.4,2.41,30.7))
	o.LandMine(pos=(8.6,2.41,33.3))
	#e0
	o.BeeSideBlock(pos=(1.8,.5,-53.8))
	o.BeeSideBlock(pos=(-1.8,.5,-53.8))
	o.BeeSideTree(pos=(1.7,.4,-60))
	o.BeeSideTree(pos=(-1.7,.4,-60),m=True)
	o.BeeSideTree(pos=(1.7,.4,-56.3))
	o.BeeSideTree(pos=(-1.7,.4,-56.3),m=True)
	o.BeeSideWall(pos=(-.5,.8,-45),t=0)
	o.BeeFloor(pos=(0,-1.8,-61.5),t=0)
	o.SnowPlatform(pos=(0,0,-58.5))
	o.SnowPlatform(pos=(0,0,-56.4))
	o.BeeFloor(pos=(0,-1.8,-54),t=0)
	o.BeeFloor(pos=(1,-1.8,-50),t=0)
	o.BeeFloor(pos=(-1,-1.8,-44),t=0)
	o.BeeFloor(pos=(0,-1.6,-41),t=0)
	o.SnowPlatform(pos=(0,0,-47))
	#e1
	o.BeeFloor(pos=(0,-1.2,-38.5),t=0)
	o.BeeFloor(pos=(0,-.8,-35.9),t=0)
	o.BeeFloor(pos=(0,-.8,-31.9),t=0)
	o.BeeSideWall(pos=(-.51,.7,-34),t=0)
	o.BeeBigGround(pos=(0,.2,-25),sca=(4,1,12))
	for stt1 in range(4):
		o.BeeSideTree(pos=(1.7,1,-30+stt1*3.7))
		o.BeeSideTree(pos=(-1.7,1,-30+stt1*3.7),m=True)
	o.BeeSideTree(pos=(1.7,1,-12.4))
	o.BeeSideTree(pos=(-1.7,1,-12.4),m=True)
	o.BeeSideTree(pos=(5.5,1,-8))
	o.BeeSideTree(pos=(-5.5,1,-8),m=True)
	o.BeeSideWall(pos=(-.5,2.6,3.2),t=0)
	o.BeeSideWall(pos=(-.5,2.6,14),t=0)
	#e2
	o.FrontStoneWall(pos=(-4.4,1,-6.1))
	o.FrontStoneWall(pos=(4.4,1,-6.1))
	o.BeeFloor(pos=(-2.2,1,-16),t=0)
	o.BeeFloor(pos=(2.2,1,-16),t=0)
	o.BeeFloor(pos=(0,-1,-15.8),t=0)
	o.BeeFloor(pos=(0,-1,-11.8),t=0)
	o.BeeFloor(pos=(0,-1,-7.8),t=0)
	o.BeeFloor(pos=(-4,-1,-7.8),t=0)
	o.BeeFloor(pos=(4,-1,-7.8),t=0)
	o.BeeFloor(pos=(0,-.7,-4.8),t=1)
	o.BeeFloor(pos=(0,-.3,-2.8),t=1)
	o.BeeFloor(pos=(0,.1,-.8),t=1)
	o.BeeBigGround(pos=(0,1.3,8),sca=(4,1,16))
	o.BeeFloor(pos=(0,.1,17),t=0)
	o.BeeFloor(pos=(0,.4,19),t=0)
	o.BeeFloor(pos=(0,.7,21),t=0)
	o.BeeFloor(pos=(3,.7,21),t=1)
	o.BeeFloor(pos=(6,.7,21),t=1)
	o.BeeFloor(pos=(9,.7,21),t=1)
	o.BeeFloor(pos=(9,.7,24),t=1)
	#e3
	o.BeeSideTree(pos=(-1.8,2.7,19),m=True)
	o.BeeSideTree(pos=(10.7,3.1,21))
	o.BeeSideWall(pos=(8.5,3.4,32.1),t=0)
	o.BeeSideTree(pos=(7.4,3,36.5),m=True)
	o.BeeSideTree(pos=(10.6,3,36.5))
	o.FrontStoneWall(pos=(-1,1.5,22.8))
	o.FrontStoneWall(pos=(4.3,1.5,23))
	o.FrontStoneWall(pos=(13.7,1.5,23))
	o.BeeBigGround(pos=(9,1.91,32),sca=(4,1,16))
	o.EndRoom(pos=(10.1,4.2,43.5),c=color.rgb32(180,160,160))

def load_crate():
	#normals
	mt.crate_wall(ID=2,POS=(-0.7,0.16,-60.8),CNT=[1,2])
	mt.crate_wall(ID=1,POS=(-0.7,0.96,-11.9),CNT=[2,2])
	mt.crate_wall(ID=2,POS=(3.4,0.96,-7.2),CNT=[1,2])
	mt.crate_wall(ID=1,POS=(0.4,1.96,12.3),CNT=[2,2])
	mt.crate_wall(ID=2,POS=(-0.7,1.96,14.5),CNT=[1,2])
	mt.crate_wall(ID=1,POS=(9.8,2.66,21.5),CNT=[1,2])
	mt.crate_plane(ID=1,POS=(-4.3,.96,-8),CNT=[3,3])
	mt.crate_plane(ID=2,POS=(2.6,2.66,20.6),CNT=[1,4])
	mt.crate_plane(ID=1,POS=(8.6,2.57,28.5),CNT=[2,3])
	mt.crate_block(ID=1,POS=(4,.96,-8.4),CNT=[3,3,2])
	c.place_crate(ID=4,p=(0,.8,-17.8))
	c.place_crate(ID=11,p=(.32,.8,-17.8))
	c.place_crate(ID=11,p=(-.32,.8,-17.8))
	c.place_crate(ID=3,p=(.6,.76,-39.1))
	c.place_crate(ID=3,p=(-.4,.96,-15.4))
	c.place_crate(ID=3,p=(-.7,2.66,21.4))
	c.place_crate(ID=3,p=(8.5,4.3,36.4))
	#nitro
	c.place_crate(ID=10,p=(8.5,2.57,36.4))
	c.place_crate(ID=12,p=(.1,.16,-50.9))
	c.place_crate(ID=12,p=(-.3,.16,-47.0))
	c.place_crate(ID=12,p=(-.5,.36,-40.3))
	c.place_crate(ID=12,p=(.6,.36,-41.8))
	c.place_crate(ID=12,p=(-.5,.86,-27.3))
	c.place_crate(ID=12,p=(.6,.86,-23.9))
	c.place_crate(ID=12,p=(-.5,.86,-19.8))
	c.place_crate(ID=12,p=(0,1.26,-5.8))
	c.place_crate(ID=12,p=(-.6,2.36,18.3))
	c.place_crate(ID=12,p=(.7,2.66,20.9))
	c.place_crate(ID=12,p=(3.6,2.66,21.5))
	c.place_crate(ID=12,p=(5.8,2.66,20.3))
	c.place_crate(ID=12,p=(9.8,2.66,21.1))
	c.place_crate(ID=12,p=(9.4,2.57,33.2))
	#aku
	c.place_crate(ID=5,p=(0.7,0.16,-61.0))
	c.place_crate(ID=5,p=(-0.5,1.16,-35.6))
	c.place_crate(ID=5,p=(0.0,2.06,16.7))
	#checkpoints
	c.place_crate(ID=6,p=(0.0,1.16,-31.5))
	c.place_crate(ID=6,p=(0.0,0.96,-7.9))
	c.place_crate(ID=6,p=(9.0,2.66,21.1))
def load_wumpa():
	mt.wumpa_row(POS=(0.6,0.20,-50.8),CNT=4,WAY=1)
	mt.wumpa_row(POS=(-0.4,0.20,-44.8),CNT=4,WAY=1)
	mt.wumpa_row(POS=(0.1,0.80,-39.3),CNT=4,WAY=1)
	mt.wumpa_row(POS=(0.1,0.90,-26.4),CNT=4,WAY=1)
	mt.wumpa_row(POS=(0.1,0.90,-23.1),CNT=4,WAY=1)
	mt.wumpa_row(POS=(0.1,1.00,-12.4),CNT=4,WAY=1)
	mt.wumpa_row(POS=(9.0,2.61,25.8),CNT=4,WAY=1)
	mt.wumpa_row(POS=(9.0,2.61,34.4),CNT=4,WAY=1)
def load_npc():
	n.spawn(ID=16,POS=(-.36,.7,-22.33))
	n.spawn(ID=16,POS=(0,1.5,-2.31))
	n.spawn(ID=16,POS=(0,1.8,9.74))
	n.spawn(ID=16,POS=(3.6,2.5,20.58))
	n.spawn(ID=16,POS=(8.6,2.41,30.33))

## bonus level / gem path
def bonus_zone():
	o.FallingZone(pos=(0,-38.5,0),s=(32,.1,20),v=True)
	Entity(model='quad',color=color.black,scale=(30,12),position=(0,-37,2))
	o.BonusBeeWall(pos=(0,-40,0))
	o.BonusBeeWall(pos=(20,-40,0))
	o.StoneWall(pos=(0,-37.5,U))
	o.StoneWall(pos=(-3,-37,U))
	o.StoneWall(pos=(3,-37.5,U))
	o.StoneWall(pos=(6,-38,U))
	o.StoneWall(pos=(9,-38,U))
	o.BonusPlatform(pos=(10.7,-36.9,U))
	#crates
	mt.bounce_twin(POS=(-3.8,-35.91+.32,U),CNT=1,trs=1.7)
	c.place_crate(ID=11,p=(-3.8,-35.91,U))
	c.place_crate(ID=13,p=(-2.8,-35.91,-3.0),m=41,l=7)
	c.place_crate(ID=8,p=(5.3,-36.91,U))
	c.place_crate(ID=3,p=(5.3,-35.3,U))
	c.place_crate(ID=1,p=(5.3,-35.3+.32,U))
	c.place_crate(ID=2,p=(5.3,-35.3+.64,U))
	c.place_crate(ID=4,p=(5.3,-35.3+.96,U))
	c.place_crate(ID=8,p=(8.9,-36.91,U))
	c.place_crate(ID=9,p=(8.9,-34.8,U),m=41)
	mt.crate_wall(ID=12,POS=(-3.3,-35.91,U),CNT=[1,3])
	mt.crate_wall(ID=12,POS=(5.8,-36.91,U),CNT=[1,3])
	mt.crate_wall(ID=2,POS=(0.7,-36.41,U),CNT=[1,2])
	mt.crate_wall(ID=1,POS=(3.6,-36.41,U),CNT=[1,3])
	mt.crate_wall(ID=4,POS=(6.3,-36.91,U),CNT=[1,2])
	mt.crate_wall(ID=2,POS=(9.7,-36.91,U),CNT=[1,3])
	#wumpa
	mt.wumpa_double_row(POS=(-2.5,-35.87,U),CNT=2)
	mt.wumpa_double_row(POS=(-.9,-36.37,U),CNT=4)
	mt.wumpa_double_row(POS=(2.1,-36.37,U),CNT=3)
	mt.wumpa_double_row(POS=(6.3,-36.87,U),CNT=2)
	mt.wumpa_double_row(POS=(8,-36.87,U),CNT=2)
def gem_zone():
	return