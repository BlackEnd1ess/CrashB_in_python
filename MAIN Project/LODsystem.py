from ursina import Sequence,Entity,Animation,Wait,scene,distance,distance_xz
import _core,_loc,status,item,settings

st=status
cc=_core
LC=_loc

## short names from objects (entity.name)
LOD_VAR=['rmdr','ctsc','bush']
LV1=LOD_VAR+['trd2','tssn','mptf']
LV2=LOD_VAR+['plnk','ickk','wdlg','pilr','icec','snwa','sngg']
LV3=LOD_VAR+['wtfa','mptf','trd2','tile','foam','wdst','mtbt']
LV4=LOD_VAR+['swpl','swp2','swpi','drpw','ssww','swri']
LV5=LOD_VAR+['mnks','loos','rnsp','rubl','rncr']
LL={1:LV1,2:LV2,3:LV3,4:LV4,5:LV5,6:LV5}

##level decoration (side)
PLO=['strm']
BGSO={1:PLO+['grsi','mblo','tmpw','trrw','cori'],
	2:PLO+['snhi','mblo'],
	3:PLO+['tmpw'],
	4:PLO+['swec','swtu'],
	5:PLO+['rrrr']}

## BSGO distance
LD={0:0,1:30,2:12,3:16,4:24,5:25,6:16}

## init lod
def start():
	Sequence(lambda:refr(st.level_index),Wait(.6),loop=True)()
	cwo()
def cwo():
	import gc
	from collections import Counter
	all_objects = gc.get_objects()
	class_counts = Counter()
	audio_details = []
	for obj in all_objects:
		if isinstance(obj, (Animation, Entity)):
			class_name = type(obj).__name__
			class_counts[class_name] += 1
			if class_name == "Entity":
				filename = getattr(obj,'name',None) or getattr(obj,'texture')
				audio_details.append(filename)
	print("Aktuelle Objekte im Speicher:")
	for class_name, count in class_counts.items():
		print(f"{class_name}: {count} Instanzen")
	print("\nDetails der Entity-Instanzen:")
	for i, filename in enumerate(audio_details, 1):
		print(f"Entities {i}: textur,name = {filename if filename else 'Unbekannt'}")



## check distance
def check_dst(p,v,dz):
	return (v.z < p.z+dz and p.z < v.z+3 and abs(p.x-v.x) < 8)

def check_dynamic(o):
	return any({(cc.is_enemie(o) and not (o.is_hitten or o.is_purge)),(o.name in LL[st.level_index])})

def outside(v):
	return any({(not st.bonus_round and v.y < -15),(not st.death_route and v.x >= 180)})

def refr(idx):
	if st.gproc():
		return
	bc={r for r in scene.entities if r.parent == scene}
	p=LC.ACTOR.position
	for v in bc:
		u=(check_dst(p,v.position,dz=int(scene.fog_density[1])) and not outside(v))
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
		if idx != 6:
			if v.name in BGSO[idx]:
				v.enabled=(w < LD[idx])