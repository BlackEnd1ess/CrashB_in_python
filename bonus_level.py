import crate,item,status,objects,map_tools,npc,random
from ursina import *

MT=map_tools
st=status
o=objects
c=crate
N=npc
U=-3
def load_bonus_level(idx):
	lv_lst={1:bonus1,2:bonus2,3:bonus3,4:bonus4,5:bonus5,6:dev_bonus}
	lv_lst[idx]()

##bonus level
def bonus1():
	o.BonusPlatform(pos=(11.5,-37,U))
	o.Water(pos=(0,-39,0),s=(60,60),c=color.rgb32(100,110,110),a=.9)
	for w in range(2):
		o.BackgroundWall(p=(0+w*14,-37,2))
	for bc0 in range(6):
		c.place_crate(ID=0,p=(0+bc0/3.1,-37,U))
		c.place_crate(ID=0,p=(3+bc0/3.1,-37,U))
		c.place_crate(ID=0,p=(6+bc0/3.1,-37,U))
		c.place_crate(ID=0,p=(9+bc0/3.1,-37,U))
	c.place_crate(ID=8,p=(4,-36.66,U))
	MT.crate_row(ID=1,POS=(4,-35,U),WAY=2,CNT=4)
	MT.crate_wall(ID=1,POS=(1,-36.66,U),CNT=[3,3])
	MT.crate_wall(ID=2,POS=(6,-36.66,U),CNT=[2,2])
	c.place_crate(ID=4,p=(9,-36.66,U))
	MT.wumpa_row(POS=(9,-36,U),CNT=4,WAY=2)
	MT.wumpa_row(POS=(9.4,-36.6,U),CNT=4,WAY=0)
	MT.wumpa_row(POS=(1.6,-36,U),CNT=4,WAY=0)

def bonus2():
	o.FallingZone(pos=(0,-40,0),s=(64,1,64))
	for sw in range(5):
		o.SnowWall(pos=(-4+sw*5.4,-33.9,-2.5))
		o.SnowWall(pos=(-4+sw*5.4,-37,-2.5))
		o.SnowWall(pos=(-4+sw*5.4,-40.1,-2.5))
	o.mBlock(pos=(0,-37.4,U),sca=(3,.5,.5))
	o.mBlock(pos=(4,-37.4,U),sca=(3,.5,.5))
	o.mBlock(pos=(8,-37.4,U),sca=(3,.5,.5))
	o.mBlock(pos=(14,-37.4,U),sca=(3,.5,.5))
	MT.crate_row(ID=0,POS=(3.8,-35,U),WAY=0,CNT=8)
	MT.crate_wall(ID=2,POS=(4,-34.68,U),CNT=[2,2])
	c.place_crate(ID=4,p=(5.3,-34.68,U))
	c.place_crate(ID=1,p=(8.3,-36.68,U))
	c.place_crate(ID=1,p=(7.5,-36,U))
	c.place_crate(ID=1,p=(7,-35.5,U))
	c.place_crate(ID=9,p=(15,-37,U),m=1)
	c.place_crate(ID=13,p=(4,-37,U),m=1,l=2)
	MT.crate_row(ID=1,POS=(10,-37.32,U),WAY=0,CNT=7)
	MT.crate_row(ID=3,POS=(10.32,-37.64,U),WAY=0,CNT=5)
	MT.wumpa_double_row(POS=(-.5,-37.1,U),CNT=5)
	MT.wumpa_double_row(POS=(10,-36.3,U),CNT=7)
	MT.wumpa_double_row(POS=(10,-36.9,U),CNT=7)
	MT.wumpa_double_row(POS=(2.8,-37.1,U),CNT=8)
	MT.wumpa_double_row(POS=(7,-37.1,U),CNT=8)
	o.BonusPlatform(pos=(16,-37.1,U))

def bonus3():
	o.BonusBackground(pos=(10,-40,35),sca=(80,35))
	MT.wumpa_double_row(POS=(12.8,-35,U),CNT=6)
	MT.wumpa_double_row(POS=(-.5,-36.5,U),CNT=4)
	MT.wumpa_row(POS=(1.5,-36.35,U),CNT=3,WAY=0)
	MT.wumpa_row(POS=(3.5,-35.35,U),CNT=3,WAY=0)
	MT.wumpa_row(POS=(5.5,-34.85,U),CNT=3,WAY=0)
	MT.wumpa_row(POS=(17.5,-35.35,U),CNT=3,WAY=0)
	o.FallingZone(pos=(0,-40,0),s=(64,1,64))
	o.MushroomTree(pos=(2,-39,U+1.2),typ=1)
	o.MushroomTree(pos=(4,-39,U+1.2),typ=1)
	o.MushroomTree(pos=(6,-38.5,U+1.2),typ=1)
	MT.crate_row(ID=0,POS=(-1,-37,U),WAY=0,CNT=7)
	MT.bounce_twin(POS=(7.2,-36.16,U),CNT=5)
	o.MushroomTree(pos=(9.5,-38.5,U+1.2),typ=1)
	o.MushroomTree(pos=(10.5,-38,U+1.2),typ=1)
	o.MushroomTree(pos=(11.5,-38,U+1.2),typ=1)
	o.BonusScene(pos=(-5,-43,4))
	o.BonusScene(pos=(8,-43,3.9))
	o.BonusScene(pos=(21,-43,3.9))

	o.BonusScene(pos=(-3,-44,6))
	o.BonusScene(pos=(6,-44,5.9))
	o.BonusScene(pos=(19,-44,6))

	c.place_crate(ID=11,p=(12.5,-36,U))
	MT.crate_row(ID=12,POS=(12.82,-36,U),WAY=0,CNT=7)
	MT.crate_row(ID=1,POS=(12.82,-35.68,U),WAY=0,CNT=7)
	o.MushroomTree(pos=(16,-38,U+1.2),typ=1)
	o.MushroomTree(pos=(18,-38,U+1.2),typ=1)
	MT.crate_wall(ID=1,POS=(16,-35.65+.16,U+.1),CNT=[2,2])
	c.place_crate(ID=2,p=(4,-36.65+.16,U+.1))
	c.place_crate(ID=4,p=(5.8,-35.1,U))
	MT.crate_row(ID=2,POS=(10.4,-35.65+.16,U+.1),CNT=4,WAY=0)
	o.BonusPlatform(pos=(19.3,-35.7,U))

def bonus4():
	o.FallingZone(pos=(0,-42,0),s=(64,1,64))
	#bg walls
	Entity(model='quad',texture='res/terrain/l4/sewer_tiles.jpg',scale=(60,20),texture_scale=(30,10),position=(0,-35,1),color=color.rgb32(160,150,150))
	#pipes
	o.SewerPipe(pos=(8.3,-36.4,U),typ=3)
	for swp in range(3):
		o.SewerPipe(pos=(2+swp*13,-34,.6),typ=2)
		o.SewerPipe(pos=(4.5+swp*13,-34,.6),typ=2)
		o.SewerPipe(pos=(7+swp*13,-34,.6),typ=2)
		o.SewerPipe(pos=(3+swp*13,-36,.6),typ=0)
		o.SewerPipe(pos=(6+swp*13,-36,.6),typ=0)
	#
	for swl in range(3):
		o.SewerWall(pos=(-2+swl*13,-38,0))
		o.SewerWall(pos=(-2+swl*13,-30.8,0))
	#platform
	o.swr_multi_ptf(p=(0,-36.5,U),cnt=[3,1])
	o.swr_multi_ptf(p=(2,-36,U),cnt=[1,1])
	o.swr_multi_ptf(p=(3,-35.5,U),cnt=[4,1])
	o.swr_multi_ptf(p=(5,-34,U),cnt=[7,1])
	o.swr_multi_ptf(p=(9,-34,U),cnt=[3,1])
	
	o.swr_multi_ptf(p=(8.5,-36,U),cnt=[5,1])
	o.swr_multi_ptf(p=(12,-36,U),cnt=[3,1])
	o.swr_multi_ptf(p=(14,-35.5,U),cnt=[1,1])
	o.swr_multi_ptf(p=(15,-35,U),cnt=[1,1])
	o.swr_multi_ptf(p=(16,-34.5,U),cnt=[1,1])
	o.swr_multi_ptf(p=(17,-34.5,U),cnt=[4,1])
	o.swr_multi_ptf(p=(20,-34.5,U),cnt=[4,1])
	#crate
	c.place_crate(ID=4,p=(2,-35.9+.16,U))
	c.place_crate(ID=1,p=(2,-35.9+.48,U))
	c.place_crate(ID=7,p=(4.4,-35.4+.16,U))
	c.place_crate(ID=11,p=(4.4-.32,-35.4+.16,U))
	c.place_crate(ID=12,p=(5.57,-33.74,U))
	c.place_crate(ID=12,p=(6.49,-33.74,U))
	c.place_crate(ID=12,p=(7.45,-33.74,U))
	c.place_crate(ID=9,p=(10,-33.7,U),m=2)
	MT.crate_row(ID=13,POS=(6.1,-36,U),CNT=7,WAY=0,m=2,l=3)
	MT.crate_row(ID=2,POS=(12.5,-35.74,U),CNT=3,WAY=2)
	MT.crate_wall(ID=2,POS=(17.47,-34.24,U),CNT=[3,2])
	c.place_crate(ID=11,p=(21.2,-34.24,U))
	c.place_crate(ID=12,p=(12.97,-35.74,U))
	c.place_crate(ID=1,p=(12.97,-35.74+.32,U))
	c.place_crate(ID=12,p=(14.12,-35.24,U))
	c.place_crate(ID=2,p=(14.12,-35.24+.32,U))
	c.place_crate(ID=12,p=(14.97,-34.74,U))
	c.place_crate(ID=1,p=(14.97,-34.74+.32,U))
	c.place_crate(ID=12,p=(15.98,-34.24,U))
	c.place_crate(ID=1,p=(15.98,-34.24+.32,U))
	c.place_crate(ID=12,p=(16.97,-34.24,U))
	c.place_crate(ID=1,p=(16.97,-34.24+.32,U))
	#wumpa fruits
	MT.wumpa_double_row(POS=(.4,-36.24,U),CNT=3)
	MT.wumpa_double_row(POS=(3,-35.24,U),CNT=3)
	MT.wumpa_double_row(POS=(8.48,-35.74,U),CNT=7)
	MT.wumpa_double_row(POS=(20.02,-34.24,U),CNT=3)
	MT.wumpa_row(POS=(4.5,-34.6,U),CNT=4,WAY=2)
	MT.wumpa_row(POS=(12,-35.74,U),CNT=4,WAY=2)
	MT.wumpa_row(POS=(8.48,-35.3,U),CNT=8,WAY=2)
	o.BonusPlatform(pos=(22.3,-34.2,U))

def bonus5():
	o.FallingZone(pos=(0,-42,0),s=(128,.3,32))
	o.spw_ruin_ptf(p=(-1,-37,U),cnt=4,way=0)
	o.spw_ruin_ptf(p=(2,-36.5,U),cnt=2,way=0)
	o.spw_ruin_ptf(p=(4.5,-36.5,U),cnt=3,way=0)
	o.spw_ruin_ptf(p=(6.75,-36,U),cnt=4,way=0)
	o.LoosePlatform(pos=(10,-35.8,U),t=1)
	o.LoosePlatform(pos=(11.5,-36,U),t=1)
	o.LoosePlatform(pos=(13,-36.5,U),t=1)
	o.spw_ruin_ptf(p=(14,-36.7,U),cnt=8,way=0)
	o.spw_ruin_ptf(p=(21,-36.7,U),cnt=1,way=0)
	o.spw_ruin_ptf(p=(21.75,-36.2,U),cnt=1,way=0)
	o.spw_ruin_ptf(p=(24,-36.2,U),cnt=1,way=0)
	o.spw_ruin_ptf(p=(24.75,-36.7,U),cnt=3,way=0)
	o.spw_ruin_ptf(p=(31.17,-36.7,U),cnt=6,way=0)
	#crate
	MT.crate_stair(ID=1,POS=(26.8,-36.3,U),CNT=4,WAY=0)
	MT.crate_row(ID=1,POS=(26.8+.32*4,-36.3+.32*3,U),CNT=5,WAY=0)
	MT.crate_stair(ID=1,POS=(26.8+.32*9,-36.3+.32*3,U),CNT=4,WAY=1)
	MT.bounce_twin(POS=(26.8+.32*4,-36.3+.32*4,U),CNT=5)
	#
	MT.crate_wall(ID=2,POS=(-1.1,-36.34,U),CNT=[2,2])
	MT.crate_wall(ID=1,POS=(8.2,-35.34,U),CNT=[1,2])
	MT.crate_wall(ID=2,POS=(14.7,-36,U),CNT=[1,2])
	MT.crate_wall(ID=1,POS=(25.5,-36,U),CNT=[1,2])
	MT.crate_wall(ID=2,POS=(34.4,-36,U),CNT=[1,2])
	c.place_crate(ID=12,p=(4.4,-35.84,U))
	c.place_crate(ID=12,p=(16.3,-36,U))
	c.place_crate(ID=12,p=(17.7,-36,U))
	c.place_crate(ID=12,p=(32.9,-36,U))
	c.place_crate(ID=9,p=(35,-36,U),m=103)
	MT.crate_row(ID=13,POS=(22.42,-35.86,U),CNT=4,m=103,l=1,WAY=0)
	MT.crate_row(ID=13,POS=(22.42,-35.86-.32,U),CNT=4,m=103,l=2,WAY=0)
	MT.crate_row(ID=13,POS=(22.42,-35.86-.64,U),CNT=4,m=103,l=3,WAY=0)
	MT.crate_row(ID=13,POS=(22.42,-35.86-.96,U),CNT=4,m=103,l=11,WAY=0)
	c.place_crate(ID=4,p=(21.7,-35.54,U))
	#wumpa
	MT.wumpa_double_row(POS=(.5,-36.2,U),CNT=3)
	MT.wumpa_double_row(POS=(1.9,-35.7,U),CNT=4)
	MT.wumpa_double_row(POS=(4.9,-35.7,U),CNT=4)
	MT.wumpa_double_row(POS=(6.7,-35.2,U),CNT=4)
	MT.wumpa_double_row(POS=(33.4,-35.9,U),CNT=4)
	MT.wumpa_double_row(POS=(13.8,-35.9,U),CNT=2)
	MT.wumpa_double_row(POS=(15.2,-35.9,U),CNT=3)
	MT.wumpa_double_row(POS=(16.7,-35.9,U),CNT=3)
	MT.wumpa_double_row(POS=(18.2,-35.9,U),CNT=4)
	MT.wumpa_row(POS=(9.9,-35.25,U),CNT=5,WAY=2)
	MT.wumpa_row(POS=(11.5,-35.45,U),CNT=5,WAY=2)
	MT.wumpa_row(POS=(13,-35.95,U),CNT=5,WAY=2)
	MT.wumpa_row(POS=(21,-35.90,U),CNT=5,WAY=2)
	MT.wumpa_row(POS=(23.9,-35.40,U),CNT=5,WAY=2)
	#stair left
	MT.wumpa_row(POS=(26.8,-35.9,U),CNT=3,WAY=2)
	MT.wumpa_row(POS=(26.8+.32,-35.9+.32,U),CNT=3,WAY=2)
	MT.wumpa_row(POS=(26.8+.32*2,-35.9+.32*2,U),CNT=3,WAY=2)
	MT.wumpa_row(POS=(26.8+.32*3,-35.9+.32*3,U),CNT=3,WAY=2)
	#stair right
	MT.wumpa_row(POS=(26.8+.32*9,-35.9+.32*3,U),CNT=3,WAY=2)
	MT.wumpa_row(POS=(26.8+.32*10,-35.9+.32*2,U),CNT=3,WAY=2)
	MT.wumpa_row(POS=(26.8+.32*11,-35.9+.32,U),CNT=3,WAY=2)
	MT.wumpa_row(POS=(26.8+.32*12,-35.9,U),CNT=3,WAY=2)
	#background
	o.RuinRuins(pos=(-2.5,-37,U+1),ro_y=45,typ=0)
	o.RuinRuins(pos=(0,-37,U+2),ro_y=90,typ=0)
	o.RuinRuins(pos=(3,-36.8,U+2),ro_y=90,typ=0)
	o.RuinRuins(pos=(6,-36.6,U+2),ro_y=90,typ=0)
	o.RuinRuins(pos=(9,-36.8,U+2),ro_y=90,typ=0)
	o.RuinRuins(pos=(12,-36.6,U+2),ro_y=90,typ=0)
	o.RuinRuins(pos=(15,-36.8,U+2),ro_y=90,typ=0)
	o.RuinRuins(pos=(18,-36.6,U+2),ro_y=90,typ=0)
	o.RuinRuins(pos=(21,-36.8,U+2),ro_y=90,typ=0)
	o.RuinRuins(pos=(24,-36.6,U+2),ro_y=90,typ=0)
	o.RuinRuins(pos=(27,-36.8,U+2),ro_y=90,typ=0)
	o.RuinRuins(pos=(30,-36.6,U+2),ro_y=90,typ=0)
	o.RuinRuins(pos=(33,-36.8,U+2),ro_y=90,typ=0)
	o.RuinRuins(pos=(36,-36.6,U+2),ro_y=90,typ=0)
	o.RuinRuins(pos=(39,-36.8,U+2),ro_y=90,typ=0)
	o.BonusPlatform(pos=(36,-36,U))

def dev_bonus():
	return

## gem route
def gem_route1():
	o.LevelScene(pos=(200,0,128),sca=(200,40,1))
	o.LevelScene(pos=(200,-20,127),sca=(200,40,1))
	o.Water(pos=(200,-.1,10),s=(8,50),c=color.rgb32(80,80,120),a=1)
	o.Water(pos=(200,2.3,50),s=(16,40),c=color.rgb32(80,80,120),a=1)
	o.FallingZone(pos=(200,-4,0),s=(40,1,32))
	o.mBlock(pos=(200,0,-3),sca=(2,4))
	o.mBlock(pos=(200,0,1),sca=(1,1))
	o.mBlock(pos=(200,.5,3),sca=(1,1))
	o.mBlock(pos=(200,1,5),sca=(1,1))
	o.MossPlatform(p=(200,.6,7),ptm=0)
	o.MossPlatform(p=(200,.6,9),ptm=0)
	o.MossPlatform(p=(200,.6,11),ptm=0)
	o.mBlock(pos=(200,1,15),sca=(1,5))
	o.mBlock(pos=(200,1,20),sca=(3,5))
	o.mBlock(pos=(200,2,25),sca=(3,5))
	o.mBlock(pos=(200,3,28),sca=(3,1))
	o.mBlock(pos=(200,3,29),sca=(1,1))
	o.mBlock(pos=(200,3,30),sca=(1,1))
	o.mBlock(pos=(200,3,31),sca=(1,1))
	o.mBlock(pos=(201,3,31),sca=(1,1))
	o.mBlock(pos=(202,3,31),sca=(1,1))
	o.mBlock(pos=(202,3,32),sca=(1,1))
	o.mBlock(pos=(202,3,33),sca=(1,1))
	o.mBlock(pos=(202,3,34),sca=(1,1))
	o.mBlock(pos=(201,3,34),sca=(1,1))
	o.mBlock(pos=(200,3,34),sca=(1,1))
	o.mBlock(pos=(200,3,35),sca=(1,1))
	o.mBlock(pos=(200,3,36),sca=(1,1))
	o.mBlock(pos=(200,3,37),sca=(1,1))
	o.mBlock(pos=(201,3,37),sca=(1,1))
	o.mBlock(pos=(202,3,37),sca=(1,1))
	o.mBlock(pos=(202,3,38),sca=(1,1))
	o.mBlock(pos=(202,3,39),sca=(1,1))
	o.mBlock(pos=(202,3,40),sca=(1,1))
	o.mBlock(pos=(202,3,41),sca=(1,1))
	for moss_x in range(3):
		for moss_z in range(5):
			c.place_crate(ID=13,p=(201+moss_x/1.1,3.3,42+moss_z*1.2),m=121,l=11)
			o.MossPlatform(p=(201+moss_x/1.1,2.6,42+moss_z*1.2),ptm=random.randint(0,1))
	o.mBlock(pos=(202,3,50),sca=(3,4))
	c.place_crate(ID=8,p=(200,1.125+.16,22.14))
	c.place_crate(ID=8,p=(200,2.125+.16,27))
	#decoration
	twc=color.rgb32(50,50,255)
	o.TempleWall(col=twc,pos=(197.5,-.5,15.5),side=2)
	o.TempleWall(col=twc,pos=(202.5,-.5,15.5),side=1)
	o.TempleWall(col=twc,pos=(197.5,0,19),side=2)
	o.TempleWall(col=twc,pos=(202.5,0,19),side=1)
	o.TempleWall(col=twc,pos=(197.5,.5,23),side=2)
	o.TempleWall(col=twc,pos=(202.5,.5,23),side=1)
	o.TempleWall(col=twc,pos=(197.5,1,27),side=2)
	o.TempleWall(col=twc,pos=(202.5,1,27),side=1)
	o.TempleWall(col=twc,pos=(198,1.5,31),side=2)
	o.TempleWall(col=twc,pos=(203.5,1.5,31),side=1)
	o.TempleWall(col=twc,pos=(198,1.5,35),side=2)
	o.TempleWall(col=twc,pos=(198,1.5,39),side=2)
	o.TempleWall(col=twc,pos=(199.5,1.5,62),side=2)
	o.TempleWall(col=twc,pos=(204.8,1.5,61),side=1)
	#trees
	o.spawn_tree_wall(pos=(197.6,1.1,-7),cnt=11,d=0)
	o.spawn_tree_wall(pos=(202.2,1.1,-7),cnt=11,d=1)
	o.spawn_tree_wall(pos=(199,3.8,41),cnt=11,d=0)
	o.spawn_tree_wall(pos=(205,3.8,32),cnt=15,d=1)
	o.TreeScene(pos=(202.7,3.725,51.7),s=.0175)
	#bush
	o.bush(pos=(198.7,0,17.45),s=1.5,c=color.green)
	o.bush(pos=(197.8,0,17.44),s=1.5,c=color.green)
	o.bush(pos=(201,0,17.45),s=1.5,c=color.green)
	o.bush(pos=(202,0,17.44),s=1.5,c=color.green)
	o.bush(pos=(199,2.3,29.4),s=1.5,c=color.green)
	o.bush(pos=(201,2.3,29.4),s=1.5,c=color.green)
	o.bush(pos=(202,2.3,29.41),s=1.5,c=color.green)
	o.bush(pos=(199,1.5,29.),s=1.5,c=color.green)
	o.bush(pos=(201,1.5,29.),s=1.5,c=color.green)
	o.bush(pos=(202,1.5,29.01),s=1.5,c=color.green)
	o.bush(pos=(199.1,2,39.7),s=2,c=color.green)
	o.bush(pos=(199.1,3,39.72),s=2,c=color.green)
	#grass
	o.GrassSide(pos=(197.5,.9,0),ry=0)
	o.GrassSide(pos=(202.5,.9,0),ry=180)
	o.GrassSide(pos=(199,3.3,55.1),ry=0)
	o.GrassSide(pos=(205,3.3,47),ry=180)
	#crate
	MT.crate_wall(ID=1,POS=(199.3,.29,-3.7),CNT=[1,2])
	MT.crate_plane(ID=1,POS=(200.3,3.29-.32,32.3),CNT=[2,2])
	MT.crate_plane(ID=11,POS=(201,3.29-.32,35.3),CNT=[2,2])
	MT.crate_plane(ID=1,POS=(200.6,3.29-.32,38.3),CNT=[2,2])
	MT.bounce_twin(POS=(199,3.29,28),CNT=1)
	MT.bounce_twin(POS=(200.9,3.29,28),CNT=1)
	MT.crate_plane(ID=11,POS=(200,1.26-.32,7.8),CNT=[1,1])
	c.place_crate(ID=9,p=(203.3,3.29-.32,37),m=121)
	MT.crate_plane(ID=3,POS=(200,1.26-.32,9.8),CNT=[1,1])
	c.place_crate(ID=5,p=(200,1.28,16.2))
	MT.crate_plane(ID=1,POS=(199,1.28,20.2),CNT=[2,2])
	MT.crate_plane(ID=2,POS=(200.9,2.29,24.7),CNT=[2,3])
	MT.crate_wall(ID=2,POS=(202.9,3.29,50.3),CNT=[2,2])
	MT.bounce_twin(POS=(201,3.29,50.9),CNT=1)
	#wumpa
	MT.wumpa_row(POS=(200,1.32,12.9),CNT=9,WAY=1)
	MT.wumpa_row(POS=(200,3.33,28.8),CNT=5,WAY=1)
	MT.wumpa_row(POS=(202,3.33,31.3),CNT=8,WAY=1)
	MT.wumpa_row(POS=(200,3.33,34.3),CNT=8,WAY=1)
	MT.wumpa_row(POS=(202,3.33,37),CNT=12,WAY=1)
	MT.wumpa_row(POS=(200.0,3.33,30.9),CNT=7,WAY=0)
	MT.wumpa_row(POS=(200.0,3.33,33.9),CNT=6,WAY=0)
	MT.wumpa_row(POS=(200.4,3.33,36.9),CNT=5,WAY=0)
	MT.wumpa_plane(POS=(200.7,.33,-4.7),CNT=[1,6])
	MT.wumpa_plane(POS=(199.8,.33,.7),CNT=[2,2])
	MT.wumpa_plane(POS=(199.8,.82,2.7),CNT=[2,2])
	MT.wumpa_plane(POS=(199.8,1.32,4.7),CNT=[2,2])
	MT.wumpa_plane(POS=(200,1.32,18.1),CNT=[5,8])
	MT.wumpa_plane(POS=(199,2.33,23),CNT=[5,8])
	MT.wumpa_plane(POS=(201,3.33,48.5),CNT=[5,3])
	#npc
	N.spawn(mID=1,pos=(200,1.125,18.565),mDirec=0)
	N.spawn(mID=2,pos=(200,2.125,24.3),mDirec=0)
	N.spawn(mID=2,pos=(201.15,3.125,31),mDirec=0)
	N.spawn(mID=1,pos=(201,3.125,34),mDirec=0)
	N.spawn(mID=2,pos=(202,3.125,38.8587),mDirec=1)
	o.GemPlatform(pos=(202,3.3,51.2),t=4)

def gem_route4():
	Entity(model='cube',scale=(16,1,96),position=(200,-1.2,-16),collider='box',color=color.black)
	o.swr_multi_ptf(p=(199.75,-.4,-3.25),cnt=[2,2])
	o.EletricWater(pos=(200,-.5,22),sca=(8,64),ID=3)
	o.SewerTunnel(pos=(200,-.3,5),c=color.rgb32(0,200,180))
	o.SewerTunnel(pos=(200,-.3,15),c=color.rgb32(0,200,180))
	o.SewerTunnel(pos=(200,-.3,25),c=color.rgb32(0,200,180))
	o.SewerEntrance(pos=(200,1,-3))
	o.SwimPlatform(pos=(200,-.45,-.7))
	o.SwimPlatform(pos=(200-.3,-.45,.7))
	c.place_crate(ID=0,p=(200,-.5,-2))
	c.place_crate(ID=0,p=(200,-.5,2))
	c.place_crate(ID=9,p=(200,-.5,3),m=101)
	c.place_crate(ID=13,p=(200,-.5,4),l=8,m=101)
	c.place_crate(ID=9,p=(200,-.5,6),m=102)
	MT.crate_row(ID=13,POS=(200,-.5,6.32),CNT=8,WAY=1,l=0,m=102)
	MT.crate_row(ID=13,POS=(200,-.5,6+.32*9),CNT=3,WAY=0,l=0,m=102)
	MT.crate_row(ID=13,POS=(200+.32*2,-.5,6+.32*10),CNT=5,WAY=1,l=0,m=102)
	o.SwimPlatform(pos=(200+.3,-.45,11.8))
	o.SwimPlatform(pos=(200,-.45,12.8))
	o.SwimPlatform(pos=(200-.3,-.45,13.8))
	MT.crate_row(ID=13,POS=(200-.32*2,-.5,14.5),CNT=5,WAY=1,l=0,m=102)
	MT.crate_row(ID=13,POS=(200-.32*2,-.5,14.5+.32*5),CNT=4,WAY=0,l=0,m=102)
	MT.crate_row(ID=13,POS=(200+.32*2,-.5,14.5+.32*5),CNT=7,WAY=1,l=0,m=102)
	o.SwimPlatform(pos=(200+.3,-.45,18.7))
	o.SwimPlatform(pos=(200,-.45,19.7))
	o.SwimPlatform(pos=(200-.3,-.45,20.7))
	MT.crate_row(ID=13,POS=(200-.32,-.5,21.5),CNT=7,WAY=1,l=0,m=102)
	MT.crate_row(ID=13,POS=(200-.32,-.5,21.5+.32*7),CNT=4,WAY=0,l=0,m=102)
	MT.crate_row(ID=13,POS=(200-.32+.32*3,-.5,21.5+.32*8),CNT=8,WAY=1,l=0,m=102)
	N.spawn(pos=(200,0,5),mID=13,mDirec=1)
	N.spawn(pos=(200,0,16),mID=13,mDirec=1)
	N.spawn(pos=(200,0,19.7),mID=13,mDirec=1)
	N.spawn(pos=(200,0,23.7),mID=13,mDirec=1)
	o.SewerEscape(pos=(200,-1,30),c=color.rgb32(0,200,180))
	o.SewerEntrance(pos=(200,1,27))
	Entity(model='cube',scale=(4,.5,7),position=(200,-.5,31),texture_scale=(4,5),collider='box',texture='res/terrain/l4/metal_01.jpg')
	N.spawn(pos=(200,-.25,29),mID=11,mDirec=0,ro_mode=1)
	o.SewerWall(pos=(200,-1.7,33))
	if not 2 in st.COLOR_GEM:
		item.GemStone(c=2,pos=(200,0,28.9))
	o.GemPlatform(pos=(200,0,31.9),t=5)

def gem_route5():
	o.FallingZone(pos=(200,-5,0),s=(40,1,32))
	o.spw_ruin_ptf(p=(200,-3,U),cnt=1,way=0)
	o.spw_ruin_ptf(p=(200-.75,-3,U+1.5),cnt=3,way=0)
	for rn_a in range(3):
		o.spw_ruin_ptf(p=(200+(.75*3+rn_a*1.5),-3,U+1.5),cnt=1,way=0)
	o.spw_ruin_ptf(p=(206.5,-3,U+1.5),cnt=2,way=0)
	for rn_b in range(5):
		o.spw_ruin_ptf(p=(200.5+.75*8,-3,U+(.75*3+rn_b*1.5)),cnt=1,way=0)
	o.spw_ruin_ptf(p=(206.4-.75,-3,6.8),cnt=3,way=0)
	for rn_c in range(7):
		o.spw_ruin_ptf(p=(202+(.75*3-rn_c*1.5),-3,U+.75*13),cnt=1,way=0)
	o.spw_ruin_ptf(p=(194,-3,U+.75*13),cnt=3,way=1)
	o.spw_ruin_ptf(p=(193.25,-3,U+.75*13),cnt=3,way=1)
	for rn_dx in range(6):
		for rn_dz in range(4):
			o.spw_ruin_ptf(p=(189.5+(rn_dx*1.5),-3,U+(.75*17)+(rn_dz*1.3)),cnt=1,way=0)
	o.spw_ruin_ptf(p=(194,-3,15.5),cnt=5,way=1)
	for llpf in range(7):
		o.LoosePlatform(pos=(194,-2.8,19.5+llpf*1.5),t=0)
	for fnp_x in range(4):
		for fnp_z in range(4):
			o.spw_ruin_ptf(p=(193.25+.75*fnp_x,-3,30+.75*fnp_z),cnt=1,way=0)
	o.MonkeySculpture(pos=(194-1,-2.6,21),r=False,d=True,ro_y=-90)
	o.MonkeySculpture(pos=(194+1,-2.6,24),r=False,d=True,ro_y=90)
	o.MonkeySculpture(pos=(194-1,-2.6,27),r=False,d=True,ro_y=-90)
	# npc
	N.spawn(mID=14,pos=(206.4,-2.5,7.1),mDirec=0)
	N.spawn(mID=14,pos=(195.2,-2.5,6.75),mDirec=3)
	N.spawn(mID=14,pos=(206.75,-2.5,-1.5),mDirec=1)
	N.spawn(mID=14,pos=(197.3,-2.5,9.7),mDirec=1)
	N.spawn(mID=14,pos=(197.3,-2.5,12.3),mDirec=1)
	N.spawn(mID=14,pos=(189.2,-2.5,11),mDirec=3)
	N.spawn(mID=14,pos=(189.2,-2.5,13.6),mDirec=3)
	#background
	o.RuinRuins(pos=(198,-4,0),ro_y=-90,typ=3)
	o.RuinRuins(pos=(193,-4,1),ro_y=-90,typ=3)
	o.RuinRuins(pos=(209,-4,2),ro_y=90,typ=3)
	o.RuinRuins(pos=(200,-3,1),ro_y=60,typ=0)
	o.RuinRuins(pos=(202,-3,4),ro_y=90,typ=0)
	o.RuinRuins(pos=(203.5,-3,1),ro_y=70,typ=0)
	o.RuinRuins(pos=(203.7,-3,3.3),ro_y=0,typ=0)
	o.RuinRuins(pos=(205,-3.2,3.3),ro_y=0,typ=0)
	o.RuinRuins(pos=(199,-3,5),ro_y=90,typ=0)
	o.RuinRuins(pos=(196.5,-2.4,8.2),ro_y=90,typ=0)
	o.RuinRuins(pos=(199,-2.5,9.2),ro_y=90,typ=0)
	o.RuinRuins(pos=(201.5,-2.6,8.2),ro_y=90,typ=0)
	o.RuinRuins(pos=(204,-2.3,9.2),ro_y=90,typ=0)
	o.RuinRuins(pos=(206.5,-2.4,8.2),ro_y=90,typ=0)
	o.RuinRuins(pos=(209,-2.6,9.2),ro_y=90,typ=0)
	o.RuinRuins(pos=(211.5,-2.5,8.2),ro_y=90,typ=0)
	o.RuinRuins(pos=(190,-3,8.2),ro_y=90,typ=0)
	o.RuinRuins(pos=(192,-2.9,7.3),ro_y=0,typ=0)
	o.RuinRuins(pos=(197,-4,22),ro_y=90,typ=3)
	o.RuinRuins(pos=(191,-4,22),ro_y=-90,typ=3)
	o.RuinRuins(pos=(198,-4,35),ro_y=90,typ=3)
	o.RuinRuins(pos=(191,-4,35),ro_y=-90,typ=3)
	if not 3 in st.COLOR_GEM:
		item.GemStone(c=3,pos=(194.4,-2,37.7))
	o.EndRoom(pos=(195.5,-1.01,37.7),c=color.rgb32(220,100,220))