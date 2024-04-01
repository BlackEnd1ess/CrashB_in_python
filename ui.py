from ursina import *
import status,_core

_icn='res/ui/icon/'
_fnt='res/ui/font.ttf'

def text_blink(M,t):
	if M.blink_time <= 0:
		if t.color == M.font_color:
			t.color=color.white
		else:
			t.color=M.font_color
		M.blink_time=.3

def wumpa_count_anim():
	wmA=Entity(model='quad',texture=_icn+'wumpa_fruits/w0.png',scale=.075,parent=camera.ui,position=(-.2,-.4,-.1))
	wmA.animate_position((-1.2,1.3,-.1),duration=.3)
	invoke(wmA.disable,delay=.3)

## Main Counter ##
class WumpaCounter(Entity):
	def __init__(self):
		self.pa='res/ui/wumpa_font/'
		super().__init__(model='quad',texture=_icn+'wumpa_fruits/w0.png',parent=camera.ui,position=(-.75,0.43,0),scale=(.07,.08,0),visible=False,texture_position=(0,0))
		self.digit_0=Entity(model='quad',texture=self.pa+'0.png',parent=camera.ui,position=(self.x+.075,self.y),scale=.06,visible=False)
		self.digit_1=Entity(model='quad',texture=self.pa+'0.png',parent=camera.ui,position=(self.digit_0.x+.06,self.digit_0.y),scale=.06,visible=False)
		self.w_animation=0
		WumpaBonus()
	def digits(self):
		n=str(status.wumpa_fruits)
		self.digit_0.texture=self.pa+n[0]
		self.digit_0.show()
		if status.wumpa_fruits >= 10:
			self.digit_1.visible=True
			self.digit_1.texture=self.pa+n[1]
			return
		self.digit_1.visible=False
	def update(self):
		if status.wumpa_fruits > 99:
			status.wumpa_fruits=0
			_core.give_extra_live()
		if status.show_wumpas > 0:
			self.w_animation+=time.dt*20
			if self.w_animation > 12:
				self.w_animation=0
			self.texture=_icn+'wumpa_fruits/w'+str(int(self.w_animation))+'.png'
			self.show()
			self.digits()
			status.show_wumpas-=time.dt
			if status.show_wumpas <= 0:
				self.w_animation=0
				self.hide()
				self.digit_0.hide()
				self.digit_1.hide()

class CrateCounter(Animation):
	def __init__(self):
		super().__init__(_icn+'crate.gif',parent=camera.ui,scale=0.1,color=color.rgb(92,57,27),position=(-0.1,0.43,0),fps=4,visible=False)
		self.c_text=Text(text=None,font=_fnt,x=self.x+0.05,y=self.y+0.035,scale=3,color=color.rgb(75,35,10),visible=False)
		CrateBonus()
	def update(self):
		if status.show_crates > 0 and status.crates_in_level > 0:
			self.show()
			self.c_text.show()
			self.c_text.text=str(status.crate_count)+'/'+str(status.crates_in_level)
			status.show_crates-=time.dt
			if status.show_crates <= 0:
				self.hide()
				self.c_text.hide()

class LiveCounter(Entity):
	def __init__(self):
		super().__init__(parent=camera.ui,model='quad',texture=_icn+'lives.png',scale=(0.08,0.085),position=(0.7,0.43,0),visible=False)
		self.l_text=Text(text=None,font=_fnt,x=self.x+0.05,y=self.y+0.035,scale=3,color=color.rgb(255,31,31),visible=False)
		LiveBonus()
	def update(self):
		if status.show_lives > 0:
			self.show()
			self.l_text.show()
			self.l_text.text=str(status.extra_lives)
			status.show_lives-=time.dt
			if status.show_lives <= 0:
				self.hide()
				self.l_text.hide()


## Bonus Counter ##
class WumpaBonus(Entity):
	def __init__(self):
		super().__init__(model='quad',texture=_icn+'wumpa_fruits/w0.png',parent=camera.ui,position=(-.2,-.4,0),scale=(.05,.06,0),visible=False)
		self.w_text=Text(text=None,font=_fnt,x=self.x+.04,y=self.y+.025,scale=2,color=color.rgb(175,235,30),parent=camera.ui,visible=False)
		self.w_animation=0
	def update(self):
		if status.bonus_round or status.bonus_solved and status.wumpa_bonus > 0:
			self.show()
			self.w_text.show()
			self.w_text.text=str(status.wumpa_bonus)
			self.w_animation+=time.dt*20
			if self.w_animation > 12:
				self.w_animation=0
			self.texture=_icn+'wumpa_fruits/w'+str(int(self.w_animation))+'.png'
		else:
			self.hide()
			self.w_text.hide()
			return

class CrateBonus(Animation):
	def __init__(self):
		super().__init__(_icn+'crate.gif',parent=camera.ui,scale=0.075,color=color.rgb(92,57,27),position=(0,-0.4,0),fps=4,visible=False)
		self.c_text=Text(text=None,font=_fnt,x=self.x+0.05,y=self.y+0.025,scale=2,color=color.rgb(75,35,10),visible=False)
		if status.crates_in_level < 1:
			self.hide()
			self.c_text.hide()
	def update(self):
		if status.bonus_round or status.bonus_solved and status.crate_bonus > 0:
			self.show()
			self.c_text.show()
			self.c_text.text=str(status.crate_bonus)+'/'+str(status.crates_in_bonus)
		else:
			self.hide()
			self.c_text.hide()
			return

class LiveBonus(Entity):
	def __init__(self):
		super().__init__(parent=camera.ui,model='quad',texture=_icn+'lives.png',scale=0.06,position=(0.225,-0.4,0),visible=False)
		self.l_text=Text(text=None,font=_fnt,x=self.x+0.04,y=self.y+0.023,scale=2,color=color.rgb(255,31,31),visible=False)
	def update(self):
		if status.bonus_round or status.bonus_solved and status.lives_bonus > 0:
			self.show()
			self.l_text.show()
			self.l_text.text=str(status.lives_bonus)
		else:
			self.hide()
			self.l_text.hide()
			return


## Loading Screen
class LoadingScreen(Entity):
	def __init__(self):
		super().__init__(model='quad',color=color.black,scale=(16,10),visible=False,parent=camera.ui,z=1)
		self.ltext=Text('Loading...',font=_fnt,scale=3.5,position=(-.15,.1),color=color.orange,visible=False,parent=camera.ui)
	def update(self):
		if status.loading:
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
				if not status.loading:
					status.loading=True
					LoadingScreen()
				if self.timer >= 2:
					self.disable()

class BlackScreen(Entity):
	def __init__(self):
		super().__init__(model='quad',parent=camera.ui,scale=5,color=color.black,alpha=1)
		self.timer=2
	def update(self):
		if self.timer > 0:
			self.timer-=time.dt/1.5
			if self.timer <= 1:
				self.alpha=self.timer
				if self.timer <= 0:
					self.parent=None
					self.disable()


## Bonusround Text
class BonusText(Entity):
	def __init__(self):
		super().__init__()
		self.bonus_text=Text(text=None,font=_fnt,position=(-0.2,0.4),scale=5,color=color.azure,parent=camera.ui)
		self.bonus_t='BONUS!'
		self.seq_time=0
	def update(self):
		if status.bonus_round:
			self.seq_time+=time.dt*1.5
			bt=self.bonus_t[:int(self.seq_time)]
			self.bonus_text.text=str(bt)
			if self.seq_time > 6.98:
				self.seq_time=0
		else:
			self.bonus_text.disable()
			self.disable()
			return

K=40
O=140
## Pause Menu
class PauseMenu(Entity):
	def __init__(self):
		e='res/ui/pause/pause_ui'
		super().__init__(model=e+'.ply',texture=e+'.tga',rotation=(-90,180,0),scale=(0.1/705,0,0.1/550),parent=camera.ui,z=1,color=color.rgb(130,140,130),visible=False)
		##text
		self.selection=['RESUME','OPTIONS','QUIT']
		self.font_color=color.rgb(230,100,0)
		self.need_loop=True
		self.blink_time=0
		self.choose=0
		self.p_name=Text('Crash B.',font='res/ui/font.ttf',scale=3,position=(self.x+.4,self.y+.475,self.z-1),color=self.font_color,parent=camera.ui,visible=False)
		self.lvl_name=Text(status.level_name[status.level_index],font='res/ui/font.ttf',scale=3,position=(self.x-.7,self.y-.025,self.z-1),color=color.azure,parent=camera.ui,visible=False)
		self.select_0=Text(self.selection[0],font='res/ui/font.ttf',scale=3,tag=0,position=(self.x-.5,self.y-.2,self.z-1),color=self.font_color,parent=camera.ui,visible=False)
		self.select_1=Text(self.selection[1],font='res/ui/font.ttf',scale=3,tag=1,position=(self.x-.5,self.y-.275,self.z-1),color=self.font_color,parent=camera.ui,visible=False)
		self.select_2=Text(self.selection[2],font='res/ui/font.ttf',scale=3,tag=2,position=(self.x-.5,self.y-.35,self.z-1),color=self.font_color,parent=camera.ui,visible=False)
		self.crystal_counter=Text('0/5',font='res/ui/font.ttf',scale=6,position=(self.x+.325,self.y+.325,self.z-1),color=color.rgb(160,0,160),parent=camera.ui,visible=False)
		self.gem_counter=Text('0/15 GEMS',font='res/ui/font.ttf',scale=5,position=(self.x+.3,self.y-.1,self.z-1),color=color.rgb(170,170,190),parent=camera.ui,visible=False)
		self.add_text=Text('+ 0',font='res/ui/font.ttf',scale=4,position=(self.x+.325,self.y+.025,self.z-1),color=self.font_color,parent=camera.ui,visible=False)
		self.game_progress=Text('Progress 0%',font='res/ui/font.ttf',scale=3,position=(self.x+.325,self.y-.35,self.z-1),color=color.gold,parent=camera.ui,visible=False)
		##animation
		self.cry_anim=Animation('res/ui/icon/crystal.gif',position=(self.x+.6,self.y+.26,self.z-1),scale=.15,fps=12,parent=camera.ui,color=color.magenta,visible=False)
		self.col_gem1=Animation('res/ui/icon/gem.gif',position=(self.x+.32,self.y+.075,self.z-1),scale=.15,fps=12,parent=camera.ui,color=color.rgb(K,K,K),visible=False)
		self.col_gem2=Animation('res/ui/icon/gem1.gif',position=(self.x+.44,self.y+.075,self.z-1),scale=.15,fps=12,parent=camera.ui,color=color.rgb(K,K,K),visible=False)
		self.col_gem3=Animation('res/ui/icon/gem2.gif',position=(self.x+.56,self.y+.075,self.z-1),scale=.15,fps=12,parent=camera.ui,color=color.rgb(K,K,K),visible=False)
		self.col_gem4=Animation('res/ui/icon/gem3.gif',position=(self.x+.68,self.y+.075,self.z-1),scale=.15,fps=12,parent=camera.ui,color=color.rgb(K,K,K),visible=False)
		self.col_gem5=Animation('res/ui/icon/gem.gif',position=(self.x+.8,self.y+.075,self.z-1),scale=.15,fps=12,parent=camera.ui,color=color.rgb(K,K,K),visible=False)
		self.cleargem=Animation('res/ui/icon/gem.gif',position=(self.x+.6,self.y-.03,self.z-1),scale=.2,fps=12,parent=camera.ui,color=color.rgb(130,130,190),visible=False)
	def input(self,key):
		if status.pause:
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
					if not status.LEVEL_CLEAN:
						status.LEVEL_CLEAN=True
						_core.clear_level(passed=False)
	def check_collected(self):
		gems_total=status.color_gems+status.clear_gems
		self.gem_counter.text=str(gems_total)+'/15 GEMS'
		self.crystal_counter.text=str(status.collected_crystals)+'/5'
		self.game_progress.text='Progress '+str(status.color_gems*6+status.clear_gems*7+status.collected_crystals*7)+'%'
		self.add_text.text='+ '+str(status.clear_gems)
		if self.need_loop:
			for gC in status.COLOR_GEM:
				if gC == 1:
					self.col_gem1.color=color.rgb(O,0,0)
				if gC == 2:
					self.col_gem2.color=color.rgb(0,O,0)
				if gC == 3:
					self.col_gem3.color=color.rgb(O,0,O)
				if gC == 4:
					self.col_gem4.color=color.rgb(0,0,O)
				if gC == 5:
					self.col_gem5.color=color.rgb(O,O,0)
			if len(status.COLOR_GEM) >= 5:
				self.need_loop=False
	def select_menu(self):
		for mn in [self.select_0,self.select_1,self.select_2]:
			if self.choose == mn.tag:
				text_blink(M=self,t=mn)
			else:
				mn.color=self.font_color
	def update(self):
		self.check_collected()
		if status.pause:
			self.select_menu()
			if self.blink_time > 0:
				self.blink_time-=time.dt
		for vis in [self.p_name,
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
			if status.pause:
				vis.show()
			else:
				vis.hide()

## Gem/Crytal
class CollectedGem(Animation):
	def __init__(self):
		super().__init__(_icn+'crystal.gif',parent=camera.ui,scale=.15,color=color.magenta,visible=False,position=(0,-.4,-1))
		cGLI={1:'gem3.gif',2:'gem1.gif',3:'gem2.gif',4:'gem.gif',5:'gem.gif',6:'gem.gif'}
		cGLO={1:color.rgb(0,0,O),2:color.rgb(0,O,0),3:color.rgb(O,0,O),4:color.rgb(O,0,0),5:color.rgb(O,O,0),6:color.rgb(O,0,0)}
		self.colored_gem=Animation(_icn+cGLI[status.level_index],parent=camera.ui,position=(self.x-.1,self.y,self.z),scale=self.scale,color=cGLO[status.level_index],visible=False)
		self.clear_gem=Animation(_icn+'gem.gif',parent=camera.ui,position=(self.x+.1,self.y,self.z),scale=self.scale,color=color.rgb(100,100,170),visible=False)
		if status.level_index == 5:
			self.colored_gem.scale_y=.2
	def update(self):
		if status.show_gems > 0:
			status.show_gems-=time.dt
			if status.level_crystal:
				self.show()
			if status.level_col_gem:
				self.colored_gem.show()
			if status.level_cle_gem:
				self.clear_gem.show()
			return
		self.colored_gem.hide()
		self.clear_gem.hide()
		self.hide()