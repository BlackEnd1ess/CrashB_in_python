from ursina import Entity,Animation,scene,distance,distance_xz,color,time
import _core,_loc,status,settings
st=status
cc=_core
LC=_loc

CORRIDOR='obj_type__corridor'
BLOCK='obj_type__block'
WATER='obj_type__water'
SCENE='obj_type__scene'
FLOOR='obj_type__floor'
WALL='obj_type__wall'
DECO='obj_type__deco'
WM='wmpf'

class ManageObjects(Entity):
	def __init__(self):
		s=self
		super().__init__()
		s.npc_dst=16
		s.box_dst=12
		s.frt_dst=8
		s.tm=.5
	def check_dst(self,v,p):
		s=self
		return v.z < p.z+LC.RCZ and p.z < v.z+LC.RCB and abs(p.x-v.x) < LC.RCX
	def run(self):
		s=self
		for v in scene.entities[:]:
			k=s.check_dst(v,LC.ACTOR)
			j=distance(v,LC.ACTOR)
			if cc.is_crate(v):
				if not v.vnum in {3,12,15}:
					v.enabled=bool(j < s.box_dst)
				else:
					v.visible=bool(j < s.box_dst)
			if cc.is_enemie(v):
				v.enabled=bool(j < s.npc_dst and v.vnum != 15)
			if v.name == WM:
				v.enabled=bool(j < s.frt_dst)
			if v.name == SCENE:
				v.enabled=bool(j < LC.RCZ)
			if v.name in DECO and not v.vnum in {6,13}:
				v.enabled=k
			if v.name in {CORRIDOR,BLOCK,FLOOR,WALL} or hasattr(v,'danger') or v.name == 'mptf':
				v.enabled=k
			del j,k
		del v
	def update(self):
		if st.gproc():
			return
		s=self
		s.tm=max(s.tm-time.dt,0)
		if s.tm <= 0:
			s.tm=.5
			s.run()