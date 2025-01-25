from ursina import Entity,Animation,scene,distance,distance_xz,color,time
import _core,_loc,status,settings

st=status
cc=_core
LC=_loc

## short names from objects (entity.name)
ANY_LV={'rmdr','strm'}
BIG_OBJ={
	0:ANY_LV,
	1:ANY_LV|{'grsi','trrw'},
	2:ANY_LV|{'snhi','snwa'},
	3:ANY_LV|{'tmpw','scwa'},
	4:ANY_LV|{'swec','swtu'},
	5:ANY_LV|{'rrrr'},
	6:ANY_LV,
	7:ANY_LV|set(),
	8:ANY_LV}

DYN_OBJ={
	0:set(),
	1:{'bush','htbx','block','tssn'},
	2:{'plnk','sngg','ickk','wdlg','block'},
	3:{'wtfa','wdst','block','block'},
	4:{'swpt','swff','drpw','block'},
	5:{'loos','rnsp','htbx','block'},
	6:{'ldmn','tksc','bbfl','bbst','sngg'},
	7:{'labt','epad','labo','lapi','lbbr','ltts'},
	8:set()}

## func for render culling
class ManageObjects(Entity):
	def __init__(self):
		s=self
		super().__init__()
		s.tme=.5
	def check_dst(self,v,p):
		s=self
		return v.z < p.z+24 and p.z < v.z+5 and abs(p.x-v.x) < 10
	def run(self):
		s=self
		ix=st.level_index
		pp=LC.ACTOR
		for v in scene.entities[:]:
			kd=distance_xz(v,pp)
			if v.name in DYN_OBJ[ix]:
				v.enabled=s.check_dst(v,pp)
			if v.name in BIG_OBJ[ix]:
				v.enabled=kd < 32
			if v.name == 'wmpf':
				v.enabled=kd < 8
			if cc.is_crate(v):
				if v.vnum in {0,1,2}:
					v.enabled=kd < 14
				if v.vnum == 12:
					v.visible=kd < 14
			if cc.is_enemie(v) and v.vnum != 15:
				v.enabled=kd < 12
		del ix,pp
	def update(self):
		if st.gproc():
			return
		s=self
		s.tme=max(s.tme-time.dt,0)
		if s.tme <= 0:
			s.tme=.5
			s.run()