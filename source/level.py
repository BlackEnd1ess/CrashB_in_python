import ui,_core,status,environment,sound,LODsystem,sys,os,settings,_loc,gc
from ursina import camera,invoke,load_texture
from ursina.ursinastuff import destroy

lv='level'
st=status
cc=_core
LC=_loc

flt=7 if not settings.debg else 3
## start level
def free_level():
	idx=st.level_index
	camera.rotation_x=15
	LODsystem.ManageObjects()
	sound.BackgroundMusic(m=0)
	cc.check_nitro_stack()
	st.loading=False
	if not idx in st.CRYSTAL:
		cc.spawn_level_crystal(idx)
	if idx != 3 and not idx in st.COLOR_GEM:
		cc.spawn_color_gem(idx)
	if idx in st.CRYSTAL:
		cc.spawn_trial_clock(idx)
	if idx == 3:
		sound.AmbienceSound()
		sound.WaterRiver()
	ui.load_interface()
	cc.level_ready=True
	st.fails=0
	if settings.debg:
		print(f'<info> level {idx} boxes: {st.crates_in_level}')
		print(f'<info> level {idx} wumpa: {st.wumpas_in_level}')
		print(f'<info> level {idx} npc: {st.npc_in_level}')
		print(f'<info> Level {idx} successfully loaded')
	del idx
	gc.collect()

##preload water
def preload_water_texture(ID):
	if len(LC.wtr_texture) > 0:
		LC.wtr_texture.clear()
	if ID == 0:
		LC.wtr_texture=[load_texture(f'res/objects/l1/swamp/{cbx}.png') for cbx in range(3+1)]
		return
	if ID == 1:
		LC.wtr_texture=[load_texture(f'res/objects/ev/wtr/{cbx}.png') for cbx in range(31+1)]
		return
	if ID == 3:
		LC.wtr_texture=[load_texture(f'res/objects/l8/polar_water/{cbx}.png') for cbx in range(1+1)]

## level settings
def load(idx):
	sys.path.append(os.path.join(os.path.dirname(__file__),lv))
	st.loading=True
	st.weather_thunder=bool(idx == 5)
	{1:level1,2:level2,3:level3,4:level4,5:level5,6:level6,7:level7,8:level8,9:test}[idx]()
	environment.env_switch()
	if settings.debg:
		print(f'<info> init Level {st.level_index} ...')
	del idx

## levels to load
def test():# test level
	import level_dev
	level_dev.start_load()
	invoke(free_level,delay=flt)

def level1():# rainy woods
	import level1
	preload_water_texture(0)
	level1.start_load()
	invoke(free_level,delay=flt)

def level2():# road to nowhere
	import level2
	preload_water_texture(3)
	st.gem_death=False
	level2.start_load()
	invoke(free_level,delay=flt)

def level3():# river stream
	import level3
	level3.start_load()
	invoke(free_level,delay=flt)

def level4():# drain damage
	import level4
	preload_water_texture(1)
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

def level8():# polar lights
	import level8
	preload_water_texture(3)
	level8.start_load()
	invoke(free_level,delay=flt)