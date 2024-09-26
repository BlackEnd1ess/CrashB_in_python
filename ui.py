from time import strftime,gmtime
import status,_core,_loc,sound
from ursina import *

w_pa='res/ui/icon/wumpa_fruit/w'
wmpf='res/ui/digit_wumpa/'
crtf='res/ui/digit_crate/'
crti='res/ui/crate_icon/'
lvtf='res/ui/digit_live/'
_fnt='res/ui/font.ttf'
btxt='res/ui/bonus/'
_icn='res/ui/icon/'

q='quad'

CU=camera.ui
st=status
sn=sound
cc=_core
LC=_loc

def load_interface():
	PauseMenu()
	WumpaCounter()
	CrateCounter()
	LiveCounter()
	CollectedGem()

## Interface 2D Animations
# wumpa 2d animation
def wmp_anim(w):
	w.frm+=time.dt*15
	if w.frm > 13.9:
		w.frm=0
	w.texture=w_pa+str(int(w.frm))+'.png'

def text_blink(M,t):
	if M.blink_time <= 0:
		if t.color == M.font_color:
			t.color=color.white
		else:
			t.color=M.font_color
		M.blink_time=.3

def live_get_anim():
	lvA=Entity(parent=CU,model='quad',texture=_icn+'crash_live.tga',scale=(.1,.09),position=(.5,.43,0),color=color.gold)
	lvA.animate_x(.65,duration=.3)
	invoke(lambda:cc.purge_instance(lvA),delay=3.1)

class WumpaCollectAnim(Entity):
	def __init__(self,pos):
		wsca={False:.075,True:.06}
		super().__init__(model=q,texture=w_pa+'0.png',scale=wsca[st.bonus_round],parent=CU,position=pos)
	def update(self):
		if not st.gproc():
			if st.bonus_round:
				dta_x=-.25-self.x
				dta_y=-.5-self.y
				anp=time.dt*4
			else:
				dta_x=-.75-self.x
				dta_y=.43-self.y
				anp=time.dt*8
			if abs(dta_x) > .05 and abs(dta_y) > .05:
				self.x+=dta_x*anp
				self.y+=dta_y*anp
				return
			cc.purge_instance(self)

## Main Counter ##
class WumpaCounter(Entity):
	def __init__(self):
		self.pa=wmpf
		super().__init__(model=q,texture=w_pa+'0.png',parent=CU,position=(-.75,.43,0),scale=(.07,.08,0),visible=False,texture_position=(0,0))
		self.digit_0=Entity(model=q,texture=self.pa+'0.png',parent=CU,position=(self.x+.075,self.y),scale=.06,visible=False)
		self.digit_1=Entity(model=q,texture=self.pa+'0.png',parent=CU,position=(self.digit_0.x+.06,self.digit_0.y),scale=.06,visible=False)
		self.frm=0
		_loc.uiW=self
	def digits(self):
		n=str(st.wumpa_fruits)
		self.digit_0.texture=self.pa+n[0]+'.png'
		self.digit_0.show()
		if st.wumpa_fruits >= 10:
			self.digit_1.visible=True
			self.digit_1.texture=self.pa+n[1]+'.png'
			return
		self.digit_1.visible=False
	def wumpa_max(self):
		if st.wumpa_fruits > 99:
			st.wumpa_fruits=0
			cc.give_extra_live()
	def update(self):
		if not st.gproc():
			self.wumpa_max()
			if st.show_wumpas > 0:
				self.digits()
				self.show()
				wmp_anim(self)
			st.show_wumpas=max(st.show_wumpas-time.dt,0)
			if st.show_wumpas <= 0:
				self.frm=0
				self.hide()
				self.digit_0.hide()
				self.digit_1.hide()

class CrateCounter(Entity):
	def __init__(self):
		s=self
		s.tpd=crtf
		super().__init__(model=q,texture=None,parent=CU,scale=.1,position=(-.2,.43,0),fps=4,visible=False)
		s.col_digit0=Entity(model=q,texture=None,scale=.06,position=(s.x+.08,s.y,s.z),parent=CU,visible=False)
		s.col_digit1=Entity(model=q,texture=None,scale=.06,position=(s.x+.14,s.y,s.z),parent=CU,visible=False)
		s.col_digit2=Entity(model=q,texture=None,scale=.06,position=(s.x+.2,s.y,self.z),parent=CU,visible=False)
		s.seperator=Entity(model=q,texture=crtf+'seperator.png',scale=.06,position=(s.x,s.y,s.z),parent=CU,visible=False)
		s.req_digit0=Entity(model=q,texture=None,scale=.06,position=(s.x,s.y,s.z),parent=CU,visible=False)
		s.req_digit1=Entity(model=q,texture=None,scale=.06,position=(s.x,s.y,s.z),parent=CU,visible=False)
		s.req_digit2=Entity(model=q,texture=None,scale=.06,position=(s.x,s.y,s.z),parent=CU,visible=False)
		self.icf=0
	def crate_refr_ico(self):
		self.icf+=time.dt*30
		if self.icf > 63.9:
			self.icf=0
		self.texture=crti+'anim_crt_'+str(int(self.icf))+'.png'
	def remv_ui(self):
		s=self
		s.visible=False
		s.col_digit0.visible=False
		s.col_digit1.visible=False
		s.col_digit2.visible=False
		s.seperator.visible=False
		s.req_digit0.visible=False
		s.req_digit1.visible=False
		s.req_digit2.visible=False
	def req_count_refr(self):
		s=self
		ccl=str(st.crates_in_level)
		ssep=s.seperator
		ssep.position=(s.col_digit0.x+.06*len(str(st.crate_count)),s.y,s.z)
		s.req_digit0.position=(ssep.x+.06,ssep.y,ssep.z)
		s.req_digit0.texture=s.tpd+ccl[0]+'.png'
		s.req_digit0.visible=True
		if st.crates_in_level > 9:
			s.req_digit1.position=(ssep.x+.12,ssep.y,ssep.z)
			s.req_digit1.texture=s.tpd+ccl[1]+'.png'
			s.req_digit1.visible=True
			if st.crates_in_level > 99:
				s.req_digit2.position=(ssep.x+.18,ssep.y,ssep.z)
				s.req_digit2.texture=s.tpd+ccl[2]+'.png'
				s.req_digit2.visible=True
	def col_count_refr(self):
		s=self
		ccv=str(st.crate_count)
		s.col_digit1.visible=False
		s.col_digit2.visible=False
		s.col_digit0.visible=True
		s.seperator.visible=True
		s.visible=True
		s.col_digit0.texture=s.tpd+ccv[0]+'.png'
		if st.crate_count > 9:
			s.col_digit1.texture=s.tpd+ccv[1]+'.png'
			s.col_digit1.visible=True
			s.col_digit2.visible=False
			if st.crate_count > 99:
				s.col_digit2.texture=s.tpd+ccv[2]+'.png'
				s.col_digit2.visible=True
	def update(self):
		if not st.gproc() and st.crates_in_level > 0:
			if st.show_crates > 0:
				st.show_crates=max(st.show_crates-time.dt,0)
				if st.show_crates <= 0:
					self.remv_ui()
					return
				self.crate_refr_ico()
				self.col_count_refr()
				self.req_count_refr()

class LiveCounter(Entity):
	def __init__(self):
		self.ptl=lvtf
		super().__init__(parent=CU,model=q,texture=_icn+'crash_live.tga',scale=(.1,.09),position=(.65,.43,0),visible=False)
		self.live_digit0=Entity(model=q,texture=None,scale=.06,position=(self.x+.08,self.y),parent=CU,visible=False)
		self.live_digit1=Entity(model=q,texture=None,scale=.06,position=(self.x+.14,self.y),parent=CU,visible=False)
	def lives_refr(self):
		llv=str(st.extra_lives)
		self.visible=True
		self.live_digit0.texture=self.ptl+llv[0]+'.png'
		self.live_digit0.visible=True
		if st.extra_lives > 9:
			self.live_digit1.texture=self.ptl+llv[1]+'.png'
			self.live_digit1.visible=True
	def rmv_ui(self):
		self.visible=False
		self.live_digit0.visible=False
		self.live_digit1.visible=False
	def update(self):
		if not status.gproc():
			if st.show_lives > 0:
				st.show_lives=max(st.show_lives-time.dt,0)
				if st.show_lives <= 0:
					self.rmv_ui()
					return
				self.lives_refr()


## Bonus Counter ##
class WumpaBonus(Entity):
	def __init__(self):
		super().__init__(model=q,texture=w_pa+'0.png',parent=CU,position=(-.2,-.4,0),scale=(.05,.06,0),visible=False)
		self.w_text=Text(text=None,font=_fnt,x=self.x+.04,y=self.y+.025,scale=2,color=color.rgb32(175,235,30),parent=CU,visible=False)
		self.w_time=0
		self.frm=0
	def check_w(self):
		if (st.bonus_solved and st.wumpa_bonus > 0):
			return True
		return False
	def w_count(self):
		if self.check_w() and not st.wait_screen:
			self.w_time=max(self.w_time-time.dt,0)
			if self.w_time <= 0:
				self.w_time=.1
				if st.wumpa_bonus > 50:
					st.wumpa_bonus-=10
					cc.wumpa_count(10)
				else:
					st.wumpa_bonus-=1
					cc.wumpa_count(1)
				WumpaCollectAnim(pos=(-.2,-.4))
	def update(self):
		if not st.gproc():
			if st.bonus_round or self.check_w():
				self.w_count()
				self.show()
				self.w_text.show()
				self.w_text.text=str(st.wumpa_bonus)
				wmp_anim(self)
				return
			cc.purge_instance(self.w_text)
			cc.purge_instance(self)

class CrateBonus(Entity):
	def __init__(self):
		super().__init__(model=q,texture=None,parent=CU,scale=.07,position=(0,-.4,0),visible=False)
		self.c_text=Text(text=None,font=_fnt,x=self.x+.04,y=self.y+.025,scale=2,color=color.rgb32(90,70,0),visible=False,parent=CU)
		self.c_time=0
		self.icf=0
	def crate_refr_ico(self):
		self.icf+=time.dt*30
		if self.icf > 63.9:
			self.icf=0
		self.texture=crti+'anim_crt_'+str(int(self.icf))+'.png'
	def check_c(self):
		if (st.bonus_solved and st.crate_bonus > 0):
			return True
		return False
	def c_count(self):
		s=self
		if s.check_c():
			s.c_time=max(s.c_time-time.dt,0)
			if s.c_time <= 0:
				s.c_time=.075
				st.crate_bonus-=1
				st.crate_count+=1
				st.show_crates=1
	def update(self):
		if not st.gproc():
			s=self
			if st.bonus_round or s.check_c():
				s.c_count()
				s.crate_refr_ico()
				s.c_text.show()
				s.show()
				s.c_text.text=str(st.crate_bonus)+'/'+str(st.crates_in_bonus)
				return
			cc.purge_instance(s.c_text)
			cc.purge_instance(s)

class LiveBonus(Entity):
	def __init__(self):
		super().__init__(parent=CU,model=q,texture=_icn+'crash_live.tga',scale=.06,position=(.225,-.4,0),visible=False)
		self.l_text=Text(text=None,font=_fnt,x=self.x+.04,y=self.y+.023,scale=2,color=color.rgb32(255,31,31),visible=False,parent=CU)
		self.l_time=0
	def check_l(self):
		if (st.bonus_solved and st.lives_bonus > 0):
			return True
		return False
	def l_count(self):
		if self.check_l():
			self.l_time=max(self.l_time-time.dt,0)
			if self.l_time <= 0:
				self.l_time=.075
				status.lives_bonus-=1
				status.extra_lives+=1
				status.show_lives=1
				sn.ui_audio(ID=0)
	def update(self):
		if not st.gproc():
			if st.bonus_round or self.check_l():
				if st.lives_bonus > 0:
					self.l_count()
				self.l_text.show()
				self.show()
				self.l_text.text=str(st.lives_bonus)
				return
			cc.purge_instance(self.l_text)
			cc.purge_instance(self)


## Game Over Screen
class GameOverScreen(Entity):
	def __init__(self):
		super().__init__(model=q,texture='res/background/game_over.jpg',parent=CU,scale=(2,1),z=-.3)
		self.game_o_text=Text(text='GAME OVER!',font=_fnt,color=color.orange,scale=4.5,parent=CU,position=(-.25,.05,-.31))
		self.btn_restart=Text('WARP ROOM',font=_fnt,scale=3,color=color.yellow,position=(self.x-.2,self.y-.1,-.31))
		self.btn_quit=Text('QUIT GAME',font=_fnt,scale=3,color=color.yellow,position=(self.x-.2,self.y-.2,-.31))
		self.rs_col={0:color.white,1:color.yellow}
		self.qt_col={0:color.yellow,1:color.white}
		self.opt_select=0
		sn.GameOverMusic()
	def p_restart(self):
		st.wumpa_fruits=0
		st.extra_lives=4
		st.aku_hit=0
		cc.clear_level(passed=False)
		st.game_over=False
	def input(self,key):
		if key in ['w','s']:
			sn.ui_audio(ID=0,pit=.125)
			if self.opt_select == 0:
				self.opt_select=1
				return
			self.opt_select=0
		if key == 'enter':
			sn.ui_audio(ID=1)
			opv={0:lambda:self.p_restart(),1:lambda:application.quit()}
			opv[self.opt_select]()
	def update(self):
		sbt=self.opt_select
		self.btn_restart.color=self.rs_col[sbt]
		self.btn_quit.color=self.qt_col[sbt]


## Loading Screen
class LoadingScreen(Entity):
	def __init__(self):
		super().__init__(model=q,color=color.black,scale=(16,10),visible=False,parent=CU,z=-1,eternal=True)
		self.ltext=Text('LOADING...',font=_fnt,scale=3.5,position=(-.15,.1,-1.1),color=color.orange,visible=False,parent=CU,eternal=True)
		self.lname=Text('',font=_fnt,scale=2,position=(-.25,-.05,-1.1),color=color.azure,visible=False,parent=CU,eternal=True)
	def update(self):
		s=self
		if st.loading:
			if st.level_index in [3,5]:
				s.lname.x=-.2
			else:
				s.lname.x=-.25
			s.lname.text=LC.lv_name[st.level_index]
			s.ltext.visible=True
			s.lname.visible=True
			s.visible=True
			return
		s.ltext.visible=False
		s.lname.visible=False
		s.visible=False

class WhiteScreen(Entity):
	def __init__(self):
		super().__init__(model=q,parent=CU,scale=5,color=color.white,alpha=1)
		self.timer=0
	def update(self):
		s=self
		if s.timer < 2:
			s.timer+=time.dt/2
			s.alpha=s.timer
			if s.timer > 2:
				cc.purge_instance(s)

class BlackScreen(Entity):
	def __init__(self):
		super().__init__(model=q,parent=CU,scale=5,color=color.black,alpha=1)
		self.timer=2
		st.wait_screen=True
	def update(self):
		if not st.gproc():
			s=self
			s.timer=max(s.timer-time.dt/3,0)
			if s.timer <= 1:
				st.wait_screen=False
				s.alpha=s.timer
				if s.timer <= 0:
					s.parent=None
					cc.purge_instance(s)

## Warp Room Interface
class LevelInfo(Entity):
	def __init__(self,idx,pos):
		s=self
		sf=.1
		cgs={1:'gem',2:'gem',3:'gem',4:'gem1',5:'gem2'}
		gcsa={1:sf/1.8,2:sf,3:sf*1.4,4:sf,5:sf}
		icb='res/ui/misc/icon_box.png'
		req_col=color.rgb32(25,25,25)
		super().__init__(position=pos,parent=CU)
		s.lv_crystal=Animation(_icn+'crystal.gif',position=(self.x+.8,self.y,self.z),scale=sf,parent=CU,color=req_col)
		s.lv_col_gem=Animation(cgs[idx]+'.gif',position=(s.x+.945,s.y,s.z),scale=sf,parent=CU,color=req_col)
		s.lv_clr_gem=Animation(_icn+'gem.gif',position=(s.x+1.09,s.y,s.z),scale=sf,parent=CU,color=req_col)
		s.lv_name=Text(_loc.lv_name[idx],font=_fnt,position=(s.x,s.y+.04,s.z),scale=2.5,color=color.orange,parent=CU)
		s.lv_col_gem.scale_y=gcsa[idx]
		s.lvID=idx
		for iwb in range(3):
			Entity(model=q,texture=icb,position=(s.lv_crystal.x+iwb/7,s.y,1),scale=.16,parent=CU,color=color.rgb32(120,140,120))
		if idx in st.CRYSTAL:
			s.lv_crystal.color=color.magenta
		if idx in st.CLEAR_GEM:
			s.lv_clr_gem.color=color.rgb32(180,180,210)
		if idx == 1 and 4 in st.COLOR_GEM:
			s.lv_col_gem.color=color.rgb32(0,0,220)
		if idx == 2 and 1 in st.COLOR_GEM:
			s.lv_col_gem.color=color.rgb32(160,0,0)
		if idx == 3 and 5 in st.COLOR_GEM:
			s.lv_col_gem.color=color.rgb32(160,150,0)
		if idx == 4 and 2 in st.COLOR_GEM:
			s.lv_col_gem.color=color.rgb32(0,180,0)
		if idx == 5 and 3 in st.COLOR_GEM:
			s.lv_col_gem.color=color.violet
	def update(self):
		if st.selected_level == self.lvID:
			self.lv_name.color=color.white
			return
		self.lv_name.color=color.orange

## Bonusround Text
class BonusText(Entity):
	def __init__(self):
		self.bntx=btxt+'bonus_'
		super().__init__(model=q,texture=None,parent=CU,scale=(.3,.1),position=(0,.35),visible=False)
		self.ch_seq=0
		self.t_delay=.5
	def display(self):
		self.texture=self.bntx+str(self.ch_seq)+'.tga'
		self.visible=True
	def text_ch(self):
		self.visible=False
		if self.ch_seq == 7:
			self.ch_seq=0
			return
		self.ch_seq+=1
	def update(self):
		if not status.gproc() and not st.wait_screen:
			if not st.bonus_round:
				cc.purge_instance(self)
				return
			self.t_delay=max(self.t_delay-time.dt,0)
			if self.t_delay <= 0:
				self.t_delay=.5
				if not self.visible:
					self.display()
					return
				self.text_ch()

K=40
O=140
## Pause Menu
class PauseMenu(Entity):
	def __init__(self):
		e='res/ui/pause/'
		super().__init__(parent=CU,model=q,texture=e+'c_pause1.png',scale=(1.05,.5),position=(-.375,-.25,.1),color=color.rgb32(130,140,130),visible=False)
		self.ppt=Entity(parent=CU,model=q,texture=e+'c_pause2.png',scale=(.75,1),position=(.515,0,.1),color=color.rgb32(130,140,130),visible=False)
		##text
		self.selection=['RESUME','OPTIONS','QUIT']
		self.font_color=color.rgb32(230,100,0)
		self.need_loop=True
		self.blink_time=0
		self.choose=0
		vF=0
		self.p_name=Text('Crash B.',font='res/ui/font.ttf',scale=3,position=(vF+.4,vF+.475,self.z-1),color=self.font_color,parent=CU,visible=False)
		self.lvl_name=Text(LC.lv_name[st.level_index],font='res/ui/font.ttf',scale=3,position=(vF-.7,vF-.025,self.z-1),color=color.azure,parent=CU,visible=False)
		self.select_0=Text(self.selection[0],font='res/ui/font.ttf',scale=3,tag=0,position=(vF-.5,vF-.2,self.z-1),color=self.font_color,parent=CU,visible=False)
		self.select_1=Text(self.selection[1],font='res/ui/font.ttf',scale=3,tag=1,position=(vF-.5,vF-.275,self.z-1),color=self.font_color,parent=CU,visible=False)
		self.select_2=Text(self.selection[2],font='res/ui/font.ttf',scale=3,tag=2,position=(vF-.5,vF-.35,self.z-1),color=self.font_color,parent=CU,visible=False)
		self.crystal_counter=Text('0/5',font='res/ui/font.ttf',scale=6,position=(vF+.325,vF+.325,self.z-1),color=color.rgb32(160,0,160),parent=CU,visible=False)
		self.gem_counter=Text('0/10 GEMS',font='res/ui/font.ttf',scale=5,position=(vF+.3,vF-.1,self.z-1),color=color.rgb32(170,170,190),parent=CU,visible=False)
		self.add_text=Text('+ 0',font='res/ui/font.ttf',scale=4,position=(vF+.325,vF+.025,vF-1),color=self.font_color,parent=CU,visible=False)
		self.game_progress=Text('Progress 0%',font='res/ui/font.ttf',scale=3,position=(vF+.325,vF-.35,self.z-1),color=color.gold,parent=CU,visible=False)
		##animation
		self.cry_anim=Animation('res/ui/icon/crystal.gif',position=(vF+.6,vF+.26,self.z-1),scale=.15,fps=12,parent=CU,color=color.magenta,visible=False)
		self.col_gem1=Animation('res/ui/icon/gem.gif',position=(vF+.25,vF+.075,self.z-1),scale=.15,fps=12,parent=CU,color=color.rgb32(K,K,K),visible=False)
		self.col_gem2=Animation('res/ui/icon/gem1.gif',position=(vF+.37,vF+.075,self.z-1),scale=.15,fps=12,parent=CU,color=color.rgb32(K,K,K),visible=False)
		self.col_gem3=Animation('res/ui/icon/gem2.gif',position=(vF+.49,vF+.075,self.z-1),scale=.15,fps=12,parent=CU,color=color.rgb32(K,K,K),visible=False)
		self.col_gem4=Animation('res/ui/icon/gem.gif',position=(vF+.61,vF+.075,self.z-1),scale=(.15,.075),fps=12,parent=CU,color=color.rgb32(K,K,K),visible=False)
		self.col_gem5=Animation('res/ui/icon/gem.gif',position=(vF+.73,vF+.075,self.z-1),scale=(.15,.19),fps=12,parent=CU,color=color.rgb32(K,K,K),visible=False)
		self.cleargem=Animation('res/ui/icon/gem.gif',position=(vF+.6,vF-.03,self.z-1),scale=.2,fps=12,parent=CU,color=color.rgb32(130,130,190),visible=False)
		self.check_collected()
	def input(self,key):
		if st.pause:
			if key in ['down arrow','s']:
				sn.ui_audio(ID=0,pit=.125)
				if self.choose < 2:
					self.choose+=1
				return
			elif key in ['up arrow','w']:
				sn.ui_audio(ID=0,pit=.125)
				if self.choose > 0:
					self.choose-=1
				return
			if key == 'enter':
				sn.ui_audio(ID=1)
				if self.choose == 0:
					status.pause=False
				if self.choose == 1:
					print('menu options')
				if self.choose == 2:
					if not st.LEVEL_CLEAN:
						cc.clear_level(passed=False)
	def check_collected(self):
		s=self
		gems_total=st.color_gems+st.clear_gems
		s.gem_counter.text=str(gems_total)+'/10 GEMS'
		s.crystal_counter.text=str(st.collected_crystals)+'/5'
		s.game_progress.text='Progress '+str(st.color_gems*5+st.clear_gems*5+st.collected_crystals*10)+'%'
		s.add_text.text='+ '+str(st.clear_gems)
		for gC in st.COLOR_GEM:
			gfc={1:lambda:setattr(s.col_gem1,'color',color.rgb32(O,0,0)),
				2:lambda:setattr(s.col_gem2,'color',color.rgb32(0,O,0)),
				3:lambda:setattr(s.col_gem3,'color',color.rgb32(O,0,O)),
				4:lambda:setattr(s.col_gem4,'color',color.rgb32(0,0,O)),
				5:lambda:setattr(s.col_gem5,'color',color.rgb32(O-15,O-15,0))}
			gfc[gC]()
	def select_menu(self):
		for mn in [self.select_0,self.select_1,self.select_2]:
			if self.choose == mn.tag:
				text_blink(M=self,t=mn)
			else:
				mn.color=self.font_color
	def update(self):
		pa=st.pause
		s=self
		if pa:
			s.blink_time=max(s.blink_time-time.dt,0)
			if s.blink_time <= 0:
				s.select_menu()
		s.crystal_counter.visible=(pa)
		s.game_progress.visible=(pa)
		s.gem_counter.visible=(pa)
		s.lvl_name.visible=(pa)
		s.select_0.visible=(pa)
		s.select_1.visible=(pa)
		s.select_2.visible=(pa)
		s.add_text.visible=(pa)
		s.cry_anim.visible=(pa)
		s.col_gem1.visible=(pa)
		s.col_gem2.visible=(pa)
		s.col_gem3.visible=(pa)
		s.col_gem4.visible=(pa)
		s.col_gem5.visible=(pa)
		s.cleargem.visible=(pa)
		s.p_name.visible=(pa)
		s.ppt.visible=(pa)
		s.visible=(pa)


## Gem/Crytal
class CollectedGem(Animation):
	def __init__(self):
		super().__init__(_icn+'crystal.gif',parent=CU,scale=.15,color=color.magenta,visible=False,position=(0,-.4,-1))
		if st.level_index == 4:
			cGLI='gem1.gif'
		elif st.level_index == 5:
			cGLI='gem2.gif'
		else:
			cGLI='gem.gif'
		cGLO={1:color.rgb32(0,0,O),
			2:color.rgb32(O,0,0),
			5:color.rgb32(O,0,O),
			4:color.rgb32(0,O,0),
			3:color.rgb32(O,O,0),
			6:color.rgb32(O,0,0)}
		self.colored_gem=Animation(_icn+cGLI,parent=CU,position=(self.x-.1,self.y,self.z),scale=self.scale,color=cGLO[st.level_index],visible=False)
		self.clear_gem=Animation(_icn+'gem.gif',parent=CU,position=(self.x+.1,self.y,self.z),scale=self.scale,color=color.rgb32(100,100,170),visible=False)
		if st.level_index == 3:
			self.colored_gem.scale_y=.2
		if st.level_index == 1:
			self.colored_gem.scale_y=.07
	def update(self):
		if not status.gproc():
			if st.show_gems > 0:
				status.show_gems-=time.dt
				if st.level_crystal:
					self.show()
				if st.level_col_gem:
					self.colored_gem.show()
				if st.level_cle_gem:
					self.clear_gem.show()
				return
			self.colored_gem.visible=False
			self.clear_gem.visible=False
			self.hide()


## Time Trial
class TrialTimer(Entity):
	def __init__(self,t):
		tm_str=strftime('%M:%S',gmtime(t))
		super().__init__()
		self.disp=Text(tm_str,font=_fnt,scale=3,position=(.7,-.4),parent=CU,color=color.rgb32(200,200,100))
		self.fin=False
		self.TME=t
	def trial_fail(self):
		if st.level_index == 3:
			st.gem_death=True
		self.trial_interrupt()
	def trial_interrupt(self):
		cc.purge_instance(self.disp)
		cc.purge_instance(self)
	def update(self):
		if not st.gproc():
			if (st.level_index == 3 and st.level_col_gem):
				self.trial_interrupt()
				return
			self.disp.text=strftime("%M:%S",gmtime(self.TME))
			self.TME=max(self.TME-time.dt,0)
			if self.TME <= 0:
				if not self.fin:
					self.fin=True
					self.trial_fail()
