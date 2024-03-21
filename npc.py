import settings,_core,math,animation,status,sound
from ursina import *

npc_list=['amadillo','turtle','saw_turtle','penguin','seal','eating_plant','rat','mouse','scrubber','vulture','hedgehog','lizard']
npc_folder='res/npc/'
m_SC=0.8/1000
an=animation
cc=_core

def spawn(pos,mID,mDirec,mTurn):
	npc_list={0:lambda:Amadillo(p=pos,d=mDirec,t=mTurn),
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
	npc_list[mID]()

class Amadillo(Entity):
	def __init__(self,p,d,t):
		nN='amadillo'
		super().__init__(model=nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,600,300))
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
		super().__init__(model=nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
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
		super().__init__(model=nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,600,300))
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
		super().__init__(model=nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
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
		super().__init__(model=nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC/1.5,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,300,300))
		self.is_defend_mode=False
		cc.set_val_npc(self)
		self.m_direction=d
		self.move_speed=1.1
		self.spawn_pos=p
		self.def_frame=0
		self.vnum=4
		self.turn=t
	def update(self):
		if status.pause:
			return
		if cc.is_nearby_pc(self,DX=2,DY=2):
			self.defend_mode=True
		else:
			self.defend_mode=False
		cc.npc_action(self)

class Seal(Entity):
	def __init__(self,p,d,t):
		nN='seal'
		super().__init__(model=nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
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
		super().__init__(model=nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(400,400,1200))
		self.target=_core.playerInstance[0]
		self.is_attacking=False
		self.is_bite=False
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
		if cc.is_nearby_pc(self,DX=1,DY=1) and self.atk_wait <= 0:
			if not self.is_bite:
				self.is_bite=True
				Audio(sound.snd_eating_plant)
		if self.atk_wait > 0:
			self.atk_wait-=time.dt
		if self.is_bite:
			an.plant_bite(self)
			if cc.is_nearby_pc(self,DX=1,DY=1):
				if not self.target.is_attack:
					cc.get_damage(self.target)
	def update(self):
		if status.pause:
			return
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
		super().__init__(model=nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,300,400))
		self.target=_core.playerInstance[0]
		cc.set_val_npc(self)
		self.m_direction=d
		self.move_speed=.25
		self.spawn_pos=p
		self.snd_time=1
		self.vnum=7
		self.turn=t
	def update(self):
		if status.pause:
			return
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
		super().__init__(model=nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
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
		super().__init__(model=nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+200),size=Vec3(300,600,300))
		self.n_snd=Audio(sound.snd_scrubber,volume=0,loop=True)
		cc.set_val_npc(self)
		self.move_speed=1.2
		self.m_direction=d
		self.spawn_pos=p
		self.vnum=9
		self.turn=t
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
		super().__init__(model=nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
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
		super().__init__(model=nN+'/'+nN+'.ply',texture=npc_folder+nN+'/'+nN+'.tga',rotation_x=-90,scale=m_SC,position=p)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+400),size=Vec3(300,600,300))
		self.target=_core.playerInstance[0]
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

class AkuAkuMask(Entity):
	def __init__(self,pos):
		self.tpa='res/npc/akuaku/'
		super().__init__(model=self.tpa+'aku.ply',texture=self.tpa+'aku.tga',scale=0.00075,rotation_x=-90,position=pos,unlit=False)
		self.aku_model={0:self.tpa+'aku.ply',1:self.tpa+'aku.ply',2:self.tpa+'aku2.ply',3:self.tpa+'aku2.ply'}
		self.aku_texture={0:self.tpa+'aku.tga',1:self.tpa+'aku.tga',2:self.tpa+'aku2.tga',3:self.tpa+'aku2.tga'}
		self.aku_direct=0
		self.target=_core.playerInstance[0]
		status.aku_exist=True
	def follow_player(self):
		self.rotation_y=self.target.rotation_y
		self.x=self.target.x-.25
		self.z=self.target.z-.4
	def floating(self):
		ttf=time.dt/5
		if self.aku_direct == 1:
			self.y+=ttf
			if self.y > self.target.aku_y+.4:
				self.aku_direct=0
		if self.aku_direct == 0:
			self.y-=ttf
			if self.y < self.target.aku_y-.1:
				self.aku_direct=1
	def update(self):
		if status.pause:
			return
		self.model=self.aku_model[status.aku_hit]
		self.texture=self.aku_texture[status.aku_hit]
		self.floating()
		self.follow_player()
		if status.aku_hit < 1:
			status.aku_exist=False
			self.disable()
