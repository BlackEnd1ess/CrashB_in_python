import objects,map_tools,crate,npc,item,sys,os,_loc,status,danger
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ursina import *

mt=map_tools
st=status
dg=danger
o=objects
LC=_loc
c=crate
n=npc

def map_setting():
    LC.FOG_L_COLOR=color.gray
    LC.FOG_B_COLOR=color.black
    LC.SKY_BG_COLOR=color.black
    LC.AMB_M_COLOR=color.rgb32(240,240,200)
    LC.LV_DST=(140,160)
    LC.BN_DST=(10,14)
    st.toggle_thunder=False
    st.toggle_rain=False

def start_load():
    bonus_zone()
    load_crate()
    load_object()
    load_wumpa()
    load_npc()
    map_setting()

def load_object():
    o.StartRoom(pos=(8,.5,-1))
    o.EndRoom(pos=(8,2,14),c=color.gray)
    o.spw_block(ID=0,p=(7,0,1),vx=[5,9],sca=(.5,.5,.3))
    o.ObjType_Block(ID=5,pos=(9,.6,6),sca=(.5,.8,.5),typ=1,ro_y=90)
    dg.Piston(pos=(9,.6+4.2,6),typ=0,spd=2)

def load_crate():
    mt.crate_wall(ID=11,POS=(8,.66+.32*4,8),CNT=[1,1])
    mt.crate_wall(ID=12,POS=(8,.66,8),CNT=[1,4])

def load_npc():
    return

def load_wumpa():
    return

def bonus_zone():
    return