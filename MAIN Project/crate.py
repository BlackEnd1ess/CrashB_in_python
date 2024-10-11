import item,status,_core,animation,sound,npc,settings,_loc,ui
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
		s=self
		s.vnum=3
		super().__init__(model=cr2)
		cc.crate_set_val(cR=s,Cpos=pos,Cpse=pse)
		s.is_bounc=False
		s.lf_time=5
		s.b_cnt=0
	def empty_destroy(self):
		destroy_event(self)
	def bnc_event(self):
		s=self
		cc.wumpa_count(2)
		sn.crate_audio(ID=4,pit=1+s.b_cnt/10)
		s.b_cnt+=1
		s.lf_time=5
		if not s.is_bounc:
			s.is_bounc=True
			animation.bnc_animation(s)
		if s.b_cnt > 4 or s.lf_time <= 0:
			s.empty_destroy()
			return
	def destroy(self):
		s=self
		if st.aku_hit > 2:
			cc.wumpa_count(10)
			s.empty_destroy()
			return
		if s.lf_time > 0 and s.b_cnt < 5:
			s.bnc_event()
			return
		s.empty_destroy()
	def update(self):
		if not st.gproc():
			s=self
			if s.b_cnt > 0 and st.death_event:
				s.lf_time=5
				s.b_cnt=0
				return
			if s.visible:
				if (s.lf_time > 0 and s.b_cnt > 0):
					s.lf_time-=time.dt

class ExtraLife(Entity):
	def __init__(self,pos,pse):
		self.vnum=4
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
	def destroy(self):
		s=self
		item.ExtraLive(pos=(s.x,s.y+.1,s.z))
		destroy_event(s)

class AkuAku(Entity):
	def __init__(self,pos,pse):
		self.vnum=5
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
	def destroy(self):
		s=self
		sn.crate_audio(ID=14,pit=1.2)
		if st.aku_hit < 4:
			st.aku_hit+=1
			if st.aku_hit >= 3:
				if not st.is_invincible:
					st.is_invincible=True
					sn.AkuMusic()
		if not st.aku_exist:
			npc.AkuAkuMask(pos=(s.x,s.y,s.z))
		destroy_event(s)

class Checkpoint(Entity):
	def __init__(self,pos,pse):
		self.vnum=6
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
	def destroy(self):
		s=self
		st.checkpoint=(s.x,s.y+1.5,s.z)
		destroy_event(s)
		cc.collect_reset()
		CheckpointAnimation(p=(s.x,s.y+.5,s.z))

class SpringWood(Entity):
	def __init__(self,pos,pse):
		s=self
		s.vnum=7
		super().__init__(model=cr2)
		cc.crate_set_val(cR=s,Cpos=pos,Cpse=pse)
		s.is_bounc=False
	def c_action(self):
		animation.bnc_animation(self)
		sn.crate_audio(ID=5)
	def destroy(self):
		item.place_wumpa(self.position,cnt=1,c_prg=True)
		destroy_event(self)

class SpringIron(Entity):
	def __init__(self,pos,pse):
		s=self
		s.vnum=8
		super().__init__(model=cr2)
		cc.crate_set_val(cR=s,Cpos=pos,Cpse=pse)
		s.is_bounc=False
		s.p_snd=False
	def c_action(self):
		animation.bnc_animation(self)
		sn.crate_audio(ID=5)
	def destroy(self):
		block_destroy(self)

class SwitchEmpty(Entity):
	def __init__(self,pos,m,pse):
		s=self
		s.vnum=9
		super().__init__(model=cr2)
		cc.crate_set_val(cR=s,Cpos=pos,Cpse=pse)
		s.p_snd=False
		s.activ=False
		s.mark=m
	def c_reset(self):
		s=self
		s.model=cr2
		s.texture=s.org_tex
		s.activ=False
	def destroy(self):
		s=self
		block_destroy(s)
		if not s.activ:
			s.activ=True
			s.model=cr1
			s.texture=pp+'0.tga'
			ccount=0
			st.C_RESET.append(s)
			for _air in scene.entities[:]:
				if isinstance(_air,Air) and _air.mark == s.mark:
					invoke(_air.destroy,delay=ccount/3.5)
					ccount+=.8
			spawn_ico(s)

class SwitchNitro(Entity):
	def __init__(self,pos,pse):
		s=self
		s.vnum=10
		super().__init__(model=cr2)
		cc.crate_set_val(cR=s,Cpos=pos,Cpse=pse)
		s.p_snd=False
		s.activ=False
	def c_reset(self):
		s=self
		s.model=cr2
		s.texture=s.org_tex
		s.activ=False
	def destroy(self):
		s=self
		block_destroy(s)
		if not s.activ:
			s.activ=True
			s.model=cr1
			s.texture=pp+'0.tga'
			spawn_ico(s)
			st.C_RESET.append(s)
			for ni in scene.entities[:]:
				if isinstance(ni,Nitro) and ni.collider != None:
					ni.destroy()

class TNT(Entity):
	def __init__(self,pos,pse):
		s=self
		s.vnum=11
		s.tx=pp+'crate_tnt_'
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		s.aud=Audio('res/snd/misc/tnt.wav',name='ctn',volume=0,autoplay=False)
		s.activ=False
		s.countdown=0
	def destroy(self):
		s=self
		if not s.activ:
			s.activ=True
			s.unlit=False
			s.aud.fade_in()
			s.aud.play()
			s.countdown=3.99
	def empty_destroy(self):
		s=self
		if s.activ:
			s.activ=False
			s.aud.fade_out()
		s.countdown=0
		destroy_event(s)
	def update(self):
		s=self
		if not st.gproc():
			if s.activ:
				if s.aud.playing:
					s.aud.volume=settings.SFX_VOLUME
				s.countdown=max(s.countdown-time.dt/1.15,0)
				s.texture=s.tx+str(int(s.countdown))+'.tga'
				if s.countdown <= 0:
					s.empty_destroy()

class Nitro(Entity):
	def __init__(self,pos,pse):
		s=self
		s.vnum=12
		super().__init__(model=cr2,color=color.white,unlit=False)
		cc.crate_set_val(cR=s,Cpos=pos,Cpse=pse)
		s.start_y=s.y
		s.acustic=False
		s.snd_time=1
	def destroy(self):
		destroy_event(self)
	def update(self):
		s=self
		if not st.gproc() and s.visible:
			if distance(LC.ACTOR.position,s.position) <= 3:
				s.snd_time=max(s.snd_time-time.dt,0)
				if s.snd_time <= 0:
					s.snd_time=random.randint(2,3)
					sn.crate_audio(ID=9,pit=random.uniform(.8,1.1))
					if not s.is_stack:
						rh=random.uniform(.1,.2)
						s.animate_position((s.x,s.y+rh,s.z),duration=.02)
						invoke(lambda:s.animate_position((s.x,s.start_y,s.z),duration=.2),delay=.15)

class Air(Entity):
	def __init__(self,pos,m,l,pse):
		s=self
		s.vnum=13
		super().__init__(model=cr1,double_sided=True)
		cc.crate_set_val(cR=s,Cpos=pos,Cpse=pse)
		s.collider=None
		s.mark=m
		s.c_ID=l
	def destroy(self):
		s=self
		place_crate(p=s.position,ID=s.c_ID,pse=1)
		sn.crate_audio(ID=13)
		cc.purge_instance(s)

class Protected(Entity):
	def __init__(self,pos,pse):
		s=self
		s.vnum=14
		super().__init__(model=cr1)
		cc.crate_set_val(cR=s,Cpos=pos,Cpse=pse)
		s.hitten=False
		s.p_snd=False
	def destroy(self):
		s=self
		if not s.hitten:
			s.hitten=True
			animation.prtc_anim(s)
		block_destroy(s)
	def c_destroy(self):
		sn.crate_audio(ID=4,pit=.35)
		item.place_wumpa(self.position,cnt=random.randint(5,10),c_prg=True)
		destroy_event(self)

class cTime(Entity):
	def __init__(self,pos,tm,pse):
		s=self
		s.vnum=15
		super().__init__(model=cr2)
		s.time_stop=tm
		cc.crate_set_val(cR=s,Cpos=pos,Cpse=pse)
	def destroy(self):
		destroy_event(self)

class LvInfo(Entity):
	def __init__(self,pos,pse):
		self.vnum=16
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
	def destroy(self):
		s=self
		if st.level_index == 3:
			item.GemStone(pos=(-.05,2.75,88),c=5)
		ui.GemHint()
		destroy_event(s)

##crate effects
class Fireball(Entity):
	def __init__(self,C):
		s=self
		nC={11:color.red,12:color.green}
		super().__init__(model='quad',texture=None,position=(C.x,C.y+.1,C.z+random.uniform(-.1,.1)),color=nC[C.vnum],scale=.75,unlit=False)
		s.wave=Entity(model=None,texture=pp+'anim/exp_wave/0.tga',position=s.position,scale=.001,rotation_x=-90,color=nC[C.vnum],alpha=.8,unlit=False)
		s.e_step=0
		s.w_step=0
	def e_wave(self):
		s=self
		s.w_step+=time.dt*15
		if s.w_step > 4.9:
			s.w_step=0
			cc.purge_instance(s.wave)
			return
		s.wave.model=pp+'anim/exp_wave/'+str(int(s.w_step))+'.ply'
	def f_ball(self):
		s=self
		s.e_step+=time.dt*25
		if s.e_step > 14.9:
			s.e_step=0
			cc.purge_instance(s)
			return
		s.texture=pp+'anim/exp_fire/'+str(int(s.e_step))+'.png'
	def update(self):
		if not st.gproc():
			s=self
			s.f_ball()
			s.e_wave()

class CheckpointAnimation(Entity):
	def __init__(self,p):
		s=self
		super().__init__(position=(p[0]-.1,p[1]+.4,p[2]))
		s.c_text='CHECKPOINT'
		s.wtime=.05
		s.index=0
		sn.crate_audio(ID=6)
	def shw_text(self):
		s=self
		s.wtime=max(s.wtime-time.dt,0)
		if s.wtime <= 0:
			s.wtime=.05
			_d=1.5
			letter=s.c_text[s.index]
			ct=Text(letter,font=ui._fnt,position=(s.x+s.index/10,s.y,s.z),scale=7,parent=scene,color=color.rgb32(255,255,0),unlit=False)
			invoke(ct.disable,delay=_d)
			invoke(lambda:sn.pc_audio(ID=1,pit=.9),delay=_d+.1)
			s.index+=1
			if s.index >= 10:
				s.index=0
				cc.purge_instance(s)
	def update(self):
		if not st.gproc():
			self.shw_text()