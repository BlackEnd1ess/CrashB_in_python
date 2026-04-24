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
BTFLY='butterfly'
WM='wmpf'

class ManageObjects(Entity):
	def __init__(self):
		s=self
		super().__init__()
		s.is_done=False
		s.npc_dst_zf=12
		s.npc_dst_zb=3
		s.box_dst_zf=12
		s.box_dst_bf=4
		s.frt_dst=8
		s.tm=.5
	def purge(self):
		if not self.is_done:
			self.is_done=True
			destroy(self)
	def check_dst(self,v,p):
		return bool(v.z < p.z+LC.RCZ and p.z < v.z+LC.RCB and abs(p.x-v.x) < LC.RCX)
	def run(self):
		s=self
		for v in scene.entities:
			if not v:
				continue
			AZ=LC.ACTOR
			if cc.is_box(v):
				v.visible=not((AZ.z > v.z+s.box_dst_bf) or (AZ.z < v.z-s.box_dst_zf))
			if cc.is_enemie(v):
				if v.vnum != 15:
					v.enabled=not((AZ.z > v.z+s.npc_dst_zb) or (AZ.z < v.z-s.npc_dst_zf))
			dx=distance_xz(AZ,v)
			if v.name == WM:
				v.enabled=dx < s.frt_dst
			if v.name == BTFLY:
				v.enabled=dx < s.npc_dst_zf
			if v.name == SCENE:
				v.enabled=dx < LC.RCZ
			if v.name in DECO and not v.vnum in (6,13):
				v.enabled=s.check_dst(v,LC.ACTOR)
			if v.name in (CORRIDOR,BLOCK,FLOOR,WALL) or hasattr(v,'danger') or v.name == 'mptf':
				v.enabled=s.check_dst(v,LC.ACTOR)
	def update(self):
		if st.gproc():
			return
		if st.LV_CLEAR_PROCESS:
			s.purge()
			return
		s=self
		s.tm=max(s.tm-time.dt,0)
		if s.tm <= 0:
			s.tm=.5
			s.run()