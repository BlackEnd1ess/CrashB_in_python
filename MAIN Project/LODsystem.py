from ursina import Entity,Animation,scene,distance,distance_xz,color,time
import _core,_loc,status,item,settings

st=status
cc=_core
LC=_loc

## short names from objects (entity.name)
LOD_VAR=['rmdr','wpvx']
LV1=LOD_VAR+['trd2','tssn','mptf','mblo','bush','cori','htbx']
LV2=LOD_VAR+['plnk','ickk','wdlg','pilr','icec','snwa','sngg']
LV3=LOD_VAR+['wtfa','mptf','trd2','tile','foam','wdst','mtbt']
LV4=LOD_VAR+['swpl','swp2','swpi','drpw','ssww','swri','swff']
LV5=LOD_VAR+['mnks','loos','rnsp','rubl','rncr','htbx']
LV6=LOD_VAR+['ldmn','tksc','bbfl','bbst','sngg']
LV7=LOD_VAR+['labt','epad','tser']
LL={1:LV1,2:LV2,3:LV3,4:LV4,5:LV5,6:LV6,7:LV7}

##level decoration (side)
PLO=['strm']
BGSO={1:PLO+['grsi','trrw'],
	2:PLO+['snhi'],
	3:PLO+['tmpw'],
	4:PLO+['swec','swtu'],
	5:PLO+['rrrr'],
	7:PLO+['lbbr']}

## BSGO distance
LD={0:0,1:30,2:18,3:16,4:24,5:16,6:16,7:14}

## init lod
def start():
	LODinGame()

## check distance
def check_dst(p,v,dz):
	return (v.z < p.z+dz and p.z < v.z+3 and abs(p.x-v.x) < 8 and abs(p.y-v.y) < 6)

def check_dynamic(o):
	return any({(cc.is_enemie(o) and not (o.is_hitten or o.is_purge or o.vnum == 15)),(o.name in LL[st.level_index])})

class LODinGame(Entity):
	def __init__(self):
		s=self
		super().__init__()
		s.idx=st.level_index
		s.tme=.5
	def update(self):
		if st.gproc():
			return
		s=self
		s.tme=max(s.tme-time.dt,0)
		if s.tme <= 0:
			s.tme=.5
			bc={r for r in scene.entities if r.parent == scene}
			p=LC.ACTOR.position
			for v in bc:
				u=check_dst(p,v.position,int(scene.fog_density[1]))
				w=distance_xz(v.position,p)
				if cc.is_crate(v):
					if v.vnum in {0,1,2}:
						v.enabled=u
					if v.vnum in {3,11,12}:
						v.visible=u
				if check_dynamic(v):
					v.enabled=u
				if v.name == 'wmpf':
					v.enabled=(w < 8)
				if s.idx != 6:
					if v.name in BGSO[s.idx]:
						v.enabled=(w < LD[s.idx])