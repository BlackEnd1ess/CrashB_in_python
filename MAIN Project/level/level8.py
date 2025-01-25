import objects,map_tools,crate,npc,item,sys,os,_loc,status
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ursina import *

mt=map_tools
st=status
o=objects
LC=_loc
c=crate
n=npc

def map_setting():
    LC.LV_DST=(10,15)
    LC.BN_DST=(5,10)
    window.color=color.black
    scene.fog_density=(15,20)
    scene.fog_color=color.black
    LC.AMBIENT_LIGHT.color=color.rgb32(140,140,200)
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
    o.StartRoom(pos=(8,0,-1))
    o.EndRoom(pos=(8,2,68),c=color.gray)
    o.FloorBlock(pos=Vec3(5, 0, 6),ID=1,sca=.5)
    o.FloorBlock(pos=Vec3(6, 0, 6),ID=1,sca=.5)
    o.FloorBlock(pos=Vec3(7, 0, 6),ID=1,sca=.5)
    o.FloorBlock(pos=Vec3(8, 0, 6),ID=1,sca=.5)
    o.FloorBlock(pos=Vec3(9, 0, 6),ID=1,sca=.5)
    o.FloorBlock(pos=Vec3(10, 0, 6),ID=1,sca=.5)
    o.FloorBlock(pos=Vec3(11, 0, 6),ID=1,sca=.5)

def load_crate():
    c.place_crate(ID=1,p=(5.0, 0.66, 6.0))
    c.place_crate(ID=1,p=(8.0, 0.66, 6.0))
    c.place_crate(ID=1,p=(11.0, 0.66, 6.0))
    c.place_crate(ID=1,p=(8.0, 0.66, 5.0))
    c.place_crate(ID=1,p=(8.0, 0.66, 4.0))
    c.place_crate(ID=1,p=(8.0, 0.66, 3.0))
    c.place_crate(ID=1,p=(8.0, 0.66, 2.0))
    c.place_crate(ID=1,p=(8.0, 0.66, 7.0))
    c.place_crate(ID=1,p=(8.0, 0.66, 8.0))
    c.place_crate(ID=1,p=(8.0, 0.66, 9.0))

def load_npc():
    npc.spawn(ID=2,POS=Vec3(6, 0.5, 6))
    npc.spawn(ID=2,POS=Vec3(10, 0.5, 6))

def load_wumpa():
    return

def bonus_zone():
    return