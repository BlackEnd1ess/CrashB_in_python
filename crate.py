import item,status,_core,animation,sound,npc,settings
from ursina.shaders import *
from ursina import *

pp='res/crate/'
ic=(.15,.2)
chckPA=[]
cc=_core
sn=sound

cr1=pp+'crate_t1.obj'
cr2=pp+'crate_t2.obj'

##spawn/remove event
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
	if not ID in [0,8,9,10,15,16] and not pse == 1 and not p[1] == -256:
		status.crates_in_level+=1
		if p[1] < -20:
			status.crates_in_bonus+=1
		if ID == 13 and l in [0,8]:
			status.crates_in_level-=1

def destroy_event(c):
	c.disable()
	c.collider=None
	c.parent=None
	c.hide()
	if c.vnum in [11,12]:
		Explosion(cr=c)
	if not status.preload_phase:
		if not c.poly == 1:
			status.C_RESET.append(c)
		if status.bonus_round:
			status.crate_bonus+=1
		else:
			if not c.vnum in [15,16]:
				status.crate_to_sv+=1
				status.crate_count+=1
				status.show_crates=5
		Audio(sn.snd_break,volume=settings.SFX_VOLUME)
	animation.CrateBreak(cr=c)
	scene.entities.remove(c)
	cc.check_crates_over(c)
	c.disable()

def block_destroy(c):
	if not c.p_snd and not status.preload_phase:
		c.p_snd=True
		Audio(sn.snd_steel)
		invoke(lambda:setattr(c,'p_snd',False),delay=.5)

def spawn_ico(c):
	sound.snd_switch()
	ico=Entity(model='quad',texture='res/ui/icon/trigger.png',position=(c.x,c.y,c.z),scale=ic)
	ico.animate_y(c.y+1,duration=1.2)
	invoke(ico.disable,delay=3)

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
		item.WumpaFruit(pos=(wuPo[0],wuPo[1]-.16,wuPo[2]))
		destroy_event(self)

class QuestionMark(Entity):
	def __init__(self,pos,pse):
		self.vnum=2
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
	def destroy(self):
		for _w in range(5):
			item.WumpaFruit(pos=(self.x+random.uniform(-.1,.1),self.y-.16,self.z+random.uniform(-.1,.1)))
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
		if self.b_cnt < 5:
			animation.bnc_animation(self)
			Audio(sn.snd_bounc,pitch=1+self.b_cnt/10)
		self.b_cnt+=1
		if self.b_cnt > 4 or self.lf_time <= 0:
			self.empty_destroy()
			return
		self.lf_time=5
	def destroy(self):
		if not self.is_bounc:
			if self.lf_time > 0 and self.b_cnt < 5:
				self.bnc_event()
				return
			self.empty_destroy()
	def update(self):
		if status.is_dying and self.b_cnt > 0:
			self.lf_time=5
			self.b_cnt=0
		if self.lf_time > 0 and self.b_cnt > 0:
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
		status.checkpoint=(self.x,self.y+1,self.z)
		destroy_event(self)
		cc.collect_reset()
		CheckpointAnimation(p=(self.x,self.y+.5,self.z))

class SpringWood(Entity):
	def __init__(self,pos,pse):
		self.vnum=7
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.is_bounc=False
	def anim_act(self):
		animation.bnc_animation(self)
		Audio(sound.snd_sprin)
	def destroy(self):
		item.WumpaFruit(pos=self.position)
		destroy_event(self)

class SpringIron(Entity):
	def __init__(self,pos,pse):
		self.vnum=8
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.is_bounc=False
		self.p_snd=False
	def anim_act(self):
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
			self.texture=pp+'0/c_tex.png'
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
			self.texture=pp+'0/c_tex.png'
			spawn_ico(self)
			status.C_RESET.append(self)
			for ni in scene.entities[:]:
				if isinstance(ni,Nitro) and ni.collider != None:
					ni.destroy()

class TNT(Entity):
	def __init__(self,pos,pse):
		self.vnum=11
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.e_snd=Audio(sn.snd_c_tnt,autoplay=False)
		self.activ=False
		self.countdown=0
	def destroy(self):
		self.activ=True
		self.e_snd.fade_in()
		self.e_snd.play()
		self.countdown=3.99
		self.shader=unlit_shader
	def empty_destroy(self):
		self.e_snd.fade_out()
		self.countdown=0
		destroy_event(self)
	def update(self):
		if self.countdown > 0 and self.activ:
			self.countdown-=time.dt/1.15
			ctnt=int(self.countdown)
			self.texture=pp+'11/crate_tnt_'+str(ctnt)+'.png'
			if self.countdown <= 0:
				self.empty_destroy()

class Nitro(Entity):
	def __init__(self,pos,pse):
		self.vnum=12
		super().__init__(model=cr2)
		self.reload=False
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.start_y=self.y
		self.acustic=False
		self.snd_time=1
		if status.level_index != 2:
			self.shader=unlit_shader
	def destroy(self):
		destroy_event(self)
	def update(self):
		if not status.gproc():
			if not self.reload and status.level_index != 2:
				self.reload=True
				self.shader=unlit_shader
			dst=distance(cc.playerInstance[0].position,self.position)
			self.snd_time-=time.dt
			if self.snd_time <= 0:
				rh=random.uniform(0.1,0.2)
				self.snd_time=random.randint(2,3)
				if dst <= 2:
					Audio(sn.snd_nitro,volume=0.2)
				if not self.is_stack:
					self.animate_position((self.x,self.y+rh,self.z),duration=0.02)
					invoke(lambda:self.animate_position((self.x,self.start_y,self.z),duration=0.2),delay=0.15)

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
	def destroy(self):
		for dw in range(random.randint(5,10)):
			item.WumpaFruit(pos=(self.x+random.uniform(-.1,.1),self.y-.16,self.z+random.uniform(-.1,.1)))
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
		l_inf={0:'this is a developer test level, place the gem where you want',
				1:'blue gem - reach the end of this level without breaking boxes',
				2:'red gem - solve this level without loosing extra lifes.',
				3:'green gem - find the hidden gem',
				4:'yellow gem - solve the hard sewer path',
				5:'purple gem - collect 300 or more wumpa fruits in this level'}
		mText=Text(text=l_inf[status.level_index],parent=camera.ui,font='res/ui/font.ttf',color=color.orange,scale=2.5,position=(-.3,-.3,.1))
		invoke(mText.disable,delay=5)
		destroy_event(self)

##crate effects
class Explosion(Entity):
	def __init__(self,cr):
		nC={11:color.red,12:color.green}
		super().__init__(model='sphere',position=cr.position,color=nC[cr.vnum],alpha=.4,scale=.1)
		if not status.e_audio:
			status.e_audio=True
			Audio(sn.snd_explo,volume=settings.SFX_VOLUME)
		if cr.vnum == 12 and not status.n_audio:
			status.n_audio=True
			invoke(lambda:Audio(sn.snd_glass,volume=settings.SFX_VOLUME,pitch=1.4),delay=.1)
		self.eR=2
		self.exp_radius()
		invoke(self.reset_audio,delay=.5)
	def reset_audio(self):
		status.e_audio=False
		status.n_audio=False
	def exp_radius(self):
		self.shader=unlit_shader
		for exI in scene.entities[:]:
			jD=distance(self,exI)
			if cc.is_crate(exI) and jD <= self.eR and exI.collider != None:
				if not exI.vnum == 6:
					if exI.vnum in [3,11]:
						exI.empty_destroy()
					else:
						exI.destroy()
			if str(exI) == 'crash_b' and jD < self.eR:
				cc.get_damage(cc.playerInstance[0])
		self.parent=None
		self.disable()
	def update(self):
		if not status.gproc():
			self.scale_x+=.2
			self.scale_y+=.2
			self.scale_z+=.2
			if self.scale >= self.eR:
				self.scale=0
				self.hide()

class CheckpointAnimation(Entity):
	def __init__(self,p):
		super().__init__(position=(p[0]-.1,p[1]+.4,p[2]))
		self.c_text='CHECKPOINT'
		self.run=True
		self.wtime=0
		self.index=0
		self.cr_snd(t=0)
	def cr_snd(self,t):
		if self.y > -250:
			c_au={0:lambda:sn.snd_checkp(),1:lambda:Audio(sn.snd_jump,pitch=.9)}
			c_au[t]()
	def shw_text(self):
		self.wtime+=time.dt
		if self.wtime >= .05:
			self.wtime=0
			_d=1.5
			letter=self.c_text[self.index]
			ct=Text(letter,font='res/ui/font.ttf',position=(self.x+self.index/10,self.y,self.z),scale=7,parent=scene,color=color.rgb(255,255,0))
			invoke(ct.disable,delay=_d)
			invoke(lambda:self.cr_snd(t=1),delay=_d+.1)
			self.index+=1
			if self.index >= 10:
				self.run=False
				self.disable()
	def update(self):
		if self.run:
			self.shw_text()