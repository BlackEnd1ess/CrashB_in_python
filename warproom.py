import status,_loc,ui
from ursina import *
st=status

cgs={1:'gem',2:'gem',3:'gem',4:'gem1',5:'gem2'}
req_col=color.rgb32(25,25,25)
icb='res/ui/misc/icon_box.png'
fnt='res/ui/font.ttf'
icp='res/ui/icon/'

k=camera.ui
q='quad'
sca=.1
class LevelInfo(Entity):
	def __init__(self,idx,pos):
		s=self
		gcsa={1:sca/1.8,2:sca,3:sca*1.4,4:sca,5:sca}
		super().__init__(position=pos,parent=k)
		s.lv_crystal=Animation(icp+'crystal.gif',position=(self.x+.8,self.y,self.z),scale=sca,parent=k,color=req_col)
		s.lv_col_gem=Animation(cgs[idx]+'.gif',position=(s.x+.945,s.y,s.z),scale=sca,parent=k,color=req_col)
		s.lv_clr_gem=Animation(icp+'gem.gif',position=(s.x+1.09,s.y,s.z),scale=sca,parent=k,color=req_col)
		s.lv_name=Text(_loc.lv_name[idx],font=fnt,position=(s.x,s.y+.04,s.z),scale=2.5,color=color.orange,parent=k)
		s.lv_col_gem.scale_y=gcsa[idx]
		s.font_color=color.orange
		s.blink_time=.3
		s.lvID=idx
		for iwb in range(3):
			Entity(model=q,texture=icb,position=(s.lv_crystal.x+iwb/7,s.y,1),scale=.16,parent=k,color=color.rgb32(150,180,150))
		if idx in st.CRYSTAL:
			s.lv_crystal.color=color.magenta
		if idx in st.CLEAR_GEM:
			s.lv_clr_gem.color=color.rgb32(180,180,210)
		if idx == 1 and 4 in st.COLOR_GEM:
			s.lv_col_gem.color=color.blue
		if idx == 2 and 1 in st.COLOR_GEM:
			s.lv_col_gem.color=color.red
		if idx == 3 and 5 in st.COLOR_GEM:
			s.lv_col_gem.color=color.yellow
		if idx == 4 and 2 in st.COLOR_GEM:
			s.lv_col_gem.color=color.green
		if idx == 5 and 3 in st.COLOR_GEM:
			s.lv_col_gem.color=color.violet
	def update(self):
		if st.selected_level == self.lvID:
			self.blink_time=max(self.blink_time-time.dt,0)
			if self.blink_time <= 0:
				ui.text_blink(self,t=self.lv_name)

def level_select():
	Entity(model=q,texture='res/background/wroom.png',scale=(2,1),parent=k,color=color.rgb32(140,160,140),position=(0,0,2))
	for lvs in range(1,6):
		LevelInfo(idx=lvs,pos=(-.8,.5-lvs/6))