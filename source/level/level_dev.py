import sys,os,_loc,item,status,objects,map_tools,crate,npc,danger
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ursina.ursinastuff import destroy
from ursina import *

mt=map_tools
st=status
o=objects
dg=danger
LC=_loc
c=crate
n=npc

def map_setting():
	LC.FOG_L_COLOR=color.rgb32(20,70,50)
	LC.FOG_B_COLOR=color.rgb32(20,70,50)
	LC.AMB_M_COLOR=color.rgb32(150,150,150)
	LC.SKY_BG_COLOR=color.rgb32(20,20,20)
	st.toggle_thunder=False
	st.toggle_rain=False
	LC.LV_DST=(15,20)
	LC.BN_DST=(10,15)
	LC.RCZ=30
	LC.RCX=16
	LC.RCB=6

def start_load():
	load_crate()
	load_object()
	load_wumpa()
	load_npc()
	map_setting()

##for youtube and git
def presentation():
	item.GemStone(pos=(-.8,.3,6.2),c=0)
	item.GemStone(pos=(-.8,.3+.225,6.6),c=1)
	item.GemStone(pos=(-.8,.3+.51,7),c=3)
	item.GemStone(pos=(-.4,.3,6.2),c=2)
	item.GemStone(pos=(-.4,.3+.225,6.6),c=4)
	item.GemStone(pos=(-.4,.3+.45,7),c=5)
	item.EnergyCrystal(pos=(.2,.6,7))
	item.ExtraLive(pos=(-3.8,.3,7))
	item.TimeTrialClock(pos=(-3.8,.6,7))
	item.TimeRelic(pos=(.6,-.3,7),rank=0)
	item.TimeRelic(pos=(.6,.2,7),rank=1)
	item.TimeRelic(pos=(.6,.7,7),rank=2)
	c.spawn(ID=0,p=(-3,.16,7))
	c.spawn(ID=1,p=(-3,.16+.32,7))
	c.spawn(ID=2,p=(-3,.16+.32*2,7))
	c.spawn(ID=3,p=(-3,.16+.32*3,7))
	c.spawn(ID=4,p=(-3+.4,.16,7))
	c.spawn(ID=5,p=(-3+.4,.16+.32,7))
	c.spawn(ID=6,p=(-3+.4,.16+.32*2,7))
	c.spawn(ID=7,p=(-3+.4,.16+.32*3,7))
	c.spawn(ID=8,p=(-3+.8,.16,7))
	c.spawn(ID=9,p=(-3+.8,.16+.32,7))
	c.spawn(ID=10,p=(-3+.8,.16+.32*2,7),m=1)
	c.spawn(ID=11,p=(-3+.8,.16+.32*3,7))
	c.spawn(ID=12,p=(-3+1.2,.16,7))
	c.spawn(ID=13,p=(-3+1.2,.16+.32,7))
	c.spawn(ID=14,p=(-3+1.2,.16+.32*2,7),m=1)
	c.spawn(ID=16,p=(-3+1.2,.16+.32*3,7))
	c.spawn(ID=15,p=(-3+1.6,.16,7),m=1,l=1)
	c.spawn(ID=15,p=(-3+1.6,.16+.32,7),m=1,l=2)
	c.spawn(ID=15,p=(-3+1.6,.16+.32*2,7),m=1,l=3)
	o.BonusPlatform(pos=(0,.15,4))
	o.BonusPlatform(pos=(1.3,.15,4),ID=1)
	o.PseudoGemPlatform(pos=(0,.3,2),t=1)
	o.PseudoGemPlatform(pos=(.8,.3,2),t=2)
	o.PseudoGemPlatform(pos=(1.6,.3,2),t=3)
	o.PseudoGemPlatform(pos=(.4,.3,2.8),t=4)
	o.PseudoGemPlatform(pos=(1.2,.3,2.8),t=5)

def load_object():
	Entity(model='cube',scale=(16,1,16),y=-.5,texture_scale=(16,16),collider='box',texture='grass',alpha=0)
	o.StartRoom(pos=(0,0,-8.1))
	#o.EndRoom(pos=(2,2,12.),c=color.rgb32(180,200,200))
def load_crate():
	CZ=5
	mt.crate_block(ID=12,POS=(0,.16,0),CNT=[3,1,1])
	mt.crate_block(ID=0,POS=(0,.16+.32,0),CNT=[3,1,1])
	#mt.crate_block(ID=0,POS=(-7.5,.16,CZ),CNT=[3,1,1])
	#mt.crate_block(ID=0,POS=(-7.5,.16,CZ+.32),CNT=[3,2,2])
	#mt.crate_block(ID=0,POS=(-7.5,.16,CZ+.64),CNT=[3,1,3])
	#mt.crate_block(ID=1,POS=(-6.5,.16,CZ),CNT=[3,3,1])
	#mt.crate_block(ID=2,POS=(-5.5,.16,CZ),CNT=[3,3,1])
	#mt.crate_block(ID=3,POS=(-4.5,.16,CZ),CNT=[3,3,1])
	#mt.crate_block(ID=4,POS=(-3.5,.16,CZ),CNT=[3,3,1])
	#mt.crate_block(ID=5,POS=(-2.5,.16,CZ),CNT=[3,1,1])
	#mt.crate_block(ID=6,POS=(-1.5+.32,.16,CZ),CNT=[1,1,1])
	#mt.crate_block(ID=7,POS=(-.5,.16,CZ),CNT=[3,3,1])
	#mt.crate_block(ID=8,POS=(.5,.16,CZ),CNT=[3,3,1])
	#mt.crate_block(ID=9,POS=(1.5+.32,.16,CZ),CNT=[1,1,1])
	#mt.crate_block(ID=10,POS=(2.5+.32,.16,CZ),CNT=[1,1,1])
	#mt.crate_block(ID=11,POS=(3.5+.32,.16,CZ),CNT=[1,1,8])
	#mt.crate_block(ID=12,POS=(4.5+.32,.16,CZ),CNT=[1,1,3])
	#mt.crate_block(ID=13,POS=(5.5,.16,CZ),CNT=[3,3,3])
	#mt.crate_block(ID=14,POS=(6.5,.16,CZ),CNT=[3,3,3])
	#c.spawn(ID=15,p=(5,.16,CZ-3),m=-1,l=1)
	#c.spawn(ID=15,p=(5.5,.16,CZ-3),m=-1,l=2)
	#c.spawn(ID=15,p=(6,.16,CZ-3),m=-1,l=3)
def load_wumpa():
	return
def load_npc():
	return
## bonus level / gem path
def bonus_zone():
	Entity(model='wireframe_cube',scale=2,position=(0,-30,-3),collider='box')
def gem_zone():
	return