from ursina import Entity,Animation,scene,distance,distance_xz,color,time
import _core,_loc,status,settings
st=status
cc=_core
LC=_loc

fw=24
sw=10
bw=5

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
		s.tm=.5
	def check_dst(self,v,p):
		s=self
		return v.z < p.z+fw and p.z < v.z+bw and abs(p.x-v.x) < sw
	def run(self):
		s=self
		for v in scene.entities[:]:
			k=s.check_dst(v,LC.ACTOR)
			j=distance(v,LC.ACTOR)
			if cc.is_crate(v) and not v.vnum in [3,15]:
				v.enabled=j < 12
			if cc.is_enemie(v) and v.vnum != 15:
				if v.vnum == 17:
					v.visible= j < 16
				else:
					v.enabled=j < 16
			if v.name == WM:
				v.enabled=j < 8
			if v.name == SCENE:
				v.enabled= j < 32
			if v.name in DECO and not v.vnum in {6,13}:
				v.enabled=k
			if v.name in {CORRIDOR,BLOCK,FLOOR,WALL} or hasattr(v,'danger') or v.name == 'mptf':
				v.enabled=k
	def update(self):
		if st.gproc():
			return
		s=self
		s.tm=max(s.tm-time.dt,0)
		if s.tm <= 0:
			s.tm=.5
			s.run()