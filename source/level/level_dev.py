import sys,os,_loc,item,status,objects,map_tools,crate,npc,item,danger
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
	LC.AMB_M_COLOR=color.rgb32(140,140,140)
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

def load_object():
	Entity(model='cube',scale=(16,1,16),y=-.5,texture_scale=(16,16),collider='box',texture='white_cube',alpha=1)
	for gm in range(6):
		item.GemStone(pos=(-5+gm/2,.3,7),c=gm)
	#item.GemStone(pos=(1,.3,1),c=5)
	item.TimeTrialClock(pos=(-1.75,.3,7))
	item.EnergyCrystal(pos=(-1,.3,7))
	item.ExtraLive(pos=(-.3,.3,7))
	#o.BonusPlatform(pos=(1,.15,-25))
	#o.PseudoGemPlatform(pos=(0,.3,-25),t=1)
	#o.PseudoGemPlatform(pos=(1,.3,-25),t=2)
	#o.PseudoGemPlatform(pos=(2,.3,-25),t=3)
	#o.PseudoGemPlatform(pos=(3,.3,-25),t=4)
	#o.PseudoGemPlatform(pos=(4,.3,-25),t=5)
	#o.GemPlatform(pos=(0,.3,-26),t=1)
	#o.GemPlatform(pos=(1,.3,-26),t=2)
	#o.GemPlatform(pos=(2,.3,-26),t=3)
	#o.GemPlatform(pos=(3,.3,-26),t=4)
	#o.GemPlatform(pos=(4,.3,-26),t=5)
	o.StartRoom(pos=(0,0,-8.1))
	#o.EndRoom(pos=(20,2,0),c=color.rgb32(180,200,200))
def load_crate():
	CZ=5
	mt.crate_block(ID=0,POS=(-7.5,.16,CZ),CNT=[3,1,1])
	mt.crate_block(ID=0,POS=(-7.5,.16,CZ+.32),CNT=[3,2,2])
	mt.crate_block(ID=0,POS=(-7.5,.16,CZ+.64),CNT=[3,1,3])
	mt.crate_block(ID=1,POS=(-6.5,.16,CZ),CNT=[3,3,1])
	mt.crate_block(ID=2,POS=(-5.5,.16,CZ),CNT=[3,3,1])
	mt.crate_block(ID=3,POS=(-4.5,.16,CZ),CNT=[3,3,1])
	mt.crate_block(ID=4,POS=(-3.5,.16,CZ),CNT=[3,3,1])
	mt.crate_block(ID=5,POS=(-2.5,.16,CZ),CNT=[3,1,1])
	mt.crate_block(ID=6,POS=(-1.5+.32,.16,CZ),CNT=[1,1,1])
	mt.crate_block(ID=7,POS=(-.5,.16,CZ),CNT=[3,3,1])
	mt.crate_block(ID=8,POS=(.5,.16,CZ),CNT=[3,3,1])
	mt.crate_block(ID=9,POS=(1.5+.32,.16,CZ),CNT=[1,1,1])
	mt.crate_block(ID=10,POS=(2.5+.32,.16,CZ),CNT=[1,1,1])
	mt.crate_block(ID=11,POS=(3.5+.32,.16,CZ),CNT=[1,1,8])
	mt.crate_block(ID=12,POS=(4.5+.32,.16,CZ),CNT=[1,1,3])
	mt.crate_block(ID=13,POS=(5.5,.16,CZ),CNT=[3,3,3])
	mt.crate_block(ID=14,POS=(6.5,.16,CZ),CNT=[3,3,3])
def load_wumpa():
	mt.wumpa_wall(POS=(.5,.3,7),CNT=[5,2])
def load_npc():
	return
	#n.spawn(ID=0,POS=(-3,0,-14),RNG=.5,DRC=2,RTYP=1)
	#n.spawn(ID=8,POS=(1,0,-12),RNG=.5,DRC=2,RTYP=1,CMV=True)
	#n.spawn(ID=2,POS=(-1,0,-14),RNG=1,DRC=2)
	#n.spawn(ID=3,POS=(-0,0,-14),RNG=0,DRC=1)
	#n.spawn(ID=4,POS=(1,0,-14),RNG=0,DRC=1)
	#n.spawn(ID=5,POS=(2,0,-14),RNG=0,DRC=1)
	#n.spawn(ID=6,POS=(3,0,-14),RNG=0,DRC=1)
	########################################
	#n.spawn(ID=7,POS=(-3,0,-16),RNG=0,DRC=1)
	#n.spawn(ID=8,POS=(-2,0,-16),RNG=1,DRC=0,CMV=True)
	#n.spawn(ID=10,POS=(-1,0,-16),RNG=0,DRC=1)
	#n.spawn(ID=11,POS=(0,0,-16),RNG=0,DRC=1)
	#n.spawn(ID=12,POS=(1,0,-16),RNG=0,DRC=1)
	#n.spawn(ID=13,POS=(2,0,-16),RNG=0,DRC=1)
	#n.spawn(ID=14,POS=(3,0,-16),RNG=0,DRC=1)
	########################################
	#n.spawn(ID=16,POS=(-3,0,-18),RNG=0,DRC=1)
	#n.spawn(ID=17,POS=(-2,0,-18),RNG=0,DRC=1)
	#n.spawn(ID=19,POS=(-1,0,-18),RNG=1,DRC=0)

## bonus level / gem path
def bonus_zone():
	Entity(model='wireframe_cube',scale=2,position=(0,-30,-3),collider='box')
def gem_zone():
	return