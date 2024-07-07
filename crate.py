import item,status,_core,animation,sound,npc,settings,_loc
from ursina.shaders import *
from ursina import *

pp='res/crate/'
ic=(.15,.2)
cc=_core
sn=sound
LC=_loc
cr1=pp+'cr_t0.ply'# single texture
cr2=pp+'cr_t1.ply'# double texture

##spawn, destroy event
def place_crate(p,ID,m=None,l=None,pse=None,tm=None):
	CRATES={0:lambda:Iron(pos=p,pse=pse),
			1:lambda:Normal(pos=p,pse=pse),
			2:lambda:QuestionMark(pos=p,pse=pse),
			3:lambda:Bounce(pos=p,pse=pse),
			4:lambda:ExtraLife(pos=p,pse=pse),
			5:lambda:AkuAku(pos=p,pse=pse),
			6:lambda:Checkpoint(pos=p,pse=pse),
			7:lambda:SpringWood(pos=p,pse=pse),
			8:lambda:SpringIron(pos=p,pse=pse),
			9:lambda:SwitchEmpty(pos=p,m=m,pse=pse),
			10:lambda:SwitchNitro(pos=p,pse=pse),
			11:lambda:TNT(pos=p,pse=pse),
			12:lambda:Nitro(pos=p,pse=pse),
			13:lambda:Air(pos=p,m=m,l=l,pse=pse),
			14:lambda:Protected(pos=p,pse=pse),
			15:lambda:cTime(pos=p,pse=pse,tm=tm),
			16:lambda:LvInfo(pos=p,pse=pse)}
	CRATES[ID]()
	if not ID in [0,8,9,10,15,16] and not pse == 1 and not p[1] <= -255:
		status.crates_in_level+=1
		if p[1] < -20:
			status.crates_in_bonus+=1
		if ID == 13 and l in [0,8]:
			status.crates_in_level-=1

def destroy_event(c):
	c.collider=None
	c.hide()
	if c.vnum in [11,12]:
		explosion(cr=c)
	if not c.poly == 1 and not c.vnum == 16:
		status.C_RESET.append(c)
	if status.bonus_round:
		status.crate_bonus+=1
	else:
		if not c.vnum in [15,16]:
			status.crate_to_sv+=1
			status.crate_count+=1
			status.show_crates=5
	if not status.b_audio:
		status.b_audio=True
		Audio(sn.snd_break,volume=settings.SFX_VOLUME)
		invoke(cc.reset_audio,delay=.1)
	animation.CrateBreak(cr=c)
	cc.check_crates_over(c)
	cc.purge_instance(c)

def block_destroy(c):
	if not c.p_snd:
		c.p_snd=True
		w={0:1,8:1,9:1,10:1,14:.55}
		Audio(sn.snd_steel,pitch=w[c.vnum])
		invoke(lambda:setattr(c,'p_snd',False),delay=.5)

def spawn_ico(c):
	sound.snd_switch()
	ico=Entity(model='quad',texture='res/ui/icon/trigger.png',position=(c.x,c.y,c.z),scale=ic)
	ico.animate_y(c.y+1,duration=1.2)
	invoke(ico.disable,delay=3)

def explosion(cr):
	Fireball(C=cr)
	if not status.preload_phase:
		if not status.e_audio:
			status.e_audio=True
			Audio(sn.snd_explo,volume=settings.SFX_VOLUME*1.5)
		if cr.vnum == 12 and not status.n_audio:
			status.n_audio=True
			invoke(lambda:Audio(sn.snd_glass,volume=settings.SFX_VOLUME/1.5,pitch=1.4),delay=.1)
		invoke(cc.reset_audio,delay=.2)
		for exR in scene.entities[:]:
			if distance(cr,exR) < 1:
				if cc.is_crate(exR) and exR.collider != None and exR.y > -250:
					if exR.vnum in [3,11]:
						exR.empty_destroy()
					else:
						exR.destroy()
				elif cc.is_enemie(exR) and exR.collider != None:
					exR.is_hitten=True
				elif exR == LC.ACTOR:
					cc.get_damage(exR)

##Crate Logics
class Iron(Entity):
	def __init__(self,pos,pse):
		self.vnum=0
		super().__init__(model=cr1)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.p_snd=False
	def destroy(self):
		block_destroy(self)

class Normal(Entity):
	def __init__(self,pos,pse):
		self.vnum=1
		super().__init__(model=cr1)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
	def destroy(self):
		wuPo=self.position
		item.place_wumpa(self.position,cnt=1)
		destroy_event(self)

class QuestionMark(Entity):
	def __init__(self,pos,pse):
		self.vnum=2
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
	def destroy(self):
		item.place_wumpa(self.position,cnt=5)
		destroy_event(self)

class Bounce(Entity):
	def __init__(self,pos,pse):
		self.vnum=3
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.is_bounc=False
		self.lf_time=5
		self.b_cnt=0
	def empty_destroy(self):
		destroy_event(self)
	def bnc_event(self):
		cc.wumpa_count(2)
		Audio(sn.snd_bounc,pitch=1+self.b_cnt/10)
		self.b_cnt+=1
		self.lf_time=5
		if not self.is_bounc:
			self.is_bounc=True
			animation.bnc_animation(self)
		if self.b_cnt > 4 or self.lf_time <= 0:
			self.empty_destroy()
			return
	def destroy(self):
		if self.lf_time > 0 and self.b_cnt < 5:
			self.bnc_event()
			return
		self.empty_destroy()
	def update(self):
		if not status.gproc():
			if status.is_dying and self.b_cnt > 0:
				self.lf_time=5
				self.b_cnt=0
				return
			if self.visible:
				if (self.lf_time > 0 and self.b_cnt > 0):
					self.lf_time-=time.dt

class ExtraLife(Entity):
	def __init__(self,pos,pse):
		self.vnum=4
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
	def destroy(self):
		item.ExtraLive(pos=(self.x,self.y+.25,self.z))
		destroy_event(self)

class AkuAku(Entity):
	def __init__(self,pos,pse):
		self.vnum=5
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
	def destroy(self):
		if not status.preload_phase:
			Audio(sn.snd_aku_m,pitch=1.2,volume=settings.SFX_VOLUME)
			if status.aku_hit < 4:
				status.aku_hit+=1
				if status.aku_hit >= 3:
					sn.AkuMusic()
			if not status.aku_exist:
				npc.AkuAkuMask(pos=(self.x,self.y,self.z))
			destroy_event(self)

class Checkpoint(Entity):
	def __init__(self,pos,pse):
		self.vnum=6
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
	def destroy(self):
		status.checkpoint=(self.x,self.y+1.5,self.z)
		destroy_event(self)
		cc.collect_reset()
		CheckpointAnimation(p=(self.x,self.y+.5,self.z))

class SpringWood(Entity):
	def __init__(self,pos,pse):
		self.vnum=7
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.is_bounc=False
	def c_action(self):
		animation.bnc_animation(self)
		Audio(sound.snd_sprin)
	def destroy(self):
		item.place_wumpa(self.position,cnt=1)
		destroy_event(self)

class SpringIron(Entity):
	def __init__(self,pos,pse):
		self.vnum=8
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.is_bounc=False
		self.p_snd=False
	def c_action(self):
		animation.bnc_animation(self)
		Audio(sound.snd_sprin)
	def destroy(self):
		block_destroy(self)

class SwitchEmpty(Entity):
	def __init__(self,pos,m,pse):
		self.vnum=9
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.p_snd=False
		self.activ=False
		self.mark=m
	def c_reset(self):
		self.model=cr2
		self.texture=self.org_tex
		self.activ=False
	def destroy(self):
		block_destroy(self)
		if not self.activ:
			self.activ=True
			self.model=cr1
			self.texture=pp+'0.png'
			ccount=0
			status.C_RESET.append(self)
			for _air in scene.entities[:]:
				if isinstance(_air,Air) and _air.mark == self.mark:
					invoke(_air.destroy,delay=ccount/3.5)
					ccount+=.8
			spawn_ico(self)

class SwitchNitro(Entity):
	def __init__(self,pos,pse):
		self.vnum=10
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.p_snd=False
		self.activ=False
	def c_reset(self):
		self.model=cr2
		self.texture=self.org_tex
		self.activ=False
	def destroy(self):
		block_destroy(self)
		if not self.activ:
			self.activ=True
			self.model=cr1
			self.texture=pp+'0.png'
			spawn_ico(self)
			status.C_RESET.append(self)
			for ni in scene.entities[:]:
				if isinstance(ni,Nitro) and ni.collider != None:ni.destroy()

class TNT(Entity):
	def __init__(self,pos,pse):
		self.vnum=11
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.e_snd=Audio(sn.snd_c_tnt,autoplay=False,volume=settings.SFX_VOLUME)
		self.activ=False
		self.countdown=0
	def destroy(self):
		self.activ=True
		self.e_snd.fade_in()
		if not status.preload_phase:
			self.e_snd.play()
		self.countdown=3.99
		self.shader=unlit_shader
	def empty_destroy(self):
		self.e_snd.fade_out()
		self.countdown=0
		destroy_event(self)
	def update(self):
		if not status.gproc() and self.visible:
			if self.countdown > 0 and self.activ:
				self.countdown-=time.dt/1.15
				ctnt=int(self.countdown)
				self.texture=pp+'crate_tnt_'+str(ctnt)+'.png'
				if self.countdown <= 0:
					self.empty_destroy()

class Nitro(Entity):
	def __init__(self,pos,pse):
		self.vnum=12
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.start_y=self.y
		self.acustic=False
		self.snd_time=1
		if status.level_index != 2:
			self.shader=unlit_shader
	def destroy(self):
		destroy_event(self)
	def update(self):
		if not status.gproc() and self.visible:
			self.snd_time=max(self.snd_time-time.dt,0)
			if self.snd_time <= 0:
				rh=random.uniform(.1,.2)
				self.snd_time=random.randint(2,3)
				if distance(LC.ACTOR.position,self.position) <= 2:
					Audio(sn.snd_nitro,volume=.2)
				elif not self.is_stack:
					self.animate_position((self.x,self.y+rh,self.z),duration=.02)
					invoke(lambda:self.animate_position((self.x,self.start_y,self.z),duration=.2),delay=.15)

class Air(Entity):
	def __init__(self,pos,m,l,pse):
		self.vnum=13
		super().__init__(model=cr1)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.collider=None
		self.mark=m
		self.c_ID=l
		self.double_sided=True
	def destroy(self):
		status.C_RESET.append(self)
		place_crate(p=self.position,ID=self.c_ID,pse=1)
		Audio(sn.snd_c_air,volume=settings.SFX_VOLUME)
		scene.entities.remove(self)
		self.disable()

class Protected(Entity):
	def __init__(self,pos,pse):
		self.vnum=14
		super().__init__(model=cr1)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.hitten=False
		self.p_snd=False
	def destroy(self):
		if not self.hitten:
			self.hitten=True
			animation.prtc_anim(self)
		block_destroy(self)
	def c_destroy(self):
		item.place_wumpa(self.position,cnt=random.randint(5,10))
		destroy_event(self)

class cTime(Entity):
	def __init__(self,pos,tm,pse):
		self.vnum=15
		super().__init__(model=cr2)
		self.time_stop=tm
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
	def destroy(self):
		destroy_event(self)

class LvInfo(Entity):
	def __init__(self,pos,pse):
		self.vnum=16
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
	def destroy(self):
		if status.level_index == 3:
			item.GemStone(pos=(-.05,2.75,88),c=5)
		l_inf={0:'this is a developer test level, place the gem where you want',
				1:'blue gem - reach the end of this level without breaking boxes',
				2:'red gem - solve this level without loosing extra lifes.',
				3:'yellow gem - reach the end of level before time up',
				4:'green gem - solve the hard sewer path',
				5:'purple gem - good luck, you will need it'}
		mText=Text(text=l_inf[status.level_index],parent=camera.ui,font='res/ui/font.ttf',color=color.orange,scale=2.2,position=(-.6,-.3,.1))
		invoke(mText.disable,delay=5)
		destroy_event(self)

##crate effects
class Fireball(Entity):
	def __init__(self,C):
		nC={11:color.red,12:color.green}
		super().__init__(model='quad',texture=None,position=(C.x,C.y+.1,C.z+random.uniform(-.1,.1)),color=nC[C.vnum],scale=.75)
		self.wave=Entity(model=None,texture=pp+'anim/exp_wave/0.tga',position=self.position,scale=.001,rotation_x=-90,color=nC[C.vnum],alpha=.8)
		self.e_step=0
		self.w_step=0
	def e_wave(self):
		self.w_step+=time.dt*15
		if self.w_step > 4.75:
			self.w_step=0
			self.wave.visible=False
			return
		self.wave.model=pp+'anim/exp_wave/'+str(int(self.w_step))+'.ply'
	def f_ball(self):
		self.e_step+=time.dt*25
		if self.e_step > 14.75:
			self.visible=False
			self.e_step=0
			return
		self.texture=pp+'anim/exp_fire/'+str(int(self.e_step))+'.png'
	def update(self):
		if not status.gproc():
			self.f_ball()
			if self.wave.visible:
				self.e_wave()
			if not self.visible and not self.wave.visible:
				self.wave.disable()
				self.disable()

class CheckpointAnimation(Entity):
	def __init__(self,p):
		super().__init__(position=(p[0]-.1,p[1]+.4,p[2]))
		self.c_text='CHECKPOINT'
		self.wtime=.05
		self.index=0
		sn.snd_checkp()
	def shw_text(self):
		self.wtime=max(self.wtime-time.dt,0)
		if self.wtime <= 0:
			self.wtime=.05
			_d=1.5
			letter=self.c_text[self.index]
			ct=Text(letter,font='res/ui/font.ttf',position=(self.x+self.index/10,self.y,self.z),scale=7,parent=scene,color=color.rgb32(255,255,0))
			invoke(ct.disable,delay=_d)
			invoke(lambda:Audio(sn.snd_jump,pitch=.9),delay=_d+.1)
			self.index+=1
			if self.index >= 10:
				self.index=0
				cc.purge_instance(self)
	def update(self):
		if not status.gproc():
			self.shw_text()