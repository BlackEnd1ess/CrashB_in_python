import crate,objects,_core,status,environment,bonus_level,sound,item,npc,map_tools,_loc
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
	if status.level_index == 3:
		sound.AmbienceSound()
		sound.WaterRiver()
	o.LODProcess()
	print('level '+str(status.level_index)+' loaded successfully')

## level settings
def main_instance(idx):
	status.loading=True
	status.level_index=idx
	day_m=_loc.day_m
	s_rm={0:(0,0,0),1:(-.3,1,-66.5),2:(0,1,-64.2),3:(0,0,-32.2),4:(0,.3,-64.2),5:(0,0,-32.2)}
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
	o.EndRoom(pos=(0,1.5,27),c=color.rgb32(80,100,80))##end
	Entity(model='cube',scale=(16,1,64),y=-.5,texture_scale=(16,64),collider='box',texture='grass')
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
	#o.EndRoom(pos=(1,2,-15),c=color.rgb32(200,210,200))
	Entity(model='cube',scale=(16,1,64),y=-.5,texture_scale=(16,64),collider='box',texture='grass')
	#mt.crate_block(ID=11,POS=(.5,.16,-25.1),CNT=[1,1,1])
	#npc.spawn(pos=(1,0,-23),mID=6,mDirec=0,mTurn=0)
	o.Role(pos=(0,.5,-24),di=1)
	invoke(free_level,delay=1)

def level1():##wood
	TS=16
	cG=color.green
	o.Water(pos=(0,.6,0),s=(10,128),c=color.rgb32(80,80,120),a=1,typ=2)
	o.InvWall(pos=(-5,.5,-64),sca=(5.,10,200))
	o.InvWall(pos=(4.7,.5,-64),sca=(5.,10,200))
	o.BonusPlatform(pos=(1.4,1,-6))
	o.GemPlatform(pos=(-.2,.9,-18),t=4)
	bn.gem_route1()
	#scene
	gs=1.6
	o.GrassSide(pos=(-4,gs,-47),ry=0)
	o.GrassSide(pos=(-4,gs,-16),ry=0)
	o.GrassSide(pos=(-4,gs,15),ry=0)
	o.GrassSide(pos=(-4,gs,46),ry=0)
	o.GrassSide(pos=(4,gs,-47),ry=180)
	o.GrassSide(pos=(4,gs,-16),ry=180)
	o.GrassSide(pos=(4,gs,15),ry=180)
	o.GrassSide(pos=(4,gs,46),ry=180)
	o.LevelScene(pos=(0,0,128),sca=(350,40,1))
	o.LevelScene(pos=(0,-20,127),sca=(350,40,1))
	#plants
	Entity(model='cube',texture='res/terrain/l1/bricks.png',scale=(9,2,.3),position=(0,-.2,-64.5),texture_scale=(9,2))
	o.TreeScene(pos=(-3.7,1,-63),s=.0175)
	o.TreeScene(pos=(-4.7,1,-63),s=.0175)
	o.TreeScene(pos=(3.6,1.2,-63.5),s=.0175)
	o.TreeScene(pos=(4.6,1.2,-63.5),s=.0175)
	o.TreeScene(pos=(-1.37,1.5,-46),s=.0175)
	o.TreeScene(pos=(1.32,1.5,-46),s=.0175)
	o.TreeScene(pos=(0,1.7,-26.4),s=.0175)
	o.TreeScene(pos=(3,1.7,10.6),s=.02)
	o.spawn_tree_wall(pos=(-4,2.3,-64),cnt=50,d=0)
	o.spawn_tree_wall(pos=(-4,2,-64),cnt=50,d=0)
	o.spawn_tree_wall(pos=(4.5,2.3,-64),cnt=50,d=1)
	o.spawn_tree_wall(pos=(4,2.3,-63),cnt=50,d=1)
	o.bush(pos=(.37,1.3,-26.5),s=2,c=color.orange)
	o.bush(pos=(1.5,1.4,-14.2),s=2,c=cG)
	o.bush(pos=(-1.5,1.4,-14.2),s=2,c=color.orange)
	o.bush(pos=(-1,1.4,-12),s=2,c=cG)
	o.bush(pos=(1,1.4,-12),s=2,c=color.orange)
	o.bush(pos=(2.43,1.5,10.7),s=2,c=cG)
	o.bush(pos=(-2,1.5,10.2),s=2,c=color.yellow)
	o.TreeScene(pos=(-1.5,1.6,19.3),s=.02)
	o.TreeScene(pos=(1.2,1.8,19.3),s=.02)
	o.TreeScene(pos=(-.2,1.5,-2.6),s=.02)
	o.TreeScene(pos=(1.1,1.5,11),s=.02)
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
	bu_h=.85
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
	o.bush(pos=(-.8,3,22.75),s=(2,1.5,.1),c=color.rgb32(0,80,0))
	o.bush(pos=(.4,3,23),s=(2,1.5,.1),c=color.rgb32(0,80,0))
	o.bush(pos=(-.2,3.3,22.8),s=(2,1.5,.1),c=color.rgb32(0,80,0))
	#platform
	d0=.85
	o.mBlock(pos=(0,d0,-57),sca=(4,24))
	o.mBlock(pos=(0,d0,-36),sca=(4,5))
	o.mBlock(pos=(0,d0,-30),sca=(1,7))
	o.mBlock(pos=(-2,d0,-25),sca=(1,7))
	o.mBlock(pos=(.7,d0,-20),sca=(1,6))
	o.mBlock(pos=(0,d0,-14),sca=(4,4))
	o.mBlock(pos=(0,d0,-9.5),sca=(1,5))
	o.mBlock(pos=(0,d0,-5),sca=(1,4))
	o.mBlock(pos=(1.5,d0,-1.5),sca=(2,5))
	o.mBlock(pos=(1.5,d0,5.7),sca=(2,3))
	o.mBlock(pos=(1.5,d0,9.5),sca=(2,2))
	o.mBlock(pos=(-1.5,d0,-1.5),sca=(2,5))
	o.mBlock(pos=(-1.5,d0,4),sca=(2,3))
	o.mBlock(pos=(-1.5,d0,8.5),sca=(2,3))
	o.mBlock(pos=(0,d0,10),sca=(1,4))
	o.mBlock(pos=(0,d0,18),sca=(4,4))
	o.MossPlatform(p=(0,.5,-44),ptm=0)
	o.MossPlatform(p=(0,.5,-42),ptm=0)
	o.MossPlatform(p=(0,.5,-40),ptm=0)
	o.MossPlatform(p=(-2,.5,-6),ptm=0)
	o.MossPlatform(p=(0,.5,13.5),ptm=0)
	o.MossPlatform(p=(0,.5,15),ptm=0)
	#NPC
	N.spawn(mID=0,pos=(0,1.1,-52),mDirec=0,mTurn=0)
	N.spawn(mID=0,pos=(0,1.1,-38),mDirec=0,mTurn=0)
	N.spawn(mID=1,pos=(0,1.1,-15),mDirec=0,mTurn=0)
	#wumpa fruits
	wu_h=1.3
	mt.wumpa_plane(POS=(-.5,wu_h,-56.1),CNT=4)
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
	if not 4 in status.COLOR_GEM:
		c.place_crate(ID=16,p=(-.3,CRP,-58))
	mt.crate_block(ID=2,POS=(-1.8,CRP,3.3),CNT=[2,2,2])
	mt.crate_block(ID=1,POS=(-1.5,CRP,-2.5),CNT=[2,2,2])
	mt.crate_wall(ID=1,POS=(1,CRP,-56.5),CNT=[2,2])
	mt.crate_wall(ID=1,POS=(-1,CRP,-49),CNT=[2,2])
	c.place_crate(ID=5,p=(0,CRP,-54))
	mt.bounce_twin(POS=(-1,CRP,-36),CNT=1)
	mt.bounce_twin(POS=(1,CRP,-36),CNT=1)
	mt.crate_row(ID=1,POS=(-1.3,.9,-22.3),CNT=5,WAY=0)
	c.place_crate(ID=9,m=1,l=0,p=(-1.3,.9,-22.82))
	for aE in range(4):
		c.place_crate(ID=13,m=1,l=0,p=(-.98+.32*aE,.9,-22.82))
	mt.crate_row(ID=3,POS=(-1.3,.9,-27),CNT=3,WAY=0)
	mt.crate_row(ID=2,POS=(-1.3,2.56,-27),CNT=3,WAY=0)
	mt.crate_row(ID=1,POS=(1.8,.8,1.1),CNT=10,WAY=1)
	mt.crate_row(ID=0,POS=(-.1,.8,20.16),CNT=10,WAY=1)
	c.place_crate(ID=4,p=(.9,CRP,-3.9))
	c.place_crate(ID=3,m=1,l=0,p=(-2,CRP,-6))
	mt.crate_block(ID=1,POS=(-1.09,CRP,17),CNT=[2,2,2])
	mt.bounce_twin(POS=(1.1,CRP,18),CNT=2)
	#checkpoints
	c.place_crate(ID=6,p=(0,CRP,-46))
	c.place_crate(ID=6,p=(.6,CRP,-17.8))
	c.place_crate(ID=6,p=(0,CRP,11.1))
	#collectable
	if not status.level_index in status.CRYSTAL:
		item.EnergyCrystal(pos=(0,1.5,-13))
	#M_objects
	o.Corridor(pos=(0,.975,-13))
	o.EndRoom(pos=(1,2.4,28.2),c=color.rgb32(80,100,80))
	invoke(free_level,delay=3)

def level2():##snow
	o.spawn_ice_wall(pos=(-2.3,-.5,-58.6),cnt=8,d=0)
	o.spawn_ice_wall(pos=(2.3,-.5,-58.6),cnt=7,d=1)
	o.spawn_ice_wall(pos=(20,4,8),cnt=4,d=0)
	o.spawn_ice_wall(pos=(26,4,8),cnt=2,d=1)
	o.spawn_ice_wall(pos=(45,4,28),cnt=3,d=1)
	status.gem_death=False
	o.Water(pos=(12,-.5,-32),s=(32,128),c=color.cyan,a=1,typ=0)
	o.Water(pos=(51,4.5,23.5),s=(64,40),c=color.cyan,a=1,typ=0)
	Entity(model='quad',scale=(512,512,1),color=color.white,z=64)
	o.BonusPlatform(pos=(5,1.1,2.1))
	#invisible walls
	o.InvWall(pos=(17,0,1.5),sca=(30,40,1))
	#cam trigger
	o.CamSwitch(pos=(.5,1.4,.9),sca=(4,.3,1))
	o.CamSwitch(pos=(.5,1.7,2.5),sca=(4,.2,.5))
	o.CamSwitch(pos=(6,1.8,2.4),sca=(.5,.2,.5))
	o.CamSwitch(pos=(7.4,2.3,2.4),sca=(1,.2,.5))
	o.CamSwitch(pos=(10.5,2.5,2.3),sca=(2,.2,.5))
	o.CamSwitch(pos=(16,2.9,2.3),sca=(7,.2,.5))
	o.CamSwitch(pos=(23,6,2.4),sca=(.6,.3,.5))
	o.CamSwitch(pos=(24.5,5,2.2),sca=(.3,2,.2))
	o.CamSwitch(pos=(23,3,2.2),sca=(1.5,.2,.2))
	o.CamSwitch(pos=(42,6.5,35),sca=(6,.3,1))
	o.CamSwitch(pos=(42,7,37),sca=(6,.7,1))
	#ice
	for i_ch in range(50):
		o.IceChunk(pos=(-4-random.uniform(-.5,-1),1.8,-63+i_ch*1.5),rot=(-90,30,0),typ=1)
		if i_ch < 38:
			o.IceChunk(pos=(2.9+random.uniform(.5,1),1.8,-63+i_ch*1.5),rot=(-90,-30,0),typ=1)
	for u_ch in range(20):
		o.IceChunk(pos=(18.2-random.uniform(-.5,-1),6.3,3.7+u_ch*1.5),rot=(-90,30,0),typ=1)
		if u_ch < 11:
			o.IceChunk(pos=(26.5+random.uniform(.5,1),6.3,3.7+u_ch*1.5),rot=(-90,-30,0),typ=1)
	for e_ch in range(20):
		o.IceChunk(pos=(45.4+random.uniform(.5,1),6.3,26+e_ch*1.5),rot=(-90,-30,0),typ=1)
	o.IceChunk(pos=(21.7,6,2.6),typ=1,rot=(-180,-90,0))
	o.IceChunk(pos=(24.4,6,2.6),typ=1,rot=(0,-90,0))
	o.IceChunk(pos=(21.2,5.3,3.2),typ=1,rot=(260,-90,0))
	o.IceChunk(pos=(24.8,5.3,3.2),typ=1,rot=(-80,-90,0))
	o.IceChunk(pos=(28,5.35,28.1),typ=1,rot=(-180,-90,0))
	o.IceChunk(pos=(28,7.8,28),typ=1,rot=(-180,-90,0))
	#dangers
	wlO=3.7
	o.WoodLog(pos=(10.5,wlO,2.2))
	o.WoodLog(pos=(8.2,wlO,2.2))
	o.Role(pos=(42.2,6.6,31),di=1)
	o.Role(pos=(42.2,6.6,32),di=0)
	#rock
	for ro in range(40):
		o.Rock(pos=(0+random.uniform(-3,3),-2,-61+ro*2))
		o.Rock(pos=(0+random.uniform(-4,4),-2,-59+ro*2))
	o.mBlock(pos=(0,.8,-59),sca=(3,6))
	o.mBlock(pos=(0,.8,-41),sca=(3,4))
	o.mBlock(pos=(0,.8,-20),sca=(3,4))
	o.mBlock(pos=(0,.8,0),sca=(3,4))
	#2d area
	o.mBlock(pos=(1.5,1.2,2.5),sca=(6,1))
	o.mBlock(pos=(6,1.5,2.5),sca=(1,1))
	o.mBlock(pos=(7.5,2,2.5),sca=(2,1))
	o.mBlock(pos=(10.5,2,2.5),sca=(2,1))
	o.mBlock(pos=(12,2.5,2.5),sca=(1,1))
	o.IceGround(pos=(15,2.125,2.5),sca=(5,1))
	o.mBlock(pos=(19,2.5,2.5),sca=(3,1))
	o.mBlock(pos=(23,2.5,2.5),sca=(2,1))
	o.mBlock(pos=(23,5.25,2.2),sca=(1,1.75))
	o.mBlock(pos=(24.5,3,2.5),sca=(1,1))
	o.mBlock(pos=(23,5.25,5.2),sca=(4,4))
	o.mBlock(pos=(23,5.25,23),sca=(2,7))
	o.mBlock(pos=(23.5,5.25,27),sca=(3,1))
	o.mBlock(pos=(31.8,5.248,26.98),sca=(3,1))
	o.mBlock(pos=(42,5.6,32),sca=(4,8))
	o.mBlock(pos=(42,6.2,38),sca=(4,4))
	#pillar
	phe=1.1
	o.pillar_twin(p=(-.75,phe,-56),ro_y=(-90,45,0))
	o.pillar_twin(p=(-.75,phe,-42.6),ro_y=(-90,45,0))
	o.pillar_twin(p=(-.75,phe,-39),ro_y=(-90,45,0))
	o.pillar_twin(p=(-.75,phe,-21.65),ro_y=(-90,45,0))
	o.pillar_twin(p=(-.75,phe,-18),ro_y=(-90,45,0))
	o.pillar_twin(p=(-.75,phe,-1.8),ro_y=(-90,45,0))
	o.pillar_twin(p=(22.25,5.35,7),ro_y=(-90,45,0))
	o.pillar_twin(p=(22.25,5.35,19.85),ro_y=(-90,45,0))
	o.pillar_twin(p=(22.25,5.35,26.3),ro_y=(-90,45,0))
	o.Ropes(pos=(-.5,.7,-56),le=55)
	o.Ropes(pos=(22.5,5.3,7),le=16)
	#npc
	npc.spawn(pos=(3,1.4,2.5),mID=3,mDirec=0,mTurn=0)
	npc.spawn(pos=(0,.9,1),mID=3,mDirec=0,mTurn=0)
	npc.spawn(pos=(14.5,2.7,2.5),mID=5,mDirec=0,mTurn=0)
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
	for snw in range(7):
		o.SnowWall(pos=(-5+snw*5.4,.1,2.65))
		o.SnowWall(pos=(-5+snw*5.4,3.2,2.65))
	o.SnowWall(pos=(19,6.3,2.65))
	o.SnowWall(pos=(27,6.3,2.65))
	o.SnowWall(pos=(30,2,38))
	for sna in range(2):
		o.SnowWall(pos=(20+sna*5.4,5,28))
		o.SnowWall(pos=(20+sna*5.4,8.2,28))
	#crates
	h1=.75+.16
	h2=.925+.16
	h3=5.375+.16
	mt.crate_block(ID=1,POS=(.5,h2,-58),CNT=[2,2,2])
	mt.crate_plane(ID=2,POS=(-.7,h2,-57),CNT=[2,2])
	mt.crate_wall(ID=12,POS=(-.3,h2,-18.6),CNT=[3,3])
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
	mt.crate_row(ID=2,POS=(18,2.625+.16,2.3),CNT=4,WAY=0)
	mt.crate_row(ID=3,POS=(21,2.6,2.3),CNT=3,WAY=0)
	c.place_crate(ID=8,p=(24.5,3.525+.16,2.2))
	c.place_crate(ID=8,p=(23.7,4.5,2.2))
	mt.crate_plane(ID=1,POS=(21.6,h3,5.4),CNT=[3,3])
	c.place_crate(ID=3,p=(23.2,5.45+.16,13))
	c.place_crate(ID=10,p=(37,h3+.48,30.4))
	c.place_crate(ID=5,p=(6.8,2.125+.16,2.3))
	c.place_crate(ID=5,p=(24.3,h3,5))
	mt.bounce_twin(POS=(24.5,h3,6),CNT=1)
	if not 1 in status.COLOR_GEM:
		c.place_crate(ID=16,p=(.75,.925+.16,-56.7))
	#checkpoints
	c.place_crate(ID=6,p=(-.2,h2,-40))
	c.place_crate(ID=6,p=(3.2,1.325+.16,2.3))
	c.place_crate(ID=6,p=(23,h3,4.2))
	c.place_crate(ID=6,p=(24.4,h3,27))
	#wumpa fruits
	whl=1.2
	mt.wumpa_plane(POS=(-.5,whl,-58.4),CNT=3)
	mt.wumpa_plane(POS=(-.3,1.1,-46),CNT=3)
	mt.wumpa_plane(POS=(-.3,1.1,-37),CNT=3)
	mt.wumpa_plane(POS=(-.3,1.1,-29.5),CNT=3)
	mt.wumpa_plane(POS=(-.3,1.1,-27.8),CNT=2)
	mt.wumpa_plane(POS=(-.3,1.1,-24),CNT=2)
	mt.wumpa_plane(POS=(-.3,1.1,-19.8),CNT=3)
	mt.wumpa_double_row(POS=(-.5,1.5,2.25),CNT=8)
	mt.wumpa_double_row(POS=(5.7,1.8,2.25),CNT=3)
	mt.wumpa_double_row(POS=(13,2.85,2.25),CNT=12)
	mt.wumpa_plane(POS=(22.7,5.6,5),CNT=3)
	mt.wumpa_plane(POS=(22.7,5.6,8.4),CNT=3)
	mt.wumpa_plane(POS=(22.7,5.7,22),CNT=3)
	mt.wumpa_double_row(POS=(25,5.6,27),CNT=16)
	#collecable
	if not status.level_index in status.CRYSTAL:
		item.EnergyCrystal(pos=(35.5,6.4,28.5))
	#end
	o.EndRoom(pos=(43,8,44),c=color.rgb32(80,80,120))
	#mt.crate_row(ID=11,POS=(19.96,2.96,2.5),WAY=0,CNT=4)
	invoke(free_level,delay=3)

def level3():##water
	#default
	o.EndRoom(pos=(1,3.7,88),c=color.rgb32(200,210,200))
	o.BonusPlatform(pos=(.85,1.3,.85*8))
	if not status.level_index in status.CRYSTAL:
		item.EnergyCrystal(pos=(0,2.5,60.5))
	if not 5 in status.COLOR_GEM:
		c.place_crate(ID=16,p=(0,.24+.16,-21))
	#cam switch
	o.CamSwitch(pos=(1,1.2,2.5),sca=(2,.2,6))
	o.CamSwitch(pos=(-.8,1.2,6.8),sca=(2,.2,1))
	o.CamSwitch(pos=(0,1.2,54.7),sca=(1,.2,1))
	o.CamSwitch(pos=(0,2.1,57.1),sca=(2,.2,1))
	#waterflow
	o.WaterFlow(pos=(0,-.3,-16),sca=(5,32))
	o.WaterFlow(pos=(0,.7,30),sca=(5,62))
	o.WaterFlow(pos=(0,1.7,73),sca=(5,32))
	#waterfall
	o.WaterFall(pos=(0,-.8,-1))
	o.WaterFall(pos=(0,.2,57))
	#scene
	o.SceneWall(pos=(-3.1,.65,-13),s=1)
	o.SceneWall(pos=(3,.5,-13),s=2)
	o.SceneWall(pos=(-3.1,1.7,16),s=1)
	o.SceneWall(pos=(3,1.7,16),s=2)
	o.SceneWall(pos=(-3.1,1.7,45),s=1)
	o.SceneWall(pos=(3,1.7,45),s=2)
	o.SceneWall(pos=(-3.1,2.4,74),s=1)
	o.SceneWall(pos=(3,2.4,74),s=2)
	#bush
	for wbu in range(16):
		o.bush(pos=(-3.2,2.7,-30+wbu*2),s=(2,2+random.uniform(.5,2.5),2),c=color.rgb32(0,100+random.uniform(20,100),0),ro_y=-35)
		o.bush(pos=(3.2,3,-31+wbu*2),s=(2,2+random.uniform(.5,2.5),2),c=color.rgb32(0,100+random.uniform(20,100),0),ro_y=35)
		o.bush(pos=(-3.2,3.5,1+wbu*2),s=(2,2+random.uniform(.5,2.5),2),c=color.rgb32(0,100+random.uniform(20,100),0),ro_y=-35)
		o.bush(pos=(3.2,3.5,1+wbu*2),s=(2,2+random.uniform(.5,2.5),2),c=color.rgb32(0,100+random.uniform(20,100),0),ro_y=35)
	for wba in range(32):
		o.bush(pos=(-3.2,4.2,31+wba*2),s=(2,2+random.uniform(.5,2.5),2),c=color.rgb32(0,100+random.uniform(20,100),0),ro_y=-35)
		o.bush(pos=(3.2,3.6,31+wba*2),s=(2,2+random.uniform(.5,2.5),2),c=color.rgb32(0,100+random.uniform(20,100),0),ro_y=35)
	#crate
	u0=.82
	mt.bounce_twin(POS=(-.85,.1,-26.5),CNT=1)
	mt.crate_block(ID=2,POS=(.5,.1,-27.1),CNT=[2,2,2])
	mt.crate_block(ID=1,POS=(-1.4,.24+.16,-21.6),CNT=[2,2,2])
	c.place_crate(ID=4,p=(1.2,.24+.16,-21.4))
	mt.crate_plane(ID=2,POS=(-.85,.16,-15),CNT=[3,3])
	mt.bounce_twin(POS=(-1.4,.24+.16,-11.5),CNT=1)
	mt.bounce_twin(POS=(1.6,.24+.16,-11.5),CNT=1)
	mt.crate_wall(ID=2,POS=(-.2,.16,-3.8),CNT=[2,2])
	mt.crate_wall(ID=1,POS=(.65,1.05+.16,2.5),CNT=[2,2])
	mt.crate_row(ID=1,POS=(0,u0,19.7),CNT=6,WAY=1)
	c.place_crate(ID=1,p=(0,u0,24.5))
	c.place_crate(ID=2,p=(0,u0,27.5))
	c.place_crate(ID=1,p=(0,u0,30.5))
	c.place_crate(ID=3,p=(0,u0,34.5))
	c.place_crate(ID=3,p=(0,u0,35.5))
	c.place_crate(ID=1,p=(-1,u0,35.5))
	c.place_crate(ID=2,p=(-1,u0,36.5))
	c.place_crate(ID=3,p=(-1,u0,37.5))
	c.place_crate(ID=3,p=(0,u0,37.5))
	c.place_crate(ID=1,p=(0,u0,38.5))
	c.place_crate(ID=4,p=(0,u0,39.5))
	mt.crate_plane(ID=1,POS=(-.7,u0,44),CNT=[3,3])
	mt.crate_plane(ID=1,POS=(.3,u0,48),CNT=[2,2])
	c.place_crate(ID=9,p=(1.3,1.16,52.4),m=1)
	for _c in range(10):
		c.place_crate(ID=13,p=(0,u0,52.4+.32*_c),m=1,l=0)
	mt.crate_plane(ID=1,POS=(-.36,1.8,69.8),CNT=[3,6])
	c.place_crate(ID=10,p=(.85,1.95+.16,80.85))
	mt.crate_wall(ID=1,POS=(-.2,1.05+.16,14.5),CNT=[2,2])
	mt.crate_row(ID=2,POS=(-.85,1.05+.16,40.4),CNT=4,WAY=1)
	c.place_crate(ID=7,p=(-1,2.04+.16,58.4),m=1)
	mt.crate_row(ID=2,POS=(-1,3.6,58.4),CNT=4,WAY=2)
	mt.bounce_twin(POS=(1,2.04+.16,58.4),CNT=1)
	#aku
	c.place_crate(ID=5,p=(-.85,1.05+.16,9.3))
	#checkpoints
	c.place_crate(ID=6,p=(0,.24+.16,-9.2))
	c.place_crate(ID=6,p=(0,1.05+.16,32.8))
	c.place_crate(ID=6,p=(.85,1.05+.16,44.6))
	c.place_crate(ID=6,p=(0,2.04+.16,58.5))
	#temple
	o.TempleWall(pos=(-2.55,-.3,-1.7),side=2)
	o.TempleWall(pos=(2.7,-.3,-1.7),side=1)
	o.TempleWall(pos=(-2.55,.7,27),side=2)
	o.TempleWall(pos=(2.7,.7,27),side=1)
	o.TempleWall(pos=(-2.55,.65,56.4),side=2)
	o.TempleWall(pos=(2.7,.65,56.4),side=1)
	#tree
	o.TreeScene(pos=(-2.3,2.2,82.5),s=.02)
	o.TreeScene(pos=(2.3,2.2,82.5),s=.02)
	o.TreeScene(pos=(-3,2.8,84),s=.02)
	o.TreeScene(pos=(2.4,2.8,84),s=.02)
	o.bush(pos=(-1,4,82),s=2,c=color.green)
	o.bush(pos=(0,4.3,82.1),s=2,c=color.green)
	o.bush(pos=(1,4,82.11),s=2,c=color.green)
	#stage
	o.WoodStage(pos=(0,.2,-20))
	o.WoodStage(pos=(0,.2,-10))
	o.WoodStage(pos=(0,2,60))
	#platforms
	o.MossPlatform(p=(0,-.3,-24.5),ptm=3)
	o.MossPlatform(p=(0,-.1,-1.3),ptm=0)
	o.MossPlatform(p=(0,.5,0),ptm=0)
	o.MossPlatform(p=(0,-.3,-7),ptm=0)
	o.MossPlatform(p=(-.3,.7,11.5),ptm=2)
	o.MossPlatform(p=(-.85,.5,52.5),ptm=3)
	o.MossPlatform(p=(.85,.5,52.5),ptm=0)
	o.MossPlatform(p=(0,1,56.5),ptm=0)
	#o.MossPlatform(p=(0,1.5,63.5),ptm=3)
	o.MossPlatform(p=(0,1.5,77),ptm=3)
	#blocks
	tH=-.2
	#e0
	o.multi_tile(p=(-.85,tH,-29),cnt=[3,4])
	o.multi_tile(p=(-1,tH,-17),cnt=[3,1])
	o.multi_tile(p=(-1,tH,-15),cnt=[3,3])
	o.multi_tile(p=(0,tH,-5),cnt=[1,4])
	#e1
	o.multi_tile(p=(.85,tH+1.1,0),cnt=[1,6])
	o.multi_tile(p=(-.85,tH+1.1,.85*5),cnt=[2,1])
	o.multi_tile(p=(-.85,tH+1.1,.85*5),cnt=[1,8])
	o.multi_tile(p=(0,tH+1.1,.85*8),cnt=[2,1])
	o.multi_tile(p=(0,tH+1.1,13),cnt=[1,3])
	o.StoneTile(pos=(0,tH+1.1,17))
	o.StoneTile(pos=(0,tH+1.1,19))
	o.multi_tile(p=(-.85,tH+1.1,23),cnt=[2,1])
	o.multi_tile(p=(0,tH+1.1,26),cnt=[2,1])
	o.multi_tile(p=(-.85,tH+1.1,29),cnt=[2,1])
	o.multi_tile(p=(0,tH+1.1,32),cnt=[1,2])
	o.multi_tile(p=(-.85,tH+1.1,40.5),cnt=[3,3])
	o.multi_tile(p=(.85,tH+1.1,40.5+.85*3),cnt=[1,4])
	o.multi_tile(p=(-.85,tH+1.1,40.5+.85*7),cnt=[3,1])
	o.multi_tile(p=(-.85,tH+1.1,40.5+.85*8),cnt=[1,4])
	#e3
	o.multi_tile(p=(0,1.7,57.4),cnt=[1,1])
	o.multi_tile(p=(0,1.8,66.5),cnt=[1,3])
	o.multi_tile(p=(0,1.8,66.5+.85*7),cnt=[1,4])
	o.multi_tile(p=(0,1.8,80),cnt=[1,5])
	o.multi_tile(p=(.85,1.8,80+.85),cnt=[1,1])
	#npc
	N.Hippo(pos=(0,1.8,64.7))
	N.Hippo(pos=(0,1.8,63))
	N.spawn(mID=6,pos=(-.85,1.05,29),mDirec=0,mTurn=0)
	N.spawn(mID=6,pos=(.85,1.05,25.8),mDirec=0,mTurn=0)
	N.spawn(mID=6,pos=(-.85,1.05,23),mDirec=0,mTurn=0)
	N.spawn(mID=6,pos=(0,1.05,41.4),mDirec=0,mTurn=0)
	N.spawn(mID=6,pos=(0,1.95,74.1),mDirec=0,mTurn=0)
	N.spawn(mID=2,pos=(0,1.05,4.2),mDirec=0,mTurn=0)
	invoke(free_level,delay=3)

def level4():## sewer
	o.Water(pos=(0,.2,-45),s=(8,8),c=color.rgb(100,100,130),a=.5,typ=1)
	o.SewerTunnel(pos=(0,.4,-53))
	o.SewerTunnel(pos=(0,.4,-44))
	o.SewerTunnel(pos=(0,.4,-35))
	o.SewerTunnel(pos=(0,.4,-26))
	o.SewerPlatform(pos=(0,.5,-58))
	#o.SewerTunnel(pos=(0,1.2,-45))
	N.spawn(pos=(0,.5,-58),mID=9,mDirec=0,mTurn=0)
	o.swr_multi_ptf(p=(-.5,.5,-61.3),cnt=[3,3])
	#o.SewerEscape(pos=(0,-1,-52.6))
	invoke(free_level,delay=1)