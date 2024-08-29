import settings,_core,math,animation,status,sound,_loc,effect
from math import radians,cos,sin
from ursina import *

npf='res/npc/'
m_SC=.8/1000
an=animation
sn=sound
cc=_core
LC=_loc
st=status

def spawn(pos,mID,mDirec,mTurn,ro_mode=0):
	npc_={0:lambda:Amadillo(p=pos,d=mDirec,t=mTurn),
		1:lambda:Turtle(p=pos,d=mDirec,t=mTurn),
		2:lambda:SawTurtle(p=pos,d=mDirec,t=mTurn),
		3:lambda:Vulture(p=pos,d=mDirec,t=mTurn),
		4:lambda:Penguin(p=pos,d=mDirec,t=mTurn),
		5:lambda:Hedgehog(p=pos,d=mDirec,t=mTurn),
		6:lambda:Seal(p=pos,d=mDirec,t=mTurn),
		7:lambda:EatingPlant(p=pos,d=mDirec,t=mTurn),
		8:lambda:Rat(p=pos,d=mDirec,t=mTurn),
		9:lambda:Lizard(p=pos,d=mDirec,t=mTurn),
		10:lambda:Scrubber(p=pos,d=mDirec,t=mTurn,ro=ro_mode),
		11:lambda:Mouse(p=pos,d=mDirec,t=mTurn,ro=ro_mode),
		12:lambda:Eel(p=pos,d=mDirec,t=mTurn),
		13:lambda:SewerMine(p=pos,d=mDirec,t=mTurn)}
	npc_[mID]()

## Enemies
class Amadillo(Entity):
	def __init__(self,p,d,t):
		nN='amadillo'
		self.vnum=0
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(500,700,300))
		cc.set_val_npc(self,tu=t,di=d)
		self.move_speed=1
	def update(self):
		if not st.gproc():
			an.npc_walking(self)
			cc.npc_action(self)

class Turtle(Entity):
	def __init__(self,p,d,t):
		nN='turtle'
		self.vnum=1
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,600,300))
		cc.set_val_npc(self,tu=t,di=d)
		self.move_speed=.7
	def update(self):
		if not st.gproc():
			an.npc_walking(self)
			cc.npc_action(self)

class SawTurtle(Entity):
	def __init__(self,p,d,t):
		nN='saw_turtle'
		self.vnum=2
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,600,300))
		cc.set_val_npc(self,tu=t,di=d)
		self.def_mode=True
		self.move_speed=1
	def update(self):
		if not st.gproc():
			an.npc_walking(self)
			cc.npc_action(self)

class Vulture(Entity):
	def __init__(self,p,d,t):
		nN='vulture'
		self.vnum=3
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+400),size=Vec3(300,600,300))
		cc.set_val_npc(self,tu=t,di=d)
		self.target=LC.ACTOR
		self.move_speed=1.2
	def wait_on_player(self):
		pv=abs(self.target.y-self.y)
		pd=distance_xz(self.target,self)
		if pv < 2 and pd < 2:
			self.x=self.target.x
			self.y=self.target.y
	def update(self):
		if not st.gproc():
			if not self.is_hitten:
				self.wait_on_player()
			cc.npc_action(self)

class Penguin(Entity):
	def __init__(self,p,d,t):
		nN='penguin'
		self.vnum=4
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,300,800))
		cc.set_val_npc(self,tu=t,di=d)
		self.move_speed=1.1
	def update(self):
		if not st.gproc():
			an.npc_walking(self)
			cc.npc_action(self)

class Hedgehog(Entity):
	def __init__(self,p,d,t):
		nN='hedgehog'
		self.vnum=5
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC/1.5,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,300,300))
		cc.set_val_npc(self,tu=t,di=d)
		self.def_mode=False
		self.move_speed=1.1
		self.def_frame=0
	def anim_act(self):
		an.hedge_defend(self)
	def update(self):
		if not st.gproc():
			an.npc_walking(self)
			cc.npc_action(self)
			if distance(self,LC.ACTOR) < 2:
				self.defend_mode=True
				self.anim_act()
				return
			self.defend_mode=False

class Seal(Entity):
	def __init__(self,p,d,t):
		nN='seal'
		self.vnum=6
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,800,300))
		cc.set_val_npc(self,tu=t,di=d)
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
	def __init__(self,p,d,t):
		nN='eating_plant'
		self.vnum=7
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(400,400,1200))
		cc.set_val_npc(self,tu=t,di=d)
		self.m_direction=0
		self.ta=LC.ACTOR
		self.atk_frame=0
		self.eat_frame=0
		self.atk=False
		self.eat=False
	def action(self):
		dc=distance(self,self.ta)
		if dc < 3:
			cc.rotate_to_crash(self)
			if dc <= 1 and not self.atk:
				if st.death_event:
					return
				self.atk=True
				sn.npc_audio(ID=0)
				if not (self.ta.is_attack or self.ta.jumping):
					if status.aku_hit < 1:
						self.eat=True
					_core.get_damage(LC.ACTOR,rsn=5)
				invoke(lambda:setattr(self,'atk',False),delay=1)
	def update(self):
		if not st.gproc():
			if self.is_hitten:
				cc.fly_away(self)
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
	def __init__(self,p,d,t):
		nN='rat'
		self.vnum=8
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,size=Vec3(500,500,300))
		cc.set_val_npc(self,tu=t,di=d)
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
	def __init__(self,p,d,t):
		nN='lizard'
		self.vnum=9
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(500,500,1100))
		cc.set_val_npc(self,tu=t,di=d)
		self.move_speed=1.3
		self.spawn_pos=p
	def update(self):
		if not st.gproc():
			an.npc_walking(self)
			cc.npc_action(self)

class Scrubber(Entity):
	def __init__(self,p,d,t,ro):
		nN='scrubber'
		self.vnum=10
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,600,300))
		cc.set_val_npc(self,tu=t,di=d)
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
	def __init__(self,p,d,t,ro):
		nN='mouse'
		self.vnum=11
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,size=Vec3(500,700,500))
		cc.set_val_npc(self,tu=t,di=d)
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
	def __init__(self,p,d,t):
		nN='eel'
		self.vnum=12
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/0.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,size=Vec3(500,700,500))
		cc.set_val_npc(self,tu=t,di=d)
	def update(self):
		if not st.gproc():
			cc.npc_action(self)
			an.npc_walking(self)
			if distance(self,LC.ACTOR) < 2:
				self.x=lerp(self.x,LC.ACTOR.x,time.dt*2)

class SewerMine(Entity):
	def __init__(self,p,d,t):
		nN='sewer_mine'
		self.vnum=13
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,size=Vec3(500,700,500))
		cc.set_val_npc(self,tu=t,di=d)
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

## passive NPC
class AkuAkuMask(Entity):
	def __init__(self,pos):
		self.tpa='res/npc/akuaku/'
		super().__init__(model=None,texture=None,scale=.00075,rotation_x=-90,position=pos,unlit=False)
		self.ta=LC.ACTOR
		st.aku_exist=True
		self.change_skin()
		self.spt=.5
	def change_skin(self):
		if st.aku_hit > 1:
			self.model=self.tpa+'aku2.ply'
			self.texture=self.tpa+'aku2.tga'
			self.spark()
			return
		self.model=self.tpa+'aku.ply'
		self.texture=self.tpa+'aku.tga'
	def spark(self):
		self.spt=max(self.spt-time.dt,0)
		if self.spt == 0:
			self.spt=1
			effect.Sparkle((self.x+random.uniform(-.1,.1),self.y+random.uniform(-.1,.1),self.z+random.uniform(-.1,.1)))
	def follow_player(self):
		TG=self.ta
		aSP=time.dt*4
		self.rotation_y=lerp(self.rotation_y,TG.rotation_y,aSP)
		if st.aku_hit < 3:
			self.position=lerp(self.position,(TG.x-.25,TG.y+.6,TG.z-.4),aSP)
			return
		fwd=Vec3(-sin(radians(TG.rotation_y)),0,-cos(radians(TG.rotation_y)))
		mask_pos=TG.position+fwd*.25
		self.position=(mask_pos.x,TG.y+.6,mask_pos.z)
	def check_dist_player(self):
		if distance(self,self.ta) > 3:self.position=self.ta.position
	def update(self):
		if not st.gproc() and LC.ACTOR != None:
			self.check_dist_player()
			self.follow_player()
			self.change_skin()
			if st.aku_hit < 1:
				st.aku_exist=False
				cc.purge_instance(self)

class Hippo(Entity):
	def __init__(self,pos):
		hPO=npf+'hippo/'
		super().__init__(model=hPO+'0.ply',texture=hPO+'hpo.tga',position=pos,rotation_x=-90,scale=.0005,double_sided=True,unlit=False)
		self.col=Entity(model='cube',name='HPP',position=(self.x,self.y-.15,self.z-.2),scale=(.6,.5,1),visible=False,collider='box')
		self.col.active=False
		self.active=False
		self.a_frame=0
		self.start_y=self.y
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