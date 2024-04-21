import crate,objects,_core,status,environment,bonus_level,sound,item,npc,map_tools
from ursina import *

mt=map_tools
bn=bonus_level
env=environment
cc=_core
o=objects
c=crate
N=npc

## level is loaded
def free_level():
	sound.LevelMusic(T=status.level_index)
	cc.check_cstack()
	status.fails=0
	status.loading=False
	cc.level_ready=True
	Audio(sound.snd_spawn)
	print('level '+str(status.level_index)+' loaded successfully')

## level settings
def main_instance(idx):
	status.loading=True
	status.level_index=idx
	day_m={0:'default',1:'woods',2:'snow',3:'day'}
	s_rm={0:(0,0,0),1:(-.3,1,-64.2),2:(0,1,-64.2),3:(0,0,-16.2)}
	status.day_mode=day_m[idx]
	o.StartRoom(pos=s_rm[idx],lvID=idx)
	WEATHER={0:0,1:1,2:2,3:0,4:0,5:0}
	if idx == 5:
		TDHR=1
	else:
		TDHR=0
	env.env_switch(env=day_m[idx],wth=WEATHER[idx],tdr=TDHR)

##levels
def developer_level():
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
	o.EndRoom(pos=(0,1.5,14),c=color.rgb(80,100,80))##end
	cc.preload_items()
	o.MapTerrain(MAP='map/0.png',size=(32,1,32),t='white_cube',co=color.rgb(130,150,130))
	o.CrateScore(pos=(-1,.25,-1))
	#o.SnowPlatform(pos=(0,.5,-6))
	o.Role(pos=(0,.7,-6))
	for gj in range(17):
		#c.place_crate(p=(0+.34*gj,0,-7),ID=0,m=1,l=1,tm=random.randint(1,3))
		c.place_crate(p=(0+.34*gj,0,-7.32),ID=gj,m=1,l=1,tm=random.randint(1,3))
	#o.IceGround(pos=(0,.3,4),sca=(5,1,5))
	invoke(free_level,delay=1)

def level1():##wood
	TS=16
	cG=color.green
	o.MapTerrain(MAP='map/'+str(status.level_index)+'.png',size=(TS/1.6,1.5,TS*8),t='grass',co=color.rgb(0,70,0))
	o.Water(pos=(0,.6,0),s=(10,128),c=color.rgb(40,40,60),a=.8)
	o.InvWall(pos=(-5,.5,-64),sca=(5.,10,200))
	o.InvWall(pos=(4.7,.5,-64),sca=(5.,10,200))
	o.BonusPlatform(pos=(1.5,1.4,-7))
	bn.load_bonus_level(status.level_index)
	bn.gem_route1()
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
	o.bush(pos=(1.3,1,5.95),s=(1.2,.5,.1),c=color.green)
	o.bush(pos=(2.3,1,5.95),s=(1.2,.5,.1),c=color.green)
	o.bush(pos=(2.3,1,5.95),s=(1.2,.5,.1),c=color.green)
	o.TreeScene(pos=(1.1,1.6,-34.6),c=color.rgb(110,130,100),s=.02)
	o.TreeScene(pos=(-1,1.6,-34.6),c=color.rgb(110,130,100),s=.02)
	o.TreeScene(pos=(-1.8,1.5,-21.5),c=color.rgb(110,130,100),s=.02)
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
	o.bush(pos=(.4,1.1,-10.81),s=(1.6,.5,.1),c=cG)
	o.bush(pos=(-.3,1,-26.37),s=(3,2,.1),c=cG)
	o.bush(pos=(-1.2,1,-4.12),s=(1.5,1.5,.1),c=cG)
	o.bush(pos=(-2.2,1,-4.13),s=(1.5,1.5,.1),c=cG)
	o.bush(pos=(1.3,1,-4.11),s=(1.5,1.5,.1),c=cG)
	o.bush(pos=(2.5,1,-4.14),s=(1.5,1.5,.1),c=cG)
	o.bush(pos=(1.1,1,-57),s=(2,1.5,.1),c=cG)
	o.bush(pos=(-.7,1,-55),s=(2,1.5,.1),c=color.orange)
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
	o.MossPlatform(p=(0,1,-44),MO=False,TU=0,UD=False)
	o.MossPlatform(p=(0,1,-42),MO=True,TU=0,UD=False)
	o.MossPlatform(p=(0,1,-40),MO=False,TU=0,UD=False)
	o.MossPlatform(p=(-2,1,-7),MO=False,TU=0,UD=False)
	#NPC
	N.spawn(mID=0,pos=(0,1.1,-52),mDirec=0,mTurn=0)
	N.spawn(mID=0,pos=(0,1.1,-38),mDirec=0,mTurn=0)
	N.spawn(mID=1,pos=(0,1.1,-15),mDirec=0,mTurn=0)
	#wumpa fruits
	mt.wumpa_plane(POS=(-.5,1.3,-57),CNT=4)
	mt.wumpa_plane(POS=(-.7,1.3,-50),CNT=4)
	mt.wumpa_row(POS=(0,1.3,-44),CNT=4,WAY=2)
	mt.wumpa_row(POS=(0,1.3,-40),CNT=4,WAY=2)
	mt.wumpa_plane(POS=(-.5,1.3,-36.5),CNT=4)
	mt.wumpa_row(POS=(0,1.3,-31),CNT=8,WAY=1)
	mt.wumpa_row(POS=(-2,1.3,-27),CNT=8,WAY=1)
	mt.wumpa_row(POS=(1,1.3,-22),CNT=8,WAY=1)
	mt.wumpa_plane(POS=(-.5,1.3,-9),CNT=3)
	mt.wumpa_plane(POS=(-.5,1.3,-6),CNT=3)
	mt.wumpa_plane(POS=(1.3,1.3,-1.5),CNT=3)
	#crates
	mt.crate_block(ID=2,POS=(-1.8,1.1,3.3),CNT=2)
	mt.crate_block(ID=1,POS=(-1.5,1.1,-2.5),CNT=2)
	mt.crate_wall(ID=1,POS=(1,1.1,-56.5),CNT=2)
	mt.crate_wall(ID=1,POS=(-1.2,1.1,-49),CNT=2)
	c.place_crate(ID=5,p=(0,1.1,-54))
	mt.bounce_twin(POS=(-1,1.1,-36),CNT=1)
	mt.bounce_twin(POS=(1,1.1,-36),CNT=1)
	mt.crate_row(ID=1,POS=(-1.38,.75,-22.2),CNT=6,WAY=0)
	c.place_crate(ID=9,m=1,l=0,p=(-1.42,.75,-22.7))
	for aE in range(6):
		c.place_crate(ID=13,m=1,l=0,p=(-1.10+.32*aE,.75,-22.7))
	mt.crate_row(ID=3,POS=(-1.38,.75,-27),CNT=3,WAY=0)
	mt.crate_row(ID=2,POS=(-1.38,2.4,-27),CNT=3,WAY=0)
	c.place_crate(ID=6,p=(0,1.1,-13))
	mt.crate_row(ID=1,POS=(1.38,.7,.2),CNT=18,WAY=1)
	mt.crate_row(ID=0,POS=(0,.75,19.8),CNT=12,WAY=1)
	c.place_crate(ID=4,p=(1.36,1.1,-3.9))
	c.place_crate(ID=3,m=1,l=0,p=(-2,1,-7))
	#collectable
	if not status.level_index in status.CRYSTAL:
		item.EnergyCrystal(pos=(0,1.6,-4))
	#M_objects
	o.Corridor(pos=(0,1.09,-13))
	o.RewardRoom(pos=(0,2.2,13),c=color.rgb(80,100,80))
	o.EndRoom(pos=(.3,2.2,23),c=color.rgb(80,100,80))
	invoke(free_level,delay=3)

def level2():##snow
	o.FallingZone(pos=(0,-2,0),s=(128,1,128))
	Entity(model='quad',scale=(512,512,1),color=color.white,z=64)
	bn.load_bonus_level(status.level_index)
	o.BonusPlatform(pos=(4,1.6,1.5))
	#dangers
	o.WoodLog(pos=(10.3,4,2.3))
	#rock
	for ro in range(40):
		o.Rock(pos=(0+random.uniform(-3,3),-2,-61+ro*2))
		o.Rock(pos=(0+random.uniform(-4,4),-2,-59+ro*2))
	o.mBlock(pos=(0,1.1,-59),sca=(3,.5,6))
	o.mBlock(pos=(0,1.1,-41),sca=(3,.5,4))
	o.mBlock(pos=(0,1.1,-20),sca=(3,.5,4))
	o.mBlock(pos=(0,1.1,0),sca=(3,.5,4))
	o.mBlock(pos=(1.5,1.6,2.5),sca=(6,.5,1))
	o.mBlock(pos=(6,2,2.5),sca=(1,.5,1))
	o.mBlock(pos=(7,2.5,2.5),sca=(1,.5,1))
	o.mBlock(pos=(9,2.5,2.5),sca=(3,.5,1))
	o.IceGround(pos=(14,2.5,2.5),sca=(5,1,1))
	o.mBlock(pos=(18,3.5,2.5),sca=(3,.5,1))
	o.mBlock(pos=(21,4,2.5),sca=(1,.5,1))
	o.mBlock(pos=(22,5,2.5),sca=(1,.5,1))
	o.mBlock(pos=(23,5.75,2.7),sca=(1,.5,1))
	o.mBlock(pos=(23,5.75,5.2),sca=(5,.5,4))
	o.mBlock(pos=(23,5.75,23),sca=(2,.5,7))
	o.mBlock(pos=(23.5,5.75,27),sca=(3,.5,1))
	o.mBlock(pos=(31.8,5.748,27.05),sca=(3,.5,1))
	#pillar
	o.pillar_twin(p=(-.5,.9,-56),ro_y=(0,-45,0))
	o.pillar_twin(p=(-.5,.9,-42.6),ro_y=(0,-45,0))
	o.pillar_twin(p=(-.5,.9,-39),ro_y=(0,-45,0))
	o.pillar_twin(p=(-.5,.9,-21.7),ro_y=(0,-45,0))
	o.pillar_twin(p=(-.5,.9,-18),ro_y=(0,-45,0))
	o.pillar_twin(p=(-.5,.9,-1.8),ro_y=(0,-45,0))
	o.pillar_twin(p=(22.5,5.75,7),ro_y=(0,-45,0))
	o.pillar_twin(p=(22.5,5.75,19.7),ro_y=(0,-45,0))
	o.pillar_twin(p=(22.5,5.75,26.3),ro_y=(0,-45,0))
	o.Ropes(pos=(-.5,1,-56),le=55)
	o.Ropes(pos=(22.5,5.65,7),le=16)
	#npc
	npc.spawn(pos=(3,1.6,2.5),mID=3,mDirec=0,mTurn=0)
	npc.spawn(pos=(0,1.1,1),mID=3,mDirec=0,mTurn=0)
	npc.spawn(pos=(8.8,2.5,2.5),mID=5,mDirec=0,mTurn=0)
	#planks
	o.plank_bridge(pos=(0,1,-56),ro_y=0,typ=1,cnt=12,DST=.5)
	o.plank_bridge(pos=(0,1,-48.5),ro_y=0,typ=0,cnt=10,DST=.5)
	o.plank_bridge(pos=(0,1,-38),ro_y=0,typ=0,cnt=4,DST=.5)
	o.plank_bridge(pos=(0,1,-36),ro_y=0,typ=1,cnt=2,DST=.5)
	o.plank_bridge(pos=(0,1,-34),ro_y=0,typ=1,cnt=2,DST=.5)
	o.plank_bridge(pos=(0,1,-32),ro_y=0,typ=1,cnt=2,DST=.5)
	o.plank_bridge(pos=(0,1,-30),ro_y=0,typ=0,cnt=3,DST=.5)
	o.plank_bridge(pos=(0,1,-28),ro_y=0,typ=0,cnt=2,DST=.5)
	o.plank_bridge(pos=(0,1,-26),ro_y=0,typ=0,cnt=6,DST=.5)
	o.plank_bridge(pos=(0,1,-18),ro_y=0,typ=1,cnt=2,DST=.5)
	o.plank_bridge(pos=(0,1,-16),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(0,1,-14),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(0,1,-12),ro_y=0,typ=1,cnt=4,DST=.5)
	o.plank_bridge(pos=(0,1,-10),ro_y=0,typ=0,cnt=3,DST=.5)
	o.plank_bridge(pos=(0,1,-8),ro_y=0,typ=1,cnt=2,DST=.5)
	o.plank_bridge(pos=(0,1,-6),ro_y=0,typ=1,cnt=2,DST=.5)
	o.plank_bridge(pos=(0,1,-4),ro_y=0,typ=1,cnt=2,DST=.5)
	o.plank_bridge(pos=(0,1,-3),ro_y=0,typ=0,cnt=1,DST=.5)
	o.plank_bridge(pos=(23,5.71,7.3),ro_y=0,typ=0,cnt=6,DST=.4)
	o.plank_bridge(pos=(23,5.71,11),ro_y=0,typ=1,cnt=3,DST=.5)
	o.plank_bridge(pos=(23,5.71,13),ro_y=0,typ=1,cnt=2,DST=.5)
	o.plank_bridge(pos=(23,5.71,15),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(23,5.71,16),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(23,5.71,17),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(23,5.71,18),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(23,5.71,19),ro_y=0,typ=0,cnt=1,DST=.5)
	o.plank_bridge(pos=(25.2,5.71,27),ro_y=90,typ=1,cnt=12,DST=.45)
	#walls
	for snw in range(40):
		o.SnowWall(pos=(-10+snw*7,1,3))
		o.SnowWall(pos=(-10+snw*7,3,3))
	#crates
	h1=1.1
	mt.crate_block(ID=1,POS=(.5,h1,-58),CNT=2)
	mt.crate_wall(ID=12,POS=(-.3,h1,-18.6),CNT=3)
	c.place_crate(ID=2,p=(0,h1,-54))
	c.place_crate(ID=3,p=(.2,h1,-52))
	c.place_crate(ID=2,p=(-.2,h1,-48))
	c.place_crate(ID=6,p=(-.2,h1,-40))
	c.place_crate(ID=5,p=(-.7,h1,-42.1))
	c.place_crate(ID=11,p=(.8,h1,-18.6))
	c.place_crate(ID=12,p=(.4,h1,-15))
	c.place_crate(ID=12,p=(0,h1,-13))
	c.place_crate(ID=12,p=(-.3,h1,-10))
	c.place_crate(ID=12,p=(0,h1,-8))
	c.place_crate(ID=12,p=(-.2,h1,-6))
	c.place_crate(ID=12,p=(0,h1,-4))
	c.place_crate(ID=2,p=(19,2,2.5))
	c.place_crate(ID=2,p=(19.32,2.32,2.5))
	c.place_crate(ID=2,p=(19.64,2.64,2.5))
	c.place_crate(ID=6,p=(23,5.75,23))
	#mt.crate_row(ID=11,POS=(19.96,2.96,2.5),WAY=0,CNT=4)
	invoke(free_level,delay=3)