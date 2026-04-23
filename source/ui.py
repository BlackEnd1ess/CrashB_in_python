from ursina import Entity,Audio,Text,camera,color,scene,invoke,lerp,distance,curve
import status,_core,_loc,sound,settings,warproom,level,time,random
from objects import ObjType_Background,ObjType_Deco
from ursina.ursinastuff import destroy
from time import strftime,gmtime

cr_i='res/ui/icon/crystal/'
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

CU=camera.ui
st=status
sn=sound
cc=_core
LC=_loc

def load_interface():
	PauseMenu()
	WumpaCounter()
	BoxCounter()
	LiveCounter()
	UICrystal((0,-.4,0),2,st.level_index)
	UINormalGem((-.07,-.41,0),2,st.level_index)
	UIColorGem((.07,-.41,0),2,st.level_index)
	UIRelic((.16,-.4125,0),2,2)

## Interface 2D Animations
def wmp_anim(w):
	cc.incr_frm(w,w.spd)
	if w.texture != LC.wmp_texture[int(w.frm)]:
		w.texture=LC.wmp_texture[int(w.frm)]

class LiveCollectAnim(Entity):
	def __init__(self):
		super().__init__(model=q,texture=f'{_icn}crash_live.png',position=(.5,.43,0),scale=(.1,.09),color=color.gold,parent=CU)
	def update(self):
		if st.gproc():
			return
		s=self
		if s.x < .65:
			s.x+=time.dt*2
			return
		destroy(s)

class WumpaCollectAnim(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=q,texture=f'{w_pa}0.png',scale={False:.075,True:.06}[st.bonus_round],parent=CU,position=pos)
		s.tdirec=(-.75,.43,0)
		if st.bonus_round:
			s.tdirec=(-.25,-.475,0)
		del pos,s
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
		s.max_frm=len(LC.wmp_texture)-1+.99
		s.spd=18
		s.frm=0
	def digits(self):
		s=self
		n=f'{st.wumpa_fruits}'
		s.digit_0.texture=f'{wmpf}{n[0]}.png'
		s.digit_0.visible=True
		s.visible=True
		if st.wumpa_fruits >= 10:
			s.digit_1.visible=True
			s.digit_1.texture=f'{wmpf}{n[1]}.png'
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

class BoxCounter(Entity):
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
		s.max_frm=len(LC.box_texture)-1+.99
		s.spd=30
		s.frm=0
		del s
	def crate_refr_ico(self):
		s=self
		cc.incr_frm(s,s.spd)
		s.texture=LC.box_texture[int(s.frm)]
	def remv_ui(self):
		s=self
		s.visible,s.seperator.visible=False,False
		s.col_digit0.visible,s.col_digit1.visible,s.col_digit2.visible=False,False,False
		s.req_digit0.visible,s.req_digit1.visible,s.req_digit2.visible=False,False,False
		del s
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
		super().__init__(parent=CU,model=q,texture=f'{_icn}crash_live.png',scale=(.1,.09),position=(.65,.43,0),visible=False)
		s.live_digit0=Entity(model=q,texture=None,scale=.06,position=(s.x+.08,s.y),parent=CU,visible=False)
		s.live_digit1=Entity(model=q,texture=None,scale=.06,position=(s.x+.14,s.y),parent=CU,visible=False)
	def lives_refr(self):
		s=self
		s.visible=True
		vd=str(st.extra_lives)
		s.live_digit0.texture=f'{s.ptl}{vd[0]}.png'
		s.live_digit0.visible=True
		if st.extra_lives > 9:
			s.live_digit1.texture=f'{s.ptl}{vd[1]}.png'
			s.live_digit1.visible=True
	def rmv_ui(self):
		s=self
		s.visible=False
		s.live_digit0.visible=False
		s.live_digit1.visible=False
	def update(self):
		if st.gproc():
			return
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
		super().__init__(model=q,texture=LC.wmp_texture[0],parent=CU,position=(-.2,-.4,0),scale=(.05,.06,0),visible=False)
		s.w_text=Text(text=None,font=_fnt,x=s.x+.04,y=s.y+.025,scale=2,color=color.rgb32(175,235,30),parent=CU,visible=False)
		s.max_frm=len(LC.wmp_texture)-1+.99
		s.w_time=0
		s.spd=18
		s.frm=0
		del s
	def check_w(self):
		return bool(st.bonus_solved and st.wumpa_bonus > 0)
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

class BoxBonus(Entity):
	def __init__(self):
		s=self
		super().__init__(model=q,texture=None,parent=CU,scale=.07,position=(0,-.4,0),visible=False)
		s.c_text=Text(text=None,font=_fnt,x=s.x+.04,y=s.y+.025,scale=2,color=color.rgb32(90,70,0),visible=False,parent=CU)
		s.max_frm=len(LC.box_texture)-1+.99
		s.c_time=0
		s.spd=30
		s.frm=0
		del s
	def crate_refr_ico(self):
		s=self
		cc.incr_frm(s,s.spd)
		s.texture=LC.box_texture[int(s.frm)]
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
		super().__init__(parent=CU,model=q,texture=f'{_icn}crash_live.png',scale=.06,position=(.225,-.4,0),visible=False)
		s.l_text=Text(text=None,font=_fnt,x=s.x+.04,y=s.y+.023,scale=2,color=color.rgb32(255,31,31),visible=False,parent=CU)
		s.l_time=0
		del s
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
		del s
	def p_restart(self):
		st.wumpa_fruits=0
		st.extra_lives=4
		st.aku_hit=0
		cc.clear_level(passed=False)
		st.game_over=False
	def input(self,key):
		s=self
		if key in ('w','s','down arrow','up arrow'):
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
		if key in ('enter','space down','escape'):
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
		Audio('res/music/title.mp3',loop=True,volume=settings.MUSIC_VOLUME)
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
		s.uds={0:(-.21),1:(-.23),2:(-.25),3:(-.25),4:(-.25),5:(-.175),6:(-.23),7:(-.225),8:(-.225),9:(-.2)}
		del s
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

#######################################################################
## warp room interface UI
def set_warproom_scene(n):
	ivy_sc=.2
	Entity(model=q,texture=f'{ivy_}_m.png',scale=ivy_sc,position=(-.8,.4,.1),parent=CU)
	Entity(model=q,texture=f'{ivy_}_m.png',scale=ivy_sc,position=(-.8,-.4,.1),rotation_z=-90,parent=CU)
	Entity(model=q,texture=f'{ivy_}.png',scale=ivy_sc,position=(.8,.4,.1),parent=CU)
	Entity(model=q,texture=f'{ivy_}.png',scale=ivy_sc,position=(.8,-.4,.1),rotation_z=90,parent=CU)
	if n == 0:
		ObjType_Background(ID=0,sca=(40,20),pos=(0,0,4),col=color.rgb32(140,160,140),txa=(1,1))
		return
	Entity(model='sphere',texture='res/terrain/grass_flat.png',scale=(16,5,8),texture_scale=(4,4),position=(10,-8,2),color=color.green)
	ObjType_Background(ID=2,sca=(38,24),pos=(0,0,5),col=color.rgb32(0,80,80),txa=(1,1),UL=True)
	ObjType_Deco(ID=1,pos=(7,-3.6,2),sca=.06,rot=(-90,0,0))

class LevelSelector(Entity):
	def __init__(self,idx,pos):
		s=self
		super().__init__(position=pos,parent=CU)
		s.lv_name=Text(LC.lv_name[idx],font=_fnt,position=(s.x,s.y+.04,s.z),scale=2.5,color=color.orange,parent=CU)
		s.lvID=idx
		for iwb in range(4):
			Entity(model=q,texture=icb,position=(s.lv_name.x+.75+iwb/7,s.y,1),scale=.16,parent=CU,color=color.rgb32(100,110,100))
		if idx in st.CRYSTAL:
			UICrystal((s.lv_name.x+.895,s.lv_name.y-.035,0),0,idx)
		if idx in st.CLEAR_GEM:
			UINormalGem((s.lv_name.x+1.04,s.lv_name.y-.0375,0),0,idx)
		if idx in st.COLOR_GEM:#set gem levelID
			UIColorGem((s.lv_name.x+.75,s.lv_name.y-.0375,0),0,idx)
		for lpr in st.RELIC:
			if idx == lpr[0]:
				UIRelic((s.lv_name.x+1.18,s.lv_name.y-.0375,0),0,lpr[1])
		del idx,pos,iwb
	def update(self):
		s=self
		if st.selected_level == s.lvID:
			s.lv_name.color=color.white
			return
		s.lv_name.color=color.orange

class SpecialLevelSelector(Entity):
	def __init__(self,idx,pos):
		s=self
		super().__init__(position=pos,parent=CU)
		s.lv_name=Text(LC.lv_name[idx],font=_fnt,position=(s.x,s.y+.04,s.z),scale=2.5,color=color.orange,parent=CU)
		s.lvID=idx
		for iwb in range(3):
			Entity(model=q,texture=icb,position=(s.lv_name.x+.75+iwb/7,s.y,1),scale=.16,parent=CU,color=color.rgb32(120,120,150))
		if idx in st.CLEAR_GEM:
			UINormalGem((s.lv_name.x+.75,s.lv_name.y-.0375,0),0,idx)
		if idx > 5 and idx in st.COLOR_GEM:
			UINormalGem((s.lv_name.x+.895,s.lv_name.y-.0375,0),0,idx)
		for lpr in st.RELIC:
			if idx == lpr[0]:
				UIRelic((s.lv_name.x+1.04,s.lv_name.y-.0375,0),0,lpr[1])
		del idx,pos,iwb
	def update(self):
		self.lv_name.color=color.white if (st.selected_level == self.lvID) else color.orange

##crystal, gem and relic interface
class UICrystal(Entity):
	def __init__(self,pos,typ,idx):
		s=self
		super().__init__(model=q,texture=LC.crystal_texture[0],position=pos,parent=CU,color=LC.ui_crystal_color,visible=bool(typ != 2))
		{0:lambda:setattr(s,'scale',.13),1:lambda:setattr(s,'scale',.18),2:lambda:setattr(s,'scale',.14)}[typ]()
		s.max_frm=len(LC.crystal_texture)-1
		s.index=idx
		s.typ=typ
		s.spd=13
		s.frm=0
		del pos,idx,s,typ
	def refr_frm(self):
		s=self
		cc.incr_frm(s,s.spd)
		if s.texture != LC.crystal_texture[int(s.frm)]:
			s.texture=LC.crystal_texture[int(s.frm)]
	def update(self):
		if st.LEVEL_CLEAN or st.loading:
			return
		s=self
		if s.typ > 0:
			s.visible=(s.typ == 1 and st.pause) or (s.typ == 2 and st.level_crystal and st.show_gems > 0)
		if s.visible:
			s.refr_frm()

class UINormalGem(Entity):
	def __init__(self,pos,typ,idx):
		s=self
		super().__init__(model=q,texture=LC.normal_gem_texture[0],position=pos,parent=CU,color=LC.ui_normal_gem_color,visible=bool(typ != 2))
		{0:lambda:setattr(s,'scale',.11),1:lambda:setattr(s,'scale',.16),2:lambda:setattr(s,'scale',.12)}[typ]()
		s.max_frm=len(LC.normal_gem_texture)-1
		s.index=idx
		s.typ=typ
		s.spd=20
		s.frm=0
		del pos,idx,s,typ
	def refr_frm(self):
		s=self
		cc.incr_frm(s,s.spd)
		if s.texture != LC.normal_gem_texture[int(s.frm)]:
			s.texture=LC.normal_gem_texture[int(s.frm)]
	def update(self):
		if st.LEVEL_CLEAN or st.loading:
			return
		s=self
		if s.typ > 0:
			s.visible=(s.typ == 1 and st.pause) or (s.typ == 2 and st.level_cle_gem and st.show_gems > 0)
		if s.visible:
			s.refr_frm()

GEM_COLOR={1:LC.ui_blue_gem_color,2:LC.ui_red_gem_color,3:LC.ui_yellow_gem_color,4:LC.ui_green_gem_color,5:LC.ui_purple_gem_color}
GEM_SCALE_Y={1:.06,3:.18}
class UIColorGem(Entity):
	def __init__(self,pos,typ,idx):
		s=self
		GSC=.01 if (typ == 1) else .12
		super().__init__(model=q,position=pos,parent=CU,scale=GSC,color=LC.ui_normal_gem_color,visible=(typ != 2))
		if idx in (4,5):
			s.max_frm=len(LC.green_gem_texture)-1 if idx == 4 else len(LC.purple_gem_texture)-1
		else:
			s.max_frm=len(LC.normal_gem_texture)-1
		s.scale_anim_done=False
		s.gem_scale_mode=0
		s.gem_anim_wait=0
		s.index=idx
		s.typ=typ
		s.spd=20
		s.frm=0
		del pos,idx,s,typ,GSC
	def refr_scale(self):
		s=self
		if s.typ == 1 and not s.index in st.COLOR_GEM:
			s.gem_scale_animation()
			return
		if s.scale_x != .12:
			s.scale_x=.12
		if s.index in GEM_SCALE_Y:
			if s.scale_y != GEM_SCALE_Y[s.index]:
				s.scale_y=GEM_SCALE_Y[s.index]
			return
		if s.scale_y != .12:
			s.scale_y=.12
	def gem_scale_animation(self):
		s=self
		if st.ui_gem_anim_index in st.COLOR_GEM:
			rmi=random.randint(1,5)
			if st.ui_gem_anim_index != rmi:
				st.ui_gem_anim_index=rmi
			return
		if s.index != st.ui_gem_anim_index:
			return
		if s.scale_anim_done:
			s.gem_anim_wait-=time.dt
			if s.gem_anim_wait <= 0:
				s.scale_anim_done=False
				st.ui_gem_anim_index=random.randint(1,5)
			return
		tg=time.dt
		if s.gem_scale_mode == 0:
			target_size=(.12,GEM_SCALE_Y[s.index],.12) if (s.index in GEM_SCALE_Y) else (.12,.12,.12)
			s.scale=min(s.scale+(tg,tg,tg),target_size)
			if s.scale >= target_size:
				s.gem_scale_mode=1
			return
		target_size=(.01,.01,.01)
		s.scale=max(s.scale-(tg,tg,tg),target_size)
		if s.scale <= target_size:
			if not s.scale_anim_done:
				s.scale_anim_done=True
				s.gem_anim_wait=2
				s.gem_scale_mode=0
	def refr_color(self):
		s=self
		if s.index in GEM_COLOR:
			if s.color != GEM_COLOR[s.index]:
				s.color=GEM_COLOR[s.index]
			return
		if s.color != LC.ui_normal_gem_color:
			s.color=LC.ui_normal_gem_color
	def refr_frm(self):
		s=self
		cc.incr_frm(s,s.spd)
		if s.index == 4:
			if s.texture != LC.green_gem_texture[int(s.frm)]:
				s.texture=LC.green_gem_texture[int(s.frm)]
			return
		if s.index == 5:
			if s.texture != LC.purple_gem_texture[int(s.frm)]:
				s.texture=LC.purple_gem_texture[int(s.frm)]
			return
		if s.texture != LC.normal_gem_texture[int(s.frm)]:
			s.texture=LC.normal_gem_texture[int(s.frm)]
	def update(self):
		if st.LEVEL_CLEAN or st.loading:
			return
		s=self
		if s.typ == 1:
			s.visible=st.pause
		if s.typ == 2:
			s.index=st.color_gem_id
			s.visible=(st.level_col_gem and st.show_gems > 0)
		if s.visible:
			s.refr_color()
			s.refr_scale()
			s.refr_frm()

class UIRelic(Entity):
	def __init__(self,pos,typ,idx):
		s=self
		super().__init__(model=q,texture=LC.relic_texture[0],color=LC.relic_color[idx],position=pos,parent=CU)
		s.scale=.14 if (typ != 1) else .12
		s.max_frm=len(LC.relic_texture)-1
		s.index=idx
		s.typ=typ
		s.spd=12
		s.frm=0
		del pos,idx,s
	def refr_frm(self):
		s=self
		cc.incr_frm(s,s.spd)
		s.texture=LC.relic_texture[int(s.frm)]
	def refr_func(self):
		s=self
		if s.typ == 1:
			s.visible=st.pause
			return
		if s.typ == 2:
			s.color=LC.relic_color[st.relic_rank]
			s.visible=(st.RELIC_TRIAL_DONE and st.show_gems > 0)
	def update(self):
		s=self
		s.refr_func()
		if s.visible:
			s.refr_frm()

#######################################################################################
#######################################################################################
K=50
O=200
vF=0
## Pause Menu
class PauseMenu(Entity):
	def __init__(self):
		s=self
		super().__init__(parent=CU,model=q,texture=f'{e}c_pause1.png',scale=(1.05,.5),position=(-.375,-.25,.1),color=color.rgb32(130,140,130),visible=False)
		s.ppt=Entity(parent=CU,model=q,texture=f'{e}c_pause2.png',scale=(.75,1),position=(.515,0,.1),color=color.rgb32(130,140,130),visible=False)
		##text
		s.font_color=color.rgb32(230,100,0)
		s.blink_time=0
		s.choose=0
		s.p_name=Text('Crash B.',font=_fnt,scale=3,position=(vF+.4,vF+.475,s.z-1),color=s.font_color,parent=CU,visible=False)
		s.lvl_name=Text(LC.lv_name[st.level_index],font=_fnt,scale=3,position=(vF-.7,vF-.025,s.z-1),color=color.azure,parent=CU,visible=False)
		s.select_0=Text('RESUME',font=_fnt,scale=3,tag=0,position=(vF-.5,vF-.2,s.z-1),color=s.font_color,parent=CU,visible=False)
		s.select_1=Text('OPTIONS',font=_fnt,scale=3,tag=1,position=(vF-.5,vF-.275,s.z-1),color=s.font_color,parent=CU,visible=False)
		s.select_2=Text('QUIT',font=_fnt,scale=3,tag=2,position=(vF-.5,vF-.35,s.z-1),color=s.font_color,parent=CU,visible=False)
		s.crystal_counter=Text('0/5',font=_fnt,scale=6,position=(vF+.325,vF+.325,s.z-1),color=color.rgb32(160,0,160),parent=CU,visible=False)
		s.relic_counter=Text('0/8',font=_fnt,scale=3,position=(vF+.6,vF+.01,s.z-1),color=color.azure,parent=CU,visible=False)
		s.gem_counter=Text('0/16 GEMS',font=_fnt,scale=5,position=(vF+.3,vF-.1,s.z-1),color=color.rgb32(170,170,190),parent=CU,visible=False)
		s.add_text=Text('+ 0',font=_fnt,scale=4,position=(vF+.2,vF+.025,vF-1),color=s.font_color,parent=CU,visible=False)
		s.game_progress=Text('Progress 0%',font=_fnt,scale=3,position=(vF+.325,vF-.35,s.z-1),color=color.gold,parent=CU,visible=False)
		##options
		s.music_vol=Text(f'SOUND VOLUME {settings.SFX_VOLUME*10}',tag=0,font=_fnt,scale=3,color=s.font_color,parent=CU,position=(vF-.7,vF-.2,s.z-1),visible=False)
		s.sound_vol=Text(f'MUSIC VOLUME {settings.MUSIC_VOLUME*10}',tag=1,font=_fnt,scale=3,color=s.font_color,parent=CU,position=(vF-.7,vF-.275,s.z-1),visible=False)
		s.opt_exit=Text('PRESS ENTER TO EXIT',tag=3,font=_fnt,scale=2.5,color=color.yellow,parent=CU,position=(vF-.75,vF-.4,s.z-1),visible=False)
		s.opt_menu=False
		s.sel_opt=0
		##gem animation
		UICrystal((s.crystal_counter.x+.24,s.crystal_counter.y-.06,s.crystal_counter.z),1,st.level_index)
		UIRelic((s.relic_counter.x+.14,s.relic_counter.y-.035,s.relic_counter.z),1,2)
		UINormalGem((s.add_text.x+.2,s.add_text.y-.05,s.add_text.z),1,st.level_index)
		UIColorGem((s.add_text.x-.05+.105,s.add_text.y+.065,s.add_text.z),1,2)#red
		UIColorGem((s.add_text.x-.05+.21,s.add_text.y+.04,s.add_text.z),1,4)#green
		UIColorGem((s.add_text.x-.05+.315,s.add_text.y+.065,s.add_text.z),1,5)#purple
		UIColorGem((s.add_text.x-.05+.42,s.add_text.y+.04,s.add_text.z),1,1)#blue
		UIColorGem((s.add_text.x-.05+.525,s.add_text.y+.065,s.add_text.z),1,3)#yellow
		s.check_collected()
	def select_btn(self,action):
		s=self
		sn.ui_audio(ID=0,pit=.125)
		if s.opt_menu:
			s.sel_opt=0 if action == 0 else 1
			return
		if action == 0:
			s.choose=s.choose-1 if s.choose > 0 else 0
			return
		s.choose=s.choose+1 if s.choose < 2 else 2
	def select_action(self):
		s=self
		sn.ui_audio(ID=1)
		if s.opt_menu:
			s.opt_menu=False
			for inv_opt in (s.music_vol,s.sound_vol,s.opt_exit):
				setattr(inv_opt,'visible',False)
			for vis_opt in (s.select_0,s.select_1,s.select_2):
				setattr(vis_opt,'visible',True)
			return
		if s.choose == 0:
			cc.game_pause()
			return
		if s.choose == 1:
			for vis_text in (s.music_vol,s.sound_vol,s.opt_exit):
				setattr(vis_text,'visible',True)
			for inv_text in (s.select_0,s.select_1,s.select_2):
				setattr(inv_text,'visible',False)
			s.opt_menu=True
		if s.choose == 2:
			if not st.LEVEL_CLEAN:
				cc.clear_level(passed=False)
	def change_volume(self,a):
		s=self
		if s.opt_menu:
			sn.ui_audio(ID=1)
			if s.sel_opt == 1:
				if a == 1:
					if settings.SFX_VOLUME < 1:
						settings.SFX_VOLUME=min(settings.SFX_VOLUME+.1,1)
					return
				if settings.SFX_VOLUME > 0:
					settings.SFX_VOLUME=max(settings.SFX_VOLUME-.1,0)
				return
			if a == 1:
				if settings.MUSIC_VOLUME < 1:
					settings.MUSIC_VOLUME=min(settings.MUSIC_VOLUME+.1,1)
				return
			if settings.MUSIC_VOLUME > 0:
				settings.MUSIC_VOLUME=max(settings.MUSIC_VOLUME-.1,0)
	def input(self,key):
		s=self
		if st.pause:
			sk={'down arrow'	:lambda:s.select_btn(1),
				's'				:lambda:s.select_btn(1),
				'up arrow'		:lambda:s.select_btn(0),
				'w'				:lambda:s.select_btn(0),
				'+'				:lambda:s.change_volume(1),
				'd'				:lambda:s.change_volume(1),
				'right arrow'	:lambda:s.change_volume(1),
				'-'				:lambda:s.change_volume(0),
				'a'				:lambda:s.change_volume(0),
				'left arrow'	:lambda:s.change_volume(0),
				'enter'		:lambda:s.select_action()}
			if key in sk:
				sk[key]()
		del key
	def check_collected(self):
		s=self
		s.gem_counter.text=f'{len(st.CLEAR_GEM)+len(st.COLOR_GEM)}/16 GEMS'
		s.relic_counter.text=f'{len(st.RELIC)}/8'
		s.crystal_counter.text=f'{len(st.CRYSTAL)}/5'
		s.game_progress.text=f'Progress {len(st.COLOR_GEM)*3+len(st.CLEAR_GEM)*3+len(st.CRYSTAL)*5+len(st.RELIC)*4}%'
		s.add_text.text=f'+ {len(st.CLEAR_GEM)}'
	def select_menu(self):
		s=self
		s.select_0.color=color.white if (s.select_0.tag == s.choose) else s.font_color
		s.select_1.color=color.white if (s.select_1.tag == s.choose) else s.font_color
		s.select_2.color=color.white if (s.select_2.tag == s.choose) else s.font_color
	def option_menu(self):
		s=self
		s.music_vol.color=color.white if (s.music_vol.tag == s.sel_opt) else s.font_color
		s.sound_vol.color=color.white if (s.sound_vol.tag == s.sel_opt) else s.font_color
	def refr_progress_text(self):
		self.music_vol.text=f'MUSIC VOLUME {int(round(settings.MUSIC_VOLUME*100))}%'
		self.sound_vol.text=f'SOUND VOLUME {int(round(settings.SFX_VOLUME*100))}%'
	def show_options(self):
		self.opt_exit.visible=True
		self.music_vol.visible=True
		self.sound_vol.visible=True
	def hide_options(self):
		self.opt_exit.visible=False
		self.music_vol.visible=False
		self.sound_vol.visible=False
	def refr_visible(self):
		s=self
		s.select_0.visible=st.pause and not s.opt_menu
		s.select_1.visible=st.pause and not s.opt_menu
		s.select_2.visible=st.pause and not s.opt_menu
		s.crystal_counter.visible=st.pause
		s.game_progress.visible=st.pause
		s.relic_counter.visible=st.pause
		s.gem_counter.visible=st.pause
		s.lvl_name.visible=st.pause
		s.add_text.visible=st.pause
		s.p_name.visible=st.pause
		s.ppt.visible=st.pause
		s.visible=st.pause
	def update(self):
		s=self
		s.refr_visible()
		if st.pause:
			if s.opt_menu:
				s.show_options()
				s.refr_progress_text()
			if s.opt_menu:
				s.option_menu()
				return
			s.select_menu()
			return
		if s.opt_exit.visible:
			s.hide_options()

## Gem Hint
class GemInfo(Entity):
	def __init__(self):
		s=self
		super().__init__()
		info_text=LC.ge_inf[st.level_index] if (st.level_index != 9) else 'none'
		s.mText=Text(info_text,parent=camera.ui,font=_fnt,color=color.orange,scale=2.2,position=(-.6,-.3,.1))
		if st.level_index == 3:
			cc.spawn_color_gem(st.level_index)
			GemTimeTrial(t=90)
		s.tm=0
	def update(self):
		s=self
		s.mText.visible=not(st.gproc())
		if s.visible:
			s.tm+=time.dt
			if s.tm > 5:
				destroy(s.mText)
				destroy(s)

## Checkpoint Letters
class CheckpointLetter(Entity):
	def __init__(self,pos):
		s=self
		s.checkp='CHECKPOINT'
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
			s.ckt.text={False:s.checkp[:s.idx],True:s.checkp[-s.idx+1:]}[s.rev]
			if s.rev:
				sn.pc_audio(ID=1,pit=.9)
				s.ckt.x+=time.dt*4.4
				s.idx-=1
				if s.idx <= 0:
					s.purge()
				return
			if s.idx >= len(s.checkp):
				s.tm=.3
				s.rev=True
				return
			s.idx+=1

## Bonusround Text
class BonusText(Entity):
	def __init__(self):
		self.bntx=f'{btxt}bonus_'
		super().__init__(model=q,texture=None,parent=CU,scale=(.3,.1),position=(0,.35),visible=False)
		self.ch_seq=0
		self.t_delay=0
	def display(self):
		s=self
		s.texture=f'{s.bntx}{s.ch_seq}.png'
		s.visible=True
	def text_ch(self):
		s=self
		s.visible=False
		if s.ch_seq == 7:
			s.ch_seq=0
			return
		s.ch_seq+=1
	def update(self):
		if st.gproc() or st.wait_screen:
			return
		s=self
		if not st.bonus_round:
			destroy(s)
			return
		s.t_delay+=time.dt
		if s.t_delay >= .5:
			s.t_delay=0
			if not s.visible:
				s.display()
				return
			s.text_ch()

##gem challange
class GemTimeTrial(Entity):
	def __init__(self,t):
		s=self
		tm_str=strftime('%M:%S',gmtime(t))
		super().__init__()
		s.disp=Text(tm_str,font=_fnt,scale=3,position=(.7,-.4),parent=CU,color=color.rgb32(200,200,100))
		s.fin=False
		s.tme=t
	def trial_fail(self):
		st.gem_death=True
		self.trial_interrupt()
	def trial_interrupt(self):
		destroy(self.disp)
		destroy(self)
	def update(self):
		if st.gproc():
			return
		s=self
		if st.level_index == 3 and st.level_col_gem:
			s.trial_interrupt()
			return
		s.disp.text=strftime("%M:%S",gmtime(s.tme))
		s.tme=max(s.tme-time.dt,0)
		if s.tme <= 0 or st.bonus_round:
			if not s.fin:
				s.fin=True
				s.trial_fail()

class RelicTimer(Entity):
	def __init__(self):
		s=self
		st.relic_time_stop=0
		st.level_relic_time=0
		st.relic_challange=True
		super().__init__()
		s.disp=Text('',font=_fnt,scale=3,position=(.7,-.4),parent=CU,color=color.rgb32(170,170,200))
		s.icon=Entity(model=q,texture=LC.relic_texture[0],position=(s.x+.67,-.435),scale=.2,color=color.gray,parent=CU)
		s.is_pit=False
		s.ttime=0
		s.rank=0
	def sfx_action(self):
		s=self
		s.ttime+=time.dt
		if s.ttime > .2:
			s.ttime=0
			s.is_pit=not(s.is_pit)
			sn.ui_audio(ID=6,pit=.75 if (s.is_pit) else 1)
	def refr_function(self):
		s=self
		s.rank=cc.refresh_relic_rank(st.level_index)
		st.relic_time_stop=max(st.relic_time_stop-time.dt,0)
		if st.relic_time_stop <= 0:
			st.level_relic_time+=time.dt
			s.disp.text=strftime("%M:%S",gmtime(st.level_relic_time))
			return
		s.sfx_action()
	def refr_color(self):
		s=self
		s.disp.color=LC.relic_color[s.rank]
		s.icon.color=LC.relic_color[s.rank]
	def update(self):
		if st.gproc():
			return
		s=self
		s.refr_color()
		if st.death_event or st.LEVEL_CLEAN or not st.relic_challange:
			destroy(self.disp)
			destroy(self.icon)
			destroy(self)
			return
		if not st.RELIC_TRIAL_DONE:
			s.refr_function()

class CreditText(Entity):
	def __init__(self,t,d):
		super().__init__()
		self.ctext=Text(t,font=_fnt,scale=2.5,parent=CU,color=color.orange,position=(-.7,-.6,-.1))
		self.wait=True
		invoke(lambda:setattr(self,'wait',False),delay=d/2)
		del t,d
	def update(self):
		if not self.wait:
			self.ctext.y+=time.dt/10