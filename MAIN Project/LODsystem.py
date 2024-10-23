import _core,_loc,status,item
from ursina import *

st=status
cc=_core
LC=_loc

## short names from objects (entity.name)
LOD_VAR=['rmd1','ctsc']
LV1=LOD_VAR+['bush','trd2','tssn','mptf']
LV2=LOD_VAR+['plnk','ickk','wdlg','pilr','icec','snwa']
LV3=LOD_VAR+['wtfa','mptf','bush','trd2','tile','foam','wdst']
LV4=LOD_VAR+['swpl','swp2','swpi','drpw','ssww','swri']
LV5=LOD_VAR+['mnks','loos','rnsp','rubl','rncr']
LL={1:LV1,2:LV2,3:LV3,4:LV4,5:LV5,6:LV5}

##level decoration (side)
BGSO={1:['grsi','mblo'],
	2:['snhi','mblo'],
	3:['scwa'],
	4:['swec','swtu'],
	5:['ruin'],
	6:[]}

## init lod
def start():
	Sequence(refr,Wait(.5),loop=True)()

## check distance
def check_dst(p,v,dz):
	if v.z < p.z+dz and p.z < v.z+3 and abs(p.x-v.x) < 8:
		return True
	return False

def refr():
	if st.gproc():
		return
	for v in scene.entities[:]:
		far_dst=int(scene.fog_density[1])
		p=LC.ACTOR
		if isinstance(v,item.WumpaFruit):
			v.enabled=check_dst(p,v,dz=6)
		if cc.is_crate(v):
			u=check_dst(p,v,dz=far_dst)
			if v.vnum in [0,1,2]:
				v.enabled=u
			if v.vnum in [3,11,12]:
				v.visible=u
		if (cc.is_enemie(v) and not (v.is_hitten or v.is_purge)) or (v.name in LL[st.level_index]):
			v.enabled=check_dst(p,v,dz=far_dst)
		if v.name in BGSO[st.level_index]:
			v.enabled=(p.z < v.z+16)