import settings,_core,math,animation,status,sound,_loc,effect
from math import radians,cos,sin
from ursina import *

npc_folder='res/npc/'
m_SC=.8/1000
an=animation
sn=sound
cc=_core
LC=_loc

def spawn(pos,mID,mDirec,mTurn):
	npc_={0:lambda:Amadillo(p=pos,d=mDirec,t=mTurn),
		1:lambda:Turtle(p=pos,d=mDirec,t=mTurn),
		2:lambda:SawTurtle(p=pos,d=mDirec,t=mTurn),
		3:lambda:Penguin(p=pos,d=mDirec,t=mTurn),
		4:lambda:Hedgehog(p=pos,d=mDirec,t=mTurn),
		5:lambda:Seal(p=pos,d=mDirec,t=mTurn),
		6:lambda:EatingPlant(p=pos,d=mDirec,t=mTurn),
		7:lambda:Rat(p=pos,d=mDirec,t=mTurn),
		8:lambda:Lizard(p=pos,d=mDirec,t=mTurn),
		9:lambda:Scrubber(p=pos,d=mDirec,t=mTurn),
		10:lambda:Mouse(p=pos,d=mDirec,t=mTurn),
		11:lambda:Vulture(p=pos,d=mDirec,t=mTurn)}
	npc_[mID]()

## Enemies
class Amadillo(Entity):
	def __init__(self,p,d,t):
		nN='amadillo'
		self.vnum=0
		super().__init__(model=npc_folder+nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(500,700,300))
		cc.set_val_npc(self)
		self.m_direction=d
		self.move_speed=1
		self.turn=t
	def update(self):
		if not status.gproc():
			an.npc_walking(self)
			cc.npc_action(self)

class Turtle(Entity):
	def __init__(self,p,d,t):
		nN='turtle'
		self.vnum=1
		super().__init__(model=npc_folder+nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,600,300))
		cc.set_val_npc(self)
		self.m_direction=d
		self.move_speed=.7
		self.turn=t
	def update(self):
		if not status.gproc():
			an.npc_walking(self)
			cc.npc_action(self)

class SawTurtle(Entity):
	def __init__(self,p,d,t):
		nN='saw_turtle'
		self.vnum=2
		super().__init__(model=npc_folder+nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,600,300))
		self.def_mode=True
		cc.set_val_npc(self)
		self.m_direction=d
		self.move_speed=1
		self.turn=t
	def update(self):
		if not status.gproc():
			an.npc_walking(self)
			cc.npc_action(self)

class Penguin(Entity):
	def __init__(self,p,d,t):
		nN='penguin'
		self.vnum=3
		super().__init__(model=npc_folder+nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,300,800))
		cc.set_val_npc(self)
		self.m_direction=d
		self.move_speed=1.1
		self.turn=t
	def update(self):
		if not status.gproc():
			an.npc_walking(self)
			cc.npc_action(self)

class Hedgehog(Entity):
	def __init__(self,p,d,t):
		nN='hedgehog'
		self.vnum=4
		super().__init__(model=npc_folder+nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC/1.5,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,300,300))
		self.def_mode=False
		cc.set_val_npc(self)
		self.m_direction=d
		self.move_speed=1.1
		self.def_frame=0
		self.turn=t
	def anim_act(self):
		an.hedge_defend(self)
	def update(self):
		if not status.gproc():
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
		self.vnum=5
		super().__init__(model=npc_folder+nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,800,300))
		cc.set_val_npc(self)
		self.m_direction=d
		self.move_speed=1.1
		self.n_snd=False
		self.turn=t
	def update(self):
		if not status.gproc() and self.visible:
			cc.npc_action(self)
			if not self.n_snd and distance(self,LC.ACTOR) < 1:
				self.n_snd=True
				sn.npc_audio(ID=3,pit=random.uniform(.36,.38))
				invoke(lambda:setattr(self,'n_snd',False),delay=random.choice([1,1.5,1.2]))

class EatingPlant(Entity):
	def __init__(self,p,d,t):
		nN='eating_plant'
		self.vnum=6
		super().__init__(model=npc_folder+nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(400,400,1200))
		self.m_direction=0
		self.ta=LC.ACTOR
		cc.set_val_npc(self)
		self.atk_frame=0
		self.eat=False
	def action(self):
		dc=distance(self,self.ta)
		if dc < 3:
			cc.rotate_to_crash(self)
			if dc <= 1 and not self.eat:
				if not (self.ta.is_attack or self.ta.jumping):
					_core.get_damage(LC.ACTOR)
				self.eat=True
				sn.npc_audio(ID=0)
				invoke(lambda:setattr(self,'eat',False),delay=1)
	def update(self):
		if not status.gproc():
			if self.is_hitten:
				cc.fly_away(self)
				return
			if self.eat:
				an.plant_bite(self)
				return
			self.atk_frame=0
			an.npc_walking(self)
			self.action()

class Rat(Entity):
	def __init__(self,p,d,t):
		nN='rat'
		self.vnum=7
		super().__init__(model=npc_folder+nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,300,400))
		cc.set_val_npc(self)
		self.m_direction=d
		self.move_speed=.25
		self.snd_time=1
		self.turn=t
	def update(self):
		if not status.gproc():
			cc.npc_action(self)
			if distance(self,LC.ACTOR) < 2:
				cc.rotate_to_crash(self)
				self.snd_time=max(self.snd_time-time.dt,0)
				if self.snd_time <= 0:
					self.snd_time=random.choice([1,1.5,1.2])
					sn.npc_audio(ID=4,pit=random.uniform(.7,.8))

class Lizard(Entity):
	def __init__(self,p,d,t):
		nN='lizard'
		self.vnum=8
		super().__init__(model=npc_folder+nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(500,500,1100))
		cc.set_val_npc(self)
		self.m_direction=d
		self.move_speed=1.3
		self.spawn_pos=p
		self.turn=t
	def update(self):
		if not status.gproc():cc.npc_action(self)

class Scrubber(Entity):
	def __init__(self,p,d,t):
		nN='scrubber'
		self.vnum=9
		super().__init__(model=npc_folder+nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,600,300))
		self.n_snd=Audio(sn.SND_NPC[1],volume=0,loop=True)
		self.ro_mode=True
		cc.set_val_npc(self)
		self.move_speed=1.2
		self.m_direction=d
		self.turn=t
		self.angle=0
	def update(self):
		if not status.gproc() and self.visible:
			cc.npc_action(self)
			if (self.is_hitten or self.is_purge):
				self.n_snd.fade_out()
				return
			if distance(self,LC.ACTOR) < 2:
				self.n_snd.volume=settings.SFX_VOLUME
				return
			self.n_snd.volume=0

class Mouse(Entity):
	def __init__(self,p,d,t):
		nN='mouse'
		self.vnum=10
		super().__init__(model=npc_folder+nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,600,300))
		self.n_snd=Audio(sound.snd_mouse,volume=0,loop=True)
		cc.set_val_npc(self)
		self.m_direction=d
		self.move_speed=1.2
		self.snd_time=.5
		self.turn=t
	def update(self):
		if not status.gproc() and self.visible:
			cc.npc_action(self)
			if (self.is_hitten or self.is_purge):
				self.n_snd.fade_out()
				cc.purge_instance(self.n_snd)
				return
			if distance(self,LC.ACTOR) < 2:
				self.n_snd.volume=1
				return
			self.n_snd.volume=0

class Vulture(Entity):
	def __init__(self,p,d,t):
		nN='vulture'
		self.vnum=11
		super().__init__(model=npc_folder+nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+400),size=Vec3(300,600,300))
		self.target=LC.ACTOR
		cc.set_val_npc(self)
		self.move_speed=1.2
		self.m_direction=d
		self.turn=t
	def wait_on_player(self):
		pv=abs(self.target.y-self.y)
		pd=distance_xz(self.target,self)
		if pv < 2 and pd < 2:
			self.x=self.target.x
			self.y=self.target.y
	def update(self):
		if not status.gproc():
			if not self.is_hitten:
				self.wait_on_player()
			cc.npc_action(self)

## passive NPC
class AkuAkuMask(Entity):
	def __init__(self,pos):
		self.tpa='res/npc/akuaku/'
		super().__init__(model=None,texture=None,scale=.00075,rotation_x=-90,position=pos,unlit=False)
		self.ta=LC.ACTOR
		status.aku_exist=True
		self.change_skin()
		self.spt=.5
	def change_skin(self):
		if status.aku_hit > 1:
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
		if status.aku_hit < 3:
			self.position=lerp(self.position,(TG.x-.25,TG.y+.6,TG.z-.4),aSP)
			return
		fwd=Vec3(-sin(radians(TG.rotation_y)),0,-cos(radians(TG.rotation_y)))
		mask_pos=TG.position+fwd*.25
		self.position=(mask_pos.x,TG.y+.6,mask_pos.z)
	def check_dist_player(self):
		if distance(self,self.ta) > 3:self.position=self.ta.position
	def update(self):
		if not status.gproc() and LC.ACTOR != None:
			self.check_dist_player()
			self.follow_player()
			self.change_skin()
			if status.aku_hit < 1:
				status.aku_exist=False
				cc.purge_instance(self)

class Hippo(Entity):
	def __init__(self,pos):
		hPO=npc_folder+'hippo/'
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
		if not status.gproc():
			if self.col.active:
				self.col.active=False
				self.do_act()
				return
			if not self.active:
				animation.hippo_wait(self)
				return
			animation.hippo_dive(self)