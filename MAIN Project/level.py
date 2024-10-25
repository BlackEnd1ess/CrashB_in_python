import ui,_core,status,environment,bonus_level,_loc,sound,level_structure,LODsystem
from ursina import *

lvs=level_structure
bn=bonus_level
env=environment
st=status
cc=_core
sn=sound
## start level
def free_level():
	camera.rotation_x=15
	LODsystem.start()
	st.loading=False
	cc.spawn_level_crystal(st.level_index)
	st.fails=0
	sn.LevelMusic(T=st.level_index)
	if st.level_index == 3:
		sn.AmbienceSound()
		sn.WaterRiver()
	cc.level_ready=True
	ui.load_interface()

## level settings
def main_instance(idx):
	st.loading=True
	st.weather_thunder=(idx == 5)
	lv_info={1:lambda:level1(),
			2:lambda:level2(),
			3:lambda:level3(),
			4:lambda:level4(),
			5:lambda:level5(),
			6:lambda:test()}
	lv_info[idx]()
	env.env_switch(idx)
	bn.load_bonus_level(idx)

## levels to load
def test():
	lvs.dev_object()
	lvs.dev_crate()
	lvs.dev_wumpa()
	lvs.dev_npc()
	free_level()

def level1():## turtle woods
	bn.gem_route1()
	lvs.lv1_crate()
	lvs.lv1_object()
	lvs.lv1_wumpa()
	lvs.lv1_npc()
	invoke(free_level,delay=3)

def level2():## road to nowhere
	st.gem_death=False
	lvs.lv2_crate()
	lvs.lv2_object()
	lvs.lv2_wumpa()
	lvs.lv2_npc()
	invoke(free_level,delay=3)

def level3():## upstream
	lvs.lv3_crate()
	lvs.lv3_object()
	lvs.lv3_wumpa()
	lvs.lv3_npc()
	invoke(free_level,delay=3)

def level4():## drained eel
	lvs.lv4_crate()
	lvs.lv4_object()
	lvs.lv4_wumpa()
	lvs.lv4_npc()
	bn.gem_route4()
	invoke(free_level,delay=3)

def level5():## ruined
	lvs.lv5_crate()
	lvs.lv5_object()
	lvs.lv5_wumpa()
	lvs.lv5_npc()
	bn.gem_route5()
	invoke(free_level,delay=3)