import settings,_core,math,animation,status,sound,_loc
from math import radians,cos,sin
from ursina import *

npc_folder='res/npc/'
m_SC=0.8/1000
an=animation
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

def walk_frames(m):
	an.npc_walking(m)

## Enemies
class Amadillo(Entity):
	def __init__(self,p,d,t):
		nN='amadillo'
		super().__init__(model=npc_folder+nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(500,700,300))
		cc.set_val_npc(self)
		self.m_direction=d
		self.move_speed=1
		self.spawn_pos=p
		self.vnum=0
		self.turn=t
	def update(self):
		cc.npc_action(self)

class Turtle(Entity):
	def __init__(self,p,d,t):
		nN='turtle'
		super().__init__(model=npc_folder+nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,600,300))
		cc.set_val_npc(self)
		self.m_direction=d
		self.move_speed=.7
		self.spawn_pos=p
		self.vnum=1
		self.turn=t
	def update(self):
		cc.npc_action(self)

class SawTurtle(Entity):
	def __init__(self,p,d,t):
		nN='saw_turtle'
		super().__init__(model=npc_folder+nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,600,300))
		self.def_mode=True
		cc.set_val_npc(self)
		self.m_direction=d
		self.move_speed=1
		self.spawn_pos=p
		self.vnum=2
		self.turn=t
	def update(self):
		cc.npc_action(self)

class Penguin(Entity):
	def __init__(self,p,d,t):
		nN='penguin'
		super().__init__(model=npc_folder+nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,300,800))
		cc.set_val_npc(self)
		self.m_direction=d
		self.move_speed=1.1
		self.spawn_pos=p
		self.vnum=3
		self.turn=t
	def update(self):
		cc.npc_action(self)

class Hedgehog(Entity):
	def __init__(self,p,d,t):
		nN='hedgehog'
		super().__init__(model=npc_folder+nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC/1.5,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,300,300))
		self.def_mode=False
		cc.set_val_npc(self)
		self.m_direction=d
		self.move_speed=1.1
		self.spawn_pos=p
		self.def_frame=0
		self.vnum=4
		self.turn=t
	def anim_act(self):
		an.hedge_defend(self)
	def update(self):
		if status.pause:
			return
		cc.npc_action(self)
		if cc.is_nearby_pc(self,DX=2,DY=2):
			self.defend_mode=True
			self.anim_act()
		else:
			self.defend_mode=False

class Seal(Entity):
	def __init__(self,p,d,t):
		nN='seal'
		super().__init__(model=npc_folder+nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,800,300))
		cc.set_val_npc(self)
		self.m_direction=d
		self.move_speed=1.1
		self.spawn_pos=p
		self.snd_time=1
		self.vnum=5
		self.turn=t
	def update(self):
		if status.pause:
			return
		if self.snd_time > 0:
			self.snd_time-=time.dt
		cc.npc_action(self)
		if self.snd_time <= 0 and cc.is_nearby_pc(self,DX=1,DY=1):
			self.snd_time=random.choice([1,1.5,1.2])
			Audio(sound.snd_seal,pitch=random.uniform(.36,.38))

class EatingPlant(Entity):
	def __init__(self,p,d,t):
		nN='eating_plant'
		super().__init__(model=npc_folder+nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(400,400,1200))
		self.is_attacking=False
		self.is_bite=False
		self.ta=LC.ACTOR
		cc.set_val_npc(self)
		self.m_direction=d
		self.move_speed=10
		self.spawn_pos=p
		self.atk_frame=0
		self.atk_wait=0
		self.vnum=6
		self.turn=t
	def wait_on_player(self):
		if cc.is_nearby_pc(self,DX=2,DY=2):
			cc.rotate_to_crash(self)
		if cc.is_nearby_pc(self,DX=.75,DY=1) and self.atk_wait <= 0:
			if not self.is_bite:
				self.is_bite=True
				Audio(sound.snd_eating_plant)
		if self.atk_wait > 0:
			self.atk_wait-=time.dt
		if self.is_bite:
			an.plant_bite(self)
			if cc.is_nearby_pc(self,DX=.75,DY=1):
				if self.ta.is_attack or status.p_in_air(self.ta):
					return
				cc.get_damage(self.ta)
	def update(self):
		if not status.gproc() and self.visible and LC.ACTOR != None:
			if self.is_purge:
				cc.npc_purge(self)
				return
			if self.is_hitten:
				self.collider=None
				cc.fly_away(self)
				return
			self.wait_on_player()
			if not self.is_attacking:
				an.npc_walking(self)

class Rat(Entity):
	def __init__(self,p,d,t):
		nN='rat'
		super().__init__(model=npc_folder+nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,300,400))
		cc.set_val_npc(self)
		self.m_direction=d
		self.move_speed=.25
		self.spawn_pos=p
		self.snd_time=1
		self.vnum=7
		self.turn=t
	def update(self):
		if not status.gproc() and self.visible and LC.ACTOR != None:
			cc.npc_action(self)
			if cc.is_nearby_pc(self,DX=2,DY=2):
				cc.rotate_to_crash(self)
				if self.snd_time <= 0:
					self.snd_time=random.choice([1,1.5,1.2])
					Audio(sound.snd_rat,pitch=random.uniform(.7,.8))
			if self.snd_time > 0:
				self.snd_time-=time.dt

class Lizard(Entity):
	def __init__(self,p,d,t):
		nN='lizard'
		super().__init__(model=npc_folder+nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(500,500,1100))
		cc.set_val_npc(self)
		self.m_direction=d
		self.move_speed=1.3
		self.spawn_pos=p
		self.vnum=8
		self.turn=t
	def update(self):
		cc.npc_action(self)

class Scrubber(Entity):
	def __init__(self,p,d,t):
		nN='scrubber'
		super().__init__(model=npc_folder+nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,600,300))
		self.n_snd=Audio(sound.snd_scrubber,volume=0,loop=True)
		self.ro_mode=True
		cc.set_val_npc(self)
		self.move_speed=1.2
		self.m_direction=d
		self.spawn_pos=p
		self.vnum=9
		self.turn=t
		self.angle=0
	def update(self):
		if not status.pause:
			cc.npc_action(self)
		if self.is_hitten or self.is_purge:
			self.n_snd.fade_out()
		if cc.is_nearby_pc(self,DX=2,DY=2):
			self.n_snd.volume=1
			return
		self.n_snd.volume=0

class Mouse(Entity):
	def __init__(self,p,d,t):
		nN='mouse'
		super().__init__(model=npc_folder+nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,600,300))
		self.n_snd=Audio(sound.snd_mouse,volume=0,loop=True)
		cc.set_val_npc(self)
		self.m_direction=d
		self.move_speed=1.2
		self.snd_time=.5
		self.spawn_pos=p
		self.vnum=10
		self.turn=t
	def update(self):
		if not status.pause:
			cc.npc_action(self)
		if self.is_hitten or self.is_purge:
			self.n_snd.fade_out()
		if cc.is_nearby_pc(self,DX=2,DY=1):
			self.n_snd.volume=1
			return
		self.n_snd.volume=0

class Vulture(Entity):
	def __init__(self,p,d,t):
		nN='vulture'
		super().__init__(model=npc_folder+nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+400),size=Vec3(300,600,300))
		self.target=_core.playerInstance
		cc.set_val_npc(self)
		self.move_speed=1.2
		self.m_direction=d
		self.spawn_pos=p
		self.vnum=11
		self.turn=t
	def wait_on_player(self):
		pv=abs(self.target.y-self.y)
		pd=distance_xz(self.target,self)
		if pv < 2 and pd < 2:
			self.x=self.target.x
			self.y=self.target.y
	def update(self):
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
	def change_skin(self):
		if status.aku_hit > 1:
			self.model=self.tpa+'aku2.ply'
			self.texture=self.tpa+'aku2.tga'
			return
		self.model=self.tpa+'aku.ply'
		self.texture=self.tpa+'aku.tga'
	def follow_player(self):
		TG=self.ta
		aSP=time.dt*4
		self.rotation_y=lerp(self.rotation_y,TG.rotation_y,aSP)
		if status.aku_hit < 3:
			self.position=lerp(self.position,(TG.x-.25,TG.y+.6,TG.z-.4),aSP)
		else:
			fwd=Vec3(-sin(radians(TG.rotation_y)),0,-cos(radians(TG.rotation_y)))
			mask_pos=TG.position+fwd*.25
			self.position=(mask_pos.x,TG.y+.6,mask_pos.z)
	def check_dist_player(self):
		if not cc.is_nearby_pc(self,DX=3,DY=3):
			self.position=self.ta.position
	def update(self):
		if not status.gproc() and LC.ACTOR != None:
			self.check_dist_player()
			self.follow_player()
			self.change_skin()
			if status.aku_hit < 1:
				status.aku_exist=False
				self.disable()

class Hippo(Entity):
	def __init__(self,pos):
		hPO=npc_folder+'hippo/'
		super().__init__(model=hPO+'0.ply',texture=hPO+'hpo.tga',position=pos,rotation_x=-90,scale=.0005,double_sided=True,unlit=False)
		self.col=Entity(model='cube',name='HPP',position=(self.x,self.y-.15,self.z-.2),scale=(.6,.5,1),alpha=.5,collider='box',visible=False)
		self.up_y=self.y
		self.down_y=self.y-.5
		self.active=False
		self.p_aud=False
		self.is_uw=False
		self.a_frame=0
		self.uw_time=0
	def underwtr(self):
		if self.uw_time < 3:
			self.uw_time+=time.dt
		if self.uw_time >= 3:
			self.y+=time.dt/2
			if self.y >= self.up_y:
				self.col.collider='box'
				self.active=False
				self.is_uw=False
				self.p_aud=False
				self.a_frame=0
				self.uw_time=0
	def dive_down(self):
		if not self.p_aud:
			self.p_aud=True
			Audio(sound.snd_wtrl,volume=settings.SFX_VOLUME)
			invoke(lambda:Audio(sound.snd_bubbl,volume=settings.SFX_VOLUME),delay=.3)
		if self.a_frame > 40:
			self.col.collider=None
			self.y-=time.dt/2
			if self.y <= self.down_y:
				self.active=False
	def update(self):
		if not status.gproc() and self.visible and LC.ACTOR != None:
			if not self.active:
				if cc.is_nearby_pc(self,DX=.35,DY=.4):
					self.active=True
			else:
				if self.is_uw:
					self.underwtr()
				else:
					self.dive_down()
					animation.hippo_dive(self)
				return
			animation.hippo_wait(self)