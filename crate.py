import item,status,_core,animation,sound,npc,settings,_loc
from ursina.shaders import *
from ursina import *

ic=(.15,.2)
cc=_core
sn=sound
st=status
LC=_loc

pp='res/crate/'
cr1=pp+'cr_t0.ply'# single texture
cr2=pp+'cr_t1.ply'# double texture

##spawn, destroy event
def place_crate(p,ID,m=0,l=1,pse=None,tm=None):
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
	if not ID in [0,8,9,10,15,16] and not pse == 1:
		st.crates_in_level+=1
		if p[1] < -20:
			st.crates_in_bonus+=1
		if ID == 13 and l in [0,8]:
			st.crates_in_level-=1
	del p,ID,m,l,pse,tm

def destroy_event(c):
	c.collider=None
	c.hide()
	if c.vnum in [11,12]:
		explosion(cr=c)
	if not c.poly == 1 and not c.vnum == 16:
		st.C_RESET.append(c)
	if st.bonus_round:
		st.crate_bonus+=1
	else:
		if not c.vnum in [15,16]:
			st.crate_to_sv+=1
			st.crate_count+=1
			st.show_crates=5
	if not st.b_audio:
		st.b_audio=True
		sn.crate_audio(ID=2)
		invoke(cc.reset_audio,delay=.1)
	cc.check_crates_over(c)
	animation.CrateBreak(cr=c)
	cc.purge_instance(c)

def block_destroy(c):
	if not c.p_snd:
		c.p_snd=True
		dpt=1
		if c.vnum == 14:
			dpt=.75
		sn.crate_audio(ID=0,pit=dpt)
		invoke(lambda:setattr(c,'p_snd',False),delay=.5)

def spawn_ico(c):
	sn.crate_audio(ID=12)
	sn.crate_audio(ID=1)
	ico=Entity(model='quad',texture='res/ui/icon/trigger.png',position=(c.x,c.y,c.z),scale=ic)
	ico.animate_y(c.y+1,duration=1.2)
	invoke(lambda:cc.purge_instance(ico),delay=3)

def explosion(cr):
	Fireball(C=cr)
	if not st.e_audio:
		st.e_audio=True
		sn.crate_audio(ID=10)
	if cr.vnum == 12 and not st.n_audio:
		st.n_audio=True
		invoke(lambda:sn.crate_audio(ID=11,pit=1.9),delay=.1)
	invoke(cc.reset_audio,delay=.2)
	for exR in scene.entities[:]:
		if distance(cr,exR) < 1 and exR.collider != None:
			if cc.is_crate(exR):
				if exR.vnum in [3,11]:
					exR.empty_destroy()
				else:
					exR.destroy()
			if cc.is_enemie(exR):
				if not exR.is_hitten:
					cc.bash_enemie(e=exR,h=cr)
			if exR == LC.ACTOR:
				cc.get_damage(exR,rsn=3)

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
		item.place_wumpa(self.position,cnt=1,c_prg=True)
		destroy_event(self)

class QuestionMark(Entity):
	def __init__(self,pos,pse):
		self.vnum=2
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
	def destroy(self):
		item.place_wumpa(self.position,cnt=5,c_prg=True)
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
		sn.crate_audio(ID=4,pit=1+self.b_cnt/10)
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
			if self.b_cnt > 0 and st.death_event:
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
		item.ExtraLive(pos=(self.x,self.y+.1,self.z))
		destroy_event(self)

class AkuAku(Entity):
	def __init__(self,pos,pse):
		self.vnum=5
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
	def destroy(self):
		sn.crate_audio(ID=14,pit=1.2)
		if st.aku_hit < 4:
			st.aku_hit+=1
			if st.aku_hit >= 3:
				if not st.is_invincible:
					st.is_invincible=True
					sn.AkuMusic()
		if not st.aku_exist:
			npc.AkuAkuMask(pos=(self.x,self.y,self.z))
		destroy_event(self)

class Checkpoint(Entity):
	def __init__(self,pos,pse):
		self.vnum=6
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
	def destroy(self):
		st.checkpoint=(self.x,self.y+1.5,self.z)
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
		sn.crate_audio(ID=5)
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
		sn.crate_audio(ID=5)
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
		self.tx=pp+'crate_tnt_'
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.aud=Audio('res/snd/misc/tnt.wav',name='ctn',volume=0,autoplay=False)
		self.activ=False
		self.countdown=0
	def destroy(self):
		self.aud.fade_in()
		self.aud.play()
		self.activ=True
		self.countdown=3.99
		self.shader=unlit_shader
	def empty_destroy(self):
		if self.activ:
			self.activ=False
			self.aud.fade_out()
		self.countdown=0
		destroy_event(self)
	def update(self):
		if not st.gproc():
			if self.activ:
				if self.aud.playing:
					self.aud.volume=settings.SFX_VOLUME
				self.countdown=max(self.countdown-time.dt/1.15,0)
				self.texture=self.tx+str(int(self.countdown))+'.png'
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
		s=self
		if not st.gproc() and s.visible:
			s.snd_time=max(s.snd_time-time.dt,0)
			if s.snd_time <= 0:
				rh=random.uniform(.1,.2)
				s.snd_time=random.randint(2,3)
				if distance(LC.ACTOR.position,s.position) <= 2:
					sn.crate_audio(ID=9,pit=random.uniform(.8,1.1))
				elif not s.is_stack:
					s.animate_position((s.x,s.y+rh,s.z),duration=.02)
					invoke(lambda:s.animate_position((s.x,s.start_y,s.z),duration=.2),delay=.15)

class Air(Entity):
	def __init__(self,pos,m,l,pse):
		self.vnum=13
		super().__init__(model=cr1,double_sided=True)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.collider=None
		self.mark=m
		self.c_ID=l
	def destroy(self):
		status.C_RESET.append(self)
		place_crate(p=self.position,ID=self.c_ID,pse=1)
		sn.crate_audio(ID=13)
		cc.purge_instance(self)

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
		sn.crate_audio(ID=4,pit=.35)
		item.place_wumpa(self.position,cnt=random.randint(5,10),c_prg=True)
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
				4:'green gem - unlock the yellow gem path',
				5:'purple gem - unlock the green gem path'}
		mText=Text(text=l_inf[status.level_index],parent=camera.ui,font='res/ui/font.ttf',color=color.orange,scale=2.2,position=(-.6,-.3,.1))
		invoke(mText.disable,delay=5)
		destroy_event(self)

##crate effects
class Fireball(Entity):
	def __init__(self,C):
		nC={11:color.red,12:color.green}
		super().__init__(model='quad',texture=None,position=(C.x,C.y+.1,C.z+random.uniform(-.1,.1)),color=nC[C.vnum],scale=.75,unlit=False,shader=unlit_shader)
		self.wave=Entity(model=None,texture=pp+'anim/exp_wave/0.tga',position=self.position,scale=.001,rotation_x=-90,color=nC[C.vnum],alpha=.8,unlit=False,shader=unlit_shader)
		self.e_step=0
		self.w_step=0
	def e_wave(self):
		self.w_step+=time.dt*15
		if self.w_step > 4.9:
			self.w_step=0
			cc.purge_instance(self.wave)
			return
		self.wave.model=pp+'anim/exp_wave/'+str(int(self.w_step))+'.ply'
	def f_ball(self):
		self.e_step+=time.dt*25
		if self.e_step > 14.9:
			self.e_step=0
			cc.purge_instance(self)
			return
		self.texture=pp+'anim/exp_fire/'+str(int(self.e_step))+'.png'
	def update(self):
		if not st.gproc():
			self.f_ball()
			self.e_wave()

class CheckpointAnimation(Entity):
	def __init__(self,p):
		super().__init__(position=(p[0]-.1,p[1]+.4,p[2]))
		self.c_text='CHECKPOINT'
		self.wtime=.05
		self.index=0
		sn.crate_audio(ID=6)
	def shw_text(self):
		self.wtime=max(self.wtime-time.dt,0)
		if self.wtime <= 0:
			self.wtime=.05
			_d=1.5
			letter=self.c_text[self.index]
			ct=Text(letter,font='res/ui/font.ttf',position=(self.x+self.index/10,self.y,self.z),scale=7,parent=scene,color=color.rgb32(255,255,0))
			invoke(ct.disable,delay=_d)
			invoke(lambda:sn.pc_audio(ID=1,pit=.9),delay=_d+.1)
			self.index+=1
			if self.index >= 10:
				self.index=0
				cc.purge_instance(self)
	def update(self):
		if not status.gproc():
			self.shw_text()