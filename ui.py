import status,_core,_loc,sound
from ursina import *

w_pa='res/ui/icon/wumpa_fruit/w'
_icn='res/ui/icon/'
_fnt='res/ui/font.ttf'
st=status
cc=_core
LC=_loc

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
	lvA=Entity(parent=camera.ui,model='quad',texture=_icn+'lives.png',scale=(.08,.085),position=(.5,.43,0),color=color.gold)
	lvA.animate_x(.7,duration=.3)
	invoke(lvA.disable,delay=3.1)

class WumpaCollectAnim(Entity):
	def __init__(self,pos):
		super().__init__(model='quad',texture=w_pa+'0.png',scale=.075,parent=camera.ui,position=pos)
	def update(self):
		if not st.gproc():
			dta_x=-.75-self.x
			dta_y=.43-self.y
			anp=time.dt*8
			if abs(dta_x) > .05 and abs(dta_y) > .05:
				self.x+=dta_x*anp
				self.y+=dta_y*anp
				return
			self.disable()

## Main Counter ##
class WumpaCounter(Entity):
	def __init__(self):
		self.pa='res/ui/wumpa_font/'
		super().__init__(model='quad',texture=w_pa+'0.png',parent=camera.ui,position=(-.75,.43,0),scale=(.07,.08,0),visible=False,texture_position=(0,0))
		self.digit_0=Entity(model='quad',texture=self.pa+'0.png',parent=camera.ui,position=(self.x+.075,self.y),scale=.06,visible=False)
		self.digit_1=Entity(model='quad',texture=self.pa+'0.png',parent=camera.ui,position=(self.digit_0.x+.06,self.digit_0.y),scale=.06,visible=False)
		self.frm=0
		_loc.uiW=self
	def digits(self):
		n=str(st.wumpa_fruits)
		self.digit_0.texture=self.pa+n[0]
		self.digit_0.show()
		if st.wumpa_fruits >= 10:
			self.digit_1.visible=True
			self.digit_1.texture=self.pa+n[1]
			return
		self.digit_1.visible=False
	def wumpa_max(self):
		if st.wumpa_fruits > 99:
			status.wumpa_fruits=0
			cc.give_extra_live()
	def update(self):
		if not status.gproc():
			self.wumpa_max()
			if st.show_wumpas > 0:
				self.digits()
				self.show()
				wmp_anim(self)
			status.show_wumpas=max(status.show_wumpas-time.dt,0)
			if st.show_wumpas <= 0:
				self.frm=0
				self.hide()
				self.digit_0.hide()
				self.digit_1.hide()

class CrateCounter(Animation):
	def __init__(self):
		super().__init__(_icn+'crate.gif',parent=camera.ui,scale=.1,color=color.rgb32(90,70,0),position=(-.1,.43,0),fps=4,visible=False)
		self.c_text=Text(text=None,font=_fnt,x=self.x+.05,y=self.y+.035,scale=3,color=self.color,visible=False)
	def update(self):
		if not status.gproc() and st.crates_in_level > 0:
			if st.show_crates > 0:
				status.show_crates-=time.dt
				if st.show_crates <= 0:
					self.hide()
					self.c_text.hide()
					return
				self.show()
				self.c_text.show()
				self.c_text.text=str(st.crate_count)+'/'+str(st.crates_in_level)

class LiveCounter(Entity):
	def __init__(self):
		super().__init__(parent=camera.ui,model='quad',texture=_icn+'lives.png',scale=(.08,.085),position=(.7,.43,0),visible=False)
		self.l_text=Text(text=None,font=_fnt,x=self.x+.05,y=self.y+.035,scale=3,color=color.rgb32(255,31,31),visible=False)
	def update(self):
		if not status.gproc():
			if st.show_lives > 0:
				status.show_lives-=time.dt
				if st.show_lives <= 0:
					self.hide()
					self.l_text.hide()
					return
				self.l_text.show()
				self.show()
				self.l_text.text=str(st.extra_lives)


## Bonus Counter ##
class WumpaBonus(Entity):
	def __init__(self):
		super().__init__(model='quad',texture=w_pa+'0.png',parent=camera.ui,position=(-.2,-.4,0),scale=(.05,.06,0),visible=False)
		self.w_text=Text(text=None,font=_fnt,x=self.x+.04,y=self.y+.025,scale=2,color=color.rgb32(175,235,30),parent=camera.ui,visible=False)
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
				self.w_time=.075
				status.wumpa_bonus-=1
				WumpaCollectAnim(pos=(-.2,-.4))
				cc.wumpa_count(1)
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

class CrateBonus(Animation):
	def __init__(self):
		super().__init__(_icn+'crate.gif',parent=camera.ui,scale=.075,color=color.rgb32(90,70,0),position=(0,-.4,0),fps=4,visible=False)
		self.c_text=Text(text=None,font=_fnt,x=self.x+.05,y=self.y+.025,scale=2,color=self.color,visible=False)
		self.c_time=0
	def check_c(self):
		if (st.bonus_solved and st.crate_bonus > 0):
			return True
		return False
	def c_count(self):
		if self.check_c():
			self.c_time=max(self.c_time-time.dt,0)
			if self.c_time <= 0:
				self.c_time=.075
				status.crate_bonus-=1
				status.crate_count+=1
				status.show_crates=1
	def update(self):
		if not st.gproc():
			if st.bonus_round or self.check_c():
				self.c_count()
				self.c_text.show()
				self.show()
				self.c_text.text=str(st.crate_bonus)+'/'+str(st.crates_in_bonus)
				return
			cc.purge_instance(self.c_text)
			cc.purge_instance(self)

class LiveBonus(Entity):
	def __init__(self):
		super().__init__(parent=camera.ui,model='quad',texture=_icn+'lives.png',scale=.06,position=(.225,-.4,0),visible=False)
		self.l_text=Text(text=None,font=_fnt,x=self.x+.04,y=self.y+.023,scale=2,color=color.rgb32(255,31,31),visible=False)
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
				Audio(sound.snd_lifes)
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
class GameOverScreen(Entity):## call event?
	def __init__(self):
		super().__init__(model='quad',parent=camera.ui,scale=(16,10),color=color.black,z=-.1)
		self.game_o_text=Text(text='GAME OVER!',font=_fnt,color=color.orange,scale=4,parent=camera.ui,position=(.5,.5,-.1))

## Loading Screen
class LoadingScreen(Entity):
	def __init__(self):
		super().__init__(model='quad',color=color.black,scale=(16,10),visible=False,parent=camera.ui,z=1)
		self.ltext=Text('Loading...',font=_fnt,scale=3.5,position=(-.15,.1),color=color.orange,visible=False,parent=camera.ui)
	def update(self):
		if st.loading:
			self.ltext.visible=True
			self.visible=True
			return
		self.ltext.visible=False
		self.visible=False

class WhiteScreen(Entity):
	def __init__(self):
		super().__init__(model='quad',parent=camera.ui,scale=5,color=color.white,alpha=1)
		self.timer=0
	def update(self):
		if self.timer < 2:
			self.timer+=time.dt/2
			self.alpha=self.timer
			if self.timer >= 1:
				if not st.loading:
					status.loading=True
					LoadingScreen()
				if self.timer >= 2:
					self.parent=None
					scene.entities.remove(self)
					self.disable()

class BlackScreen(Entity):
	def __init__(self):
		super().__init__(model='quad',parent=camera.ui,scale=5,color=color.black,alpha=1)
		self.timer=2
		status.wait_screen=True
	def update(self):
		if not st.gproc():
			self.timer=max(self.timer-time.dt/1.5,0)
			if self.timer <= 1:
				status.wait_screen=False
				self.alpha=self.timer
				if self.timer <= 0:
					self.parent=None
					scene.entities.remove(self)
					self.disable()

## Bonusround Text
class BonusText(Entity):
	def __init__(self):
		super().__init__()
		self.bn_text=Text(text='',font=_fnt,position=(-.2,.4),scale=5,color=color.azure,parent=camera.ui)
		self.letters='BONUS!'
		self.ch_seq=0
		self.t_delay=.5
	def display(self):
		self.bn_text.text=self.letters[:self.ch_seq]
		self.bn_text.visible=True
	def text_ch(self):
		self.bn_text.visible=False
		if self.ch_seq == 6:
			self.ch_seq=0
		self.ch_seq+=1
	def update(self):
		if not status.gproc() and not status.wait_screen:
			if not st.bonus_round:
				cc.purge_instance(self.bn_text)
				cc.purge_instance(self)
				return
			self.t_delay=max(self.t_delay-time.dt,0)
			if self.t_delay <= 0:
				self.t_delay=.5
				if not self.bn_text.visible:
					self.display()
					return
				self.text_ch()

K=40
O=130
## Pause Menu
class PauseMenu(Entity):
	def __init__(self):
		e='res/ui/pause/'
		super().__init__(parent=camera.ui,model='quad',texture=e+'c_pause1.png',scale=(1.05,.5),position=(-.375,-.25,.1),color=color.rgb32(130,140,130),visible=False)
		self.ppt=Entity(parent=camera.ui,model='quad',texture=e+'c_pause2.png',scale=(.75,1),position=(.515,0,.1),color=color.rgb32(130,140,130),visible=False)
		##text
		self.selection=['RESUME','OPTIONS','QUIT']
		self.font_color=color.rgb32(230,100,0)
		self.need_loop=True
		self.blink_time=0
		self.choose=0
		vF=0
		self.p_name=Text('Crash B.',font='res/ui/font.ttf',scale=3,position=(vF+.4,vF+.475,self.z-1),color=self.font_color,parent=camera.ui,visible=False)
		self.lvl_name=Text(LC.lv_name[st.level_index],font='res/ui/font.ttf',scale=3,position=(vF-.7,vF-.025,self.z-1),color=color.azure,parent=camera.ui,visible=False)
		self.select_0=Text(self.selection[0],font='res/ui/font.ttf',scale=3,tag=0,position=(vF-.5,vF-.2,self.z-1),color=self.font_color,parent=camera.ui,visible=False)
		self.select_1=Text(self.selection[1],font='res/ui/font.ttf',scale=3,tag=1,position=(vF-.5,vF-.275,self.z-1),color=self.font_color,parent=camera.ui,visible=False)
		self.select_2=Text(self.selection[2],font='res/ui/font.ttf',scale=3,tag=2,position=(vF-.5,vF-.35,self.z-1),color=self.font_color,parent=camera.ui,visible=False)
		self.crystal_counter=Text('0/5',font='res/ui/font.ttf',scale=6,position=(vF+.325,vF+.325,self.z-1),color=color.rgb32(160,0,160),parent=camera.ui,visible=False)
		self.gem_counter=Text('0/15 GEMS',font='res/ui/font.ttf',scale=5,position=(vF+.3,vF-.1,self.z-1),color=color.rgb32(170,170,190),parent=camera.ui,visible=False)
		self.add_text=Text('+ 0',font='res/ui/font.ttf',scale=4,position=(vF+.325,vF+.025,vF-1),color=self.font_color,parent=camera.ui,visible=False)
		self.game_progress=Text('Progress 0%',font='res/ui/font.ttf',scale=3,position=(vF+.325,vF-.35,self.z-1),color=color.gold,parent=camera.ui,visible=False)
		##animation
		self.cry_anim=Animation('res/ui/icon/crystal.gif',position=(vF+.6,vF+.26,self.z-1),scale=.15,fps=12,parent=camera.ui,color=color.magenta,visible=False)
		self.col_gem1=Animation('res/ui/icon/gem.gif',position=(vF+.25,vF+.075,self.z-1),scale=.15,fps=12,parent=camera.ui,color=color.rgb32(K,K,K),visible=False)
		self.col_gem2=Animation('res/ui/icon/gem1.gif',position=(vF+.37,vF+.075,self.z-1),scale=.15,fps=12,parent=camera.ui,color=color.rgb32(K,K,K),visible=False)
		self.col_gem3=Animation('res/ui/icon/gem2.gif',position=(vF+.49,vF+.075,self.z-1),scale=.15,fps=12,parent=camera.ui,color=color.rgb32(K,K,K),visible=False)
		self.col_gem4=Animation('res/ui/icon/gem.gif',position=(vF+.61,vF+.075,self.z-1),scale=(.15,.075),fps=12,parent=camera.ui,color=color.rgb32(K,K,K),visible=False)
		self.col_gem5=Animation('res/ui/icon/gem.gif',position=(vF+.73,vF+.075,self.z-1),scale=(.15,.19),fps=12,parent=camera.ui,color=color.rgb32(K,K,K),visible=False)
		self.cleargem=Animation('res/ui/icon/gem.gif',position=(vF+.6,vF-.03,self.z-1),scale=.2,fps=12,parent=camera.ui,color=color.rgb32(130,130,190),visible=False)
	def input(self,key):
		if st.pause:
			if key in ['down arrow','s']:
				if self.choose < 2:
					self.choose+=1
			elif key in ['up arrow','w']:
				if self.choose > 0:
					self.choose-=1
			if key == 'enter':
				if self.choose == 0:
					status.pause=False
				if self.choose == 1:
					print('menu options')
				if self.choose == 2:
					if not st.LEVEL_CLEAN:
						status.LEVEL_CLEAN=True
						cc.clear_level(passed=False)
	def check_collected(self):
		gems_total=st.color_gems+st.clear_gems
		self.gem_counter.text=str(gems_total)+'/15 GEMS'
		self.crystal_counter.text=str(st.collected_crystals)+'/5'
		self.game_progress.text='Progress '+str(st.color_gems*6+st.clear_gems*7+st.collected_crystals*7)+'%'
		self.add_text.text='+ '+str(st.clear_gems)
		if self.need_loop:
			for gC in st.COLOR_GEM:
				if gC == 1:
					self.col_gem1.color=color.rgb32(O,0,0)
				if gC == 2:
					self.col_gem2.color=color.rgb32(0,O,0)
				if gC == 3:
					self.col_gem3.color=color.rgb32(O,0,O)
				if gC == 4:
					self.col_gem4.color=color.rgb32(0,0,O)
				if gC == 5:
					self.col_gem5.color=color.rgb32(O-15,O-15,0)
			if len(st.COLOR_GEM) >= 5:
				self.need_loop=False
	def select_menu(self):
		for mn in [self.select_0,self.select_1,self.select_2]:
			if self.choose == mn.tag:
				text_blink(M=self,t=mn)
			else:
				mn.color=self.font_color
	def update(self):
		self.check_collected()
		if st.pause:
			self.select_menu()
			if self.blink_time > 0:
				self.blink_time-=time.dt
		for vis in [self.p_name,
					self.ppt,
					self.lvl_name,
					self.select_0,
					self.select_1,
					self.select_2,
					self.crystal_counter,
					self.gem_counter,
					self.add_text,
					self.game_progress,
					self.cry_anim,
					self.col_gem1,
					self.col_gem2,
					self.col_gem3,
					self.col_gem4,
					self.col_gem5,
					self.cleargem,
					self]:
			if st.pause:
				vis.show()
			else:
				vis.hide()

## Gem/Crytal
class CollectedGem(Animation):
	def __init__(self):
		super().__init__(_icn+'crystal.gif',parent=camera.ui,scale=.15,color=color.magenta,visible=False,position=(0,-.4,-1))
		if st.level_index == 4:
			cGLI='gem1.gif'
		elif st.level_index == 5:
			cGLI='gem2.gif'
		else:
			cGLI='gem.gif'
		cGLO={1:color.rgb32(0,0,O),2:color.rgb32(O,0,0),5:color.rgb32(O,0,O),4:color.rgb32(O,0,0),3:color.rgb32(O,O,0),6:color.rgb32(O,0,0)}
		self.colored_gem=Animation(_icn+cGLI,parent=camera.ui,position=(self.x-.1,self.y,self.z),scale=self.scale,color=cGLO[st.level_index],visible=False)
		self.clear_gem=Animation(_icn+'gem.gif',parent=camera.ui,position=(self.x+.1,self.y,self.z),scale=self.scale,color=color.rgb32(100,100,170),visible=False)
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
class ElapsedTime(Entity):
	def __init__(self):
		super().__init__(model='quad',position=(-.3,-.3,.1))
		self.tmText=Text(text=None,font=_fnt,position=self.position,scale=3,color=color.silver)
		self.TME=0