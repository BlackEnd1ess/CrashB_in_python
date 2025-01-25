import objects,_loc,status,__le_cfg,crate,_core,npc
from ursina import *
CU=camera.ui
st=__le_cfg
o=objects
c=crate

mvb='wireframe_cube'
crt='res/crate/cr_t0.ply'
b='box'

sc=(.1,.05)
ts=.85
j=.6

class Cursor(Entity):
	def __init__(self):
		s=self
		super().__init__(model=mvb,scale=1,double_sided=True,color=st.selected_color,collider=None)
		s.def_model=s.model
		st.cursor=s
	def update(self):
		s=self
		if st.pcm == 0:
			s.model=s.def_model
			s.texture=None
			s.rotation_x=0
			s.scale=1
			return
		if st.pcm == 1:
			s.scale=.16
			s.model=crt
			s.rotation_x=90
			s.texture=f'res/crate/{st.CRATE_ID}.tga'
		if st.pcm == 2:
			lk=st.NPC[st.NPC_ID]
			s.scale=.16
			s.model=f'res/npc/{lk}.ply'
			s.texture=f'res/npc/{lk}.tga'
			s.rotation_x=-90
			s.scale=.8/1200
			del lk

class MapBlock(Entity):
	def __init__(self,pos):
		super().__init__(model='plane',name='sccb',texture=st.grid_tex,color=st.grid_color,position=pos,collider='box',on_click=self.spw_obj)
		del pos
	def spw_obj(self):
		s=self
		for ct in scene.entities[:]:
			if not ct.name in {'sccb','cursor'} and ct.position == s.position:
				for rk in st.MAP_DATA:
					if str(ct.position) in rk:
						st.MAP_DATA.remove(rk)
				for ck in st.CRATE_DATA:
					if str(ct.position) in ck:
						st.MAP_DATA.remove(ck)
				for nk in st.CRATE_DATA:
					if str(ct.position) in nk:
						st.MAP_DATA.remove(nk)
				destroy(ct)
				return
		if st.pcm == 0:
			o.FloorBlock(pos=s.position,ID=1,sca=.5,EMD=True)
			st.MAP_DATA.append(f'o.BlockFloor(pos={s.position},ID=1,sca=.5)')
		if st.pcm == 1:
			c.place_crate(ID=st.CRATE_ID,p=(s.x,s.y+.16,s.z))
			st.CRATE_DATA.append(f'c.place_crate(ID={st.CRATE_ID},p={s.x,s.y+.16,s.z})')
		if st.pcm == 2:
			Entity(model='res/npc/'+st.NPC[st.NPC_ID]+'.ply',texture='res/npc/'+st.NPC[st.NPC_ID]+'.tga',rotation_x=-90,scale=.8/1200,name='snpc',position=s.position)
			st.NPC_DATA.append(f'npc.spawn(ID={st.NPC_ID},p={s.position})')
	def update(self):
		s=self
		st.bl_height=s.y
		if mouse.hovered_entity == s and mouse.hovered_entity != st.cursor:
			st.cursor.position=s.position
			s.color=st.selected_color
			return
		s.color=st.grid_color

class MapInfo(Entity):
	def __init__(self):
		s=self
		super().__init__()
		s.info_dbg=Text(None,parent=camera.ui,position=(.25,-.45),color=color.pink,scale=.8)
		s.info_ctrl=Text(st.ct_info,parent=camera.ui,position=(-.85,.475),color=color.green,scale=1)
	def update(self):
		s=self
		s.info_dbg.text=f'MAP SIZE:{st.m_size[0]}x{st.m_size[1]} ::: GRID Y: {st.bl_height} ::: {len(scene.entities)} ::: PLACE MODE = {st.mde[st.pcm]}'

class SpawnMenu(Button):
	def __init__(self):
		s=self
		Text('SELECT SPAWN MODE:',color=color.orange,parent=CU,position=(.6,.475))
		super().__init__(text='SCENE',parent=CU,position=(j,.4),radius=.1,scale=sc,text_size=ts,collider=b,pressed_color=color.green,highlight_color=color.azure,color=color.dark_gray,on_click=lambda:s.swi_mode(0))
		s.btn0=Button(text='BOX ID:',parent=CU,position=(j,.35),radius=.1,scale=sc,text_size=ts,collider=b,pressed_color=color.green,highlight_color=color.azure,color=color.dark_gray,on_click=lambda:s.swi_mode(1))
		s.btn1=Button(text='NPC ID:',parent=CU,position=(j,.3),radius=.1,scale=sc,text_size=ts,collider=b,pressed_color=color.green,highlight_color=color.azure,color=color.dark_gray,on_click=lambda:s.swi_mode(2))
		s.btn2=Button(text='WUMPA',parent=CU,position=(j,.25),radius=.1,scale=sc,text_size=ts,collider=b,pressed_color=color.green,highlight_color=color.azure,color=color.dark_gray,on_click=lambda:s.swi_mode(3))
		s.btn3=Button(text='Bonus-Platform',parent=CU,position=(j,.2),radius=.1,scale=(.2,.05),text_size=ts,collider=b,pressed_color=color.green,highlight_color=color.azure,color=color.dark_gray,on_click=lambda:s.swi_mode(4))
		s.btn4=Button(text='Gem-Platform',parent=CU,position=(j,.15),radius=.1,scale=(.2,.05),text_size=ts,collider=b,pressed_color=color.green,highlight_color=color.azure,color=color.dark_gray,on_click=lambda:s.swi_mode(5))
		s.scin=InputField(default_value='0',max_lines=1,character_limit=2,position=(s.x+.1,s.y),color=color.dark_gray,scale=(.1,.05))
		s.bbin=InputField(default_value='0',max_lines=1,character_limit=2,position=(s.btn0.x+.1,s.btn0.y),color=color.dark_gray,scale=(.1,.05))
		s.npin=InputField(default_value='0',max_lines=1,character_limit=2,position=(s.btn1.x+.1,s.btn1.y),color=color.dark_gray,scale=(.1,.05))
	def swi_mode(self,m):
		st.pcm=m
		del m
	def update(self):
		s=self
		if len(s.scin.text) <= 0 or len(s.bbin.text) <= 0 or len(s.npin.text) <= 0:
			return
		if (s.scin.text.isdigit() or s.bbin.text.isdigit() or s.npin.text.isdigit()):
			st.CRATE_ID=int(s.bbin.text)
			st.OBJ_ID=int(s.scin.text)
			st.NPC_ID=int(s.npin.text)
			return
		print('not int')