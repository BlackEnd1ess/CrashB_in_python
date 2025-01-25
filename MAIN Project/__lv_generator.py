import os, __le_cfg
lc=__le_cfg

def lv_data():
	ln=[]
	ln.append('import objects,map_tools,crate,npc,item,sys,os,_loc,status')
	ln.append("sys.path.append(os.path.join(os.path.dirname(__file__), '..'))")
	ln.append('from ursina import *')
	ln.append('')
	ln.append('mt=map_tools')
	ln.append('st=status')
	ln.append('o=objects')
	ln.append('LC=_loc')
	ln.append('c=crate')
	ln.append('n=npc')
	ln.append(' ')
	ln.append('def map_setting():')
	ln.append('    LC.LV_DST=(10,15)')
	ln.append('    LC.BN_DST=(5,10)')
	ln.append('    window.color=color.black')
	ln.append('    scene.fog_density=(15,20)')
	ln.append('    scene.fog_color=color.black')
	ln.append('    LC.AMBIENT_LIGHT.color=color.rgb32(140,140,200)')
	ln.append('    st.toggle_thunder=False')
	ln.append('    st.toggle_rain=False')
	ln.append(' ')
	ln.append('def start_load():')
	ln.append('    bonus_zone()')
	ln.append('    load_crate()')
	ln.append('    load_object()')
	ln.append('    load_wumpa()')
	ln.append('    load_npc()')
	ln.append('    map_setting()')
	ln.append(' ')
	ln.append('def load_object():')
	ln.append('    o.StartRoom(pos=(8,0,-1))')
	ln.append('    o.EndRoom(pos=(8,2,68),c=color.gray)')
	if len(lc.MAP_DATA) > 0:
		for k in lc.MAP_DATA[:]:
			ln.append(f'    {k}')
	ln.append(' ')
	ln.append('def load_crate():')
	if len(lc.CRATE_DATA) > 0:
		for k in lc.CRATE_DATA[:]:
			ln.append(f'    {k}')
	else:
		ln.append('    return')
	ln.append(' ')
	ln.append('def load_npc():')
	if len(lc.NPC_DATA) > 0:
		for k in lc.NPC_DATA[:]:
			ln.append(f'    {k}')
	else:
		ln.append('    return')
	ln.append(' ')
	ln.append('def load_wumpa():')
	ln.append('    return')
	ln.append(' ')
	ln.append('def bonus_zone():')
	ln.append('    return')
	return ln

def output_data():
	file_n=lc.lv_name
	with open(file_n,"w") as f:
		for line in lv_data():
			f.write(line+"\n")
	print(f'Level-Data stored successfully in "{file_n}".')