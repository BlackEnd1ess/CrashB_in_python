import ui,_core,status,environment,sound,LODsystem,sys,os,gc
from ursina import camera,invoke

lv='level'
st=status
cc=_core
sn=sound

## start level
def free_level():
	camera.rotation_x=15
	cc.check_nitro_stack()
	LODsystem.start()
	st.loading=False
	cc.spawn_level_crystal(st.level_index)
	st.fails=0
	sn.LevelMusic(T=st.level_index)
	if st.level_index == 3:
		sn.AmbienceSound()
		sn.WaterRiver()
	ui.load_interface()
	cc.level_ready=True
	gc.collect()

## level settings
def main_instance(idx):
	sys.path.append(os.path.join(os.path.dirname(__file__),lv))
	st.loading=True
	st.weather_thunder=(idx == 5)
	goto={1:lambda:level1(),
		2:lambda:level2(),
		3:lambda:level3(),
		4:lambda:level4(),
		5:lambda:level5(),
		6:lambda:test()}
	goto[idx]()
	environment.env_switch(idx)
	del idx,goto

## levels to load
def test():# test level
	import level_dev
	level_dev.start_load()
	invoke(free_level,delay=1)

def level1():# rainy woods
	import level1
	level1.start_load()
	invoke(free_level,delay=3)

def level2():# road to nowhere
	import level2
	st.gem_death=False
	level2.start_load()
	invoke(free_level,delay=3)

def level3():# river stream
	import level3
	level3.start_load()
	invoke(free_level,delay=3)

def level4():# drain damage
	import level4
	level4.start_load()
	invoke(free_level,delay=3)

def level5():# ruined
	import level5
	level5.start_load()
	invoke(free_level,delay=3)