import settings,_core,math,animation,status,sound,_loc,effect,objects
from math import radians,cos,sin
from ursina.shaders import *
from ursina import *

npf='res/npc/'
m_SC=.8/1200
rx=-90
an=animation
sn=sound
cc=_core
LC=_loc
st=status

def spawn(pos,mID,mDirec,ro_mode=0):
	npc_={0:lambda:Amadillo(p=pos,d=mDirec),
		1:lambda:Turtle(p=pos,d=mDirec),
		2:lambda:SawTurtle(p=pos,d=mDirec),
		3:lambda:Vulture(p=pos,d=mDirec),
		4:lambda:Penguin(p=pos,d=mDirec),
		5:lambda:Hedgehog(p=pos,d=mDirec),
		6:lambda:Seal(p=pos,d=mDirec),
		7:lambda:EatingPlant(p=pos,d=mDirec),
		8:lambda:Rat(p=pos,d=mDirec),
		9:lambda:Lizard(p=pos,d=mDirec),
		10:lambda:Scrubber(p=pos,d=mDirec,ro=ro_mode),
		11:lambda:Mouse(p=pos,d=mDirec,ro=ro_mode),
		12:lambda:Eel(p=pos,d=mDirec),
		13:lambda:SewerMine(p=pos,d=mDirec),
		14:lambda:Gorilla(p=pos,d=mDirec)}
	npc_[mID]()
	del pos,mID,mDirec,ro_mode

## Enemies
class Amadillo(Entity):
	def __init__(self,p,d):
		nN='amadillo'
		self.vnum=0
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(500,700,300))
		cc.set_val_npc(self,di=d)
		self.move_speed=1
	def update(self):
		if not st.gproc():
			an.npc_walking(self)
			cc.npc_action(self)

class Turtle(Entity):
	def __init__(self,p,d):
		nN='turtle'
		self.vnum=1
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,600,300))
		cc.set_val_npc(self,di=d)
		self.move_speed=.7
	def update(self):
		if not st.gproc():
			an.npc_walking(self)
			cc.npc_action(self)

class SawTurtle(Entity):
	def __init__(self,p,d):
		nN='saw_turtle'
		self.vnum=2
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,600,300))
		cc.set_val_npc(self,di=d)
		self.def_mode=True
		self.move_speed=1
	def update(self):
		if not st.gproc():
			an.npc_walking(self)
			cc.npc_action(self)

class Vulture(Entity):
	def __init__(self,p,d):
		nN='vulture'
		self.vnum=3
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+400),size=Vec3(300,600,300))
		cc.set_val_npc(self,di=d)
		self.target=LC.ACTOR
		self.move_speed=1.2
	def wait_on_player(self):
		an.npc_walking(self)
		if distance_xz(self.target,self) < 2:
			self.x=self.target.x
	def update(self):
		if not st.gproc():
			if not self.is_hitten:
				self.wait_on_player()
			cc.npc_action(self)

class Penguin(Entity):
	def __init__(self,p,d):
		nN='penguin'
		self.vnum=4
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=.8/1100,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+400),size=Vec3(300,300,600))
		cc.set_val_npc(self,di=d)
		self.move_speed=1.1
	def update(self):
		if not st.gproc():
			an.npc_walking(self)
			cc.npc_action(self)

class Hedgehog(Entity):
	def __init__(self,p,d):
		s=self
		nN='hedgehog'
		s.vnum=5
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC/1.5,position=p)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+250),size=Vec3(400,400,400))
		cc.set_val_npc(s,di=d)
		s.def_mode=False
		s.move_speed=1.1
		s.def_frame=0
	def anim_act(self):
		an.hedge_defend(self)
	def update(self):
		if not st.gproc():
			s=self
			an.npc_walking(s)
			cc.npc_action(s)
			if distance(s,LC.ACTOR) < 2:
				s.def_mode=True
				s.anim_act()
				return
			s.def_mode=False

class Seal(Entity):
	def __init__(self,p,d):
		nN='seal'
		self.vnum=6
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,800,300))
		cc.set_val_npc(self,di=d)
		self.move_speed=1.1
		self.n_snd=False
	def update(self):
		if not st.gproc() and self.visible:
			cc.npc_action(self)
			an.npc_walking(self)
			if not self.n_snd and distance(self,LC.ACTOR) < 1:
				self.n_snd=True
				sn.npc_audio(ID=3,pit=random.uniform(.36,.38))
				invoke(lambda:setattr(self,'n_snd',False),delay=random.choice([1,1.5,1.2]))

class EatingPlant(Entity):
	def __init__(self,p,d):
		nN='eating_plant'
		self.vnum=7
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=.8/900,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+500),size=Vec3(400,400,700))
		cc.set_val_npc(self,di=d)
		self.m_direction=0
		self.ta=LC.ACTOR
		self.atk_frame=0
		self.eat_frame=0
		self.atk=False
		self.eat=False
	def action(self):
		s=self
		dc=distance(s,s.ta)
		if dc < 3:
			cc.rotate_to_crash(s)
			if dc <= 1 and not s.atk:
				if st.death_event:
					return
				s.atk=True
				sn.npc_audio(ID=0)
				if not (s.ta.is_attack or s.ta.jumping):
					if st.aku_hit < 1:
						s.eat=True
					if s.ta.y <= s.y+.2:
						cc.get_damage(LC.ACTOR,rsn=5)
				invoke(lambda:setattr(s,'atk',False),delay=1)
	def update(self):
		if not st.gproc():
			if self.is_hitten:
				cc.fly_away(self)
				return
			if self.is_purge:
				cc.npc_purge(self)
				return
			if not self.eat:
				if self.atk:
					an.plant_bite(self)
				else:
					self.atk_frame=0
					an.npc_walking(self)
					self.action()
				return
			an.plant_eat(self)

class Rat(Entity):
	def __init__(self,p,d):
		nN='rat'
		self.vnum=8
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=(self.x,self.y,self.z+200),size=Vec3(500,600,300))
		cc.set_val_npc(self,di=d)
		self.move_speed=.25
		self.snd_time=1
	def update(self):
		if not st.gproc():
			cc.npc_action(self)
			an.npc_walking(self)
			if distance(self,LC.ACTOR) < 2:
				cc.rotate_to_crash(self)
				self.snd_time=max(self.snd_time-time.dt,0)
				if self.snd_time <= 0:
					self.snd_time=random.choice([1,1.5,1.2])
					sn.npc_audio(ID=4,pit=random.uniform(.7,.8))

class Lizard(Entity):
	def __init__(self,p,d):
		nN='lizard'
		self.vnum=9
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+400),size=Vec3(500,500,700))
		cc.set_val_npc(self,di=d)
		self.move_speed=1.3
		self.spawn_pos=p
	def update(self):
		if not st.gproc():
			an.npc_walking(self)
			cc.npc_action(self)

class Scrubber(Entity):
	def __init__(self,p,d,ro):
		nN='scrubber'
		self.vnum=10
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+350),size=Vec3(400,600,500))
		cc.set_val_npc(self,di=d)
		self.move_speed=1.2
		self.n_snd=False
		self.ro_mode=ro
		self.angle=0
	def update(self):
		if not st.gproc() and self.visible:
			an.npc_walking(self)
			cc.npc_action(self)
			if not self.n_snd and distance(self,LC.ACTOR) < 3:
				self.n_snd=True
				if not (self.is_hitten or self.is_purge):
					sn.npc_audio(ID=1)
				invoke(lambda:setattr(self,'n_snd',False),delay=.7)

class Mouse(Entity):
	def __init__(self,p,d,ro):
		nN='mouse'
		self.vnum=11
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=(self.x,self.y,self.z+150),size=Vec3(500,700,200))
		cc.set_val_npc(self,di=d)
		self.move_speed=1.2
		self.snd_time=.5
		self.n_snd=False
		self.ro_mode=ro
		self.angle=0
	def update(self):
		if not st.gproc() and self.visible:
			an.npc_walking(self)
			cc.npc_action(self)
			if not self.n_snd and distance(self,LC.ACTOR) < 3:
				self.n_snd=True
				if not (self.is_hitten or self.is_purge):
					sn.npc_audio(ID=2)
				invoke(lambda:setattr(self,'n_snd',False),delay=1)

class Eel(Entity):
	def __init__(self,p,d):
		nN='eel'
		self.vnum=12
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/0.tga',rotation_x=rx,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=(self.x,self.y,self.z+100),size=Vec3(500,700,200))
		cc.set_val_npc(self,di=d)
	def update(self):
		if not st.gproc():
			cc.npc_action(self)
			an.npc_walking(self)
			if distance(self,LC.ACTOR) < 2:
				self.x=lerp(self.x,LC.ACTOR.x,time.dt*2)

class SewerMine(Entity):
	def __init__(self,p,d):
		nN='sewer_mine'
		self.vnum=13
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=p)
		self.collider=BoxCollider(self,size=Vec3(500,700,500))
		cc.set_val_npc(self,di=d)
		self.move_speed=1.2
	def floating_y(self):
		if self.turn == 0:
			self.y-=time.dt/2
			if self.y <= self.spawn_pos[1]-.8:
				self.turn=1
			return
		self.y+=time.dt/2
		if self.y > self.spawn_pos[1]+.8:
			self.turn=0
	def floating_x(self):
		if self.turn == 0:
			self.x-=time.dt/2
			if self.x <= self.spawn_pos[0]-.8:
				self.turn=1
			return
		self.x+=time.dt/2
		if self.x > self.spawn_pos[0]+.8:
			self.turn=0
	def update(self):
		if not st.gproc() and self.visible:
			an.npc_walking(self)
			if self.m_direction == 0:
				self.floating_y()
				return
			self.floating_x()

class Gorilla(Entity):
	def __init__(self,p,d):
		nN='gorilla'
		self.vnum=14
		rmo={0:0,1:90,2:180,3:-90}
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation=(rx,rmo[d],0),position=p,scale=m_SC)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y,self.z+450),size=Vec3(400,400,800))
		self.throw_act={0:lambda:an.gorilla_take(self),1:lambda:an.gorilla_throw(self)}
		cc.set_val_npc(self,di=d)
		self.t_sleep=.5
		self.t_mode=0
		self.f_frame=0
		self.t_frame=0
	def throw_log(self):
		invoke(lambda:objects.LogDanger(pos=(self.x,self.y+.6,self.z),ro_y=self.rotation_y),delay=.1)
	def update(self):
		if not st.gproc():
			if self.is_hitten or self.is_purge:
				an.gorilla_fall(self)
				return
			self.t_sleep=max(self.t_sleep-time.dt,0)
			if self.t_sleep <= 0:
				self.throw_act[self.t_mode]()

## passive NPC
class AkuAkuMask(Entity):
	def __init__(self,pos):
		s=self
		s.tpa='res/npc/akuaku/'
		super().__init__(model=None,texture=None,scale=.00075,rotation_x=rx,position=pos,unlit=False)
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
			s.model=s.skin_1
			s.texture=s.tex_1
			s.spark()
			return
		s.model=s.skin_0
		s.texture=s.tex_0
	def spark(self):
		s=self
		s.spt=max(s.spt-time.dt,0)
		if s.spt <= 0:
			s.spt=1
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
	def __init__(self,pos):
		s=self
		hPO=npf+'hippo/'
		super().__init__(model=hPO+'0.ply',texture=hPO+'hpo.tga',position=pos,rotation_x=rx,scale=.0005,double_sided=True,unlit=False)
		s.col=Entity(model='cube',name='HPP',position=(s.x,s.y-.15,s.z-.2),scale=(.6,.5,1),visible=False,collider='box')
		s.col.active=False
		s.active=False
		s.a_frame=0
		s.start_y=self.y
	def do_act(self):
		if not self.active:
			self.active=True
			sn.pc_audio(ID=10)
			invoke(lambda:self.dive_down(),delay=1)
	def dive_down(self):
		self.animate_y(self.start_y-1,duration=1)
		invoke(lambda:setattr(self.col,'collider',None),delay=1)
		invoke(self.dive_up,delay=3)
	def dive_up(self):
		self.animate_y(self.start_y,duration=1)
		invoke(lambda:setattr(self,'active',False),delay=3)
		invoke(lambda:setattr(self.col,'collider','box'),delay=1)
	def update(self):
		if not st.gproc():
			if self.col.active:
				self.col.active=False
				self.do_act()
				return
			if not self.active:
				animation.hippo_wait(self)
				return
			animation.hippo_dive(self)