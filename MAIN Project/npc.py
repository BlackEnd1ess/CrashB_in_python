import settings,_core,math,animation,status,sound,_loc,effect,objects
from math import radians,cos,sin
from ursina import *

di={0:'x',1:'y',2:'z'}
npf='res/npc/'

m_SC=.8/1200
rx=-90

an=animation
st=status
sn=sound
cc=_core
LC=_loc

def spawn(ID,POS,DRC=0,RTYP=0,RNG=1,CMV=True):
	npc_={
		0:lambda:Amadillo(pos=POS,drc=DRC,rng=RNG),
		1:lambda:Turtle(pos=POS,drc=DRC,rng=RNG),
		2:lambda:SawTurtle(pos=POS,drc=DRC,rng=RNG),
		3:lambda:Vulture(pos=POS,drc=DRC,rng=RNG),
		4:lambda:Penguin(pos=POS,drc=DRC,rng=RNG),
		5:lambda:Hedgehog(pos=POS,drc=DRC,rng=RNG),
		6:lambda:Seal(pos=POS,drc=DRC,rng=RNG),
		7:lambda:EatingPlant(pos=POS,drc=DRC,rng=RNG),
		8:lambda:Rat(pos=POS,drc=DRC,rng=RNG,cmv=CMV),
		9:lambda:Lizard(pos=POS,drc=DRC,rng=RNG),
		10:lambda:Scrubber(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP),
		11:lambda:Mouse(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP),
		12:lambda:Eel(pos=POS,drc=DRC,rng=RNG),
		13:lambda:SewerMine(pos=POS,drc=DRC,rng=RNG),
		14:lambda:Gorilla(pos=POS,drc=DRC,rng=RNG)}
	npc_[ID]()
	del ID,POS,DRC,RTYP,RNG,CMV

def npc_walk(m):
	pdv={0:m.spawn_pos[0],1:m.spawn_pos[1],2:m.spawn_pos[2]}
	spd=time.dt*m.move_speed
	mm=m.mov_direc
	mt=m.turn
	kv=getattr(m,di[mm])
	pmd={0:lambda:setattr(m,di[mm],kv+spd),1:lambda:setattr(m,di[mm],kv-spd)}
	pmd[mt]()
	if (mt == 0 and kv >= pdv[mm]+m.mov_range) or (mt == 1 and kv <= pdv[mm]-m.mov_range):
		if mt == 0:
			mr={0:90,1:0,2:0}
			m.rotation_y=mr[mm]
			m.turn=1
			return
		mr={0:270,1:0,2:180}
		m.rotation_y=mr[mm]
		m.turn=0

def npc_action(m):
	if not st.gproc():
		if m.is_hitten:
			cc.fly_away(m)
			return
		if m.is_purge:
			effect.JumpDust(m.position)
			cc.purge_instance(m)
			return
		an.npc_walking(m)
		if m.vnum in [10,11]:
			rma={0:lambda:npc_walk(m),
				1:lambda:cc.circle_move_xz(m),
				2:lambda:cc.circle_move_y(m)}
			rma[m.ro_mode]()
			return
		npc_walk(m)

## Enemies
class Amadillo(Entity):
	def __init__(self,pos,drc,rng):
		s=self
		nN='amadillo'
		s.vnum=0
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+200),size=Vec3(500,700,300))
		cc.set_val_npc(s,drc,rng)
		s.move_speed=1
	def update(self):
		npc_action(self)

class Turtle(Entity):
	def __init__(self,pos,drc,rng):
		s=self
		nN='turtle'
		s.vnum=1
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+200),size=Vec3(300,600,300))
		cc.set_val_npc(s,drc,rng)
		s.move_speed=.7
	def update(self):
		npc_action(self)

class SawTurtle(Entity):
	def __init__(self,pos,drc,rng):
		s=self
		nN='saw_turtle'
		s.vnum=2
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+200),size=Vec3(300,600,300))
		cc.set_val_npc(s,drc,rng)
		s.def_mode=True
		s.move_speed=1
	def update(self):
		npc_action(self)

class Vulture(Entity):
	def __init__(self,pos,drc,rng):
		s=self
		nN='vulture'
		s.vnum=3
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+400),size=Vec3(300,600,300))
		cc.set_val_npc(s,drc,rng)
		s.move_speed=1.2
	def wait_on_player(self):
		s=self
		target=LC.ACTOR
		an.npc_walking(s)
		if distance_xz(target,s) < 2:
			if s.mov_direc == 0:
				s.x=lerp(s.x,target.x,time.dt*3)
				return
			s.z=lerp(s.z,target.z,time.dt*3)
			if target.x < s.x:
				s.rotation_y=90
			else:
				s.rotation_y=270
	def update(self):
		if not st.gproc():
			s=self
			if s.is_purge:
				effect.JumpDust(s.position)
				cc.purge_instance(s)
				return
			if s.is_hitten:
				cc.fly_away(s)
				return
			s.wait_on_player()

class Penguin(Entity):
	def __init__(self,pos,drc,rng):
		s=self
		nN='penguin'
		s.vnum=4
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=.8/1100,position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+400),size=Vec3(300,300,600))
		cc.set_val_npc(s,drc,rng)
		s.move_speed=1.1
	def update(self):
		npc_action(self)

class Hedgehog(Entity):
	def __init__(self,pos,drc,rng):
		s=self
		nN='hedgehog'
		s.vnum=5
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC/1.5,position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+250),size=Vec3(400,400,400))
		cc.set_val_npc(s,drc,rng)
		s.def_mode=False
		s.move_speed=1.1
		s.def_frame=0
	def anim_act(self):
		an.hedge_defend(self)
	def update(self):
		s=self
		npc_action(s)
		if distance(s,LC.ACTOR) < 2:
			s.def_mode=True
			if not st.gproc():
				s.anim_act()
			return
		s.def_mode=False

class Seal(Entity):
	def __init__(self,pos,drc,rng):
		s=self
		nN='seal'
		s.vnum=6
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+200),size=Vec3(300,800,300))
		cc.set_val_npc(s,drc,rng)
		s.move_speed=1.1
		s.n_snd=False
	def update(self):
		s=self
		if st.gproc():
			return
		npc_action(s)
		if distance(s,LC.ACTOR) < 2:
			if not s.n_snd:
				s.n_snd=True
				sn.npc_audio(ID=3,pit=random.uniform(.36,.38))
				invoke(lambda:setattr(s,'n_snd',False),delay=random.choice([1,1.5,1.2]))

class EatingPlant(Entity):
	def __init__(self,pos,drc,rng):
		s=self
		nN='eating_plant'
		s.vnum=7
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=.8/900,position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+500),size=Vec3(400,400,700))
		cc.set_val_npc(s,drc,rng)
		s.m_direction,s.atk_frame,s.eat_frame=0,0,0
		s.atk,s.eat=False,False
	def action(self):
		s=self
		ta=LC.ACTOR
		dc=distance(s,ta)
		if (dc < 3):
			cc.rotate_to_crash(s)
		if (dc <= 1.25):
			if (st.death_event or s.atk):
				return
			s.atk=True
			sn.npc_audio(ID=0)
			if not (ta.is_attack or ta.jumping):
				if ta.y <= s.y+.2:
					cc.get_damage(ta,rsn=5)
					if st.aku_hit < 1:
						s.eat=True
	def npc_anim(self):
		s=self
		if not s.eat:
			if s.atk:
				an.plant_bite(s)
				return
			s.atk_frame=0
			an.npc_walking(s)
			s.action()
			return
		an.plant_eat(s)
	def update(self):
		if not st.gproc():
			s=self
			if s.is_hitten:
				cc.fly_away(s)
				return
			if s.is_purge:
				effect.JumpDust(s.position)
				cc.purge_instance(s)
				return
			s.npc_anim()

class Rat(Entity):
	def __init__(self,pos,drc,rng,cmv):
		s=self
		nN='rat'
		s.vnum=8
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=.8/1000,position=pos)
		s.collider=BoxCollider(s,center=(s.x,s.y,s.z+200),size=Vec3(500,600,300))
		cc.set_val_npc(s,drc,rng)
		s.move_speed=1
		s.can_move=cmv
		s.snd_time=1
		s.idl_frm=0
	def npc_snd(self):
		s=self
		s.snd_time=max(s.snd_time-time.dt,0)
		if s.snd_time <= 0:
			s.snd_time=random.uniform(1,1.5)
			sn.npc_audio(ID=4,pit=random.uniform(.7,.8))
	def idle_action(self):
		if st.gproc():
			return
		s=self
		an.rat_idle(s)
		if s.is_purge:
			effect.JumpDust(s.position)
			cc.purge_instance(s)
			return
		if s.is_hitten:
			cc.fly_away(s)
			return
		if distance(s,LC.ACTOR) < 2:
			cc.rotate_to_crash(s)
			s.npc_snd()
	def update(self):
		s=self
		if not s.can_move:
			s.idle_action()
			return
		npc_action(s)
		if distance(s,LC.ACTOR) < 2:
			s.npc_snd()

class Lizard(Entity):
	def __init__(self,pos,drc,rng):
		s=self
		nN='lizard'
		s.vnum=9
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+400),size=Vec3(500,500,700))
		cc.set_val_npc(s,drc,rng)
		s.move_speed=1.2
	def update(self):
		npc_action(self)

class Scrubber(Entity):
	def __init__(self,pos,drc,rng,rtyp):
		s=self
		nN='scrubber'
		s.vnum=10
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+350),size=Vec3(400,600,500))
		cc.set_val_npc(s,drc,rng)
		s.move_speed=1.2
		s.n_snd=False
		s.ro_mode=rtyp
		s.angle=0
	def npc_snd(self):
		s=self
		if not s.n_snd:
			s.n_snd=True
			if not (s.is_hitten or s.is_purge):
				sn.npc_audio(ID=1)
			invoke(lambda:setattr(s,'n_snd',False),delay=.75)
	def update(self):
		s=self
		npc_action(s)
		if distance(s,LC.ACTOR) < 3:
			s.npc_snd()

class Mouse(Entity):
	def __init__(self,pos,drc,rng,rtyp):
		s=self
		nN='mouse'
		s.vnum=11
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=pos)
		s.collider=BoxCollider(s,center=(s.x,s.y,s.z+150),size=Vec3(500,700,200))
		cc.set_val_npc(s,drc,rng)
		s.move_speed=1.2
		s.snd_time=.5
		s.n_snd=False
		s.ro_mode=rtyp
		s.angle=0
	def npc_snd(self):
		s=self
		if not s.n_snd:
			s.n_snd=True
			if not (s.is_hitten or s.is_purge):
				sn.npc_audio(ID=2)
			invoke(lambda:setattr(s,'n_snd',False),delay=1)
	def update(self):
		s=self
		npc_action(s)
		if distance(s,LC.ACTOR) < 3:
			s.npc_snd()

class Eel(Entity):
	def __init__(self,pos,drc,rng):
		s=self
		nN='eel'
		s.vnum=12
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/0.tga',rotation_x=rx,scale=m_SC,position=pos)
		s.collider=BoxCollider(s,center=(s.x,s.y,s.z+100),size=Vec3(500,700,200))
		cc.set_val_npc(s,drc,rng)
		s.move_speed=1
	def update(self):
		npc_action(self)

class SewerMine(Entity):
	def __init__(self,pos,drc,rng):
		s=self
		nN='sewer_mine'
		s.vnum=13
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=pos)
		s.collider=BoxCollider(s,size=Vec3(500,700,500))
		cc.set_val_npc(s,drc,rng)
		s.move_speed=.75
	def update(self):
		npc_action(self)

class Gorilla(Entity):
	def __init__(self,pos,drc,rng):
		s=self
		nN='gorilla'
		self.vnum=14
		rmo={0:0,1:90,2:180,3:-90}
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation=(rx,rmo[drc],0),position=pos,scale=m_SC)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y,s.z+450),size=Vec3(400,400,800))
		s.throw_act={0:lambda:an.gorilla_take(s),1:lambda:an.gorilla_throw(s)}
		cc.set_val_npc(s,drc,rng)
		s.t_sleep=.5
		s.t_mode=0
		s.f_frame=0
		s.t_frame=0
	def throw_log(self):
		s=self
		invoke(lambda:objects.LogDanger(pos=(s.x,s.y+.6,s.z),ro_y=s.rotation_y),delay=.1)
	def update(self):
		if st.gproc():
			return
		s=self
		if s.is_hitten or s.is_purge:
			an.gorilla_fall(s)
			return
		s.t_sleep=max(s.t_sleep-time.dt,0)
		if s.t_sleep <= 0:
			s.throw_act[s.t_mode]()

## passive NPC
class AkuAkuMask(Entity):
	def __init__(self,pos):
		s=self
		s.tpa='res/npc/akuaku/'
		super().__init__(model=None,texture=None,scale=.00075,rotation_x=rx,position=pos)
		s.skin_0=s.tpa+'aku.ply'
		s.tex_0=s.tpa+'aku.tga'
		s.skin_1=s.tpa+'aku2.ply'
		s.tex_1=s.tpa+'aku2.tga'
		s.last_y=s.y
		st.aku_exist=True
		s.ta=LC.ACTOR
		s.flt_di=0
		s.spt=.5
		s.change_skin()
		s.spkw=0
	def change_skin(self):
		s=self
		if st.aku_hit > 1:
			s.unlit=False
			s.model=s.skin_1
			s.texture=s.tex_1
			s.spark()
			return
		s.unlit=True
		s.model=s.skin_0
		s.texture=s.tex_0
	def spark(self):
		s=self
		s.spt=max(s.spt-time.dt,0)
		if s.spt <= 0:
			s.spt=.5
			s.spkw+=1
			if s.spkw > 2:
				effect.Sparkle((s.x+random.uniform(-.1,.1),s.y+random.uniform(-.1,.1),s.z+random.uniform(-.1,.1)))
	def follow_player(self):
		s=self
		aSP=time.dt*8
		s.rotation_y=lerp(s.rotation_y,s.ta.rotation_y,aSP)
		if st.aku_hit < 3:
			s.scale=.00075
			if not s.ta.walking and s.ta.landed:
				s.floating()
			else:
				s.position=lerp(s.position,(s.ta.x-.25,s.ta.y+.6,s.ta.z-.4),aSP)
				s.last_y=s.y
			return
		s.scale=.0012
		fwd=Vec3(-sin(radians(s.ta.rotation_y)),0,-cos(radians(s.ta.rotation_y)))
		mask_pos=s.ta.position+fwd*.25
		s.position=(mask_pos.x,s.ta.y+.5,mask_pos.z)
	def check_dist_player(self):
		s=self
		if distance(s,s.ta) > 2:
			s.position=s.ta.position
	def floating(self):
		s=self
		if s.flt_di == 0:
			s.y+=time.dt/10
			if s.y >= s.last_y+.2:
				s.flt_di=1
			return
		s.y-=time.dt/10
		if s.y <= s.last_y-.2:
			s.flt_di=0
	def update(self):
		s=self
		if not st.gproc() and LC.ACTOR != None:
			s.check_dist_player()
			s.follow_player()
			s.change_skin()
			if st.aku_hit < 1:
				cc.purge_instance(s)
				st.aku_exist=False

class Hippo(Entity):
	def __init__(self,POS):
		s=self
		hPO=npf+'hippo/'
		super().__init__(model=hPO+'0.ply',texture=hPO+'hpo.tga',position=POS,rotation_x=rx,scale=.0005)
		s.col=Entity(model='cube',name='HPP',position=(s.x,s.y-.15,s.z-.2),scale=(.6,.5,1),visible=False,collider='box')
		s.col.active=False
		s.active=False
		s.a_frame=0
		s.start_y=s.y
	def do_act(self):
		s=self
		if not s.active:
			s.active=True
			sn.pc_audio(ID=10)
			invoke(lambda:s.dive_down(),delay=1)
	def dive_down(self):
		s=self
		s.animate_y(s.start_y-1,duration=1)
		invoke(lambda:setattr(s.col,'collider',None),delay=1)
		invoke(s.dive_up,delay=3)
	def dive_up(self):
		s=self
		s.animate_y(s.start_y,duration=1)
		invoke(lambda:setattr(s,'active',False),delay=3)
		invoke(lambda:setattr(s.col,'collider','box'),delay=1)
	def update(self):
		if not st.gproc():
			s=self
			if s.col.active:
				s.col.active=False
				s.do_act()
				return
			if not s.active:
				animation.hippo_wait(s)
				return
			animation.hippo_dive(s)