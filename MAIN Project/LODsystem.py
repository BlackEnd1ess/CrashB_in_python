from ursina import Sequence,Wait,scene,distance,distance_xz
import _core,_loc,status,item,settings

st=status
cc=_core
LC=_loc

## short names from objects (entity.name)
LOD_VAR=['rmdr','ctsc','bush']
LV1=LOD_VAR+['trd2','tssn','mptf']
LV2=LOD_VAR+['plnk','ickk','wdlg','pilr','icec','snwa']
LV3=LOD_VAR+['wtfa','mptf','trd2','tile','foam','wdst','bbgn','bnsc','mtbt']
LV4=LOD_VAR+['swpl','swp2','swpi','drpw','ssww','swri']
LV5=LOD_VAR+['mnks','loos','rnsp','rubl','rncr']
LL={1:LV1,2:LV2,3:LV3,4:LV4,5:LV5,6:LV5}

##level decoration (side)
PLO=['strm']
BGSO={1:PLO+['grsi','mblo','tmpw','trrw','cori'],
	2:PLO+['snhi','mblo'],
	3:PLO+['tmpw'],
	4:PLO+['swec','swtu'],
	5:PLO+['ruin'],
	6:[]}

## BSGO distance
LD={0:0,1:30,2:20,3:16,4:28,5:32,6:16}

## init lod
def start():
	Sequence(lambda:refr(st.level_index),Wait(.6),loop=True)()
	if settings.debg:
		cwu()
def cwu():
	j=0
	for k in scene.entities[:]:
		if k.name == 'wmpf':
			j+=1
	print(f'wumpa:{j}')

## check distance
def check_dst(p,v,dz):
	return (v.z < p.z+dz and p.z < v.z+3 and abs(p.x-v.x) < 8)

def check_dynamic(o):
	return any([(cc.is_enemie(o) and not (o.is_hitten or o.is_purge)),(o.name in LL[st.level_index])])

#for e in range(0,3):
#	print(e)
#	for v in gc.get_objects(generation=e):
#		print(v)

def refr(idx):
	if st.gproc():
		return
	bc={r for r in scene.entities if r.parent == scene}
	p=LC.ACTOR.position
	for v in bc:
		u=check_dst(p,v.position,dz=int(scene.fog_density[1]))
		w=distance_xz(v.position,p)
		if (cc.is_crate(v) and v.vnum in {0,1,2}) or check_dynamic(v):
			v.enabled=u
		if (cc.is_crate(v) and v.vnum in {3,11,12}):
			v.visible=u
		if v.name == 'wmpf':
			v.enabled=(w < 8)
		if v.name in BGSO[idx]:
			v.enabled=(w < LD[idx])