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
	if status.level_index == 3:
		sound.AmbienceSound()
		sound.WaterRiver()
	o.ObjectLOD()
	print('level '+str(status.level_index)+' loaded successfully')

## level settings
def main_instance(idx):
	status.loading=True
	status.level_index=idx
	day_m={0:'default',1:'woods',2:'snow',3:'evening',4:'day'}
	s_rm={0:(0,0,0),1:(-.3,1,-64.2),2:(0,1,-64.2),3:(0,0,-32.2),4:(0,0,-16.2)}
	status.day_mode=day_m[idx]
	o.StartRoom(pos=s_rm[idx],lvID=idx)
	bn.load_bonus_level(idx)
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
	invoke(free_level,delay=1)

def test():
	#o.EndRoom(pos=(0,2,-5),c=color.rgb(80,100,80))##end
	o.BonusPlatform(pos=(0,.5,-6))
	cc.preload_items()
	o.MapTerrain(MAP='map/0.png',size=(32,1,32),t='white_cube',co=color.rgb(130,150,130))
	mt.crate_row(ID=6,POS=(-1,.16,-11),CNT=4,WAY=0)
	invoke(free_level,delay=1)

def level1():##wood
	TS=16
	cG=color.green
	o.MapTerrain(MAP='map/'+str(status.level_index)+'.png',size=(TS/1.6,1.5,TS*8),t='grass',co=color.rgb(0,70,0))
	o.Water(pos=(0,.6,0),s=(10,128),c=color.rgb(40,40,60),a=.8)
	o.InvWall(pos=(-5,.5,-64),sca=(5.,10,200))
	o.InvWall(pos=(4.7,.5,-64),sca=(5.,10,200))
	o.BonusPlatform(pos=(1.4,1,-6))
	bn.gem_route1()
	#plants
	o.TreeScene(pos=(-1.37,1.5,-46),s=.0175)
	o.TreeScene(pos=(1.32,1.5,-46),s=.0175)
	o.TreeScene(pos=(0,1.7,-26.4),s=.0175)
	o.TreeScene(pos=(0,1.5,-2.7),s=.02)
	o.TreeScene(pos=(3,1.7,10.6),s=.02)
	o.TreeScene(pos=(-2,1.7,9.5),s=.02)
	for trE in range(10):
		o.TreeScene(pos=(0+random.uniform(-.1,.1),.7,-2+trE),s=.02)
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
	o.TreeScene(pos=(-1.5,1.6,19.3),s=.02)
	o.TreeScene(pos=(1.2,1.8,19.3),s=.02)
	o.bush(pos=(2.43,1.4,23),s=3,c=cG)
	o.bush(pos=(-2.37,1.4,23),s=3,c=color.yellow)
	o.TreeScene(pos=(1,1.6,-34.6),s=.02)
	o.TreeScene(pos=(-1.4,1.6,-34.6),s=.02)
	o.TreeScene(pos=(-1.8,1.5,-21.5),s=.02)
	o.TreeScene(pos=(-1.5,1.5,-60.5),s=.02)
	o.TreeScene(pos=(1,1.5,-60.5),s=.02)
	o.TreeScene(pos=(-1.2,1.5,-54.5),s=.02)
	o.TreeScene(pos=(1.1,1.5,-53),s=.02)
	#platform grass
	bu_h=1.1
	o.bush(pos=(-1,bu_h,-45.3),s=(1.2,.5,.1),c=cG)
	o.bush(pos=(.7,bu_h,-45.3),s=(1.2,.5,.1),c=cG)
	o.bush(pos=(-1.5,bu_h,-38.61),s=(1.4,.5,.1),c=cG)
	o.bush(pos=(-.6,bu_h,-38.611),s=(1.4,.5,.1),c=cG)
	o.bush(pos=(.5,bu_h,-38.609),s=(1.4,.5,.1),c=cG)
	o.bush(pos=(1.5,bu_h,-38.608),s=(1.4,.5,.1),c=cG)
	o.bush(pos=(-2,.9,-28.55),s=(1.4,.5,.1),c=cG)
	o.bush(pos=(.6,bu_h,-23.1),s=(1.4,.5,.1),c=cG)
	o.bush(pos=(-1.4,bu_h,-16.1),s=(1.4,.5,.1),c=cG)
	o.bush(pos=(-.6,bu_h,-16.11),s=(1.4,.5,.1),c=cG)
	o.bush(pos=(.2,bu_h,-16.12),s=(1.4,.5,.1),c=cG)
	o.bush(pos=(1.2,bu_h,-16.09),s=(1.6,.5,.1),c=cG)
	o.bush(pos=(0,1,-26.37),s=(3,2,.1),c=cG)
	o.bush(pos=(-1,1,-4.12),s=(1.5,1.5,.1),c=cG)
	o.bush(pos=(-2,1,-4.13),s=(1.5,1.5,.1),c=cG)
	o.bush(pos=(1.3,1,-4.13),s=(1.7,1.5,.1),c=cG)
	o.bush(pos=(1.1,1,-57),s=(2,1.5,.1),c=cG)
	o.bush(pos=(-.7,1,-55),s=(2,1.5,.1),c=color.orange)
	o.bush(pos=(-.8,3,23),s=(2,1.5,.1),c=color.rgb(0,80,0))
	o.bush(pos=(.4,3,23.02),s=(2,1.5,.1),c=color.rgb(0,80,0))
	o.bush(pos=(-.2,3.3,23.01),s=(2,1.5,.1),c=color.rgb(0,80,0))
	#platform
	d0=1.5
	o.GemPlatform(pos=(1.5,1.4,-15),t=4)
	o.mBlock(pos=(0,d0,-57),sca=(4,1,24))
	o.mBlock(pos=(0,d0,-36),sca=(4,1,5))
	o.mBlock(pos=(0,d0,-30),sca=(1,1,7))
	o.mBlock(pos=(-2,d0,-25),sca=(1,1,7))
	o.mBlock(pos=(.7,d0,-20),sca=(1,1,6))
	o.mBlock(pos=(0,d0,-14),sca=(4,1,4))
	o.mBlock(pos=(0,d0,-9.5),sca=(1,1,5))
	o.mBlock(pos=(0,d0,-5),sca=(1,1,4))
	o.mBlock(pos=(1.5,d0,-1.5),sca=(2,1,5))
	o.mBlock(pos=(1.5,d0,5.7),sca=(2,1,3))
	o.mBlock(pos=(1.5,d0,9.5),sca=(2,1,2))
	o.mBlock(pos=(-1.5,d0,-1.5),sca=(2,1,5))
	o.mBlock(pos=(-1.5,d0,4),sca=(2,1,3))
	o.mBlock(pos=(-1.5,d0,8.5),sca=(2,1,3))
	o.mBlock(pos=(0,d0,10),sca=(1,1,4))
	o.mBlock(pos=(0,d0,18),sca=(4,1,4))
	o.MossPlatform(p=(0,1,-44),MO=False,TU=0,UD=False)
	o.MossPlatform(p=(0,1,-42),MO=True,TU=0,UD=False)
	o.MossPlatform(p=(0,1,-40),MO=False,TU=0,UD=False)
	o.MossPlatform(p=(-2,1,-6),MO=False,TU=0,UD=False)
	o.MossPlatform(p=(0,1,13.5),MO=False,TU=0,UD=False)
	o.MossPlatform(p=(0,1,15),MO=False,TU=0,UD=False)
	#NPC
	N.spawn(mID=0,pos=(0,1.1,-52),mDirec=0,mTurn=0)
	N.spawn(mID=0,pos=(0,1.1,-38),mDirec=0,mTurn=0)
	N.spawn(mID=1,pos=(0,1.1,-15),mDirec=0,mTurn=0)
	#wumpa fruits
	wu_h=1
	mt.wumpa_plane(POS=(-.5,wu_h,-57),CNT=4)
	mt.wumpa_plane(POS=(-.4,wu_h,-50),CNT=4)
	mt.wumpa_row(POS=(0,wu_h,-44),CNT=4,WAY=2)
	mt.wumpa_row(POS=(0,wu_h,-40),CNT=4,WAY=2)
	mt.wumpa_plane(POS=(-.5,wu_h,-36.5),CNT=4)
	mt.wumpa_row(POS=(0,wu_h,-33),CNT=14,WAY=1)
	mt.wumpa_row(POS=(-2,wu_h,-27),CNT=8,WAY=1)
	mt.wumpa_row(POS=(.6,wu_h,-22),CNT=8,WAY=1)
	mt.wumpa_plane(POS=(-.3,wu_h,-9),CNT=3)
	mt.wumpa_plane(POS=(-.3,wu_h,-6),CNT=3)
	mt.wumpa_plane(POS=(1.3,wu_h,-1.5),CNT=3)
	mt.wumpa_plane(POS=(0,wu_h,16.3),CNT=4)
	#crates
	CRP=1.16
	mt.crate_block(ID=2,POS=(-1.8,CRP,3.3),CNT=2)
	mt.crate_block(ID=1,POS=(-1.5,CRP,-2.5),CNT=2)
	mt.crate_wall(ID=1,POS=(1,CRP,-56.5),CNT=2)
	mt.crate_wall(ID=1,POS=(-1,CRP,-49),CNT=2)
	c.place_crate(ID=5,p=(0,CRP,-54))
	mt.bounce_twin(POS=(-1,CRP,-36),CNT=1)
	mt.bounce_twin(POS=(1,CRP,-36),CNT=1)
	mt.crate_row(ID=1,POS=(-1.3,.9,-22.3),CNT=5,WAY=0)
	c.place_crate(ID=9,m=1,l=0,p=(-1.3,.9,-22.82))
	for aE in range(5):
		c.place_crate(ID=13,m=1,l=0,p=(-1.3+.32*aE,.9,-22.82))
	mt.crate_row(ID=3,POS=(-1.3,.9,-27),CNT=3,WAY=0)
	mt.crate_row(ID=2,POS=(-1.3,2.56,-27),CNT=3,WAY=0)
	mt.crate_row(ID=1,POS=(1.38,.8,1.1),CNT=10,WAY=1)
	mt.crate_row(ID=0,POS=(0,.85,20.16),CNT=10,WAY=1)
	c.place_crate(ID=4,p=(.9,CRP,-3.9))
	c.place_crate(ID=3,m=1,l=0,p=(-2,CRP,-6))
	mt.crate_block(ID=1,POS=(-1.09,CRP,17),CNT=2)
	mt.bounce_twin(POS=(1.1,CRP,18),CNT=2)
	#checkpoints
	c.place_crate(ID=6,p=(0,CRP,-46))
	c.place_crate(ID=6,p=(.6,CRP,-17.8))
	c.place_crate(ID=6,p=(0,CRP,11.1))
	#collectable
	if not status.level_index in status.CRYSTAL:
		item.EnergyCrystal(pos=(0,1.5,-13))
	#M_objects
	o.Corridor(pos=(0,1,-13))
	o.EndRoom(pos=(1,2.4,28.2),c=color.rgb(80,100,80))
	invoke(free_level,delay=3)

def level2():##snow
	o.FallingZone(pos=(0,-2,0),s=(128,1,128))
	Entity(model='quad',scale=(512,512,1),color=color.white,z=64)
	o.BonusPlatform(pos=(4,1.6,1.5))
	#dangers
	o.WoodLog(pos=(10.3,4,2.3))
	o.WoodLog(pos=(9.2,4,2.3))
	o.Role(pos=(42.2,6.6,31),di=1)
	o.Role(pos=(42.2,6.6,32),di=0)
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
	o.mBlock(pos=(42,5.8,32),sca=(4,.5,8))
	o.mBlock(pos=(42,6.4,38),sca=(4,.5,4))
	o.mBlock(pos=(42,6.6,47),sca=(4,.5,4))
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
	o.plank_bridge(pos=(23,5.71,7.3),ro_y=0,typ=0,cnt=6,DST=.5)
	o.plank_bridge(pos=(23,5.71,11),ro_y=0,typ=1,cnt=3,DST=.5)
	o.plank_bridge(pos=(23,5.71,13),ro_y=0,typ=1,cnt=2,DST=.5)
	o.plank_bridge(pos=(23,5.71,15),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(23,5.71,16),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(23,5.71,17),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(23,5.71,18),ro_y=0,typ=1,cnt=1,DST=.5)
	o.plank_bridge(pos=(23,5.71,19),ro_y=0,typ=0,cnt=1,DST=.5)
	o.plank_bridge(pos=(25.2,5.71,27),ro_y=90,typ=1,cnt=12,DST=.45)
	#ptf object
	for ptf1 in range(4):
		for ptf2 in range(3):
			o.SnowPlatform(pos=(34+ptf1*1.5,5.8,27+ptf2*1.5))
	#walls
	for snw in range(40):
		o.SnowWall(pos=(-10+snw*7,1,3))
		o.SnowWall(pos=(-10+snw*7,3,3))
	#crates
	h1=1.1
	mt.crate_block(ID=1,POS=(.5,h1,-58),CNT=2)
	mt.crate_plane(ID=2,POS=(-.7,h1,-57),CNT=2)
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
	mt.crate_row(ID=2,POS=(18,3.5,2.5),CNT=4,WAY=0)
	c.place_crate(ID=6,p=(23,5.75,23))
	mt.crate_plane(ID=1,POS=(21.6,5.75,5.4),CNT=3)
	c.place_crate(ID=3,p=(23,5.75,13))
	c.place_crate(ID=10,p=(37,5.8,30.4))
	c.place_crate(ID=5,p=(6.8,2.5,2.5))
	c.place_crate(ID=5,p=(24.3,5.75,5))
	#collecable
	if not status.level_index in status.CRYSTAL:
		item.EnergyCrystal(pos=(35.5,6.4,28.5))
	#end
	o.EndRoom(pos=(42.5,8,48),c=color.rgb(80,80,120))
	#mt.crate_row(ID=11,POS=(19.96,2.96,2.5),WAY=0,CNT=4)
	invoke(free_level,delay=3)

def level3():##water
	#default
	o.BonusPlatform(pos=(1.3,1.1,22.5))
	#water
	o.WaterFlow(pos=(0,-.3,-16),sca=(4,32))
	o.WaterFall(pos=(0,-.8,0))
	o.WaterFlow(pos=(0,.7,16),sca=(4,32))
	#hills
	o.side_hills(p=(-2.4,-.3,-30),cnt=32)
	o.side_hills(p=(2.4,-.3,-30),cnt=32)
	o.side_hills(p=(-2.4,.6,0),cnt=32)
	o.side_hills(p=(2.4,.6,0),cnt=32)
	#walls
	o.TempleWall(pos=(-3.3,-2,-25),side=1)
	o.TempleWall(pos=(3.3,-2,-25),side=2)
	#stage
	o.WoodStage(pos=(0,.2,-20))
	o.WoodStage(pos=(0,1,24))
	#platforms
	o.MossPlatform(p=(0,.2,-25),MO=False,TU=0,UD=True)
	o.MossPlatform(p=(0,.2,-23.5),MO=False,TU=0,UD=False)
	#blocks
	o.block_plane(p=(-.8,0,-29),cnt=3)
	o.block_row(p=(0,0,-18),cnt=20,way=1)
	o.block_row(p=(0,0,-1),cnt=1,way=0)
	o.block_row(p=(.8,.7,.3),cnt=2,way=1)
	o.SingleBlock(pos=(0,0,-1))
	o.SingleBlock(pos=(.8,.5,-1))
	o.block_plane(p=(-.8,.7,3),cnt=3)
	for wSB1 in range(4):
		o.SingleBlock(pos=(0,.7,6+wSB1*2))
	o.block_plane(p=(-.4,.7,14),cnt=2)
	o.block_plane(p=(-.4,.7,17),cnt=2)
	o.block_plane(p=(-.8,.7,20),cnt=2)
	invoke(free_level,delay=1)