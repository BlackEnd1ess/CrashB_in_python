import item,status,_core,animation,player,sound,npc,settings
from ursina.shaders import *
from ursina import *

pp='res/crate/'
ic=(.15,.2)
cc=_core
sn=sound

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
		_in='iron/crate_iron'
		super().__init__(model=pp+_in+'.obj',texture=pp+_in+'.png')
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.p_snd=False
		self.vnum=0
		print(pp+_in+'.obj')
	def destroy(self):
		block_destroy(self)

class Normal(Entity):
	def __init__(self,pos,pse):
		super().__init__(model=pp+'normal/crate_normal.obj',texture=pp+'normal/crate_wooden.png')
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.vnum=1
	def destroy(self):
		item.WumpaFruit(pos=self.position)
		destroy_event(self)

class QuestionMark(Entity):
	def __init__(self,pos,pse):
		_in='suprise/crate_sup'
		super().__init__(model=pp+_in+'.obj',texture=pp+_in+'.png')
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.vnum=2
	def destroy(self):
		for _w in range(5):
			item.WumpaFruit(pos=(self.x+random.uniform(-.1,.1),self.y,self.z+random.uniform(-.1,.1)))
		destroy_event(self)

class Bounce(Entity):
	def __init__(self,pos,pse):
		_in='bounce/crate_bounce'
		super().__init__(model=pp+_in+'.obj',texture=pp+_in+'.png')
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.is_bounc=False
		self.lf_time=5
		self.b_cnt=0
		self.vnum=3
	def empty_destroy(self):
		destroy_event(self)
	def bnc_event(self):
		cc.wumpa_count(2)
		animation.bounce_animation(self)
		Audio(sn.snd_bounc,pitch=1+self.b_cnt/10)
		self.b_cnt+=1
		if self.b_cnt > 4 or self.lf_time <= 0:
			self.empty_destroy()
			return
		self.lf_time=5
	def destroy(self):
		if self.lf_time > 0 and self.b_cnt < 5:
			self.bnc_event()
			return
		self.empty_destroy()
	def update(self):
		if self.lf_time > 0 and self.b_cnt > 0:
			self.lf_time-=time.dt

class ExtraLife(Entity):
	def __init__(self,pos,pse):
		_in='live/crate_live'
		super().__init__(model=pp+_in+'.obj',texture=pp+_in+'.png')
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.vnum=4
	def destroy(self):
		item.ExtraLive(pos=(self.x,self.y+.25,self.z))
		destroy_event(self)

class AkuAku(Entity):
	def __init__(self,pos,pse):
		_in='aku/crate_aku'
		super().__init__(model=pp+_in+'.obj',texture=pp+_in+'.png')
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.vnum=5
	def destroy(self):
		if not status.preload_phase:
			if status.aku_hit < 3:
				status.aku_hit+=1
			if not status.aku_exist:
				npc.AkuAkuMask(pos=(self.x,self.y,self.z))
			destroy_event(self)

class Checkpoint(Entity):
	def __init__(self,pos,pse):
		_in='checkpoint/crate_checkp'
		super().__init__(model=pp+_in+'.obj',texture=pp+_in+'.png')
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.vnum=6
	def destroy(self):
		status.checkpoint=(self.x,self.y+1,self.z)
		CheckpointAnimation(p=self.position)
		Audio(sn.snd_aku_m,pitch=1.2,volume=settings.SFX_VOLUME)
		sn.snd_checkp()
		destroy_event(self)
		_core.collect_reset()
		if not status.preload_phase and self.y > -200:
			status.NPC_RESET.clear()

class SpringWood(Entity):
	def __init__(self,pos,pse):
		_in='spring_wood/crate_spring'
		super().__init__(model=pp+_in+'.obj',texture=pp+_in+'.png')
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.is_bounc=False
		self.vnum=7
	def anim_act(self):
		animation.spring_animation(self)
		Audio(sound.snd_sprin)
	def destroy(self):
		item.WumpaFruit(pos=self.position)
		destroy_event(self)

class SpringIron(Entity):
	def __init__(self,pos,pse):
		_in='spring_iron/crate_spring_iron'
		super().__init__(model=pp+_in+'.obj',texture=pp+_in+'.png')
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.is_bounc=False
		self.p_snd=False
		self.vnum=8
	def anim_act(self):
		animation.spring_animation(self)
		Audio(sound.snd_sprin)
	def destroy(self):
		block_destroy(self)

class SwitchEmpty(Entity):
	def __init__(self,pos,m,pse):
		self._in='empty_switch/crate_switch'
		super().__init__(model=pp+self._in+'.obj',texture=pp+self._in+'.png')
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.p_snd=False
		self.activ=False
		self.vnum=9
		self.mark=m
	def c_reset(self):
		self.texture=pp+self._in+'.png'
		self.activ=False
	def destroy(self):
		block_destroy(self)
		if not self.activ:
			self.activ=True
			self.texture=pp+'iron/crate_iron.png'
			ccount=0
			status.C_RESET.append(self)
			for _air in scene.entities[:]:
				if isinstance(_air,Air) and _air.mark == self.mark:
					invoke(_air.destroy,delay=ccount/3.5)
					ccount+=.8
			spawn_ico(self)

class SwitchNitro(Entity):
	def __init__(self,pos,pse):
		self._in='nitro_switch/crate_switch_n'
		super().__init__(model=pp+self._in+'.obj',texture=pp+self._in+'.png')
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.p_snd=False
		self.activ=False
		self.vnum=10
	def c_reset(self):
		self.texture=pp+self._in+'.png'
		self.color=color.white
		self.activ=False
	def destroy(self):
		block_destroy(self)
		if not self.activ:
			self.activ=True
			self.color=color.green
			self.texture=pp+'iron/crate_iron.png'
			spawn_ico(self)
			status.C_RESET.append(self)
			for ni in scene.entities[:]:
				if isinstance(ni,Nitro) and ni.collider != None:
					ni.destroy()

class TNT(Entity):
	def __init__(self,pos,pse):
		_in='tnt/crate_tnt'
		super().__init__(model=pp+_in+'.obj',texture=pp+_in+'.png')
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.e_snd=Audio(sn.snd_c_tnt,autoplay=False)
		self.activ=False
		self.countdown=0
		self.vnum=11
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
			self.texture='res/crate/tnt/crate_tnt_'+str(ctnt)+'.png'
			if self.countdown <= 0:
				self.empty_destroy()

class Nitro(Entity):
	def __init__(self,pos,pse):
		_in='nitro/crate_nitro'
		super().__init__(model=pp+_in+'.obj',texture=pp+_in+'.png')
		self.reload=False
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.start_y=self.y
		self.acustic=False
		self.snd_time=1
		self.vnum=12
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
		_in='air/crate_air'
		super().__init__(model=pp+_in+'.obj',texture=pp+_in+'.png')
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.collider=None
		self.vnum=13
		self.mark=m
		self.c_ID=l
	def destroy(self):
		status.C_RESET.append(self)
		place_crate(p=self.position,ID=self.c_ID,pse=1)
		Audio(sn.snd_c_air,volume=settings.SFX_VOLUME)
		scene.entities.remove(self)
		self.disable()

class Protected(Entity):
	def __init__(self,pos,pse):
		_in='protected/crate_shell'
		super().__init__(model=pp+_in+'.obj',texture=pp+_in+'.png')
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.vnum=14
	def destroy(self):
		for dw in range(random.randint(5,10)):
			item.WumpaFruit(pos=(self.x+random.uniform(-.1,.1),self.y,self.z+random.uniform(-.1,.1)))
		destroy_event(self)

class cTime(Entity):
	def __init__(self,pos,tm,pse):
		_in='timer/crate_time'
		super().__init__(model=pp+_in+'.obj',texture=pp+'timer/crate_t'+str(tm)+'.png')
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.vnum=15
	def destroy(self):
		destroy_event(self)

class LvInfo(Entity):
	def __init__(self,pos,pse):
		_in='info/crate_info'
		super().__init__(model=pp+_in+'.obj',texture=pp+_in+'.png')
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.vnum=16
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
			invoke(lambda:Audio(sn.snd_glass,volume=settings.SFX_VOLUME),delay=.1)
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
		super().__init__(position=(p[0],p[1]+1,p[2]))
		self.c_text='CHECKPOINT'
		self.wtime=0
		self.index=0
		self.run=True
	def update(self):
		if self.run:
			self.wtime+=time.dt
			if self.wtime >= 0.05:
				self.wtime=0
				letter=self.c_text[self.index]
				ct=Text(letter,font='res/ui/font.ttf',position=(self.x+self.index/10,self.y,self.z),scale=7,parent=scene,color=color.rgb(255,255,0))
				invoke(ct.disable,delay=1.5)
				self.index+=1
				if self.index >= 10:
					self.run=False
					self.disable()