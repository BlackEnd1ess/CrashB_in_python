import item,status,_core,animation,sound,npc,settings,_loc,random,time,ui
from ursina import Entity,Audio,color,scene,invoke,distance
from ursina.ursinastuff import destroy
from effect import TrialTimeStopInfo

an=animation
cc=_core
sn=sound
st=status
LC=_loc

pp='res/crate/'
cr1=f'{pp}cr_t0.obj'# single texture
cr2=f'{pp}cr_t1.obj'# double texture

## spawn func
def spawn(p,ID,m=0,l=0,pse=False):
	{0:lambda:Iron(pos=p,m=m,l=l,pse=pse),
	1:lambda:Normal(pos=p,m=m,l=l,pse=pse),##t1
	2:lambda:QuestionMark(pos=p,m=m,l=l,pse=pse),##t2
	3:lambda:Bounce(pos=p,m=m,l=l,pse=pse),
	4:lambda:ExtraLife(pos=p,m=m,l=l,pse=pse),##t3
	5:lambda:AkuAku(pos=p,m=m,l=l,pse=pse),
	6:lambda:Checkpoint(pos=p,m=m,l=l,pse=pse),##t2
	7:lambda:SpringWood(pos=p,m=m,l=l,pse=pse),##t1
	8:lambda:SpringIron(pos=p,m=m,l=l,pse=pse),
	9:lambda:SwitchEmpty(pos=p,m=m,l=l,pse=pse),
	10:lambda:SwitchNitro(pos=p,m=m,l=l,pse=pse),
	11:lambda:TNT(pos=p,m=m,l=l,pse=pse),
	12:lambda:Nitro(pos=p,m=m,l=l,pse=pse),
	13:lambda:Air(pos=p,m=m,l=l,pse=pse),
	14:lambda:Protected(pos=p,m=m,l=l,pse=pse),
	15:lambda:cTime(pos=p,m=m,l=l,pse=pse),
	16:lambda:LvInfo(pos=p,m=m,l=l,pse=pse)}[ID]()
	if not ID in (0,8,9,10,15,16) and not pse:
		st.crates_in_level+=1
		if p[1] < -20:
			st.crates_in_bonus+=1
		if ID == 13 and l in (0,8):
			st.crates_in_level-=1
	del p,ID,m,l,pse

##Crate Logics
class Iron(Entity):
	def __init__(self,pos,pse,m,l):
		self.vnum=0
		super().__init__(model=cr1)
		cc.box_set_val(cR=self,Cpos=pos,Cpse=pse,Cmk=m,Ctl=l)
		self.p_snd=False
		del pos,pse,m,l,self
	def destroy(self):
		cc.block_destroy(self)

class Normal(Entity):
	def __init__(self,pos,pse,m,l):
		self.vnum=1
		super().__init__(model=cr1)
		cc.box_set_val(cR=self,Cpos=pos,Cpse=pse,Cmk=m,Ctl=l)
		del pos,pse,m,l,self
	def destroy(self):
		s=self
		item.spawn_wumpa(s.position,cnt=1,c_prg=True)
		cc.box_destroy_event(s)

class QuestionMark(Entity):
	def __init__(self,pos,pse,m,l):
		self.vnum=2
		super().__init__(model=cr2)
		cc.box_set_val(cR=self,Cpos=pos,Cpse=pse,Cmk=m,Ctl=l)
		del pos,pse,m,l,self
	def destroy(self):
		s=self
		item.spawn_wumpa(s.position,cnt=5,c_prg=True)
		cc.box_destroy_event(s)

class Bounce(Entity):
	def __init__(self,pos,pse,m,l):
		s=self
		s.vnum=3
		super().__init__(model=cr2)
		cc.box_set_val(cR=s,Cpos=pos,Cpse=pse,Cmk=m,Ctl=l)
		s.bnc_anim_done=True
		s.lf_time=0
		s.b_cnt=0
		s.frm=0
		del pos,pse,m,l,s
	def check_status(self):
		s=self
		if s.b_cnt > 0:
			if st.death_event:
				s.reset_status()
				return
			if s.lf_time < 5:
				s.lf_time+=time.dt
	def reset_status(self):
		self.lf_time=0
		self.b_cnt=0
	def empty_destroy(self):
		if st.aku_hit > 2:
			cc.wumpa_count(10)
		cc.box_destroy_event(self)
	def destroy(self):
		s=self
		s.b_cnt+=1
		if s.b_cnt < 5 and s.lf_time < 5:
			sn.pc_audio(ID=5,pit=1+s.b_cnt/10)
			cc.wumpa_count(2)
			s.lf_time=0
			return
		s.visible=True
		s.empty_destroy()
	def update(self):
		if st.gproc():
			return
		self.check_status()

class ExtraLife(Entity):
	def __init__(self,pos,pse,m,l):
		self.vnum=4
		super().__init__(model=cr2)
		cc.box_set_val(cR=self,Cpos=pos,Cpse=pse,Cmk=m,Ctl=l)
		del pos,pse,m,l
	def destroy(self):
		s=self
		item.ExtraLive(pos=(s.x,s.y+.1,s.z))
		cc.box_destroy_event(s)

class AkuAku(Entity):
	def __init__(self,pos,pse,m,l):
		s=self
		s.vnum=5
		super().__init__(model=cr2)
		cc.box_set_val(cR=s,Cpos=pos,Cpse=pse,Cmk=m,Ctl=l)
		del pos,pse,m,l,s
	def destroy(self):
		s=self
		sn.crate_audio(ID=12,pit=1.2)
		if st.aku_hit < 4:
			st.aku_hit+=1
			if st.aku_hit > 2:
				if not st.is_invincible:
					st.is_invincible=True
					sn.AkuMusic()
				else:
					st.aku_inv_time=20
		if not st.aku_exist:
			npc.AkuAkuMask(s.position)
		cc.box_destroy_event(s)

class Checkpoint(Entity):
	def __init__(self,pos,pse,m,l):
		s=self
		s.vnum=6
		super().__init__(model=cr2)
		cc.box_set_val(cR=s,Cpos=pos,Cpse=pse,Cmk=m,Ctl=l)
		del pos,pse,m,l,s
	def destroy(self):
		s=self
		st.checkpoint=(s.x,s.y+1.5,s.z)
		sn.crate_audio(ID=6)
		ui.CheckpointLetter(s.position)
		cc.box_destroy_event(s)
		cc.collect_reset()

class SpringWood(Entity):
	def __init__(self,pos,pse,m,l):
		s=self
		s.vnum=7
		super().__init__(model=cr2)
		cc.box_set_val(cR=s,Cpos=pos,Cpse=pse,Cmk=m,Ctl=l)
		s.bnc_anim_done=True
		del pos,pse,m,l,s
	def destroy(self):
		item.spawn_wumpa(self.position,cnt=1,c_prg=True)
		cc.box_destroy_event(self)

class SpringIron(Entity):
	def __init__(self,pos,pse,m,l):
		s=self
		s.vnum=8
		super().__init__(model=cr2)
		cc.box_set_val(cR=s,Cpos=pos,Cpse=pse,Cmk=m,Ctl=l)
		s.bnc_anim_done=True
		s.p_snd=False
		del pos,pse,m,l,s
	def destroy(self):
		cc.block_destroy(self)

class SwitchEmpty(Entity):
	def __init__(self,pos,m,l,pse):
		s=self
		s.vnum=9
		super().__init__(model=cr2)
		cc.box_set_val(cR=s,Cpos=pos,Cpse=pse,Cmk=m,Ctl=l)
		s.p_snd=False
		s.activ=False
		del pos,pse,m,l,s
	def c_reset(self):
		s=self
		s.model=cr2
		s.texture=s.org_tex
		s.activ=False
	def c_transform(self):
		s=self
		s.activ=True
		s.model=cr1
		s.texture=f'{pp}0.png'
	def destroy(self):
		s=self
		cc.block_destroy(s)
		if not s.activ:
			s.c_transform()
			cc.AirBoxReplacer(mark=s.mark)
			cc.spawn_ico(s.position)
			invoke(lambda:sn.crate_audio(ID=13),delay=.15)
			st.SWI_RESET.append(s)

class SwitchNitro(Entity):
	def __init__(self,pos,pse,m,l):
		s=self
		s.vnum=10
		super().__init__(model=cr2)
		cc.box_set_val(cR=s,Cpos=pos,Cpse=pse,Cmk=m,Ctl=l)
		s.p_snd=False
		s.activ=False
		del pos,pse,m,l,s
	def c_reset(self):
		s=self
		s.model=cr2
		s.texture=s.org_tex
		s.activ=False
	def c_transform(self):
		s=self
		s.activ=True
		s.model=cr1
		s.texture=f'{pp}0.png'
	def destroy(self):
		s=self
		cc.block_destroy(s)
		if not s.activ:
			s.c_transform()
			cc.spawn_ico(s.position)
			for nt in scene.entities[:]:
				if isinstance(nt,Nitro) and nt.collider:
					nt.destroy()
			st.SWI_RESET.append(s)
			del nt

tx=f'{pp}crate_tnt_'
class TNT(Entity):
	def __init__(self,pos,pse,m,l):
		s=self
		s.vnum=11
		super().__init__(model=cr2)
		cc.box_set_val(cR=self,Cpos=pos,Cpse=pse,Cmk=m,Ctl=l)
		s.aud=Audio(sn.TC,name='ctn',volume=0,autoplay=False,auto_destroy=True,add_to_scene_entities=False)
		s.activ=False
		s.countdown=0
		del pos,pse,m,l,s
	def destroy(self):
		s=self
		if not s.activ:
			s.activ=True
			s.unlit=False
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
		cc.box_destroy_event(s)
	def update(self):
		s=self
		if st.gproc():
			return
		if s.activ:
			if s.aud.playing:
				s.aud.volume=settings.SFX_VOLUME
			s.countdown=max(s.countdown-time.dt/1.15,0)
			s.texture=tx+f'{int(s.countdown)}.png'
			if s.countdown <= 0:
				s.empty_destroy()

class Nitro(Entity):
	def __init__(self,pos,pse,m,l):
		s=self
		s.vnum=12
		super().__init__(model=cr2,color=color.white,unlit=False)
		cc.box_set_val(cR=s,Cpos=pos,Cpse=pse,Cmk=m,Ctl=l)
		s.new_y=s.spawn_pos[1]
		s.can_jmp=False
		s.is_jmp=False
		s.snd_time=1
		s.jmp_y=s.y
		s.mode=0
		del pos,pse,m,l,s
	def c_freeze(self):
		self.can_jmp=False
	def destroy(self):
		cc.box_destroy_event(self)
	def c_jmp(self):
		s=self
		s.y+=time.dt*3
		if s.y >= s.jmp_y:
			s.mode=2
	def c_fall_act(self):
		s=self
		s.y-=time.dt*3
		if s.y <= s.new_y:
			s.is_jmp=False
			s.y=s.new_y
			s.mode=0
	def refr(self):
		s=self
		s.snd_time=max(s.snd_time-time.dt,0)
		if s.snd_time <= 0:
			s.snd_time=random.randint(2,3)
			if distance(LC.ACTOR,s) < 3:
				sn.crate_audio(ID=8,pit=random.uniform(.8,1.1))
			s.jmp_y=s.y+random.uniform(.3,.5)
			if s.can_jmp:
				s.mode=1
	def update(self):
		s=self
		if st.gproc() or not s.visible:
			return
		if distance(LC.ACTOR.position,s.position) <= 3:
			s.is_jmp=True
		if s.intersects(LC.ACTOR).hit:
			s.destroy()
			return
		if s.is_jmp:
			{0:s.refr,1:s.c_jmp,2:s.c_fall_act}[s.mode]()

class Air(Entity):
	def __init__(self,pos,m,l,pse):
		s=self
		s.vnum=13
		super().__init__(model=cr1)
		cc.box_set_val(cR=s,Cpos=pos,Cpse=pse,Cmk=m,Ctl=l)
		s.collider=None
		del pos,pse,m,l,s
	def destroy(self):
		spawn(p=self.position,ID=self.c_ID,pse=True)
		sn.crate_audio(ID=13)
		cc.box_destroy_event(self)

class Protected(Entity):
	def __init__(self,pos,pse,m,l):
		s=self
		s.vnum=14
		super().__init__(model=cr1)
		cc.box_set_val(cR=s,Cpos=pos,Cpse=pse,Cmk=m,Ctl=l)
		s.p_snd=False
		s.frm=0
		del pos,pse,m,l,s
	def destroy(self):
		s=self
		cc.block_destroy(s)
	def c_destroy(self):
		sn.crate_audio(ID=4,pit=.35)
		item.spawn_wumpa(self.position,cnt=random.randint(5,10),c_prg=True)
		cc.box_destroy_event(self)

class cTime(Entity):
	def __init__(self,pos,m,l,pse=None):
		s=self
		s.vnum=15
		super().__init__(model=cr2)
		s.time_stop=l
		cc.box_set_val(cR=s,Cpos=pos,Cpse=pse,Cmk=m,Ctl=l)
		del pos,pse,m,l,s
	def destroy(self):
		s=self
		if st.relic_time_stop <= 3:
			st.relic_time_stop+=s.time_stop
			if st.relic_time_stop >= 3:
				st.relic_time_stop=3
		TrialTimeStopInfo(s.position,s.time_stop)
		cc.box_destroy_event(s)

class LvInfo(Entity):
	def __init__(self,pos,pse,m,l):
		s=self
		s.vnum=16
		super().__init__(model=cr2)
		cc.box_set_val(cR=s,Cpos=pos,Cpse=pse,Cmk=m,Ctl=l)
		if st.level_col_gem:
			destroy(s)
		del pos,pse,m,l,s
	def destroy(self):
		s=self
		if distance(s,LC.ACTOR) < 3:
			ui.GemInfo()
		cc.box_destroy_event(s)