import crate,objects,_core,status,environment,bonus_level,sound,item,npc,map_tools
from ursina import *

mt=map_tools
bn=bonus_level
env=environment
cc=_core
o=objects
c=crate
N=npc

def ambience(thunder,weather,daymode):
	status.day_mode=daymode
	dm={'day':color.cyan,
		'evening':color.rgb(255,110,90),
		'night':color.rgb(0,0,85),
		'dark':color.black,
		'rain':color.rgb(70,70,70),
		'woods':color.rgb(70,120,110)}
	env.SkyBox(m=dm[daymode],t=thunder)
	env.LightAmbience(d=daymode)
	env.Fog(d=daymode)
	env.ShadowMap(c=dm[daymode])
	wthr={0:lambda:print('rain, snow disabled'),
		1:lambda:env.RainFall(),
		2:lambda:env.SnowFall()}
	wthr[weather]()

##levels
def developer_level():
	cc.preload_objects()
	status.level_index=6
	ambience(thunder=0,weather=0,daymode='day')
	status.loading=True
	o.StartRoom(pos=(-.5,0,-8.2))##start
	status.loading=False
	o.LevelFinish(p=(-2,0,-1))##end
	o.MapTerrain(MAP='map/lv1.png',size=(16,1.5,16),t='white_cube',co=color.rgb(150,150,150))
	o.CrateScore(pos=(-1,.25,-1))##clear gem
	o.BonusPlatform(pos=(0,.1,-1))
	for CC in range(14):
		c.place_crate(ID=CC,p=(-7+CC/2,0,7),m=1,l=1)
	for GS in range(6):
		item.GemStone(pos=(1.5+GS/2,.25,7),c=GS)
	for MM in range(12):
		npc.spawn(pos=(-7+MM,0,4),mID=MM,mDirec=1,mTurn=0)
	item.EnergyCrystal(pos=(1,.5,7)) ##crystal
	for TR in range(3):
		item.TimeRelic(pos=(4.5+TR/2,.25,7),t=TR)
	for WX in range(4):
		for WY in range(4):
			item.WumpaFruit(pos=(1+WX/3,+WY/3,0))
	for gPL in range(6):
		o.GemPlatform(pos=(0+gPL,.25,-3),t=gPL)
	sound.LevelMusic(T=5)
	cc.level_ready=True

def test():
	status.level_index=1
	status.loading=True
	ambience(thunder=0,weather=0,daymode='day')
	o.StartRoom(pos=(-.5,0,-8.2))##start
	o.MapTerrain(MAP='map/0.png',size=(32,1,32),t='grass',co=color.rgb(130,150,130))
	o.CrateScore(pos=(-1,.25,-1))
	sound.LevelMusic(T=status.level_index)
	#item.WumpaFruit(pos=(0,.2,0))
	#mt.steel_bridge(POS=(-2,0,0),CNT=10)
	#mt.crate_stair(ID=0,POS=(8.16,0,6),CNT=5,WAY=0)
	mt.crate_row(ID=1,POS=(0,0,-1),CNT=10,WAY=2)
	mt.crate_row(ID=1,POS=(1,0,-1),CNT=10,WAY=2)
	mt.crate_row(ID=1,POS=(2,0,-1),CNT=10,WAY=2)
	#mt.crate_wall(ID=1,POS=(3,0,7),CNT=4)
	#mt.bounce_twin(POS=(-7,0,6),CNT=5)
	#mt.crate_block(ID=1,POS=(-3,0,3),CNT=3)
	#mt.crate_plane(ID=2,POS=(2,0,1),CNT=6)
	#mt.wumpa_row(POS=(0,0,0),CNT=5,WAY=0)
	#mt.wumpa_row(POS=(6,0,0),CNT=5,WAY=1)
	#mt.wumpa_double_row(POS=(0,0,-1),CNT=5)
	#mt.wumpa_plane(POS=(4,0,-2),CNT=5)
	status.loading=False
	cc.level_ready=True

def level1():
	TS=16
	status.level_index=1
	status.loading=True
	ambience(thunder=0,weather=1,daymode='woods')
	sound.LevelMusic(T=status.level_index)
	o.MapTerrain(MAP='map/'+str(status.level_index)+'.png',size=(TS/1.6,1.5,TS*8),t='grass',co=color.rgb(0,70,0))
	o.Water(pos=(0,.6,0),s=(10,128),c=color.rgb(40,40,60),a=.8)
	o.StartRoom(pos=(-.3,1,-64.2))
	o.BonusPlatform(pos=(1.5,1.4,-7))
	bn.load_bonus_level(status.level_index)
	#plants
	o.TreeScene(pos=(-1.37,1.5,-46),c=color.rgb(110,130,100),s=.0175)
	o.TreeScene(pos=(1.32,1.5,-46),c=color.rgb(110,130,100),s=.0175)
	o.TreeScene(pos=(0,1.7,-26.4),c=color.rgb(110,130,100),s=.0175)
	o.TreeScene(pos=(0,1.5,-2.7),c=color.rgb(110,130,100),s=.02)
	o.TreeScene(pos=(3,1.7,10.6),c=color.rgb(110,130,100),s=.02)
	o.TreeScene(pos=(-2.5,1.7,10.6),c=color.rgb(110,130,100),s=.02)
	for trE in range(10):
		o.TreeScene(pos=(0+random.uniform(-.1,.1),.7,-2+trE),c=color.rgb(110,130,100),s=.02)
	o.spawn_tree_wall(pos=(-4.6,2.73,-64),cnt=50,d=0)
	o.spawn_tree_wall(pos=(-5.7,2,-63),cnt=50,d=0)
	o.spawn_tree_wall(pos=(4.2,2.73,-64),cnt=50,d=1)
	o.spawn_tree_wall(pos=(5.3,2,-64),cnt=50,d=1)
	o.bush(pos=(.37,1.3,-26.5),s=2,c=color.orange)
	o.bush(pos=(1.5,1.4,-14.2),s=2,c=color.green)
	o.bush(pos=(-1.5,1.4,-14.2),s=2,c=color.orange)
	o.bush(pos=(-1,1.4,-12),s=2,c=color.green)
	o.bush(pos=(1,1.4,-12),s=2,c=color.orange)
	o.bush(pos=(2.43,1.4,10.7),s=3,c=color.green)
	o.bush(pos=(-2.37,1.4,10.7),s=3,c=color.yellow)
	#platform
	o.GemPlatform(pos=(1.25,1.6,-15),t=4)
	o.BigPlatform(p=(0,1,-53.5),s=(4,0,8))
	o.BigPlatform(p=(0,1,-37),s=(3,0,2))
	o.BigPlatform(p=(0,1.25,-34),s=(1,0,1))
	o.BigPlatform(p=(0,1.25,-29),s=(1,0,3))
	o.BigPlatform(p=(-2,1.25,-25),s=(1,0,3))
	o.BigPlatform(p=(1,1.25,-20),s=(1,0,3))
	o.BigPlatform(p=(0,1.4,-14),s=(4,0,2))
	o.BigPlatform(p=(0,1.4,-6.5),s=(2,0,4))
	o.BigPlatform(p=(-1.8,1,2),s=(2,0,6))
	o.BigPlatform(p=(1.8,1,-2),s=(2,0,2))
	o.BigPlatform(p=(1.8,1,8),s=(2,0,2))
	o.BigPlatform(p=(0,1.4,14),s=(6,0,6))
	o.MossPlatform(p=(0,1,-44),MO=False,TU=0)
	o.MossPlatform(p=(0,1,-42),MO=True,TU=0)
	o.MossPlatform(p=(0,1,-40),MO=False,TU=0)
	#NPC
	N.spawn(mID=0,pos=(0,1.1,-52),mDirec=0,mTurn=0)
	N.spawn(mID=0,pos=(0,1.1,-38),mDirec=0,mTurn=0)
	N.spawn(mID=1,pos=(0,1.4,-15),mDirec=0,mTurn=0)
	#crates
	mt.crate_block(ID=1,POS=(-.7,1.1,-57),CNT=2)
	mt.crate_block(ID=2,POS=(-1.8,1.03,3.3),CNT=2)
	mt.crate_block(ID=1,POS=(-1.5,1.03,-2.5),CNT=2)
	mt.crate_wall(ID=1,POS=(-.5,1.1,-49),CNT=3)
	c.place_crate(ID=5,p=(0,1.1,-54))
	mt.bounce_twin(POS=(-1,1.1,-36),CNT=1)
	mt.bounce_twin(POS=(1,1.1,-36),CNT=1)
	mt.crate_row(ID=1,POS=(-1.38,1.25,-22.5),CNT=6,WAY=0)
	c.place_crate(ID=9,m=1,l=0,p=(-1.33,1.25,-23))
	for aE in range(6):
		c.place_crate(ID=13,m=1,l=0,p=(-1.38+.32*aE,1.25,-22))
	mt.crate_row(ID=3,POS=(-1.38,1.25,-27),CNT=3,WAY=0)
	mt.crate_row(ID=2,POS=(-1.38,2.75,-27),CNT=3,WAY=0)
	c.place_crate(ID=6,p=(0,1.41,-13))
	mt.crate_row(ID=1,POS=(1.38,.7,.2),CNT=18,WAY=1)
	o.Corridor(pos=(0,1.425,-13))
	#collectable
	item.EnergyCrystal(pos=(0,2,-4))
	#M_objects
	o.RewardRoom(pos=(0,2.5,13),c=color.rgb(80,100,80))
	o.EndRoom(pos=(0,2.5,18),c=color.rgb(80,100,80))
	cc.level_ready=True

def level2():##3D
	status.level_index=2
	o.StartRoom(pos=(-.5,1,-50))
	tt='grass'#'res/terrain/texture/sand.jpg'
	o.MapTerrain(MAP='map/'+str(status.level_index)+'.png',size=(12,2,96),t=tt,co=color.gray)
	o.WaterFlow(pos=(-.5,.9,-50))
	for cr in range(4):
		for ccr in range(4):
			o.StoneTile(pos=(-1.5+cr/1.375,1,-47+ccr/1.375))
	ambience(thunder=0,weather=0,daymode='day')
	cc.level_ready=True