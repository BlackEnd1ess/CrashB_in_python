import sys,os,_loc,item,status
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import objects,map_tools,crate,npc,item,gc
from ursina import *

mt=map_tools
st=status
o=objects
LC=_loc
c=crate
n=npc

def map_setting():
	LC.FOG_L_COLOR=color.rgb32(20,70,50)
	LC.FOG_B_COLOR=color.rgb32(20,70,50)
	LC.AMB_M_COLOR=color.rgb32(140,140,140)
	LC.SKY_BG_COLOR=color.rgb32(0,60,80)
	st.toggle_thunder=False
	st.toggle_rain=False
	LC.LV_DST=(10,15)
	LC.BN_DST=(6,12)
	LC.RCZ=30
	LC.RCX=16
	LC.RCB=6

def start_load():
	load_crate()
	load_object()
	load_wumpa()
	load_npc()
	map_setting()
	gc.collect()

def load_object():
	Entity(model='cube',scale=(16,1,64),y=-.5,texture_scale=(32,64),collider='box',texture='grass',alpha=1)
	item.GemStone(pos=(4,.4,-20),c=1)
	o.PseudoGemPlatform(pos=(0,.3,-21),t=1)
	o.PseudoGemPlatform(pos=(1,.3,-21),t=2)
	o.PseudoGemPlatform(pos=(2,.3,-21),t=3)
	o.PseudoGemPlatform(pos=(3,.3,-21),t=4)
	o.PseudoGemPlatform(pos=(4,.3,-21),t=5)
	o.GemPlatform(pos=(0,.3,-22),t=1)
	o.GemPlatform(pos=(1,.3,-22),t=2)
	o.GemPlatform(pos=(2,.3,-22),t=3)
	o.GemPlatform(pos=(3,.3,-22),t=4)
	o.GemPlatform(pos=(4,.3,-22),t=5)
	o.StartRoom(pos=(0,0,-32.2))
	o.EndRoom(pos=(.5,2,0),c=color.rgb32(180,200,200))
def load_crate():
	mt.crate_block(ID=0,POS=(-7.5,.16,-18),CNT=[3,1,1])
	mt.crate_block(ID=0,POS=(-7.5,.16,-18+.32),CNT=[3,2,2])
	mt.crate_block(ID=0,POS=(-7.5,.16,-18+.64),CNT=[3,1,3])
	mt.crate_block(ID=1,POS=(-6.5,.16,-18),CNT=[3,3,3])
	mt.crate_block(ID=2,POS=(-5.5,.16,-18),CNT=[3,3,2])
	mt.crate_block(ID=3,POS=(-4.5,.16,-18),CNT=[3,3,1])
	mt.crate_block(ID=4,POS=(-3.5,.16,-18),CNT=[3,3,1])
	mt.crate_block(ID=5,POS=(-2.5,.16,-18),CNT=[3,1,1])
	mt.crate_block(ID=6,POS=(-1.5+.32,.16,-18),CNT=[1,1,1])
	mt.crate_block(ID=7,POS=(-.5,.16,-18),CNT=[3,3,1])
	mt.crate_block(ID=8,POS=(.5,.16,-18),CNT=[3,3,1])
	mt.crate_block(ID=9,POS=(1.5+.32,.16,-18),CNT=[1,1,1])
	mt.crate_block(ID=10,POS=(2.5+.32,.16,-18),CNT=[1,1,1])
	mt.crate_block(ID=11,POS=(3.5+.32,.16,-18),CNT=[1,1,2])
	mt.crate_block(ID=12,POS=(4.5+.32,.16,-18),CNT=[1,1,4])
	mt.crate_block(ID=13,POS=(5.5,.16,-18),CNT=[3,3,3])
	mt.crate_block(ID=14,POS=(6.5,.16,-18),CNT=[3,3,3])
def load_wumpa():
	mt.wumpa_plane(POS=(0,.3,-14),CNT=[5,5])
def load_npc():
	n.spawn(ID=4,POS=(0,0,-25),RNG=1,DRC=2)

## bonus level / gem path
def bonus_zone():
	return
def gem_zone():
	return