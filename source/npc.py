from ursina import BoxCollider,Vec3,Entity,Audio,distance,distance_xz,lerp,invoke,PointLight,color,scene
import settings,_core,math,animation,status,sound,_loc,effect,time,random
from ursina.ursinastuff import destroy
from math import radians,cos,sin,pi
from danger import LogDanger

npf='res/npc/'
an=animation
st=status
sn=sound
cc=_core
LC=_loc

def spawn(ID,POS,DRC=0,RTYP=0,RNG=1,CMV=True):
	{0:lambda:Amadillo(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP,cmv=CMV),
	1:lambda:Turtle(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP,cmv=CMV),
	2:lambda:SawTurtle(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP,cmv=CMV),
	3:lambda:Vulture(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP,cmv=CMV),
	4:lambda:Penguin(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP,cmv=CMV),
	5:lambda:Hedgehog(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP,cmv=CMV),
	6:lambda:Seal(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP,cmv=CMV),
	7:lambda:EatingPlant(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP,cmv=CMV),
	8:lambda:Rat(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP,cmv=CMV),
	9:lambda:Lizard(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP,cmv=CMV),
	10:lambda:Scrubber(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP,cmv=CMV),
	11:lambda:Mouse(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP,cmv=CMV),
	12:lambda:Eel(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP,cmv=CMV),
	13:lambda:SewerMine(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP,cmv=CMV),
	14:lambda:Gorilla(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP,cmv=CMV),
	15:lambda:Bee(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP,cmv=CMV),
	16:lambda:Lumberjack(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP,cmv=CMV),
	17:lambda:SpiderRobot(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP,cmv=CMV),
	18:lambda:WalkerRobot(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP,cmv=CMV),
	19:lambda:LabAssistant(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP,cmv=CMV)}[ID]()
	st.npc_in_level+=1
	del ID,POS,DRC,RTYP,RNG,CMV

## Enemies
class Amadillo(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=0
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+200),size=Vec3(500,700,300))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		s.move_speed=1
		s.max_frm=7
		del s,pos,drc,rng,rtyp,cmv
	def update(self):
		if st.gproc():
			return
		cc.npc_action(self)

class Turtle(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=1
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+200),size=Vec3(500,600,300))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		s.move_speed=.7
		s.max_frm=12
		del s,pos,drc,rng,rtyp,cmv
	def update(self):
		if st.gproc():
			return
		cc.npc_action(self)

class SawTurtle(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=2
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+200),size=Vec3(300,600,300))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		s.move_speed=1
		s.max_frm=12
		del s,pos,drc,rng,rtyp,cmv
	def update(self):
		if st.gproc():
			return
		cc.npc_action(self)

class Vulture(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=3
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+400),size=Vec3(300,600,300))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		s.follow_speed=2
		s.move_speed=1.2
		s.max_frm=13
		del s,pos,drc,rng,rtyp,cmv
	def follow_player(self):
		s=self
		an.npc_walking(s)
		if distance_xz(LC.ACTOR,s) < 2:
			if s.mov_direc == 0:
				s.x=lerp(s.x,LC.ACTOR.x,time.dt*s.follow_speed)
				return
			s.z=lerp(s.z,LC.ACTOR.z,time.dt*s.follow_speed)
			if LC.ACTOR.x < s.x:
				s.rotation_y=90
			else:
				s.rotation_y=270
	def update(self):
		if st.gproc():
			return
		s=self
		cc.npc_action(s)
		if not (s.is_hitten or s.is_purge):
			s.follow_player()

class Penguin(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=4
		super().__init__(scale=.8/1100,position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+400),size=Vec3(300,300,600))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		s.move_speed=1.1
		s.max_frm=15
		del s,pos,drc,rng,rtyp,cmv
	def update(self):
		if st.gproc():
			return
		cc.npc_action(self)

class Hedgehog(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=5
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+250),size=Vec3(450,450,450))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		s.def_mode=False
		s.move_speed=1.1
		s.scale=.00045
		s.def_frame=0
		s.def_time=5
		s.max_frm=12
		s.wait=5
		del s,pos,drc,rng,rtyp,cmv
	def update(self):
		if st.gproc():
			return
		s=self
		cc.npc_action(s)
		s.wait=max(s.wait-time.dt,0)
		if s.wait > 0:
			return
		if not (s.is_hitten or s.is_purge):
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
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=6
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+200),size=Vec3(300,800,300))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		s.move_speed=1.1
		s.max_frm=14
		s.tme=1
		s.n_snd=False
		del s,pos,drc,rng,rtyp,cmv
	def update(self):
		if st.gproc():
			return
		cc.npc_action(self)
		sn.npc_loop_audio(n=self,PIT=random.uniform(.36,.38),tme_r=random.uniform(1,2))

class EatingPlant(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=7
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+500),size=Vec3(400,400,700))
		cc.set_val_npc(s)
		s.m_direction,s.atk_frame,s.eat_frame=0,0,0
		s.atk,s.eat=False,False
		s.scale=.8/900
		s.max_frm=13
		del s,pos,drc,rng,rtyp,cmv
	def action(self):
		s=self
		dc=distance(s,LC.ACTOR)
		if dc < 3:
			cc.rotate_to_crash(s)
		if dc <= 1.25:
			if st.death_event or s.atk:
				return
			s.atk=True
			sn.npc_audio(ID=0)
			if not (LC.ACTOR.is_attack or LC.ACTOR.jumping):
				if LC.ACTOR.y <= s.y+.2:
					cc.get_damage(LC.ACTOR,rsn=5)
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
		if s.is_hitten or s.is_purge:
			cc.npc_action(s)
			return
		s.npc_anim()

class Rat(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=8
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=(s.x,s.y,s.z+200),size=Vec3(500,600,300))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		s.scale=.8/1000
		s.move_speed=1
		s.max_frm=10 if not cmv else 8
		s.tme=1
		s.frm=0
		del s,pos,drc,rng,rtyp,cmv
	def idle_action(self):
		s=self
		if (s.is_hitten or s.is_purge):
			cc.npc_action(s)
			return
		an.rat_idle(s)
		if distance(s,LC.ACTOR) < 2.5:
			cc.rotate_to_crash(s)
	def update(self):
		if st.gproc():
			return
		s=self
		sn.npc_loop_audio(n=s,PIT=random.uniform(.65,.75),tme_r=random.uniform(1,1.5))
		if not s.can_move:
			s.idle_action()
			return
		cc.npc_action(s)

class Lizard(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=9
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+400),size=Vec3(500,500,700))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		s.move_speed=1.2
		s.max_frm=11
		s.tme=1
		del s,pos,drc,rng,rtyp,cmv
	def update(self):
		cc.npc_action(self)
		sn.npc_loop_audio(n=self,PIT=random.uniform(.8,1.1),tme_r=random.uniform(.9,1.1))

class Scrubber(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=10
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+350),size=Vec3(400,600,500))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		s.move_speed=1.2
		s.max_frm=3
		s.angle=0
		s.tme=1.5
		del s,pos,drc,rng,rtyp,cmv
	def update(self):
		if st.gproc():
			return
		cc.npc_action(self)
		sn.npc_loop_audio(self,PIT=1,tme_r=1.5)

class Mouse(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=11
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=(s.x,s.y,s.z+150),size=Vec3(500,700,200))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		s.move_speed=1.2
		s.max_frm=8
		s.angle=0
		s.tme=1
		del s,pos,drc,rng,rtyp,cmv
	def update(self):
		if st.gproc():
			return
		cc.npc_action(self)
		sn.npc_loop_audio(self,PIT=1,tme_r=1)

class Eel(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=12
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=(s.x,s.y,s.z+100),size=Vec3(500,700,200))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		s.move_speed=1
		s.max_frm=12
		del s,pos,drc,rng,rtyp,cmv
	def update(self):
		cc.npc_action(self)

class SewerMine(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=13
		super().__init__(position=pos)
		s.collider=BoxCollider(s,size=Vec3(500,700,500))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		s.move_speed=.75
		s.max_frm=16
		del s,pos,drc,rng,rtyp,cmv
	def update(self):
		if st.gproc():
			return
		cc.npc_action(self)

class Gorilla(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=14
		rmo={0:0,1:90,2:180,3:-90}
		super().__init__(rotation=(-90,rmo[drc],0),position=pos,scale=.8/1200)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y,s.z+450),size=Vec3(400,400,800))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		s.wait_next=False
		s.do_throw=False
		s.max_frm=10#for death animtor
		s.t_sleep=.5
		s.t_frame=0
		s.t_mode=0
		s.frm=0
		del s,pos,drc,rng,rtyp,cmv,rmo
	def throw_log(self):
		LogDanger(pos=(self.x,self.y+.6,self.z),ro_y=self.rotation_y)
	def refr_function(self):
		s=self
		if s.t_mode == 0:
			an.gorilla_take(s)
			return
		an.gorilla_throw(s)
	def update(self):
		if st.gproc():
			return
		s=self
		if s.do_throw and not s.wait_next:
			s.do_throw=False
			s.wait_next=True
			s.throw_log()
			return
		if (s.is_hitten or s.is_purge):
			cc.npc_destroy_event(s)
			return
		s.t_sleep-=time.dt
		if s.t_sleep <= 0:
			s.refr_function()

class Bee(Entity):
	def __init__(self,pos,drc=0,rng=0,rtyp=0,cmv=True,bID=0):
		s=self
		s.vnum=15
		super().__init__(rotation_x=-90,position=pos,collider='box')
		s.buzz_snd=Audio(sn.BE,pitch=random.uniform(1,2),loop=True,volume=settings.SFX_VOLUME)
		cc.set_val_npc(s)
		s.play_sfx()
		s.is_hunt=False
		s.is_home=False
		s.move_speed=2
		s.max_frm=9
		s.snd_pit=1
		s.bID=bID
		s.pgt=0
		s.tme=0
		del s,pos,drc,rng,rtyp,cmv,bID
	def play_sfx(self):
		self.buzz_snd.fade_in()
		self.buzz_snd.play()
	def manage_sfx(self):
		s=self
		nvv=max(0,1-(distance(s,LC.ACTOR)/10))
		s.buzz_snd.volume=min(1,nvv*settings.SFX_VOLUME)
		s.buzz_snd.pitch=1.5 if s.is_hunt else 1.4
	def stop_sfx(self):
		self.buzz_snd.stop()
		self.buzz_snd.fade_out()
	def fly_event(self):
		s=self
		s.manage_sfx()
		if (LC.ACTOR.z < s.spawn_pos[2]+8 and LC.ACTOR.z > s.spawn_pos[2]-2) and abs(LC.ACTOR.x-s.x) < 4:
			if not s.purge or not s.is_hitten:
				s.hunt_p()
			s.is_hunt=True
			return
		s.fly_home()
		s.is_hunt=False
	def fly_home(self):
		s=self
		drc=(Vec3(s.spawn_pos[0],s.spawn_pos[1]+.25,s.spawn_pos[2])-Vec3(s.x,s.y,s.z)).normalized()
		s.position+=drc*s.move_speed*time.dt
		angle=math.atan2(s.spawn_pos[1]-s.y,s.spawn_pos[0]-s.x)
		s.rotation_y=math.degrees(angle)
		if abs(s.spawn_pos-s.position) < .05:
			s.pgt+=time.dt
			s.is_home=s.pgt > .5
	def hunt_p(self):
		s=self
		s.position=lerp(s.position,(LC.ACTOR.x,LC.ACTOR.y+.35,LC.ACTOR.z),time.dt*2.3)
		cc.rotate_to_crash(s)
	def purge(self):
		self.stop_sfx()
		destroy(self)
	def check_near_npc(self):
		s=self
		jbc=s.intersects()
		ksc=time.dt*10
		if jbc and str(jbc.entity) == s.name:
			jbc.entity.x=lerp(s.x,jbc.entity.x+.4,ksc) if s.x < jbc.entity.x else lerp(s.x,jbc.entity.x-.4,ksc)
	def update(self):
		if st.gproc():
			return
		s=self
		if abs(s.z-s.spawn_pos[2]) > 10.1 or st.death_event or s.is_home:
			s.purge()
			return
		cc.npc_action(s)
		s.check_near_npc()
		if s.is_hitten or s.is_purge:
			s.stop_sfx()
			return
		s.fly_event()

class Lumberjack(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=16
		super().__init__(rotation_x=-90,position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y,s.z+600),size=Vec3(400,400,800))
		cc.set_val_npc(s)
		s.move_speed=1.6
		s.is_atk=False
		s.p_snd=False
		s.sma_dst=.4
		s.max_frm=10
		s.sma_frm=0
		del s,pos,drc,rng,rtyp,cmv
	def follow_player(self):
		s=self
		drc=(Vec3(LC.ACTOR.x,s.y,LC.ACTOR.z)-s.position).normalized()
		s.position+=drc*s.move_speed*time.dt
	def back_to_spawn(self):
		s=self
		drc=(s.spawn_pos-s.position).normalized()
		s.position+=drc*s.move_speed*time.dt
		if st.death_event or abs(s.position-s.spawn_pos) < .01:
			s.position=s.spawn_pos
			s.is_atk=False
			s.p_snd=False
			s.sma_frm=0
			del drc,s
	def npc_attack(self):
		s=self
		an.lmbjack_smash(s,sp=24)
		if not s.p_snd:
			s.p_snd=True
			sn.npc_audio(ID=9)
			invoke(lambda:setattr(s,'p_snd',False),delay=2)
	def refr(self):
		s=self
		dsp=distance(s.spawn_pos,LC.ACTOR.position)
		psp=distance_xz(s,LC.ACTOR)
		if s.is_atk:
			s.npc_attack()
			if psp < s.sma_dst:
				if LC.ACTOR.landed and not LC.ACTOR.is_attack:
					if s.is_purge or s.is_hitten:
						return
					cc.get_damage(LC.ACTOR,rsn=8)
			return
		if s.is_purge or s.is_hitten:
			return
		if dsp < 8:
			cc.rotate_to_crash(s)
		if psp < s.sma_dst:
			s.is_atk=not st.death_event
			return
		if (s.position-s.spawn_pos).length() > .025:
			an.npc_walking(s)
		if dsp < 5 and abs(LC.ACTOR.y-s.y) < .4:
			s.follow_player()
			return
		s.back_to_spawn()
	def update(self):
		if st.gproc():
			return
		s=self
		cc.npc_action(s)
		if not (s.is_hitten or s.is_purge):
			s.refr()

class SpiderRobot(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=17
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+200),size=Vec3(500,700,300))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		s.move_speed=1
		s.max_frm=13
		s.tme=1
		del s,pos,drc,rng,rtyp,cmv
	def update(self):
		if st.gproc():
			return
		s=self
		cc.npc_action(s)
		sn.npc_loop_audio(n=self,PIT=1,tme_r=.26)

class WalkerRobot(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=18
		super().__init__(position=pos)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+200),size=Vec3(500,700,300))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		s.move_speed=1.8
		s.max_frm=29
		s.tma=.6
		del s,pos,drc,rng,rtyp,cmv
	def snd_action(self):
		s=self
		if distance(s,LC.ACTOR) < 5:
			s.tma=max(s.tma-time.dt,0)
			if s.tma <= 0:
				s.tma=.6
				sn.pc_audio(ID=12)
				invoke(lambda:sn.pc_audio(ID=12,pit=.8),delay=.4)
	def update(self):
		if st.gproc():
			return
		s=self
		cc.npc_action(s)
		if not (s.is_hitten or s.is_purge):
			s.snd_action()

class LabAssistant(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=19
		super().__init__(position=pos,rotation_y={0:90,1:180,2:270,3:0}[drc])
		s.collider=BoxCollider(s,size=Vec3(600,600,1200),center=Vec3(0,150,600))
		cc.set_val_npc(s,drc)
		s.do_push=False
		s.p_snd=False
		s.move_speed=1
		s.max_frm=5#for death animator
		s.tme=1
		del s,pos,drc,rng,rtyp,cmv
	def update(self):
		if st.gproc():
			return
		s=self
		if s.is_hitten or s.is_purge:
			if not s.p_snd:
				s.p_snd=True
				s.rotation_y+=90
				sn.npc_audio(ID=8)
			cc.npc_destroy_event(s)
			return
		s.tme-=time.dt
		dv=distance(s,LC.ACTOR)
		LC.ACTOR.pushed=bool(dv < .6 and s.do_push)
		if s.do_push:
			an.lba_push(s)
		if s.tme <= 0:
			if dv < 6:
				sn.npc_audio(ID=7)
			s.tme=random.randint(1,3)
			s.do_push=True

## passive NPC
tpa1='res/npc/akuaku/aku'
tpa2='res/npc/akuaku/aku2'
class AkuAkuMask(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(position=pos,scale=.75/1000,rotation_x=-90)
		s.status_changed=0
		st.aku_exist=True
		s.sparking=False
		s.spark_delay=0
		s.cur_akin=None
		s.rot_speed=12
		s.mov_speed=8
		s.mvw=0
		del pos,s
	def spark(self):
		s=self
		s.spark_delay+=time.dt
		if s.spark_delay > .5:
			s.spark_delay=0
			effect.Sparkle((s.x+random.uniform(-.1,.1),s.y+random.uniform(-.1,.1),s.z+random.uniform(-.1,.1)))
	def refr_skin(self,skin):
		s=self
		s.status_changed=skin
		s.unlit=bool(skin < 2)
		s.scale=.00075 if (skin < 3) else .0012
		s.sparking=bool(skin == 2)
		s.cur_skin=tpa1 if (skin < 2) else tpa2
		s.model=f'{s.cur_skin}.ply'
		s.texture=f'{s.cur_skin}.png'
	def cover_player(self):
		mk_pos=LC.ACTOR.position+Vec3(-sin(radians(LC.ACTOR.rotation_y)),0,-cos(radians(LC.ACTOR.rotation_y)))*.25
		self.position=(mk_pos.x,mk_pos.y+.5,mk_pos.z)
	def follow_player(self):
		s=self
		s.mvw+=.02
		if s.mvw > 99:
			s.mvw=0
		s.y=(LC.ACTOR.y+.5)+math.sin(s.mvw)*.2
		s.position=lerp(s.position,(LC.ACTOR.x-.2,s.y,LC.ACTOR.z-.35),time.dt*s.mov_speed)
	def update(self):
		if st.gproc():
			return
		s=self
		if st.aku_hit <= 0 or not LC.ACTOR:
			cc.destroy_entity(s)
			return
		if s.sparking:
			s.spark()
		if s.status_changed != st.aku_hit:
			s.refr_skin(st.aku_hit)
		if distance(LC.ACTOR,s) > 5:
			s.position=(LC.ACTOR.x,LC.ACTOR.y+.5,LC.ACTOR.z)
		s.rotation_y=lerp(s.rotation_y,LC.ACTOR.rotation_y,time.dt*s.rot_speed)
		if st.aku_hit < 3:
			s.follow_player()
			return
		s.cover_player()

hpo=f'{npf}hippo/'
class Hippo(Entity):
	def __init__(self,POS):
		s=self
		super().__init__(model=f'{hpo}0.ply',texture=f'{hpo}/0.png',position=POS,rotation_x=-90,scale=.0005)
		s.col=Entity(model='cube',name='HPP',position=(s.x,s.y-.15,s.z-.2),scale=(.6,.5,1),collider='box',visible=False)
		s.col.active=False
		s.is_dive=False
		s.active=False
		s.p_snd=False
		s.spawn_y=s.y
		s.a_frame=0
		s.tme=0
		del POS,s
	def refr_wait(self):
		s=self
		an.hippo_wait(s)
		s.y=min(s.y+time.dt/2,s.spawn_y)
		if not s.col.collider:
			s.col.collider='box'
		if s.col.active:
			s.active=True
	def refr_dive(self):
		s=self
		if s.col.active:
			s.col.active=False
		s.y=max(s.y-time.dt/2,s.spawn_y-.31)
		s.tme+=time.dt
		if s.tme > 4:
			s.tme=0
			s.is_dive=False
			s.p_snd=False
	def update(self):
		if st.gproc():
			return
		s=self
		if s.active:
			an.hippo_dive(s)
			return
		if s.is_dive:
			if not s.p_snd:
				s.p_snd=True
				sn.pc_audio(ID=10,pit=.85)
			s.refr_dive()
			return
		s.refr_wait()

ffly=f'{npf}firefly/0'
tfd=.01
class Firefly(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=ffly+'.ply',texture=ffly+'.png',position=pos,scale=.8/1200,rotation_x=-90,unlit=False)
		s.lgt=PointLight(position=s.position,scale=.2,color=color.rgb32(255,200,180))
		s.start_checkp=st.checkpoint
		s.spawn_pos=pos
		s.active=False
		s.move_speed=8
		s.glow_mode=0
		s.mov_range=1
		s.angle=0
		del pos
	def glow_light(self):
		s=self
		ttm=.0015
		if st.LV_CLEAR_PROCESS:
			s.lgt.color=color.black
			s.lgt.enabled=False
			return
		if s.glow_mode == 0:
			if s.lgt.color[0] <= .7:
				s.glow_mode=1
				return
			s.lgt.color=color.rgb(s.lgt.color[0]-ttm,s.lgt.color[1]-ttm,s.lgt.color[2]-ttm)
			return
		if s.lgt.color[0] >= 1:
			s.glow_mode=0
			return
		s.lgt.color=color.rgb(s.lgt.color[0]+ttm,s.lgt.color[1]+ttm,s.lgt.color[2]+ttm)
	def respawn(self):
		s=self
		if st.checkpoint == s.start_checkp:
			s.active=False
			s.position=s.spawn_pos
			return
		s.position=st.checkpoint
	def m_idle(self):
		s=self
		cc.circle_move_xz(s)
		s.mov_range=.3+abs(sin(time.time()))*.4
		s.y=s.spawn_pos[1]+sin(time.time()*3)*.2
	def update(self):
		if st.gproc():
			return
		s=self
		s.lgt.position=s.position
		s.glow_light()
		if distance(s,LC.ACTOR) < .8:
			s.active=not st.death_event
		if st.death_event:
			s.respawn()
			return
		if s.active:
			cc.rotate_to_crash(s)
			if st.bonus_round:
				s.position=lerp(s.position,(LC.ACTOR.x+.2,LC.ACTOR.y+.5,LC.ACTOR.z),time.dt*2)
			if st.death_route:
				s.position=lerp(s.position,(LC.ACTOR.x,LC.ACTOR.y+.5,LC.ACTOR.z-.5),time.dt*2)
			else:
				s.position=lerp(s.position,(LC.ACTOR.x,LC.ACTOR.y+.5,LC.ACTOR.z+.8),time.dt*2)
			return
		s.m_idle()