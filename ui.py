from ursina import Animation,Entity,Audio,Text,camera,color,scene,invoke,lerp,distance,curve
import status,_core,_loc,sound,settings,warproom,level,time
from ursina.ursinastuff import destroy
from time import strftime,gmtime

cr_i='res/ui/icon/crystal/cry'
icb='res/ui/misc/icon_box.png'
w_pa='res/ui/icon/wumpa/w'
wmpf='res/ui/digit_wumpa/'
crtf='res/ui/digit_crate/'
crti='res/ui/icon/crate/'
lvtf='res/ui/digit_live/'
ivy_='res/ui/misc/ivy'
_fnt='res/ui/font.ttf'
btxt='res/ui/bonus/'
_icn='res/ui/icon/'
e='res/ui/pause/'
q='quad'

sf=.003
oi=.1

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
def wmp_anim(w):
	w.frm=min(w.frm+time.dt*18,13.999)
	if w.frm > 13.99:
		w.frm=0
	w.texture=w_pa+f'{int(w.frm)}.png'
	del w

def text_blink(M,t):
	if M.blink_time <= 0:
		M.blink_time=.3
		if t.color == M.font_color:
			t.color=color.white
			return
		t.color=M.font_color

class LiveCollectAnim(Entity):
	def __init__(self):
		super().__init__(model=q,texture=_icn+'crash_live.tga',position=(.5,.43,0),scale=(.1,.09),color=color.gold,parent=CU)
	def update(self):
		if not st.gproc():
			s=self
			if s.x < .65:
				s.x+=time.dt*2
				return
			destroy(s)

class WumpaCollectAnim(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=q,texture=w_pa+'0.png',scale={False:.075,True:.06}[st.bonus_round],parent=CU,position=pos)
		s.tdirec=(-.75,.43,0)
		if st.bonus_round:
			s.tdirec=(-.25,-.475,0)
		del pos
	def update(self):
		if st.gproc():
			return
		s=self
		if distance(s.position,s.tdirec) > .1:
			s.position=lerp(s.position,s.tdirec,time.dt*5)
			return
		destroy(s)


## Main Counter ##
class WumpaCounter(Entity):
	def __init__(self):
		s=self
		super().__init__(model=q,parent=CU,position=(-.75,.43,0),scale=(.07,.08,0),visible=False)
		s.digit_0=Entity(model=q,parent=CU,position=(s.x+.075,s.y),scale=.06,visible=False)
		s.digit_1=Entity(model=q,parent=CU,position=(s.digit_0.x+.06,s.digit_0.y),scale=.06,visible=False)
		s.frm=0
	def digits(self):
		s=self
		n=f'{st.wumpa_fruits}'
		s.digit_0.texture=wmpf+n[0]+'.png'
		s.digit_0.visible=True
		s.visible=True
		if st.wumpa_fruits >= 10:
			s.digit_1.visible=True
			s.digit_1.texture=wmpf+n[1]+'.png'
			return
		s.digit_1.visible=False
	def wumpa_max(self):
		st.wumpa_fruits=0
		cc.give_extra_live()
	def update(self):
		if st.gproc():
			return
		s=self
		if st.wumpa_fruits > 99:
			s.wumpa_max()
		if st.show_wumpas > 0:
			wmp_anim(s)
			s.digits()
			st.show_wumpas=max(st.show_wumpas-time.dt,0)
			if st.show_wumpas <= 0:
				s.frm=0
				s.digit_0.visible=False
				s.digit_1.visible=False
				s.visible=False

class CrateCounter(Entity):
	def __init__(self):
		s=self
		s.tpd=crtf
		super().__init__(model=q,texture=None,parent=CU,scale=.1,position=(-.2,.43,.2),fps=4,visible=False)
		s.col_digit0=Entity(model=q,texture=None,scale=.06,position=(s.x+.08,s.y,s.z),parent=CU,visible=False)
		s.col_digit1=Entity(model=q,texture=None,scale=.06,position=(s.x+.14,s.y,s.z),parent=CU,visible=False)
		s.col_digit2=Entity(model=q,texture=None,scale=.06,position=(s.x+.2,s.y,s.z),parent=CU,visible=False)
		s.seperator=Entity(model=q,texture=crtf+'seperator.png',scale=.06,position=(s.x,s.y,s.z),parent=CU,visible=False)
		s.req_digit0=Entity(model=q,texture=None,scale=.06,position=(s.x,s.y,s.z),parent=CU,visible=False)
		s.req_digit1=Entity(model=q,texture=None,scale=.06,position=(s.x,s.y,s.z),parent=CU,visible=False)
		s.req_digit2=Entity(model=q,texture=None,scale=.06,position=(s.x,s.y,s.z),parent=CU,visible=False)
		s.icf=0
	def crate_refr_ico(self):
		s=self
		s.icf=min(s.icf+time.dt*30,63.999)
		if s.icf > 63.99:
			s.icf=0
		s.texture=crti+f'anim_crt_{int(s.icf)}.png'
	def remv_ui(self):
		s=self
		s.visible,s.seperator.visible=False,False
		s.col_digit0.visible,s.col_digit1.visible,s.col_digit2.visible=False,False,False
		s.req_digit0.visible,s.req_digit1.visible,s.req_digit2.visible=False,False,False
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
		s.col_digit0.visible,s.seperator.visible,s.visible=True,True,True
		s.col_digit1.visible,s.col_digit2.visible=False,False
		s.col_digit0.texture=s.tpd+ccv[0]+'.png'
		if st.crate_count > 9:
			s.col_digit1.texture=s.tpd+ccv[1]+'.png'
			s.col_digit1.visible=True
			s.col_digit2.visible=False
			if st.crate_count > 99:
				s.col_digit2.texture=s.tpd+ccv[2]+'.png'
				s.col_digit2.visible=True
	def update(self):
		if st.gproc() or st.crates_in_level <= 0:
			return
		s=self
		if st.show_crates > 0:
			st.show_crates=max(st.show_crates-time.dt,0)
			if st.show_crates <= 0:
				s.remv_ui()
				return
			s.crate_refr_ico()
			s.col_count_refr()
			s.req_count_refr()

class LiveCounter(Entity):
	def __init__(self):
		s=self
		s.ptl=lvtf
		super().__init__(parent=CU,model=q,texture=_icn+'crash_live.tga',scale=(.1,.09),position=(.65,.43,0),visible=False)
		s.live_digit0=Entity(model=q,texture=None,scale=.06,position=(s.x+.08,s.y),parent=CU,visible=False)
		s.live_digit1=Entity(model=q,texture=None,scale=.06,position=(s.x+.14,s.y),parent=CU,visible=False)
	def lives_refr(self):
		s=self
		llv=str(st.extra_lives)
		s.visible=True
		s.live_digit0.texture=s.ptl+llv[0]+'.png'
		s.live_digit0.visible=True
		if st.extra_lives > 9:
			s.live_digit1.texture=s.ptl+llv[1]+'.png'
			s.live_digit1.visible=True
	def rmv_ui(self):
		s=self
		s.visible=False
		s.live_digit0.visible=False
		s.live_digit1.visible=False
	def update(self):
		if not st.gproc():
			s=self
			if st.show_lives > 0:
				st.show_lives=max(st.show_lives-time.dt,0)
				if st.show_lives <= 0:
					s.rmv_ui()
					return
				s.lives_refr()


## Bonus Counter ##
class WumpaBonus(Entity):
	def __init__(self):
		s=self
		super().__init__(model=q,texture=w_pa+'0.png',parent=CU,position=(-.2,-.4,0),scale=(.05,.06,0),visible=False)
		s.w_text=Text(text=None,font=_fnt,x=s.x+.04,y=s.y+.025,scale=2,color=color.rgb32(175,235,30),parent=CU,visible=False)
		s.w_time=0
		s.frm=0
	def check_w(self):
		if (st.bonus_solved and st.wumpa_bonus > 0):
			return True
		return False
	def w_count(self):
		s=self
		s.w_time=max(s.w_time-time.dt,0)
		if s.w_time <= 0:
			s.w_time=.1
			WumpaCollectAnim(pos=(-.2,-.4))
			if st.wumpa_bonus > 50:
				st.wumpa_bonus-=10
				cc.wumpa_count(10)
				return
			st.wumpa_bonus-=1
			cc.wumpa_count(1)
	def update(self):
		if not st.gproc():
			s=self
			if st.bonus_round or s.check_w():
				s.w_text.text=f'{st.wumpa_bonus}'
				s.w_text.visible=True
				s.visible=True
				wmp_anim(s)
				if s.check_w() and not st.wait_screen:
					s.w_count()
				return
			destroy(s.w_text)
			destroy(s)

class CrateBonus(Entity):
	def __init__(self):
		s=self
		super().__init__(model=q,texture=None,parent=CU,scale=.07,position=(0,-.4,0),visible=False)
		s.c_text=Text(text=None,font=_fnt,x=s.x+.04,y=s.y+.025,scale=2,color=color.rgb32(90,70,0),visible=False,parent=CU)
		s.c_time=0
		s.icf=0
	def crate_refr_ico(self):
		s=self
		s.icf=min(s.icf+time.dt*30,63.99)
		if s.icf > 63.98:
			s.icf=0
		s.texture=crti+'anim_crt_'+str(int(s.icf))+'.png'
	def check_c(self):
		if (st.bonus_solved and st.crate_bonus > 0):
			return True
		return False
	def c_count(self):
		s=self
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
				s.c_text.text=f'{st.crate_bonus}/{st.crates_in_bonus}'
				s.crate_refr_ico()
				s.c_text.visible=True
				s.visible=True
				if s.check_c() and not st.wait_screen:
					s.c_count()
				return
			destroy(s.c_text)
			destroy(s)

class LiveBonus(Entity):
	def __init__(self):
		s=self
		super().__init__(parent=CU,model=q,texture=_icn+'crash_live.tga',scale=.06,position=(.225,-.4,0),visible=False)
		s.l_text=Text(text=None,font=_fnt,x=s.x+.04,y=s.y+.023,scale=2,color=color.rgb32(255,31,31),visible=False,parent=CU)
		s.l_time=0
	def check_l(self):
		if (st.bonus_solved and st.lives_bonus > 0):
			return True
		return False
	def l_count(self):
		s=self
		s.l_time=max(s.l_time-time.dt,0)
		if s.l_time <= 0:
			s.l_time=.075
			st.lives_bonus-=1
			st.extra_lives+=1
			st.show_lives=1
			sn.ui_audio(ID=0)
	def update(self):
		if not st.gproc():
			s=self
			if s.check_l() or st.bonus_round:
				s.l_text.text=f'{st.lives_bonus}'
				s.l_text.visible=True
				s.visible=True
				if s.check_l() and not st.wait_screen:
					s.l_count()
				return
			destroy(s.l_text)
			destroy(s)


## Game Over Screen
class GameOverScreen(Entity):
	def __init__(self):
		s=self
		super().__init__(model=q,texture='res/background/game_over.jpg',parent=CU,scale=(2,1),z=-.3)
		s.game_o_text=Text(text='GAME OVER!',font=_fnt,color=color.orange,scale=4.5,parent=CU,position=(-.25,.05,-.31))
		s.btn_restart=Text('WARP ROOM',font=_fnt,scale=3,color=color.yellow,position=(s.x-.2,s.y-.1,-.31))
		s.btn_quit=Text('QUIT GAME',font=_fnt,scale=3,color=color.yellow,position=(s.x-.2,s.y-.2,-.31))
		s.rs_col={0:color.white,1:color.yellow}
		s.qt_col={0:color.yellow,1:color.white}
		s.opt_select=0
		sn.GameOverMusic()
	def p_restart(self):
		st.wumpa_fruits=0
		st.extra_lives=4
		st.aku_hit=0
		cc.clear_level(passed=False)
		st.game_over=False
	def input(self,key):
		s=self
		if key in {'w','s','down arrow','up arrow'}:
			sn.ui_audio(ID=0,pit=.125)
			if s.opt_select == 0:
				s.opt_select=1
				return
			s.opt_select=0
		if key == 'enter':
			sn.ui_audio(ID=1)
			opv={0:lambda:s.p_restart(),1:lambda:application.quit()}
			opv[s.opt_select]()
	def update(self):
		s=self
		sbt=s.opt_select
		s.btn_restart.color=s.rs_col[sbt]
		s.btn_quit.color=s.qt_col[sbt]

## Title Screen
btv='res/ui/misc/'
class TitleScreen(Entity):
	def __init__(self):
		super().__init__(model='quad',texture=btv+'title.jpg',scale=(1.8,1),parent=CU)
		self.d_text=Text('fan-game developed by:    blackendless / blackshadow',font=_fnt,scale=2,color=color.green,position=(-.5,.5),parent=CU)
		self.s_text=Text('press start to begin',font=_fnt,scale=3,color=color.orange,position=(-.3,-.25),parent=CU)
		self.blk=.3
	def input(self,key):
		if key in ['enter','space down','escape']:
			sn.ui_audio(ID=1)
			invoke(lambda:warproom.level_select(),delay=.1)
	def update(self):
		s=self
		s.blk=max(s.blk-time.dt,0)
		if s.blk <= 0:
			s.blk=.3
			if s.s_text.color == color.orange:
				s.s_text.color=color.white
				return
			s.s_text.color=color.orange

## Bootscreen
class ProjectInfo(Entity):
	def __init__(self):
		LoadingScreen()
		Audio('res/snd/music/ev/title.mp3',loop=True,volume=settings.MUSIC_VOLUME)
		Entity(model='quad',color=color.black,scale=(4,4),parent=CU)
		super().__init__(model='quad',texture=btv+'disclaim.jpg',scale=(1.6,.8),parent=CU)
		invoke(lambda:TitleScreen(),delay=5)
		destroy(self,delay=5.1)

## Loading Screen
class LoadingScreen(Entity):
	def __init__(self):
		s=self
		super().__init__(model=q,color=color.black,scale=(16,10),visible=False,parent=CU,z=-1,eternal=True)
		s.ltext=Text('LOADING...',font=_fnt,scale=3.5,position=(-.15,.1,-1.1),color=color.orange,visible=False,parent=CU,eternal=True)
		s.lname=Text('',font=_fnt,scale=2,position=(-.25,-.05,-1.1),color=color.azure,visible=False,parent=CU,eternal=True)
		s.uds={0:(-.21),1:(-.23),2:(-.25),3:(-.25),4:(-.25),5:(-.175),6:(-.2)}
	def update(self):
		s=self
		si=st.level_index
		sl=st.loading
		s.lname.text=LC.lv_name[si]
		s.lname.x=s.uds[si]
		s.ltext.visible=(sl)
		s.lname.visible=(sl)
		s.visible=(sl)

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
				destroy(s)

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
					destroy(s)


## Warp Room Interface
class LevelSelector(Entity):
	def __init__(self,idx,pos):
		s=self
		gcsa={1:oi/1.8,2:oi,3:oi*1.4,4:oi,5:oi}
		req_col=color.rgb32(25,25,25)
		super().__init__(position=pos,parent=CU)
		s.lv_crystal=Entity(model=q,texture=cr_i+'0.png',position=(s.x+.945,s.y,s.z),scale=oi,parent=CU,color=req_col)
		s.lv_col_gem=Entity(model=q,texture=LC.fdc[idx]+'0.png',position=(s.x+.8,s.y,s.z),scale=oi,parent=CU,color=req_col)
		s.lv_clr_gem=Entity(model=q,texture=LC.ge_0+'0.png',position=(s.x+1.09,s.y,s.z),scale=oi,parent=CU,color=req_col)
		s.lv_name=Text(LC.lv_name[idx],font=_fnt,position=(s.x,s.y+.04,s.z),scale=2.5,color=color.orange,parent=CU)
		s.bgd=Entity(model=q,texture='res/background/wroom.png',scale=(40,20),position=(0,0,4),color=color.rgb32(140,160,140))
		s.lf0=Entity(model=q,texture=ivy_+'_m.png',scale=.2,position=(-.8,.4,.1),parent=CU)
		s.lf1=Entity(model=q,texture=ivy_+'_m.png',scale=.2,position=(-.8,-.4,.1),rotation_z=-90,parent=CU)
		s.lf2=Entity(model=q,texture=ivy_+'.png',scale=.2,position=(.8,.4,.1),parent=CU)
		s.lf3=Entity(model=q,texture=ivy_+'.png',scale=.2,position=(.8,-.4,.1),rotation_z=90,parent=CU)
		s.lv_col_gem.scale_y=gcsa[idx]
		s.lvID=idx
		for iwb in range(3):
			Entity(model=q,texture=icb,position=(s.lv_col_gem.x+iwb/7,s.y,1),scale=.16,parent=CU,color=color.rgb32(120,140,120))
		if idx in st.CRYSTAL:
			s.lv_crystal.color=color.magenta
		if idx in st.CLEAR_GEM:
			s.lv_clr_gem.color=color.rgb32(180,180,210)
		if idx == 1 and 4 in st.COLOR_GEM:
			s.lv_col_gem.color=LC.GMU[1]
		if idx == 2 and 1 in st.COLOR_GEM:
			s.lv_col_gem.color=LC.GMU[2]
		if idx == 3 and 5 in st.COLOR_GEM:
			s.lv_col_gem.color=LC.GMU[3]
		if idx == 4 and 2 in st.COLOR_GEM:
			s.lv_col_gem.color=LC.GMU[4]
		if idx == 5 and 3 in st.COLOR_GEM:
			s.lv_col_gem.color=LC.GMU[5]
		s.frm=0
		del gcsa,idx,pos,req_col
	def refr(self):
		s=self
		s.frm=min(s.frm+time.dt*30,89.999)
		if s.frm > 89.99:
			s.frm=0
		kg=f'{int(s.frm)}.png'
		s.lv_crystal.texture=cr_i+kg
		s.lv_col_gem.texture=LC.fdc[s.lvID]+kg
		s.lv_clr_gem.texture=LC.ge_0+kg
	def update(self):
		s=self
		s.refr()
		if st.selected_level == s.lvID:
			s.lv_name.color=color.white
			return
		s.lv_name.color=color.orange

class SpecialLevelSelector(Entity):
	def __init__(self,idx,pos):
		s=self
		req_col=color.rgb32(25,25,25)
		super().__init__(position=pos,parent=CU)
		s.lv_name=Text(LC.lv_name[idx],font=_fnt,position=(s.x,s.y+.04,s.z),scale=2.5,color=color.orange,parent=CU)
		s.bgd=Entity(model='cube',texture='res/background/wroom.png',scale=(40,10,1),position=(0,-5,4),color=color.rgb32(130,130,160))
		s.lf0=Entity(model=q,texture=ivy_+'_m.png',scale=.2,position=(-.8,-.4,.1),rotation_z=-90,parent=CU)
		s.lf1=Entity(model=q,texture=ivy_+'.png',scale=.2,position=(.8,-.4,.1),rotation_z=90,parent=CU)
		s.lv_clr_gem0=Entity(model=q,texture=LC.ge_0+'0.png',position=(s.x+.8,s.y,s.z),scale=oi,parent=CU,color=req_col)
		s.lv_clr_gem1=Entity(model=q,texture=LC.ge_0+'0.png',position=(s.x+.945,s.y,s.z),scale=oi,parent=CU,color=req_col)
		s.lvID=idx
		for iwb in range(2):
			Entity(model=q,texture=icb,position=(s.lv_clr_gem0.x+iwb/7,s.y,1),scale=.16,parent=CU,color=color.rgb32(120,120,150))
		s.frm=0
		mbg=color.rgb32(180,180,210)
		if idx in st.COLOR_GEM:
			s.lv_clr_gem0.color=mbg
		if idx in st.CLEAR_GEM:
			s.lv_clr_gem1.color=mbg
		del mbg,idx,pos,iwb
	def refr(self):
		s=self
		s.frm=min(s.frm+time.dt*30,89.999)
		if s.frm > 89.99:
			s.frm=0
		kg=f'{int(s.frm)}.png'
		s.lv_clr_gem0.texture=LC.ge_0+kg
		s.lv_clr_gem1.texture=LC.ge_0+kg
	def update(self):
		s=self
		s.refr()
		if st.selected_level == s.lvID:
			s.lv_name.color=color.white
			return
		s.lv_name.color=color.orange


## Bonusround Text
class BonusText(Entity):
	def __init__(self):
		self.bntx=btxt+'bonus_'
		super().__init__(model=q,texture=None,parent=CU,scale=(.3,.1),position=(0,.35),visible=False)
		self.ch_seq=0
		self.t_delay=.5
	def display(self):
		s=self
		s.texture=s.bntx+str(s.ch_seq)+'.tga'
		s.visible=True
	def text_ch(self):
		s=self
		s.visible=False
		if s.ch_seq == 7:
			s.ch_seq=0
			return
		s.ch_seq+=1
	def update(self):
		if not st.gproc() and not st.wait_screen:
			s=self
			if not st.bonus_round:
				destroy(s)
				return
			s.t_delay=max(s.t_delay-time.dt,0)
			if s.t_delay <= 0:
				s.t_delay=.5
				if not s.visible:
					s.display()
					return
				s.text_ch()

K=40
O=180
## Pause Menu
class PauseMenu(Entity):
	def __init__(self):
		s=self
		super().__init__(parent=CU,model=q,texture=e+'c_pause1.png',scale=(1.05,.5),position=(-.375,-.25,.1),color=color.rgb32(130,140,130),visible=False)
		s.ppt=Entity(parent=CU,model=q,texture=e+'c_pause2.png',scale=(.75,1),position=(.515,0,.1),color=color.rgb32(130,140,130),visible=False)
		##text
		s.selection=['RESUME','OPTIONS','QUIT']
		s.font_color=color.rgb32(230,100,0)
		s.blink_time=0
		s.choose=0
		vF=0
		s.p_name=Text('Crash B.',font=_fnt,scale=3,position=(vF+.4,vF+.475,s.z-1),color=s.font_color,parent=CU,visible=False)
		s.lvl_name=Text(LC.lv_name[st.level_index],font=_fnt,scale=3,position=(vF-.7,vF-.025,s.z-1),color=color.azure,parent=CU,visible=False)
		s.select_0=Text(s.selection[0],font=_fnt,scale=3,tag=0,position=(vF-.5,vF-.2,s.z-1),color=s.font_color,parent=CU,visible=False)
		s.select_1=Text(s.selection[1],font=_fnt,scale=3,tag=1,position=(vF-.5,vF-.275,s.z-1),color=s.font_color,parent=CU,visible=False)
		s.select_2=Text(s.selection[2],font=_fnt,scale=3,tag=2,position=(vF-.5,vF-.35,s.z-1),color=s.font_color,parent=CU,visible=False)
		s.crystal_counter=Text('0/5',font=_fnt,scale=6,position=(vF+.325,vF+.325,s.z-1),color=color.rgb32(160,0,160),parent=CU,visible=False)
		s.gem_counter=Text('0/16 GEMS',font=_fnt,scale=5,position=(vF+.3,vF-.1,s.z-1),color=color.rgb32(170,170,190),parent=CU,visible=False)
		s.add_text=Text('+ 0',font=_fnt,scale=4,position=(vF+.325,vF+.025,vF-1),color=s.font_color,parent=CU,visible=False)
		s.game_progress=Text('Progress 0%',font=_fnt,scale=3,position=(vF+.325,vF-.35,s.z-1),color=color.gold,parent=CU,visible=False)
		##animation
		ric='res/ui/icon/'
		s.cry_anim=Entity(model=q,texture=cr_i+'0.png',position=(vF+.6,vF+.26,s.z-1),scale=.15,parent=CU,color=color.magenta,visible=False)
		s.col_gem1=Entity(model=q,texture=LC.ge_0+'0.png',name='1',position=(vF+.25,vF+.075,s.z-1),scale=.15,parent=CU,color=color.rgb32(K,K,K),visible=False)
		s.col_gem2=Entity(model=q,texture=LC.ge_0+'0.png',name='2',position=(vF+.37,vF+.075,s.z-1),scale=.15,parent=CU,color=color.rgb32(K,K,K),visible=False)
		s.col_gem3=Entity(model=q,texture=LC.ge_0+'0.png',name='3',position=(vF+.49,vF+.075,s.z-1),scale=.15,parent=CU,color=color.rgb32(K,K,K),visible=False)
		s.col_gem4=Entity(model=q,texture=LC.ge_1+'0.png',name='4',position=(vF+.61,vF+.075,s.z-1),scale=(.15,.075),parent=CU,color=color.rgb32(K,K,K),visible=False)
		s.col_gem5=Entity(model=q,texture=LC.ge_2+'0.png',name='5',position=(vF+.73,vF+.075,s.z-1),scale=(.15,.19),parent=CU,color=color.rgb32(K,K,K),visible=False)
		s.cleargem=Entity(model=q,texture=LC.ge_0+'0.png',position=(vF+.55,vF-.03,s.z-1),scale=.16,parent=CU,color=color.rgb32(130,130,190),visible=False)
		##options
		s.music_vol=Text('SOUND VOLUME '+str(settings.SFX_VOLUME*10),tag=0,font=_fnt,scale=3,color=s.font_color,parent=CU,position=(vF-.7,vF-.2,s.z-1),visible=False)
		s.sound_vol=Text('MUSIC VOLUME '+str(settings.MUSIC_VOLUME*10),tag=1,font=_fnt,scale=3,color=s.font_color,parent=CU,position=(vF-.7,vF-.275,s.z-1),visible=False)
		s.opt_exit=Text('PRESS ENTER TO EXIT',tag=3,font=_fnt,scale=2.5,color=color.yellow,parent=CU,position=(vF-.75,vF-.4,s.z-1),visible=False)
		s.check_collected()
		s.opt_menu=False
		s.sel_opt=0
		s.frm=0
		LC.p_menu=self
	def input(self,key):
		s=self
		if not st.pause:
			del key
			return
		if not s.opt_menu:
			if key in {'down arrow','s'}:
				sn.ui_audio(ID=0,pit=.125)
				if s.choose < 2:
					s.choose+=1
				del key
				return
			elif key in ['up arrow','w']:
				sn.ui_audio(ID=0,pit=.125)
				if s.choose > 0:
					s.choose-=1
					del key
				return
			if key == 'enter':
				sn.ui_audio(ID=1)
				if s.choose == 0:
					cc.game_pause()
					del key
					return
				if s.choose == 1:
					s.music_vol.visible=True
					s.sound_vol.visible=True
					s.opt_exit.visible=True
					s.select_0.visible=False
					s.select_1.visible=False
					s.select_2.visible=False
					s.opt_menu=True
				if s.choose == 2:
					if not st.LEVEL_CLEAN:
						cc.clear_level(passed=False)
			del key
			return
		if key in ['w','s','down arrow','up arrow']:
			if s.sel_opt == 0:
				s.sel_opt=1
			else:
				s.sel_opt=0
		if key in ['+','d','right arrow']:
			if s.sel_opt == 1:
				if settings.SFX_VOLUME < 1:
					settings.SFX_VOLUME+=.1
					if settings.SFX_VOLUME > 1:
						settings.SFX_VOLUME=1
			elif s.sel_opt == 0:
				if settings.MUSIC_VOLUME < 1:
					settings.MUSIC_VOLUME+=.1
					if settings.MUSIC_VOLUME > 1:
						settings.MUSIC_VOLUME=1
			sn.ui_audio(ID=1)
		if key in ['-','a','left arrow']:
			if s.sel_opt == 1:
				if settings.SFX_VOLUME > .1:
					settings.SFX_VOLUME-=.1
			elif s.sel_opt == 0:
				if settings.MUSIC_VOLUME > .1:
					settings.MUSIC_VOLUME-=.1
			sn.ui_audio(ID=1)
		if key == 'enter':
			s.opt_menu=False
			s.music_vol.visible=False
			s.sound_vol.visible=False
			s.opt_exit.visible=False
			s.select_0.visible=True
			s.select_1.visible=True
			s.select_2.visible=True
		del key
	def check_collected(self):
		s=self
		gems_total=st.color_gems+st.clear_gems
		s.gem_counter.text=str(gems_total)+'/16 GEMS'
		s.crystal_counter.text=str(st.collected_crystals)+'/5'
		s.game_progress.text='Progress '+str(st.color_gems*6+st.clear_gems*5+st.collected_crystals*6)+'%'
		s.add_text.text='+ '+str(st.clear_gems)
		for qc in {s.col_gem1,s.col_gem2,s.col_gem3,s.col_gem3,s.col_gem4,s.col_gem5}:
			if int(qc.name) in st.COLOR_GEM:
				qc.color=LC.GMC[int(qc.name)]
	def select_menu(self):
		s=self
		for mn in [s.select_0,s.select_1,s.select_2]:
			if s.choose == mn.tag:
				text_blink(M=s,t=mn)
			else:
				mn.color=s.font_color
	def select_option(self):
		s=self
		for ot in [s.music_vol,s.sound_vol]:
			if s.sel_opt == ot.tag:
				text_blink(M=s,t=ot)
			else:
				ot.color=s.font_color
	def refr_ico(self):
		s=self
		s.frm=min(s.frm+time.dt*30,89.999)
		if s.frm > 89.99:
			s.frm=0
		kw=f'{int(s.frm)}.png'
		s.cry_anim.texture=cr_i+kw
		s.cleargem.texture=LC.ge_0+kw
		s.col_gem1.texture=LC.ge_0+kw
		s.col_gem2.texture=LC.ge_1+kw
		s.col_gem3.texture=LC.ge_2+kw
		s.col_gem4.texture=LC.ge_0+kw
		s.col_gem5.texture=LC.ge_0+kw
	def update(self):
		s=self
		if st.pause:
			s.refr_ico()
			s.music_vol.text=f'MUSIC VOLUME {int(settings.MUSIC_VOLUME*100)}%'
			s.sound_vol.text=f'SOUND VOLUME {int(settings.SFX_VOLUME*100)}%'
			s.blink_time=max(s.blink_time-time.dt,0)
			if s.blink_time <= 0:
				opv={True:lambda:s.select_option(),False:lambda:s.select_menu()}
				opv[s.opt_menu]()
			return
		s.opt_menu=False

## Gem/Crytal
class CollectedGem(Entity):
	def __init__(self):
		s=self
		idx=st.level_index
		super().__init__(position=(0,0),parent=CU,scale=.14)
		s.crystal=Entity(model=q,texture=cr_i+'0.png',scale=s.scale,position=(s.x,s.y-.4),color=color.rgb32(200,0,200),visible=False,parent=CU)
		s.clear_gem=Entity(model=q,texture=LC.ge_0+'0.png',position=(s.x-.1,s.y-.4),scale=s.scale,color=LC.cglr,visible=False,parent=CU)
		s.color_gem=Entity(model=q,texture=LC.fdc[idx]+'0.png',position=(s.x+.1,s.y-.4),scale=s.scale,color=LC.GMU[idx],visible=False,parent=CU)
		if idx == 3:
			s.color_gem.scale_y=.2
		if idx == 1:
			s.color_gem.scale_y=.07
		s.cry_frm=0
		del idx
	def refr_frm(self):
		s=self
		s.cry_frm=min(s.cry_frm+time.dt*40,89.999)
		if s.cry_frm > 89.99:
			s.cry_frm=0
		fm=f'{int(s.cry_frm)}.png'
		if s.crystal.visible:
			s.crystal.texture=cr_i+fm
		if s.clear_gem.visible:
			s.clear_gem.texture=LC.ge_0+fm
		if s.color_gem.visible:
			s.color_gem.texture=LC.fdc[st.level_index]+fm
	def update(self):
		if st.gproc():
			return
		s=self
		if st.show_gems > 0:
			st.show_gems=max(st.show_gems-time.dt,0)
			s.crystal.visible=(st.level_crystal)
			s.clear_gem.visible=(st.level_cle_gem)
			s.color_gem.visible=(st.level_col_gem)
			s.refr_frm()
			return
		s.color_gem.visible=False
		s.clear_gem.visible=False
		s.crystal.visible=False
		s.crystal.texture=None
		s.color_gem.texture=None
		s.clear_gem.texture=None

## Gem Hint
class GemHint(Entity):
	def __init__(self):
		s=self
		super().__init__()
		s.mText=Text(LC.ge_inf[st.level_index],parent=camera.ui,font=_fnt,color=color.orange,scale=2.2,position=(-.6,-.3,.1))
		s.tm=5
	def update(self):
		s=self
		s.mText.visible=not(st.gproc())
		if s.visible:
			s.tm=max(s.tm-time.dt,0)
			if s.tm <= 0:
				destroy(s.mText)
				destroy(s)

## Checkpoint Letters
class CheckpointLetter(Entity):
	def __init__(self,pos):
		s=self
		super().__init__()
		s.ckt=Text(None,font=_fnt,position=(pos[0],pos[1]+.4,pos[2]),scale=7,parent=scene,color=color.orange,unlit=False)
		s.rev=False
		s.tm=.075
		s.idx=0
		del pos
	def purge(self):
		destroy(self.ckt)
		destroy(self)
	def update(self):
		if st.gproc():
			return
		s=self
		s.tm=max(s.tm-time.dt,0)
		if s.tm <= 0:
			s.tm=.075
			s.ckt.text={False:LC.checkp[:s.idx],True:LC.checkp[-s.idx+1:]}[s.rev]
			if s.rev:
				sn.pc_audio(ID=1,pit=.9)
				s.ckt.x+=time.dt*4.4
				s.idx-=1
				if s.idx <= 0:
					s.purge()
				return
			if s.idx >= len(LC.checkp):
				s.tm=.3
				s.rev=True
				return
			s.idx+=1

## Time Trial
class TrialTimer(Entity):
	def __init__(self,t):
		s=self
		tm_str=strftime('%M:%S',gmtime(t))
		super().__init__()
		s.disp=Text(tm_str,font=_fnt,scale=3,position=(.7,-.4),parent=CU,color=color.rgb32(200,200,100))
		s.fin=False
		s.TME=t
	def trial_fail(self):
		if st.level_index == 3:
			st.gem_death=True
		self.trial_interrupt()
	def trial_interrupt(self):
		destroy(self.disp)
		destroy(self)
	def update(self):
		if not st.gproc():
			s=self
			if (st.level_index == 3 and st.level_col_gem):
				s.trial_interrupt()
				return
			s.disp.text=strftime("%M:%S",gmtime(s.TME))
			s.TME=max(s.TME-time.dt,0)
			if (s.TME <= 0 or st.bonus_round):
				if not s.fin:
					s.fin=True
					s.trial_fail()

class CreditText(Entity):
	def __init__(self,t,d):
		s=self
		super().__init__()
		s.ctext=Text(t,font=_fnt,scale=2.5,parent=CU,color=color.orange,position=(-.7,-.6,-.1))
		s.wait=True
		invoke(lambda:setattr(s,'wait',False),delay=d/2)
	def update(self):
		s=self
		if not s.wait:
			s.ctext.y+=time.dt/10