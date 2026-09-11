from ursina import Entity,scene,distance,distance_xz,color,time
from ursina.ursinastuff import destroy
import _core,_loc,status,settings,gc
st=status
cc=_core
LC=_loc

ANIMATED=('ldmn','wtmn','toxic_barrel','jungle_leaf','jungle_bush','rmdr','mnks','loos','plnk','lgtfr')
CORRIDOR='obj_type__corridor'
BLOCK='obj_type__block'
SCENE='obj_type__scene'
FLOOR='obj_type__floor'
WALL='obj_type__wall'
DECO='obj_type__deco'
ROOM=('strm','enrm')

def load_manager():
	WumpaFruitRenderManager()
	#BoxRenderManager()
	NPCRenderManager()
	LevelSceneRenderManager()
	LevelObjectRenderManager()

class WumpaFruitRenderManager(Entity):
	def __init__(self):
		super().__init__()
		self.fruits=[]
		self.dst_z=16
		self.dst_x=6
		self.dst_b=3
		self.tme=0
		for wm in tuple(scene.entities):
			if wm.name == 'wmpf':
				self.fruits.append(wm)
	def check_distance(self,wm):
		return bool(abs(LC.ACTOR.x-wm.x) < self.dst_x and LC.ACTOR.z < wm.z+self.dst_b and wm.z < LC.ACTOR.z+self.dst_z)
	def refr_function(self):
		for wm in tuple(self.fruits):
			if not wm:
				self.fruits.remove(wm)
				continue
			udv=self.check_distance(wm)
			if wm.enabled != udv:
				wm.enabled=udv
	def update(self):
		if st.gproc():
			return
		if len(self.fruits) <= 0:
			destroy(self)
			return
		self.tme+=time.dt
		if self.tme > .3:
			self.tme=0
			self.refr_function()

class BoxRenderManager(Entity):
	def __init__(self):
		super().__init__()
		self.boxes=[]
		self.dst_z=14
		self.dst_x=6
		self.dst_b=4
		self.tme=0
		for bx in tuple(scene.entities):
			if cc.is_box(bx):
				self.boxes.append(bx)
	def check_distance(self,bx):
		return bool(abs(LC.ACTOR.x-bx.x) < self.dst_x and LC.ACTOR.z < bx.z+self.dst_b and bx.z < LC.ACTOR.z+self.dst_z)
	def refr_function(self):
		for bx in tuple(self.boxes):
			if not bx:
				self.boxes.remove(bx)
				continue
			udv=self.check_distance(bx)
			if bx.vnum in (0,8,10,14):
				if bx.enabled != udv:
					bx.enabled=udv
			else:
				if bx.visible != udv:
					bx.visible=udv
	def update(self):
		if st.gproc():
			return
		if len(self.boxes) <= 0:
			destroy(self)
			return
		self.tme+=time.dt
		if self.tme > .3:
			self.tme=0
			self.refr_function()

class NPCRenderManager(Entity):
	def __init__(self):
		super().__init__()
		self.npcs=[]
		self.dst_z=14
		self.dst_x=6
		self.dst_b=3
		self.tme=0
		for np in tuple(scene.entities):
			if cc.is_enemie(np) or np.name in ('bird','butterfly','HPP'):
				self.npcs.append(np)
	def check_distance(self,np):
		return bool(abs(LC.ACTOR.x-np.x) < self.dst_x and LC.ACTOR.z < np.z+self.dst_b and np.z < LC.ACTOR.z+self.dst_z)
	def refr_function(self):
		for np in tuple(self.npcs):
			if not np:
				self.npcs.remove(np)
				continue
			udv=self.check_distance(np)
			if hasattr(np,'vnum') and np.vnum == 14:
				if np.visible != udv:
					np.visible=udv
			else:
				if np.enabled != udv:
					np.enabled=udv
	def update(self):
		if st.gproc():
			return
		if len(self.npcs) <= 0:
			destroy(self)
			return
		self.tme+=time.dt
		if self.tme > .3:
			self.tme=0
			self.refr_function()

class LevelSceneRenderManager(Entity):
	def __init__(self):
		super().__init__()
		self.map_objects=[]
		self.dst_z=LC.RCZ
		self.dst_x=LC.RCX
		self.dst_b=LC.RCB
		self.tme=0
		for mop in tuple(scene.entities):
			if mop.name in (CORRIDOR,SCENE,FLOOR,WALL,BLOCK,ROOM) or (mop.name == DECO and mop.vnum != 6):
				self.map_objects.append(mop)
	def check_distance(self,mop):
		return bool(abs(LC.ACTOR.x-mop.x) < self.dst_x and LC.ACTOR.z < mop.z+self.dst_b and mop.z < LC.ACTOR.z+self.dst_z)
	def refr_function(self):
		for mop in tuple(self.map_objects):
			if not mop:
				self.map_objects.remove(mop)
				continue
			udv=self.check_distance(mop)
			if mop.enabled != udv:
				mop.enabled=udv
	def update(self):
		if st.gproc():
			return
		if len(self.map_objects) <= 0:
			destroy(self)
			return
		self.tme+=time.dt
		if self.tme > .3:
			self.tme=0
			self.refr_function()

class LevelObjectRenderManager(Entity):
	def __init__(self):
		super().__init__()
		self.map_objects=[]
		self.dst_z=12
		self.dst_x=6
		self.dst_b=3
		self.tme=0
		for mop in tuple(scene.entities):
			if mop.name in ANIMATED or (mop.name == 'mptf' and mop.ptf_mv == 0):
				self.map_objects.append(mop)
	def check_distance(self,mop):
		return bool(abs(LC.ACTOR.x-mop.x) < self.dst_x and LC.ACTOR.z < mop.z+self.dst_b and mop.z < LC.ACTOR.z+self.dst_z)
	def refr_function(self):
		for mop in tuple(self.map_objects):
			if not mop:
				self.map_objects.remove(mop)
				continue
			udv=self.check_distance(mop)
			if mop.enabled != udv:
				mop.enabled=udv
	def update(self):
		if st.gproc():
			return
		if len(self.map_objects) <= 0:
			destroy(self)
			return
		self.tme+=time.dt
		if self.tme > .3:
			self.tme=0
			self.refr_function()