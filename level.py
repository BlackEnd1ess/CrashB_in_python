import crate,objects,_core,status,environment,bonus_level,sound,item,npc,map_tools
from ursina import *

mt=map_tools
bn=bonus_level
env=environment
cc=_core
o=objects
c=crate
N=npc

##level loaded
def free_level():
	cc.check_cstack()
	status.loading=False
	cc.level_ready=True

##levels
def developer_level():
	status.level_index=6
	env.env_switch(env='day',wth=1,tdr=0)
	status.loading=True
	o.StartRoom(pos=(0,0,-16.2))##start
	o.RewardRoom(pos=(0,1,15),c=color.rgb(80,100,80))##reward
	o.EndRoom(pos=(0,1.5,27),c=color.rgb(80,100,80))##end
	o.MapTerrain(MAP='map/0.png',size=(8,1,64),t='white_cube',co=color.rgb(150,150,150))
	o.BonusPlatform(pos=(-2,0,-1))
	for CC in range(14):
		c.place_crate(ID=CC,p=(-3+CC/2,0,2),m=1,l=1)
		c.place_crate(ID=CC,p=(-3+CC/2,1.6,2),m=2,l=1)
	for GS in range(6):
		item.GemStone(pos=(-3+GS/2,.25,3),c=GS)
	item.EnergyCrystal(pos=(0,.5,3)) ##crystal
	for MM in range(12):
		npc.spawn(pos=(0,0,5+MM),mID=MM,mDirec=0,mTurn=0)
	for TR in range(3):
		item.TimeRelic(pos=(1+TR/2,.25,3),t=TR)
	mt.wumpa_double_row(POS=(-3,0,1),CNT=20)
	for gPL in range(6):
		o.GemPlatform(pos=(-2+gPL,.25,-5),t=gPL)
	sound.LevelMusic(T=1)
	invoke(free_level,delay=1)

def test():
	status.level_index=1
	status.loading=True
	o.StartRoom(pos=(-.5,0,-8.2))##start
	cc.preload_items()
	o.MapTerrain(MAP='map/0.png',size=(32,1,32),t='grass',co=color.rgb(130,150,130))
	o.CrateScore(pos=(-1,.25,-1))
	sound.LevelMusic(T=status.level_index)
	#mt.crate_row(ID=1,POS=(0,0,-1),CNT=5,WAY=2)
	#mt.crate_row(ID=1,POS=(1,0,-1),CNT=5,WAY=2)
	#mt.crate_row(ID=1,POS=(2,0,-1),CNT=5,WAY=2)
	o.BigPlatform(p=(0,1,4),s=(1,0,1))
	#mt.crate_row(ID=2,POS=(-1,0,-2),CNT=4,WAY=0)
	invoke(free_level,delay=1)

def level1():
	TS=16
	status.level_index=1
	status.loading=True
	cG=color.green
	sound.LevelMusic(T=status.level_index)
	o.MapTerrain(MAP='map/'+str(status.level_index)+'.png',size=(TS/1.6,1.5,TS*8),t='grass',co=color.rgb(0,70,0))
	o.Water(pos=(0,.6,0),s=(10,128),c=color.rgb(40,40,60),a=.8)
	o.StartRoom(pos=(-.3,1,-64.2))
	o.InvWall(pos=(-5,.5,-64),sca=(5.,10,200))
	o.InvWall(pos=(4.7,.5,-64),sca=(5.,10,200))
	o.BonusPlatform(pos=(1.5,1.4,-7))
	bn.load_bonus_level(status.level_index)
	bn.gem_route1()
	env.env_switch(env='woods',wth=1,tdr=0)
	#plants
	o.TreeScene(pos=(-1.37,1.5,-46),c=color.rgb(110,130,100),s=.0175)
	o.TreeScene(pos=(1.32,1.5,-46),c=color.rgb(110,130,100),s=.0175)
	o.TreeScene(pos=(0,1.7,-26.4),c=color.rgb(110,130,100),s=.0175)
	o.TreeScene(pos=(0,1.5,-2.7),c=color.rgb(110,130,100),s=.02)
	o.TreeScene(pos=(3,1.7,10.6),c=color.rgb(110,130,100),s=.02)
	o.TreeScene(pos=(-2.5,1.7,10.6),c=color.rgb(110,130,100),s=.02)
	for trE in range(10):
		o.TreeScene(pos=(0+random.uniform(-.1,.1),.7,-2+trE),c=color.rgb(110,130,100),s=.02)
	o.spawn_tree_wall(pos=(-4.6,2.73,-64),cnt=48,d=0)
	o.spawn_tree_wall(pos=(-5.7,2,-63),cnt=48,d=0)
	o.spawn_tree_wall(pos=(3.6,2.73,-64),cnt=48,d=1)
	o.spawn_tree_wall(pos=(4.5,2,-64),cnt=48,d=1)
	o.bush(pos=(.37,1.3,-26.5),s=2,c=color.orange)
	o.bush(pos=(1.5,1.4,-14.2),s=2,c=cG)
	o.bush(pos=(-1.5,1.4,-14.2),s=2,c=color.orange)
	o.bush(pos=(-1,1.4,-12),s=2,c=cG)
	o.bush(pos=(1,1.4,-12),s=2,c=color.orange)
	o.bush(pos=(2.43,1.4,10.7),s=3,c=cG)
	o.bush(pos=(-2.37,1.4,10.7),s=3,c=color.yellow)
	o.TreeScene(pos=(-.9,1.8,19.3),c=color.rgb(110,130,100),s=.02)
	o.TreeScene(pos=(1.2,1.8,19.3),c=color.rgb(110,130,100),s=.02)
	o.bush(pos=(2.43,1.4,23),s=3,c=cG)
	o.bush(pos=(-2.37,1.4,23),s=3,c=color.yellow)
	#platform grass
	o.bush(pos=(-1,1.1,-45.3),s=(1.2,.5,.1),c=cG)
	o.bush(pos=(.7,1.1,-45.3),s=(1.2,.5,.1),c=cG)
	o.bush(pos=(-1,1.1,-39.1),s=(1.2,.5,.1),c=cG)
	o.bush(pos=(-.3,1.1,-39.11),s=(1.2,.5,.1),c=cG)
	o.bush(pos=(.2,1.1,-39.09),s=(1.2,.5,.1),c=cG)
	o.bush(pos=(1,1.1,-39.08),s=(1.2,.5,.1),c=cG)
	o.bush(pos=(0,1.1,-32.1),s=(1.4,.5,.1),c=cG)
	o.bush(pos=(-2,1.1,-28.1),s=(1.4,.5,.1),c=cG)
	o.bush(pos=(1,1.1,-23.1),s=(1.4,.5,.1),c=cG)
	o.bush(pos=(-1.4,1.1,-16.1),s=(1.4,.5,.1),c=cG)
	o.bush(pos=(-.6,1.1,-16.11),s=(1.4,.5,.1),c=cG)
	o.bush(pos=(.2,1.1,-16.12),s=(1.4,.5,.1),c=cG)
	o.bush(pos=(1.2,1.1,-16.09),s=(1.6,.5,.1),c=cG)
	o.bush(pos=(-.4,1.1,-10.8),s=(1.6,.5,.1),c=cG)
	o.bush(pos=(.4,1.1,-10.8),s=(1.6,.5,.1),c=cG)
	o.bush(pos=(-.3,1,-26.37),s=(3,2,.1),c=cG)
	#platform
	o.GemPlatform(pos=(1.5,1.2,-15),t=4)
	o.BigPlatform(p=(0,1,-53.5),s=(4,0,8))
	o.BigPlatform(p=(0,1,-37),s=(3,0,2))
	o.BigPlatform(p=(0,1,-34),s=(1,0,1))
	o.BigPlatform(p=(0,1,-29),s=(1,0,3))
	o.BigPlatform(p=(-2,1,-25),s=(1,0,3))
	o.BigPlatform(p=(1,1,-20),s=(1,0,3))
	o.BigPlatform(p=(0,1,-14),s=(4,0,2))
	o.BigPlatform(p=(0,1,-6.5),s=(2,0,4))
	o.BigPlatform(p=(-1.8,1,2),s=(2,0,6))
	o.BigPlatform(p=(1.8,1,-2),s=(2,0,2))
	o.BigPlatform(p=(1.8,1.01,8),s=(2,0,2))
	o.BigPlatform(p=(0,1,14),s=(6,0,6))
	o.MossPlatform(p=(0,1,-44),MO=False,TU=0)
	o.MossPlatform(p=(0,1,-42),MO=True,TU=0)
	o.MossPlatform(p=(0,1,-40),MO=False,TU=0)
	#NPC
	N.spawn(mID=0,pos=(0,1.1,-52),mDirec=0,mTurn=0)
	N.spawn(mID=0,pos=(0,1.1,-38),mDirec=0,mTurn=0)
	N.spawn(mID=1,pos=(0,1.1,-15),mDirec=0,mTurn=0)
	#crates
	mt.crate_block(ID=2,POS=(-1.8,1.1,3.3),CNT=2)
	mt.crate_block(ID=1,POS=(-1.5,1.1,-2.5),CNT=2)
	mt.crate_wall(ID=1,POS=(-.5,1.1,-57),CNT=2)
	mt.crate_wall(ID=1,POS=(-1.2,1.1,-49),CNT=2)
	c.place_crate(ID=5,p=(0,1.1,-54))
	mt.bounce_twin(POS=(-1,1.1,-36),CNT=1)
	mt.bounce_twin(POS=(1,1.1,-36),CNT=1)
	mt.crate_row(ID=1,POS=(-1.38,.75,-22.2),CNT=6,WAY=0)
	c.place_crate(ID=9,m=1,l=0,p=(-1.42,.75,-22.7))
	for aE in range(6):
		c.place_crate(ID=13,m=1,l=0,p=(-1.10+.32*aE,.75,-22.7))
	mt.crate_row(ID=3,POS=(-1.38,.75,-27),CNT=3,WAY=0)
	mt.crate_row(ID=2,POS=(-1.38,2.5,-27),CNT=3,WAY=0)
	c.place_crate(ID=6,p=(0,1.1,-13))
	mt.crate_row(ID=1,POS=(1.38,.7,.2),CNT=18,WAY=1)
	mt.crate_row(ID=0,POS=(0,.75,19.8),CNT=12,WAY=1)
	#collectable
	item.EnergyCrystal(pos=(0,1.6,-4))
	#M_objects
	o.Corridor(pos=(0,1.09,-13))
	o.RewardRoom(pos=(0,2.2,13),c=color.rgb(80,100,80))
	o.EndRoom(pos=(.3,2.2,23),c=color.rgb(80,100,80))
	invoke(free_level,delay=2)

def level2():##3D
	status.level_index=2
	o.StartRoom(pos=(-.5,1,-50))
	tt='grass'#'res/terrain/texture/sand.jpg'
	o.MapTerrain(MAP='map/'+str(status.level_index)+'.png',size=(12,2,96),t=tt,co=color.gray)
	o.WaterFlow(pos=(-.5,.9,-50))
	for cr in range(4):
		for ccr in range(4):
			o.StoneTile(pos=(-1.5+cr/1.375,1,-47+ccr/1.375))
	cc.level_ready=True