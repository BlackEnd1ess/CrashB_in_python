from ursina import BoxCollider,Vec3,Entity,Audio,distance,lerp,invoke,PointLight,color
import settings,_core,math,animation,status,sound,_loc,effect,time,random
from ursina.ursinastuff import destroy
from math import radians,cos,sin,pi
from danger import LogDanger

di={0:'x',1:'y',2:'z'}
npf='res/npc/'

an=animation
st=status
sn=sound
cc=_core
LC=_loc

def spawn(ID,POS,DRC=0,RTYP=0,RNG=1,CMV=True):
	{0:lambda:Amadillo(pos=POS,drc=DRC,rng=RNG),
	1:lambda:Turtle(pos=POS,drc=DRC,rng=RNG),
	2:lambda:SawTurtle(pos=POS,drc=DRC,rng=RNG),
	3:lambda:Vulture(pos=POS,drc=DRC,rng=RNG),
	4:lambda:Penguin(pos=POS,drc=DRC,rng=RNG),
	5:lambda:Hedgehog(pos=POS,drc=DRC,rng=RNG),
	6:lambda:Seal(pos=POS,drc=DRC,rng=RNG),
	7:lambda:EatingPlant(pos=POS),
	8:lambda:Rat(pos=POS,drc=DRC,rng=RNG,cmv=CMV),
	9:lambda:Lizard(pos=POS,drc=DRC,rng=RNG),
	10:lambda:Scrubber(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP),
	11:lambda:Mouse(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP),
	12:lambda:Eel(pos=POS,drc=DRC,rng=RNG),
	13:lambda:SewerMine(pos=POS,drc=DRC,rng=RNG),
	14:lambda:Gorilla(pos=POS,drc=DRC),
	15:lambda:Bee(pos=POS),
	16:lambda:Lumberjack(pos=POS),
	17:lambda:SpiderRobotFlat(pos=POS,drc=DRC,rng=RNG),
	18:lambda:SpiderRobotUp(pos=POS,drc=DRC,rng=RNG),
	19:lambda:Robot(pos=POS,drc=DRC,rng=RNG),
	20:lambda:LabAssistant(pos=POS,drc=DRC)}[ID]()
	st.npc_in_level+=1
	del ID,POS,DRC,RTYP,RNG,CMV

def follow_p(m):
	if abs(m.spawn_pos[0]-m.x) < m.mov_range:
		setattr(m,'x',lerp(m.x,LC.ACTOR.x,time.dt*m.move_speed))

def npc_mv_back(m):
	if m.x != m.spawn_pos[0]:
		m.x=lerp(m.x,m.spawn_pos[0],time.dt*m.move_speed)

def npc_walk(m):
	pdv={0:m.spawn_pos[0],1:m.spawn_pos[1],2:m.spawn_pos[2]}
	mm=m.mov_direc
	mt=m.turn
	kv=getattr(m,di[mm])
	{0:lambda:setattr(m,di[mm],kv+time.dt*m.move_speed),1:lambda:setattr(m,di[mm],kv-time.dt*m.move_speed)}[mt]()
	if mm == 2:
		if distance(LC.ACTOR,m) < 2 and LC.ACTOR.y == m.y:
			follow_p(m)
		else:
			npc_mv_back(m)
	if (mt == 0 and kv >= pdv[mm]+m.mov_range) or (mt == 1 and kv <= pdv[mm]-m.mov_range):
		if mt == 0:
			m.rotation_y={0:90,1:0,2:0}[mm]
			m.turn=1
			return
		m.rotation_y={0:270,1:0,2:180}[mm]
		m.turn=0

def npc_action(m):
	if st.gproc():
		return
	if m.is_hitten:
		cc.fly_away(m)
		return
	if m.is_purge:
		effect.JumpDust(m.position)
		cc.cache_instance(m)
		return
	an.npc_walking(m)
	if m.vnum in {10,11}:
		{0:lambda:npc_walk(m),1:lambda:cc.circle_move_xz(m),2:lambda:cc.circle_move_y(m)}[m.ro_mode]()
		return
	npc_walk(m)

## Enemies
class Amadillo(Entity):
	def __init__(self,pos,drc,rng):
		s=self
		s.vnum=0
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+200),size=Vec3(500,700,300))
		cc.set_val_npc(s,drc,rng)
		s.move_speed=1
		s.max_frm=7
		del pos,rng,drc,s
	def update(self):
		npc_action(self)

class Turtle(Entity):
	def __init__(self,pos,drc,rng):
		s=self
		s.vnum=1
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+200),size=Vec3(300,600,300))
		cc.set_val_npc(s,drc,rng)
		s.move_speed=.7
		s.max_frm=12
		del pos,rng,drc,s
	def update(self):
		npc_action(self)

class SawTurtle(Entity):
	def __init__(self,pos,drc,rng):
		s=self
		s.vnum=2
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+200),size=Vec3(300,600,300))
		cc.set_val_npc(s,drc,rng)
		s.move_speed=1
		s.max_frm=12
		del pos,rng,drc,s
	def update(self):
		npc_action(self)

class Vulture(Entity):
	def __init__(self,pos,drc,rng):
		s=self
		s.vnum=3
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+400),size=Vec3(300,600,300))
		cc.set_val_npc(s,drc,rng)
		s.move_speed=1.2
		s.max_frm=13
		del pos,drc,rng,s
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
		if st.gproc():
			return
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
		s.vnum=4
		super().__init__(scale=.8/1100,position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+400),size=Vec3(300,300,600))
		cc.set_val_npc(s,drc,rng)
		s.move_speed=1.1
		s.max_frm=15
		del pos,drc,rng,s
	def update(self):
		npc_action(self)

class Hedgehog(Entity):
	def __init__(self,pos,drc,rng):
		s=self
		s.vnum=5
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+250),size=Vec3(400,400,400))
		cc.set_val_npc(s,drc,rng)
		s.def_mode=False
		s.move_speed=1.1
		s.scale=.00045
		s.def_frame=0
		s.def_time=5
		s.max_frm=12
		s.wait=5
		del pos,drc,rng,s
	def update(self):
		s=self
		npc_action(s)
		s.wait=max(s.wait-time.dt,0)
		if s.wait > 0:
			return
		if s.def_mode:
			s.def_time=max(s.def_time-time.dt,0)
			an.hedge_defend(s)
			if s.def_time <= 0:
				s.def_mode=False
				s.def_time=5
				s.wait=5
			return
		if distance(s,LC.ACTOR) < 2:
			s.def_mode=True

class Seal(Entity):
	def __init__(self,pos,drc,rng):
		s=self
		s.vnum=6
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+200),size=Vec3(300,800,300))
		cc.set_val_npc(s,drc,rng)
		s.move_speed=1.1
		s.max_frm=14
		s.n_snd=False
		del pos,drc,rng,s
	def update(self):
		s=self
		if st.gproc():
			return
		npc_action(s)
		if distance(s,LC.ACTOR) < 2:
			if not s.n_snd:
				s.n_snd=True
				sn.npc_audio(ID=3,pit=random.uniform(.36,.38))
				invoke(lambda:setattr(s,'n_snd',False),delay=random.uniform(1,2))

class EatingPlant(Entity):
	def __init__(self,pos):
		s=self
		s.vnum=7
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+500),size=Vec3(400,400,700))
		cc.set_val_npc(s)
		s.m_direction,s.atk_frame,s.eat_frame=0,0,0
		s.atk,s.eat=False,False
		s.scale=.8/900
		s.max_frm=13
		del pos,s
	def action(self):
		s=self
		ta=LC.ACTOR
		dc=distance(s,ta)
		if dc < 3:
			cc.rotate_to_crash(s)
		if dc <= 1.25:
			if st.death_event or s.atk:
				return
			s.atk=True
			sn.npc_audio(ID=0)
			if not (ta.is_attack or ta.jumping):
				if ta.y <= s.y+.2:
					cc.get_damage(ta,rsn=5)
					s.eat=st.aku_hit < 1 and not s.eat
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
		if st.gproc():
			return
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
		s.vnum=8
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=(s.x,s.y,s.z+200),size=Vec3(500,600,300))
		cc.set_val_npc(s,drc,rng)
		s.scale=.8/1000
		s.move_speed=1
		s.can_move=cmv
		s.snd_time=1
		s.max_frm=8
		s.frm=0
		del pos,drc,rng,cmv,s
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
		s.vnum=9
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+400),size=Vec3(500,500,700))
		cc.set_val_npc(s,drc,rng)
		s.move_speed=1.2
		s.max_frm=11
		del pos,drc,rng,s
	def update(self):
		npc_action(self)

class Scrubber(Entity):
	def __init__(self,pos,drc,rng,rtyp):
		s=self
		s.vnum=10
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+350),size=Vec3(400,600,500))
		cc.set_val_npc(s,drc,rng)
		s.move_speed=1.2
		s.n_snd=False
		s.ro_mode=rtyp
		s.max_frm=3
		s.angle=0
		del pos,drc,rng,rtyp,s
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
		s.vnum=11
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=(s.x,s.y,s.z+150),size=Vec3(500,700,200))
		cc.set_val_npc(s,drc,rng)
		s.move_speed=1.2
		s.snd_time=.5
		s.max_frm=8
		s.n_snd=False
		s.ro_mode=rtyp
		s.angle=0
		del pos,drc,rng,rtyp,s
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
		s.vnum=12
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=(s.x,s.y,s.z+100),size=Vec3(500,700,200))
		cc.set_val_npc(s,drc,rng)
		s.move_speed=1
		s.max_frm=12
		del pos,drc,rng,s
	def update(self):
		npc_action(self)

class SewerMine(Entity):
	def __init__(self,pos,drc,rng):
		s=self
		s.vnum=13
		super().__init__(position=pos)
		s.collider=BoxCollider(s,size=Vec3(500,700,500))
		cc.set_val_npc(s,drc,rng)
		s.move_speed=.75
		s.max_frm=16
		del pos,drc,rng,s
	def update(self):
		if not st.gproc():
			an.npc_walking(self)
			npc_walk(self)

class Gorilla(Entity):
	def __init__(self,pos,drc):
		s=self
		s.vnum=14
		rmo={0:0,1:90,2:180,3:-90}
		super().__init__(rotation=(-90,rmo[drc],0),position=pos,scale=.8/1200)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y,s.z+450),size=Vec3(400,400,800))
		s.throw_act={0:lambda:an.gorilla_take(self),1:lambda:an.gorilla_throw(self)}
		cc.set_val_npc(s,drc)
		s.t_sleep=.5
		s.t_mode=0
		s.f_frame=0
		s.t_frame=0
		s.max_frm=0
		del pos,drc,s
	def throw_log(self):
		s=self
		invoke(lambda:LogDanger(pos=(s.x,s.y+.6,s.z),ro_y=s.rotation_y),delay=.1)
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

class Bee(Entity):
	def __init__(self,pos,bID=0):
		s=self
		s.vnum=15
		super().__init__(rotation_x=-90,position=pos,collider='box')
		s.buzz_snd=Audio(sn.BE,pitch=random.uniform(1,2),loop=True,volume=settings.SFX_VOLUME)
		cc.set_val_npc(s)
		s.bID=bID
		s.max_frm=0
		s.frm=0
		s.tme=0
		del pos,s
	def fly_home(self):
		s=self
		s.position=lerp(s.position,s.spawn_pos,time.dt*.5)
		angle=math.atan2(s.spawn_pos[1]-s.y,s.spawn_pos[0]-s.x)
		s.rotation_y=math.degrees(angle)
		if abs(s.spawn_pos-s.position) < .05:
			s.tme+=time.dt
			if s.tme > .5:
				s.tme=0
				s.purge()
	def purge(self):
		s=self
		s.buzz_snd.stop()
		s.buzz_snd.fade_out()
		s.enabled=False
		destroy(s)
	def hunt_p(self):
		s=self
		s.position=lerp(s.position,(LC.ACTOR.x,LC.ACTOR.y+.135,LC.ACTOR.z),time.dt*2.3)
		cc.rotate_to_crash(s)
	def fly_event(self):
		s=self
		an.bee_fly(s,sp=14)
		nvv=max(0,1-(distance(s,LC.ACTOR)/10))
		s.buzz_snd.volume=min(1,nvv*settings.SFX_VOLUME)
		if (LC.ACTOR.z < s.spawn_pos[2]+8):
			s.buzz_snd.pitch=1.5
			s.hunt_p()
			return
		s.buzz_snd.pitch=1.4
		s.fly_home()
	def update(self):
		s=self
		if abs(s.z-s.spawn_pos[2]) > 10.1 or st.death_event:# destroy if bee to far away and breaks limit
			s.purge()
			return
		jbc=s.intersects()
		ksc=time.dt*10
		if jbc and str(jbc.entity) == 'bee':
			if s.x < jbc.entity.x:
				jbc.entity.x=lerp(s.x,jbc.entity.x+.4,ksc)
			else:
				jbc.entity.x=lerp(s.x,jbc.entity.x-.4,ksc)
		if st.pause:
			s.buzz_snd.volume=0
			return
		if s.is_hitten:
			s.buzz_snd.stop()
			s.buzz_snd.fade_out()
			cc.fly_away(s)
			return
		if s.is_purge:
			effect.JumpDust(s.position)
			s.purge()
			return
		s.fly_event()
		return

class Lumberjack(Entity):
	def __init__(self,pos):
		s=self
		s.vnum=16
		super().__init__(rotation_x=-90,position=pos,collider='box')
		cc.set_val_npc(s)
		s.move_speed=1
		s.max_frm=10
		s.sma_frm=0
		s.is_atk=False
		del pos,s
	def update(self):
		if st.gproc():
			return
		s=self
		ug=LC.ACTOR
		ljsp=time.dt*3
		ljds=distance(s.spawn_pos,ug.position)
		if s.is_hitten:
			cc.fly_away(s)
			return
		if s.is_purge:
			effect.JumpDust(s.position)
			cc.cache_instance(s)
			return
		if s.is_atk:
			an.lmbjack_smash(s,sp=22)
			return
		if ljds < 4:
			cc.rotate_to_crash(s)
		if ljds < 2:
			if distance(s,ug) < .4:
				s.is_atk=True
			an.npc_walking(s)
			s.position=lerp((s.x,s.y,s.z),(ug.x,s.y,ug.z),ljsp)
			return
		s.position=lerp(s.position,s.spawn_pos,ljsp)

class SpiderRobotFlat(Entity):
	def __init__(self,pos,drc,rng):
		s=self
		s.vnum=17
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+200),size=Vec3(500,700,300))
		s.aud=Audio('res/snd/npc/spider_robot.wav',loop=True,volume=0)
		cc.set_val_npc(s,drc,rng)
		s.move_speed=1
		s.max_frm=13
		del pos,rng,drc,s
	def update(self):
		s=self
		if s.is_hitten or s.is_purge:
			s.aud.stop()
			s.aud.fade_out()
		npc_action(s)
		if not st.gproc():
			if distance(s,LC.ACTOR) < 10:
				current_distance=distance(s,LC.ACTOR)
				nvv=max(0,1-(current_distance/5))
				s.aud.volume=min(1,nvv*settings.SFX_VOLUME)

class SpiderRobotUp(Entity):
	def __init__(self,pos,drc,rng):
		s=self
		s.vnum=18
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+200),size=Vec3(500,700,300))
		s.aud=Audio('res/snd/npc/spider_robot.wav',loop=True,volume=0)
		cc.set_val_npc(s,drc,rng)
		s.move_speed=1
		s.max_frm=13
		del pos,rng,drc,s
	def update(self):
		s=self
		if s.is_hitten or s.is_purge:
			s.aud.stop()
			s.aud.fade_out()
		npc_action(s)
		if not st.gproc():
			if distance(s,LC.ACTOR) < 10:
				current_distance=distance(s,LC.ACTOR)
				nvv=max(0,1-(current_distance/5))
				s.aud.volume=min(1,nvv*settings.SFX_VOLUME)

class Robot(Entity):
	def __init__(self,pos,drc,rng):
		s=self
		s.vnum=19
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+200),size=Vec3(500,700,300))
		cc.set_val_npc(s,drc,rng)
		s.move_speed=1.8
		s.max_frm=29
		s.tme=.6
		del pos,rng,drc,s
	def update(self):
		s=self
		npc_action(s)
		if not st.gproc():
			if distance(s,LC.ACTOR) < 4:
				s.tme=max(s.tme-time.dt,0)
				if s.tme <= 0:
					s.tme=.6
					sn.pc_audio(ID=12)
					invoke(lambda:sn.pc_audio(ID=12,pit=.8),delay=.4)

class LabAssistant(Entity):
	def __init__(self,pos,drc):
		s=self
		s.vnum=20
		super().__init__(position=pos,rotation_y={0:90,1:180,2:270,3:0}[drc])
		s.collider=BoxCollider(s,size=Vec3(600,600,1200),center=Vec3(0,150,600))
		cc.set_val_npc(s,drc)
		s.do_push=False
		s.p_snd=False
		s.move_speed=1
		s.max_frm=0
		s.tme=1
		del pos,drc,s
	def update(self):
		if st.gproc():
			return
		s=self
		s.tme=max(s.tme-time.dt,0)
		dv=distance(s,LC.ACTOR)
		if dv < .6 and s.do_push:
			LC.ACTOR.pushed=True
		if s.is_hitten or s.is_purge:
			if not s.p_snd:
				s.p_snd=True
				setattr(s,'collider',None)
				s.rotation_y+=90
				sn.npc_audio(ID=8)
			an.lba_fall(s)
			return
		if s.do_push:
			an.lba_push(s)
			return
		if s.tme <= 0:
			if dv < 6:
				sn.npc_audio(ID=7)
			s.tme=random.randint(1,3)
			s.do_push=True


## passive NPC
tpa='res/npc/akuaku/'
class AkuAkuMask(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=None,texture=None,scale=.00075,rotation_x=-90,position=pos)
		st.aku_exist=True
		s.cur_skin=123
		s.spt=.5
		s.mode=0
		s.spkw=0
		del pos,s
	def change_skin(self):
		s=self
		if st.aku_hit > 1:
			s.spark()
		if st.aku_hit != s.cur_skin:
			s.cur_skin=st.aku_hit
			s.model=tpa+'aku.ply' if st.aku_hit < 2 else tpa+'aku2.ply'
			s.texture=tpa+'aku.png' if st.aku_hit < 2 else tpa+'aku2.png'
	def spark(self):
		s=self
		s.spt=max(s.spt-time.dt,0)
		if s.spt <= 0:
			s.spt=.5
			if s.spkw < 3:
				s.spkw+=1
			if s.spkw > 2:
				effect.Sparkle((s.x+random.uniform(-.1,.1),s.y+random.uniform(-.1,.1),s.z+random.uniform(-.1,.1)))
	def follow_player(self):
		s=self
		ta=LC.ACTOR
		s.rotation_y=lerp(s.rotation_y,ta.rotation_y,time.dt*10)
		s.scale=.00075 if st.aku_hit < 3 else .0012
		if st.aku_hit < 3:
			if ta.is_slp or not st.p_idle(LC.ACTOR):
				s.position=lerp(s.position,(ta.x-.2,ta.y+.5,ta.z-.35),time.dt*8)
				return
			tfn=time.dt/6
			{0:lambda:setattr(s,'y',s.y-tfn),1:lambda:setattr(s,'y',s.y+tfn)}[s.mode]()
			if abs(s.y-(ta.y+.6)) > .2:
				s.mode=0 if s.mode == 1 else 1
			return
		mask_pos=ta.position+Vec3(-sin(radians(ta.rotation_y)),0,-cos(radians(ta.rotation_y)))*.25
		s.position=(mask_pos.x,ta.y+.5,mask_pos.z)
	def check_dist_player(self):
		s=self
		if distance(s.position,LC.ACTOR.position) > 2:
			s.position=LC.ACTOR.position
	def update(self):
		if not LC.ACTOR or st.gproc():
			return
		s=self
		s.unlit=st.aku_hit < 2
		s.check_dist_player()
		s.follow_player()
		s.change_skin()
		if st.aku_hit <= 0:
			cc.purge_instance(s)

class Hippo(Entity):
	def __init__(self,POS):
		s=self
		super().__init__(position=POS,rotation_x=-90,scale=.0005)
		s.col=Entity(model='cube',name='HPP',position=(s.x,s.y-.15,s.z-.2),scale=(.6,.5,1),visible=False,collider='box')
		vgv=s.name
		s.model=npf+f'{vgv}/0.ply'
		s.texture=npf+f'{vgv}/0.tga'
		s.col.active=False
		s.active=False
		s.a_frame=0
		s.start_y=s.y
		del POS,vgv,s
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

ffly=npf+'firefly/0'
tfd=.01
class Firefly(Entity):
	def __init__(self,pos,fldd):
		s=self
		super().__init__(model=ffly+'.ply',texture=ffly+'.png',position=pos,scale=.8/1200,rotation_x=-90,unlit=False)
		s.lgt=PointLight(position=s.position,scale=.2,color=color.rgb32(255,200,180),enabled=False)
		s.spawn_pos=pos
		s.ffly_drc=fldd
		s.active=False
		s.move_speed=8
		s.way_index=0
		s.mov_range=1
		s.angle=0
		del pos,fldd,s
	def reset(self):
		s=self
		s.position=s.spawn_pos
		s.active=False
		s.way_index=0
		s.lgt.color=color.rgb32(255,200,180)
	def lgt_fadeout(self):
		s=self
		s.lgt.color-=(tfd*1.25,tfd,tfd,0)
		if s.lgt.color[0] <= 0:
			s.reset()
	def m_idle(self):
		s=self
		cc.circle_move_xz(s)
		s.mov_range=.3+abs(sin(time.time()))*.4
		s.y=s.spawn_pos[1]+sin(time.time()*3)*.2
		if (st.bonus_round and s.y > -10) or distance(s,LC.ACTOR) > 16:
			s.lgt.color=color.black
			return
		s.lgt.color=color.rgb32(255,200,180)
	def update(self):
		if st.gproc():
			return
		s=self
		s.lgt.position=s.position
		if st.death_event:
			s.reset()
			return
		if distance(s,LC.ACTOR) < 1:
			s.active=True
		if s.active:
			cc.npc_pathfinding(s)
			return
		s.m_idle()