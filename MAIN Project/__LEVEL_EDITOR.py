import environment,objects,_core,status,_loc,npc,crate,item,__le_struct,__le_cfg
from ursina import *
app=Ursina()

LE=__le_struct
st=__le_cfg

##load scene and grids
obf='res/objects/ev/'
def main_scene():
	Audio('res/snd/music/editor.mp3',loop=True,volume=.2)
	Entity(model=obf+'s_room/room.ply',texture=obf+'s_room/room.tga',position=(st.m_size[0]/2,0,-1),scale=(.07,.07,.08),rotation=(270,90),unlit=False,alpha=st.object_alpha)
	kp=Entity(model=obf+'e_room/e_room.ply',texture=obf+'e_room/e_room.tga',scale=.025,rotation=(-90,90,0),position=(0+st.m_size[0]/2,2,st.m_size[1]+4),unlit=False,alpha=st.object_alpha)
	LE.SpawnMenu()
	LE.MapInfo()
	print(kp.position)
	for vx in range(st.m_size[0]):
		for vz in range(st.m_size[1]):
			LE.MapBlock(pos=(0+vx,0,0+vz))
	LE.Cursor()
	del vx,vz

##key input
def input(key):
	if key in st.inp:
		st.inp[key]()
		del key

##init
print('Leveleditor loaded')
st.set_camera(),main_scene(),app.run()