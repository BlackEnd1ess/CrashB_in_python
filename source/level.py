import ui,_core,status,environment,sound,LODsystem,sys,os,gc
from ursina import camera,invoke,Entity,time,scene

lv='level'
st=status
cc=_core
sn=sound

flt=7
## start level
def free_level():
	camera.rotation_x=15
	LODsystem.ManageObjects()
	cc.check_nitro_stack()
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
	BoxPositionInfo()
	print(f'<info> level {st.level_index} boxes: {st.crates_in_level}')
	print(f'<info> level {st.level_index} wumpa: {st.wumpas_in_level}')
	print(f'<info> level {st.level_index} npc: {st.npc_in_level}')
	print(f'<info> Level {st.level_index} successfully loaded')

## level settings
def load(idx):
	sys.path.append(os.path.join(os.path.dirname(__file__),lv))
	st.loading=True
	st.weather_thunder=bool(idx == 5)
	{1:level1,2:level2,3:level3,4:level4,5:level5,6:level6,7:level7,8:level8,9:test}[idx]()
	environment.env_switch()
	print(f'<info> init Level {st.level_index} ...')
	del idx

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

def level8():# polar lights
	import level8
	level8.start_load()
	invoke(free_level,delay=flt)

class BoxPositionInfo(Entity):
	def __init__(self):
		s=self
		super().__init__()
		s.pos_info=[]
		s.pos_new=[]
		s.refr=.1
	def check_phys_box(self):
		s=self
		ltt=[v for v in scene.entities if (hasattr(v,'phys') and v.phys)]
		for kd in ltt[:]:
			s.pos_info.append(kd)
			s.pos_new.append(kd.y-.32)
			setattr(kd,'landed',False)
			kd.phys=False
	def refr_box_pos(self):
		s=self
		for sg,dg in list(zip(s.pos_info,s.pos_new)):
			if not sg.landed:
				sg.y-=time.dt*1.8
				if sg.y <= dg:
					sg.y=dg
					sg.landed=True
			else:
				s.pos_new.remove(dg)
				s.pos_info.remove(sg)
	def update(self):
		if st.gproc():
			return
		s=self
		s.refr=max(s.refr-time.dt,0)
		s.refr_box_pos()
		if s.refr <= 0:
			s.refr=.1
			s.check_phys_box()