from ursina import Entity,scene,distance,distance_xz,color,time
from ursina.ursinastuff import destroy
import _core,_loc,status,settings,gc
st=status
cc=_core
LC=_loc

ANIMATED=('ldmn','wtmn','toxic_barrel','jungle_leaf','jungle_bush','bird','butterfly','wmpf','HPP','rmdr','mnks','loos','plnk','lgtfr')
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
	#NPCRenderManager()
	#LevelObjectRenderManager()

class WumpaFruitRenderManager(Entity):
	def __init__(self):
		super().__init__()
		self.fruits=[]
		self.dst_z=1
		self.dst_x=1
		self.dst_b=1
		self.tme=0
		for wm in tuple(scene.entities):
			if wm.name == 'wmpf':
				self.fruits.append(wm)
		del wm
	def check_distance(self,wm):
		return bool(abs(LC.ACTOR.x-wm.x) < self.dst_x and LC.ACTOR.z < wm.z+self.dst_b and wm.z < LC.ACTOR.z+self.dst_z)
	def refr_function(self):
		for wm in s.fruits:
			if not wm:
				continue
			wm.enabled=self.check_distance(wm)
	def update(self):
		if st.gproc():
			return
		s=self
		if len(s.fruits) <= 0:
			destroy(s)
			return
		s.tme+=time.dt
		if s.tme > .3:
			s.tme=0
			s.refr_function()

#class ManageObjects(Entity):
#	def __init__(self):
#		s=self
#		super().__init__()
#		s.culling_entity=[]
#		s.is_done=False
#		s.default_dst_z=LC.RCZ/2
#		s.item_dst_z=16
#		s.block_dst=8
#		s.npc_dst=12
#		s.box_dst=10
#		s.tme=0
#		s.init_list()
#	def init_list(self):
#		s=self
#		for cev in tuple(scene.entities):
#			if cc.is_box(cev) or cc.is_enemie(cev) or (cev.name in (CORRIDOR,BLOCK,SCENE,FLOOR,WALL)) or (cev.name == DECO and cev.vnum != 6) or (cev.name in ANIMATED) or hasattr(cev,'danger') or (cev.name in ROOM and st.level_index != 3):
#				s.culling_entity.append(cev)
#		del cev
#	def check_dst(self,v,p):
#		return bool(v.z < p.z+LC.RCZ and p.z < v.z+LC.RCB and abs(p.x-v.x) < LC.RCX)
#	def refr_object_visible(self):
#		s=self
#		for v in s.culling_entity:
#			if not v:
#				continue
#			dx=distance(LC.ACTOR,v)
#			if cc.is_box(v):
#				v.visible=dx < s.box_dst
#			elif cc.is_enemie(v) and v.vnum != 15:
#				v.enabled=dx < s.npc_dst
#			elif (v.name == SCENE) or (v.name in ROOM) or (v.name in (CORRIDOR,FLOOR,WALL,DECO)):
#				v.enabled=dx < LC.RCZ
#			elif v.name == BLOCK:
#				v.enabled=dx < s.block_dst
#			else:
#				v.enabled=dx < s.item_dst_z
#	def update(self):
#		if st.gproc():
#			return
#		if st.LV_CLEAR_PROCESS:
#			if not s.is_done:
#				s.is_done=True
#				destroy(s)
#			return
#		s=self
#		s.tme+=time.dt
#		if s.tme > .5:
#			s.tme=0
#			s.refr_object_visible()