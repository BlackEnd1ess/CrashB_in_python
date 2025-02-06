import item,status,_core,animation,sound,npc,settings,_loc,ui,random,time,effect
from ursina import Entity,Text,Audio,color,scene,invoke,distance
from ursina.ursinastuff import destroy

ic=(.15,.2)
an=animation
cc=_core
sn=sound
st=status
LC=_loc

pp='res/crate/'
cr1=pp+'cr_t0.ply'# single texture
cr2=pp+'cr_t1.ply'# double texture

##spawn, destroy event
def place_crate(p,ID,m=0,l=1,pse=False):
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
			15:lambda:cTime(pos=p,pse=pse),
			16:lambda:LvInfo(pos=p,pse=pse)}
	CRATES[ID]()
	if not ID in {0,8,9,10,15,16} and not pse:
		st.crates_in_level+=1
		if p[1] < -20:
			st.crates_in_bonus+=1
		if ID == 13 and l in {0,8}:
			st.crates_in_level-=1
	del p,ID,m,l,pse,CRATES

def destroy_event(c):
	cc.crate_stack(c.position)
	c.collider=None
	if c.vnum in {11,12}:
		explosion(c)
	if not c.poly:
		st.C_RESET.append(c)
	if c.visible:
		sn.crate_audio(ID=2)
		if c.vnum in LC.cbrc:
			twc=LC.cbrc[c.vnum]
		else:
			twc=color.rgb32(180,80,0)
		an.CrateBreak(c.position,col=twc)
	if st.bonus_round:
		st.crate_bonus+=1
	else:
		if c.vnum != 16:
			st.crate_to_sv+=1
			st.crate_count+=1
			st.show_crates=5
	cc.cache_instance(c)

def block_destroy(c):
	if not c.p_snd:
		c.p_snd=True
		dpt=1
		if c.vnum == 14:
			dpt=.675
		sn.crate_audio(ID=0,pit=dpt)
		invoke(lambda:setattr(c,'p_snd',False),delay=.5)

def spawn_ico(c):
	sn.crate_audio(ID=12)
	sn.crate_audio(ID=1)
	ico=Entity(model='quad',texture='res/ui/icon/trigger.png',position=(c.x,c.y,c.z),scale=ic)
	ico.animate_y(c.y+1,duration=1.2)
	invoke(lambda:cc.purge_instance(ico),delay=3)

def explosion(c):
	if c.visible:
		effect.Fireball(c)
	sn.crate_audio(ID=10)
	if c.vnum == 12:
		invoke(lambda:sn.crate_audio(ID=11,pit=1.4),delay=.1)
	for nbc in scene.entities[:]:
		if distance(c,nbc) < 1 and nbc.collider:
			if cc.is_crate(nbc):
				if nbc.vnum in {3,11}:
					nbc.empty_destroy()
				else:
					nbc.destroy()
			if cc.is_enemie(nbc) and not nbc.is_hitten:
				cc.bash_enemie(nbc,c)
			if nbc == LC.ACTOR:
				cc.get_damage(LC.ACTOR,rsn=4)
	del c,nbc

##Crate Logics
class Iron(Entity):
	def __init__(self,pos,pse):
		self.vnum=0
		super().__init__(model=cr1)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		self.p_snd=False
		del pos,pse
	def destroy(self):
		block_destroy(self)

class Normal(Entity):
	def __init__(self,pos,pse):
		self.vnum=1
		super().__init__(model=cr1)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		del pos,pse
	def destroy(self):
		s=self
		item.place_wumpa(s.position,cnt=1,c_prg=True)
		destroy_event(s)

class QuestionMark(Entity):
	def __init__(self,pos,pse):
		self.vnum=2
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		del pos,pse
	def destroy(self):
		s=self
		item.place_wumpa(s.position,cnt=5,c_prg=True)
		destroy_event(s)

class Bounce(Entity):
	def __init__(self,pos,pse):
		s=self
		s.vnum=3
		super().__init__(model=cr2)
		cc.crate_set_val(cR=s,Cpos=pos,Cpse=pse)
		s.is_bounc=False
		s.lf_time=5
		s.b_cnt=0
		s.frm=0
		del pos,pse
	def empty_destroy(self):
		if st.aku_hit > 2:
			cc.wumpa_count(10)
		destroy_event(self)
	def bnc_event(self):
		s=self
		cc.wumpa_count(2)
		sn.crate_audio(ID=4,pit=1+s.b_cnt/10)
		s.b_cnt+=1
		s.lf_time=5
		s.is_bounc=True
		if s.b_cnt > 4 or s.lf_time <= 0:
			s.empty_destroy()
			return
	def destroy(self):
		s=self
		if s.lf_time > 0 and s.b_cnt < 5:
			s.bnc_event()
			return
		s.empty_destroy()
	def update(self):
		if st.gproc():
			return
		s=self
		if s.b_cnt > 0 and st.death_event:
			s.lf_time=5
			s.b_cnt=0
			return
		if s.is_bounc:
			an.bnc_anim(s)
		if (s.lf_time > 0 and s.b_cnt > 0):
			s.lf_time=max(s.lf_time-time.dt,0)

class ExtraLife(Entity):
	def __init__(self,pos,pse):
		self.vnum=4
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		del pos,pse
	def destroy(self):
		s=self
		item.ExtraLive(pos=(s.x,s.y+.1,s.z))
		destroy_event(s)

class AkuAku(Entity):
	def __init__(self,pos,pse):
		s=self
		s.vnum=5
		super().__init__(model=cr2)
		cc.crate_set_val(cR=s,Cpos=pos,Cpse=pse)
		del pos,pse
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
			npc.AkuAkuMask(s.position)
		destroy_event(s)

class Checkpoint(Entity):
	def __init__(self,pos,pse):
		s=self
		s.vnum=6
		super().__init__(model=cr2)
		cc.crate_set_val(cR=s,Cpos=pos,Cpse=pse)
		del pos,pse
	def destroy(self):
		s=self
		st.checkpoint=(s.x,s.y+1.5,s.z)
		sn.crate_audio(ID=6)
		ui.CheckpointLetter(s.position)
		destroy_event(s)
		cc.collect_reset()

class SpringWood(Entity):
	def __init__(self,pos,pse):
		s=self
		s.vnum=7
		super().__init__(model=cr2)
		cc.crate_set_val(cR=s,Cpos=pos,Cpse=pse)
		s.is_bounc=False
		s.frm=0
		del pos,pse
	def c_action(self):
		self.is_bounc=True
		sn.crate_audio(ID=5)
	def destroy(self):
		item.place_wumpa(self.position,cnt=1,c_prg=True)
		destroy_event(self)
	def update(self):
		if st.gproc():
			return
		s=self
		if s.is_bounc:
			an.bnc_anim(s)

class SpringIron(Entity):
	def __init__(self,pos,pse):
		s=self
		s.vnum=8
		super().__init__(model=cr2)
		cc.crate_set_val(cR=s,Cpos=pos,Cpse=pse)
		s.is_bounc=False
		s.p_snd=False
		s.frm=0
		del pos,pse
	def c_action(self):
		self.is_bounc=True
		sn.crate_audio(ID=5)
	def destroy(self):
		block_destroy(self)
	def update(self):
		if st.gproc():
			return
		s=self
		if s.is_bounc:
			an.bnc_anim(s)

class SwitchEmpty(Entity):
	def __init__(self,pos,m,pse):
		s=self
		s.vnum=9
		super().__init__(model=cr2)
		cc.crate_set_val(cR=s,Cpos=pos,Cpse=pse)
		s.p_snd=False
		s.activ=False
		s.mark=m
		del pos,pse
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
					invoke(_air.destroy,delay=ccount/4)
					if st.level_index == 5 and not st.bonus_round:
						ccount=0
					else:
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
		del pos,pse
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
			for nt in scene.entities[:]:
				if isinstance(nt,Nitro) and nt.collider:
					nt.destroy()
			del nt

tx=pp+'crate_tnt_'
class TNT(Entity):
	def __init__(self,pos,pse):
		s=self
		s.vnum=11
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		s.aud=Audio('res/snd/misc/tnt.wav',name='ctn',volume=0,autoplay=False,auto_destroy=True,add_to_scene_entities=False)
		s.activ=False
		s.countdown=0
		del pos,pse
	def destroy(self):
		s=self
		if not s.activ:
			s.activ=True
			if st.aku_hit < 3:
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
		if st.gproc():
			return
		if s.activ:
			if s.aud.playing:
				s.aud.volume=settings.SFX_VOLUME
			s.countdown=max(s.countdown-time.dt/1.15,0)
			s.texture=tx+f'{int(s.countdown)}.tga'
			if s.countdown <= 0:
				s.empty_destroy()

class Nitro(Entity):
	def __init__(self,pos,pse):
		s=self
		s.vnum=12
		super().__init__(model=cr2,color=color.white)
		cc.crate_set_val(cR=s,Cpos=pos,Cpse=pse)
		s.can_jmp=True
		s.snd_time=1
		del pos,pse
	def destroy(self):
		s=self
		destroy_event(s)
	def c_action(self):
		s=self
		s.snd_time=max(s.snd_time-time.dt,0)
		if s.snd_time <= 0:
			s.snd_time=random.randint(2,3)
			sn.crate_audio(ID=9,pit=random.uniform(.8,1.1))
			if s.can_jmp:
				s.animate_y(s.y+random.uniform(.1,.2),duration=.025)
				invoke(lambda:s.animate_y(s.spawn_pos[1],duration=.2),delay=.15)
	def update(self):
		s=self
		if not st.gproc() and s.visible:
			if (distance(LC.ACTOR,s) <= 3):
				s.c_action()

class Air(Entity):
	def __init__(self,pos,m,l,pse):
		s=self
		s.vnum=13
		super().__init__(model=cr1)
		cc.crate_set_val(cR=s,Cpos=pos,Cpse=pse)
		s.collider=None
		s.mark=m
		s.c_ID=l
		del pos,pse
	def destroy(self):
		s=self
		place_crate(p=s.position,ID=s.c_ID,pse=True)
		sn.crate_audio(ID=13)
		st.C_RESET.append(s)
		cc.cache_instance(s)

class Protected(Entity):
	def __init__(self,pos,pse):
		s=self
		s.vnum=14
		super().__init__(model=cr1)
		cc.crate_set_val(cR=s,Cpos=pos,Cpse=pse)
		s.hitten=False
		s.p_snd=False
		s.frm=0
		del pos,pse
	def destroy(self):
		s=self
		s.hitten=True
		block_destroy(s)
	def c_destroy(self):
		sn.crate_audio(ID=4,pit=.35)
		item.place_wumpa(self.position,cnt=random.randint(5,10),c_prg=True)
		destroy_event(self)
	def update(self):
		if st.gproc():
			return
		if self.hitten:
			an.prtc_anim(self)

class cTime(Entity):
	def __init__(self,pos,tm=1):
		s=self
		s.vnum=15
		super().__init__(model=cr2)
		s.time_stop=tm
		cc.crate_set_val(cR=s,Cpos=pos,Cpse=pse)
		del pos,pse
	def destroy(self):
		destroy_event(self)

class LvInfo(Entity):
	def __init__(self,pos,pse):
		self.vnum=16
		super().__init__(model=cr2)
		cc.crate_set_val(cR=self,Cpos=pos,Cpse=pse)
		del pos,pse
	def destroy(self):
		s=self
		if st.level_index == 3:
			item.GemStone(pos=(-.05,2.75,88),c=5)
		if distance(s,LC.ACTOR) < 3:
			ui.GemHint()
		destroy_event(s)