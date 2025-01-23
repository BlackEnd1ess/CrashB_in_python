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
	7:ANY_LV|set()}

DYN_OBJ={
	0:set(),
	1:{'bush','htbx','block','tssn'},
	2:{'plnk','sngg','ickk','wdlg','block'},
	3:{'wtfa','wdst','block'},
	4:{'swpt','swff','drpw'},
	5:{'loos','rnsp','htbx'},
	6:{'ldmn','tksc','bbfl','bbst','sngg'},
	7:{'labt','epad','labo','lapi','lbbr','ltts'}}

## func for render culling
class ManageObjects(Entity):
	def __init__(self):
		s=self
		super().__init__()
		s.dx={1:10,2:8,3:10,4:8,5:10,6:8,7:8}[st.level_index]#side
		s.dz={1:16,2:14,3:18,4:24,5:20,6:20,7:16}[st.level_index]#front
		s.dv={1:4,2:4,3:4,4:5,5:5,6:4,7:3}[st.level_index]#back
		s.BO={1:30,2:18,3:32,4:25,5:26,6:25,7:20}[st.level_index]#BIG OBJECT DISTANCE
		s.tme=.5
		s.CD=14
		s.ND=12
		s.WD=8
	def check_dst(self,v,p):
		s=self
		return v.z < p.z+s.dz and p.z < v.z+s.dv and abs(p.x-v.x) < s.dx
	def run(self):
		s=self
		ix=st.level_index
		pp=LC.ACTOR
		for v in scene.entities[:]:
			kd=distance_xz(v,pp)
			if v.name in DYN_OBJ[ix]:
				v.enabled=s.check_dst(v,pp)
			if v.name in BIG_OBJ[ix]:
				v.enabled=kd < s.BO
			if v.name == 'wmpf':
				v.enabled=kd < s.WD
			if cc.is_crate(v):
				if v.vnum in {0,1,2}:
					v.enabled=kd < s.CD
				if v.vnum == 12:
					v.visible=kd < s.CD
			if cc.is_enemie(v) and v.vnum != 15:
				v.enabled=kd < s.ND
		del ix,pp
	def update(self):
		if st.gproc():
			return
		s=self
		s.tme=max(s.tme-time.dt,0)
		if s.tme <= 0:
			s.tme=.5
			s.run()