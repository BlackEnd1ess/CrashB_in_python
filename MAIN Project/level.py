import ui,_core,status,environment,sound,LODsystem,sys,os,gc
from ursina import camera,invoke

lv='level'
st=status
cc=_core
sn=sound

flt=5
## start level
def free_level():
	camera.rotation_x=15
	cc.check_nitro_stack()
	LODsystem.ManageObjects()
	st.loading=False
	cc.spawn_level_crystal(st.level_index)
	st.fails=0
	sn.BackgroundMusic(m=0)
	if st.level_index == 3:
		sn.AmbienceSound()
		sn.WaterRiver()
	ui.load_interface()
	cc.level_ready=True
	gc.collect()
	print(f'<info> Level {st.level_index} successfully loaded')

## level settings
def main_instance(idx):
	sys.path.append(os.path.join(os.path.dirname(__file__),lv))
	st.loading=True
	st.weather_thunder=(idx == 5)
	goto={1:level1,2:level2,3:level3,4:level4,5:level5,6:level6,7:level7,8:level8,9:test}
	goto[idx]()
	environment.env_switch(idx)
	del idx,goto

## levels to load
def test():# test level
	import level_dev
	level_dev.start_load()
	invoke(free_level,delay=flt)

def level1():# rainy woods
	import level1
	level1.start_load()
	invoke(free_level,delay=flt)

def level2():# road to nowhere
	import level2
	st.gem_death=False
	level2.start_load()
	invoke(free_level,delay=flt)

def level3():# river stream
	import level3
	level3.start_load()
	invoke(free_level,delay=flt)

def level4():# drain damage
	import level4
	level4.start_load()
	invoke(free_level,delay=flt)

def level5():# ruined
	import level5
	level5.start_load()
	invoke(free_level,delay=flt)

def level6():# totally bee
	import level6
	level6.start_load()
	invoke(free_level,delay=flt)

def level7():# piston push
	import level7
	level7.start_load()
	invoke(free_level,delay=flt)

def level8():# ???
	import level8
	level8.start_load()
	invoke(free_level,delay=flt)