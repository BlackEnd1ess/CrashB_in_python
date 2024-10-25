import _core,_loc,status,item
from ursina import *

st=status
cc=_core
LC=_loc

## short names from objects (entity.name)
LOD_VAR=['rmdr','ctsc']
LV1=LOD_VAR+['bush','trd2','tssn','mptf']
LV2=LOD_VAR+['plnk','ickk','wdlg','pilr','icec','snwa']
LV3=LOD_VAR+['wtfa','mptf','bush','trd2','tile','foam','wdst']
LV4=LOD_VAR+['swpl','swp2','swpi','drpw','ssww','swri']
LV5=LOD_VAR+['mnks','loos','rnsp','rubl','rncr']
LL={1:LV1,2:LV2,3:LV3,4:LV4,5:LV5,6:LV5}

##level decoration (side)
PLO=['strm','enrm']
BGSO={1:PLO+['grsi','mblo','tmpw'],
	2:PLO+['snhi','mblo'],
	3:PLO+['scwa','tmpw','wafl'],
	4:PLO+['swec','swtu'],
	5:PLO+['ruin'],
	6:[]}

## BSGO distance
LD={0:0,
	1:32,
	2:24,
	3:48,
	4:32,
	5:32,
	6:16}

## init lod
def start():
	Sequence(refr,Wait(.6),loop=True)()

## check distance
def check_dst(p,v,dz):
	return (v.z < p.z+dz and p.z < v.z+3 and abs(p.x-v.x) < 8)

def check_dynamic(o):
	return any([(cc.is_enemie(o) and not (o.is_hitten or o.is_purge)),(o.name in LL[st.level_index])])

def refr():
	if st.gproc():
		return
	for v in scene.entities[:]:
		far_dst=int(scene.fog_density[1])
		hq=st.level_index
		p=LC.ACTOR
		u=check_dst(p,v,dz=far_dst)
		if v.name == 'wmpf':
			v.enabled=check_dst(p,v,dz=6)
		if v.name in BGSO[hq]:
			v.enabled=(distance_xz(p,v) < LD[hq])
		if cc.is_crate(v):
			if (v.vnum in [0,1,2]):
				v.enabled=u
			elif (v.vnum in [3,11,12]):
				v.visible=u
		if check_dynamic(v):
			v.enabled=u