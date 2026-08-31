from ursina import Entity,scene,distance,distance_xz,color,time
from ursina.ursinastuff import destroy
import _core,_loc,status,settings,gc
st=status
cc=_core
LC=_loc


CORRIDOR='obj_type__corridor'
BLOCK='obj_type__block'
SCENE='obj_type__scene'
FLOOR='obj_type__floor'
WALL='obj_type__wall'
DECO='obj_type__deco'

class ManageObjects(Entity):
	def __init__(self):
		s=self
		super().__init__()
		s.culling_entity=[]
		s.is_done=False
		s.npc_dst_zf=12
		s.npc_dst_zb=3
		s.box_dst_zf=12
		s.box_dst_bf=4
		s.frt_dst=8
		s.tme=0
		s.init_list()
	def init_list(self):
		s=self
		for cev in scene.entities[:]:
			if cc.is_box(cev) or cc.is_enemie(cev) or cev.name in (CORRIDOR,BLOCK,SCENE,FLOOR,WALL,DECO) or cev.name in ('ldmn','wtmn','toxic_barrel','jungle_leaf','jungle_bush','bird','butterfly','wmpf','mptf') or hasattr(cev,'danger'):
				s.culling_entity.append(cev)
	def check_dst(self,v,p):
		return bool(v.z < p.z+LC.RCZ and p.z < v.z+LC.RCB and abs(p.x-v.x) < LC.RCX)
	def refr_object_visible(self):
		s=self
		for v in s.culling_entity:
			if not v:
				continue
			AZ=LC.ACTOR
			dx=distance(AZ,v)
			if cc.is_box(v):
				v.visible=not((AZ.z > v.z+s.box_dst_bf) or (AZ.z < v.z-s.box_dst_zf))
			elif cc.is_enemie(v) and v.vnum != 15:
				v.enabled=not((AZ.z > v.z+s.npc_dst_zb) or (AZ.z < v.z-s.npc_dst_zf))
			elif (v.name in DECO and v.vnum != 6) or v.name in (CORRIDOR,BLOCK,FLOOR,WALL):
				v.enabled=s.check_dst(v,LC.ACTOR)
			elif v.name == SCENE:
				v.enabled=dx < LC.RCZ
			else:
				v.enabled=dx < s.frt_dst
	def update(self):
		if st.gproc():
			return
		if st.LV_CLEAR_PROCESS:
			if not s.is_done:
				s.is_done=True
				destroy(s)
			return
		s=self
		s.tme+=time.dt
		if s.tme > .5:
			s.tme=0
			s.refr_object_visible()