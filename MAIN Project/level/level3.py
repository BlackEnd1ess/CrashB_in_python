import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import objects,map_tools,status,crate,npc
from ursina.shaders import *
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
	o.StartRoom(pos=(0,0,-32.2))
	o.BonusPlatform(pos=(.85,1.3,.85*8))
	o.InvWall(pos=(-2.5,0,20),sca=(.5,15,140))
	o.InvWall(pos=(2.5,0,20),sca=(.5,15,140))
	#temple
	o.TempleWall(pos=(-2.55,-.3,-1.4),sd=2)
	o.TempleWall(pos=(2.7,-.3,-1.4),sd=1)
	o.TempleWall(pos=(-2.55,.65,56.4),sd=2)
	o.TempleWall(pos=(2.7,.65,56.4),sd=1)
	#tree
	o.TreeScene(pos=(-2.3,2.2,82.5),sca=.0175)
	o.TreeScene(pos=(2.3,2.2,82.5),sca=.0175)
	o.TreeScene(pos=(-3,2.8,84),sca=.0175)
	o.TreeScene(pos=(2.4,2.8,84),sca=.0175)
	o.Bush(pos=(-1,4.2,82),sca=2)
	o.Bush(pos=(0,4.5,82.1),sca=2)
	o.Bush(pos=(1,4.2,82.11),sca=2)
	#stage
	o.WoodStage(pos=(0,.2,-20))
	o.WoodStage(pos=(0,.2,-10))
	o.WoodStage(pos=(0,2,60))
	#platforms
	o.MossPlatform(p=(0,-.3,-24.8),ptm=2)
	o.MossPlatform(p=(0,.1,-23.25),ptm=1)
	o.MossPlatform(p=(0,-.1,-1.3),ptm=0)
	o.MossPlatform(p=(0,.5,0),ptm=0)
	o.MossPlatform(p=(0,-.3,-7),ptm=0)
	o.MossPlatform(p=(-.3,.7,11.5),ptm=2)
	o.MossPlatform(p=(-.85,.5,52.5),ptm=3)
	o.MossPlatform(p=(.85,.5,52.5),ptm=0)
	o.MossPlatform(p=(0,1,56.5),ptm=0)
	o.MossPlatform(p=(0,1.55,77.3),ptm=3)
	#blocks
	tH=-.2
	#e0
	o.multi_tile(p=(0,tH,-29),cnt=[1,1])
	o.StoneTileBig(pos=(0,tH,-27.3))
	o.multi_tile(p=(-1,tH,-17),cnt=[3,1])
	o.StoneTileBig(pos=(0,tH,-14.5))
	o.multi_tile(p=(0,tH,-5),cnt=[1,4])
	#e1
	nh=1.09
	o.multi_tile(p=(.85,tH+nh,0),cnt=[1,6])
	o.multi_tile(p=(-.85,tH+nh,2),cnt=[1,1])
	o.multi_tile(p=(-.85,tH+nh,.85*5),cnt=[2,1])
	o.multi_tile(p=(-.85,tH+nh,.85*5),cnt=[1,8])
	o.multi_tile(p=(0,tH+nh,.85*8),cnt=[2,1])
	o.multi_tile(p=(0,tH+nh,13),cnt=[1,3])
	o.StoneTile(pos=(0,tH+nh,17))
	o.StoneTile(pos=(0,tH+nh,19))
	o.multi_tile(p=(-.85,tH+nh,23),cnt=[2,1])
	o.multi_tile(p=(0,tH+nh,26),cnt=[2,1])
	o.multi_tile(p=(-.85,tH+nh,29),cnt=[2,1])
	o.multi_tile(p=(0,tH+nh,32),cnt=[1,2])
	o.StoneTileBig(pos=(0,tH+nh,41.3))
	o.multi_tile(p=(.85,tH+nh,40.5+.85*4),cnt=[1,3])
	o.multi_tile(p=(-.85,tH+nh,40.5+.85*7),cnt=[3,1])
	o.multi_tile(p=(-.85,tH+nh,40.5+.85*8),cnt=[1,4])
	#e3
	lb=1.79
	o.multi_tile(p=(0,1.72,57.4),cnt=[1,1])
	o.multi_tile(p=(0,lb,66.5),cnt=[1,3])
	o.multi_tile(p=(0,lb,66.5+.85*7),cnt=[1,4])
	o.multi_tile(p=(0,lb,80),cnt=[1,5])
	o.multi_tile(p=(.85,lb,80+.85),cnt=[1,1])
	#waterflow
	o.WaterFlow(pos=(0,-.3,-16),sca=(5,32))
	o.WaterFlow(pos=(0,.7,30),sca=(5,62))
	o.WaterFlow(pos=(0,1.7,73),sca=(5,32))
	#waterfall
	o.WaterFall(pos=(0,.2,-1))
	o.WaterFall(pos=(0,1.2,57))
	#scene
	o.SceneWall(pos=(-2.8,.3,-18),typ=1)
	o.SceneWall(pos=(2.8,.3,-18),typ=2)
	o.SceneWall(pos=(-2.8,.3,-4),typ=1)
	o.SceneWall(pos=(2.8,.3,-4),typ=2)
	o.SceneWall(pos=(-2.8,1.3,9.5),typ=1)
	o.SceneWall(pos=(2.8,1.3,9.5),typ=2)
	o.SceneWall(pos=(-2.8,1.3,23.5),typ=1)
	o.SceneWall(pos=(2.8,1.3,23.5),typ=2)
	o.SceneWall(pos=(-2.8,1.3,37.5),typ=1)
	o.SceneWall(pos=(2.8,1.3,37.5),typ=2)
	o.SceneWall(pos=(-2.8,1.3,51.5),typ=1)
	o.SceneWall(pos=(2.8,1.3,51.5),typ=2)
	o.SceneWall(pos=(-2.8,2.3,65.5),typ=1)
	o.SceneWall(pos=(2.8,2.3,65.5),typ=2)
	o.SceneWall(pos=(-2.8,2.3,79.5),typ=1)
	o.SceneWall(pos=(2.8,2.3,79.5),typ=2)
	o.EndRoom(pos=(1,3.7,88),c=color.rgb32(200,210,200))
	Entity(model='quad',color=color.black,scale=(100,20),position=(0,-10,95))
def load_crate():
	if not 5 in status.COLOR_GEM:
		c.place_crate(ID=16,p=(0,.24+.16,-21))
	#crate
	u0=.82
	mt.crate_wall(ID=1,POS=(.5,.1,-27.1),CNT=[1,2])
	mt.crate_wall(ID=1,POS=(-1.4,.24+.16,-21.6),CNT=[1,2])
	c.place_crate(ID=4,p=(1.2,.24+.16,-21.4))
	mt.crate_plane(ID=2,POS=(-.85,-.05+.16,-15),CNT=[1,2])
	mt.bounce_twin(POS=(1.6,.24+.16,-11.5),CNT=1)
	mt.crate_wall(ID=2,POS=(-.2,.16,-3.8),CNT=[2,1])
	mt.crate_wall(ID=1,POS=(.65,1.05+.16,2.5),CNT=[2,1])
	mt.crate_row(ID=1,POS=(0,u0,19.7),CNT=6,WAY=1)
	mt.crate_wall(ID=1,POS=(1.6,2.2,58.4),CNT=[1,3])
	mt.crate_wall(ID=14,POS=(.7,.125,-17),CNT=[1,2])
	c.place_crate(ID=14,p=(-.8,1.21,2))
	c.place_crate(ID=1,p=(0,u0,24.5))
	c.place_crate(ID=2,p=(0,u0,27.5))
	c.place_crate(ID=3,p=(0,u0+.32,27.5))
	c.place_crate(ID=1,p=(0,u0,30.5))
	c.place_crate(ID=2,p=(0,u0,34.5))
	c.place_crate(ID=3,p=(0,u0,35.5))
	c.place_crate(ID=1,p=(-1,u0,35.5))
	c.place_crate(ID=2,p=(-1,u0,36.5))
	c.place_crate(ID=1,p=(-1,u0,37.5))
	c.place_crate(ID=3,p=(0,u0,37.5))
	c.place_crate(ID=1,p=(0,u0,38.5))
	c.place_crate(ID=4,p=(0,u0,39.5))
	c.place_crate(ID=2,p=(-1.4,.24+.16,-11.5))
	mt.crate_plane(ID=1,POS=(-.4,u0,44),CNT=[2,3])
	mt.crate_plane(ID=1,POS=(.3,u0,48),CNT=[2,2])
	c.place_crate(ID=9,p=(1.3,1.16,52.4),m=1)
	for _c in range(10):
		c.place_crate(ID=13,p=(0,u0,52.4+.32*_c),m=1,l=0)
	mt.crate_plane(ID=1,POS=(0,1.8,70),CNT=[1,3])
	c.place_crate(ID=10,p=(.85,1.97+.16,80.85))
	mt.crate_wall(ID=1,POS=(-.175,1.05+.16,14.5),CNT=[2,1])
	mt.crate_row(ID=1,POS=(-.85,1.05+.16,40.4),CNT=2,WAY=1)
	c.place_crate(ID=7,p=(-1,2.04+.16,58.4))
	mt.crate_row(ID=1,POS=(-1,4.5,58.4),CNT=4,WAY=2)
	mt.bounce_twin(POS=(1,2.04+.16,58.4),CNT=1)
	#aku
	c.place_crate(ID=5,p=(-.85,1.05+.16,9.3))
	#checkpoints
	c.place_crate(ID=6,p=(0,.24+.16,-9.2))
	c.place_crate(ID=6,p=(0,1.05+.16,32.8))
	c.place_crate(ID=6,p=(.85,1.05+.16,44.6))
	c.place_crate(ID=6,p=(0,2.04+.16,58.5))
def load_wumpa():
	mt.wumpa_row(POS=(0,.15,-28.3),CNT=2,WAY=1)
	mt.wumpa_row(POS=(0,.44,-20.4),CNT=3,WAY=1)
	mt.wumpa_row(POS=(0,.44,-11),CNT=2,WAY=1)
	mt.wumpa_row(POS=(.9,1.25,-.2),CNT=3,WAY=1)
	mt.wumpa_row(POS=(-.8,1.25,5),CNT=4,WAY=1)
	mt.wumpa_row(POS=(0,1.18,19.7),CNT=2,WAY=1)
	mt.wumpa_row(POS=(.8,1.25,42.1),CNT=3,WAY=1)
	mt.wumpa_row(POS=(-.8,1.25,47.2),CNT=3,WAY=1)
	mt.wumpa_row(POS=(0,1.18,52.4),CNT=4,WAY=1)
	mt.wumpa_row(POS=(0,2.15,66.4),CNT=2,WAY=1)
	mt.wumpa_row(POS=(0,2.15,72.4),CNT=2,WAY=1)
	mt.wumpa_row(POS=(0,2.15,79.9),CNT=2,WAY=1)
	mt.wumpa_row(POS=(-.6,.44,-11.4),CNT=5,WAY=0)
	mt.wumpa_row(POS=(-.2,1.25,6.8),CNT=2,WAY=0)
	mt.wumpa_row(POS=(-.3,1.25,46.4),CNT=4,WAY=0)
	mt.wumpa_row(POS=(-.7,.15,-17),CNT=4,WAY=0)
	mt.wumpa_plane(POS=(.5,.15,-15.1),CNT=[1,3])
	mt.wumpa_plane(POS=(0,.15,-5.2),CNT=[1,3])
	mt.wumpa_plane(POS=(0,1.25,40.5),CNT=[3,3])
def load_npc():
	n.Hippo(POS=(0,1.8,64.7))
	n.Hippo(POS=(0,1.8,63))
	n.spawn(ID=7,POS=(-.85,1.05,29))
	n.spawn(ID=7,POS=(.85,1.05,25.8))
	n.spawn(ID=7,POS=(-.85,1.05,23))
	n.spawn(ID=7,POS=(0,1.05,41.4))
	n.spawn(ID=7,POS=(0,1.95,74.1))
	n.spawn(ID=2,POS=(0,1.05,4.2))

## bonus level / gem path
def bonus_zone():
	bn_bg='res/background/bg_woods.png'
	Entity(model='quad',texture=bn_bg,position=(0,-45,34.9),scale=(100,20,.1),color=color.rgb32(100,140,100),texture_scale=(7,1),unlit=False,shader=unlit_shader)
	Entity(model='quad',texture=bn_bg,position=(0,-60,34.8),scale=(100,40,.1),color=color.rgb32(120,160,120),texture_scale=(7,1),unlit=False,shader=unlit_shader)
	o.BonusBackground(pos=(10,-40,35),sca=(80,35))
	mt.wumpa_double_row(POS=(12.8,-35,U),CNT=6)
	mt.wumpa_double_row(POS=(-.5,-36.5,U),CNT=4)
	mt.wumpa_row(POS=(1.5,-36.35,U),CNT=3,WAY=0)
	mt.wumpa_row(POS=(3.5,-35.35,U),CNT=3,WAY=0)
	mt.wumpa_row(POS=(5.5,-34.85,U),CNT=3,WAY=0)
	mt.wumpa_row(POS=(17.5,-35.35,U),CNT=3,WAY=0)
	o.FallingZone(pos=(0,-40,0),s=(64,1,64))
	o.MushroomTree(pos=(2,-39,U+1.2))
	o.MushroomTree(pos=(4,-39,U+1.2))
	o.MushroomTree(pos=(6,-38.5,U+1.2))
	mt.crate_row(ID=0,POS=(-1,-37,U),WAY=0,CNT=7)
	mt.bounce_twin(POS=(7.2,-36,U),CNT=5,trs=1.65)
	o.MushroomTree(pos=(9.5,-38.5,U+1.2))
	o.MushroomTree(pos=(10.5,-38,U+1.2))
	o.MushroomTree(pos=(11.5,-38,U+1.2))
	o.BonusScene(pos=(-5,-43,4))
	o.BonusScene(pos=(8,-43,3.9))
	o.BonusScene(pos=(21,-43,3.9))
	o.BonusScene(pos=(-3,-44,6))
	o.BonusScene(pos=(6,-44,5.9))
	o.BonusScene(pos=(19,-44,6))
	c.place_crate(ID=11,p=(12.5,-36,U))
	mt.crate_row(ID=12,POS=(12.82,-36,U),WAY=0,CNT=7)
	mt.crate_row(ID=1,POS=(12.82,-35.68,U),WAY=0,CNT=7)
	o.MushroomTree(pos=(16,-38,U+1.2))
	o.MushroomTree(pos=(18,-38,U+1.2))
	mt.crate_wall(ID=1,POS=(16,-35.65+.16,U+.1),CNT=[2,2])
	c.place_crate(ID=2,p=(4,-36.65+.16,U+.1))
	c.place_crate(ID=4,p=(5.8,-35.1,U))
	mt.crate_row(ID=2,POS=(10.4,-35.65+.16,U+.1),CNT=4,WAY=0)
	o.BonusPlatform(pos=(19.3,-35.7,U))