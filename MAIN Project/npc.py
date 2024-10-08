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
		s=self
		nN='amadillo'
		s.vnum=0
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=p)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+200),size=Vec3(500,700,300))
		cc.set_val_npc(s,di=d)
		s.move_speed=1
	def update(self):
		if not st.gproc():
			an.npc_walking(self)
			cc.npc_action(self)

class Turtle(Entity):
	def __init__(self,p,d):
		s=self
		nN='turtle'
		s.vnum=1
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=p)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+200),size=Vec3(300,600,300))
		cc.set_val_npc(s,di=d)
		s.move_speed=.7
	def update(self):
		if not st.gproc():
			an.npc_walking(self)
			cc.npc_action(self)

class SawTurtle(Entity):
	def __init__(self,p,d):
		s=self
		nN='saw_turtle'
		s.vnum=2
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=p)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+200),size=Vec3(300,600,300))
		cc.set_val_npc(s,di=d)
		s.def_mode=True
		s.move_speed=1
	def update(self):
		if not st.gproc():
			an.npc_walking(self)
			cc.npc_action(self)

class Vulture(Entity):
	def __init__(self,p,d):
		s=self
		nN='vulture'
		s.vnum=3
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=p)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+400),size=Vec3(300,600,300))
		cc.set_val_npc(s,di=d)
		s.target=LC.ACTOR
		s.move_speed=1.2
	def wait_on_player(self):
		s=self
		an.npc_walking(s)
		if distance_xz(s.target,s) < 2:
			s.x=s.target.x
	def update(self):
		if not st.gproc():
			s=self
			if not s.is_hitten:
				s.wait_on_player()
			cc.npc_action(s)

class Penguin(Entity):
	def __init__(self,p,d):
		s=self
		nN='penguin'
		s.vnum=4
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=.8/1100,position=p)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+400),size=Vec3(300,300,600))
		cc.set_val_npc(s,di=d)
		s.move_speed=1.1
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
		s=self
		nN='seal'
		s.vnum=6
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=p)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+200),size=Vec3(300,800,300))
		cc.set_val_npc(s,di=d)
		s.move_speed=1.1
		s.n_snd=False
	def update(self):
		s=self
		if not st.gproc() and s.visible:
			cc.npc_action(s)
			an.npc_walking(s)
			if not s.n_snd and distance(s,LC.ACTOR) < 1:
				s.n_snd=True
				sn.npc_audio(ID=3,pit=random.uniform(.36,.38))
				invoke(lambda:setattr(s,'n_snd',False),delay=random.choice([1,1.5,1.2]))

class EatingPlant(Entity):
	def __init__(self,p,d):
		s=self
		nN='eating_plant'
		s.vnum=7
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=.8/900,position=p)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+500),size=Vec3(400,400,700))
		cc.set_val_npc(s,di=d)
		s.m_direction=0
		s.ta=LC.ACTOR
		s.atk_frame=0
		s.eat_frame=0
		s.atk=False
		s.eat=False
	def action(self):
		s=self
		dc=distance(s,s.ta)
		if dc < 3:
			cc.rotate_to_crash(s)
			if dc <= 1.2 and not s.atk:
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
			s=self
			if s.is_hitten:
				cc.fly_away(s)
				return
			if s.is_purge:
				cc.npc_purge(s)
				return
			if not s.eat:
				if s.atk:
					an.plant_bite(s)
				else:
					s.atk_frame=0
					an.npc_walking(s)
					s.action()
				return
			an.plant_eat(s)

class Rat(Entity):
	def __init__(self,p,d):
		s=self
		nN='rat'
		s.vnum=8
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=p)
		s.collider=BoxCollider(s,center=(s.x,s.y,s.z+200),size=Vec3(500,600,300))
		cc.set_val_npc(s,di=d)
		s.move_speed=.25
		s.snd_time=1
	def update(self):
		if not st.gproc():
			s=self
			cc.npc_action(s)
			an.npc_walking(s)
			if distance(s,LC.ACTOR) < 2:
				cc.rotate_to_crash(s)
				s.snd_time=max(s.snd_time-time.dt,0)
				if s.snd_time <= 0:
					s.snd_time=random.choice([1,1.5,1.2])
					sn.npc_audio(ID=4,pit=random.uniform(.7,.8))

class Lizard(Entity):
	def __init__(self,p,d):
		s=self
		nN='lizard'
		s.vnum=9
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=p)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+400),size=Vec3(500,500,700))
		cc.set_val_npc(s,di=d)
		s.move_speed=1.3
		s.spawn_pos=p
	def update(s):
		if not st.gproc():
			an.npc_walking(s)
			cc.npc_action(s)

class Scrubber(Entity):
	def __init__(self,p,d,ro):
		s=self
		nN='scrubber'
		s.vnum=10
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=p)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+350),size=Vec3(400,600,500))
		cc.set_val_npc(s,di=d)
		s.move_speed=1.2
		s.n_snd=False
		s.ro_mode=ro
		s.angle=0
	def update(self):
		if not st.gproc():
			s=self
			an.npc_walking(s)
			cc.npc_action(s)
			if not s.n_snd and distance(s,LC.ACTOR) < 3:
				s.n_snd=True
				if not (s.is_hitten or s.is_purge):
					sn.npc_audio(ID=1)
				invoke(lambda:setattr(s,'n_snd',False),delay=.7)

class Mouse(Entity):
	def __init__(self,p,d,ro):
		s=self
		nN='mouse'
		s.vnum=11
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=p)
		s.collider=BoxCollider(s,center=(s.x,s.y,s.z+150),size=Vec3(500,700,200))
		cc.set_val_npc(s,di=d)
		s.move_speed=1.2
		s.snd_time=.5
		s.n_snd=False
		s.ro_mode=ro
		s.angle=0
	def update(self):
		if not st.gproc():
			s=self
			an.npc_walking(s)
			cc.npc_action(s)
			if not s.n_snd and distance(s,LC.ACTOR) < 3:
				s.n_snd=True
				if not (s.is_hitten or s.is_purge):
					sn.npc_audio(ID=2)
				invoke(lambda:setattr(s,'n_snd',False),delay=1)

class Eel(Entity):
	def __init__(self,p,d):
		s=self
		nN='eel'
		s.vnum=12
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/0.tga',rotation_x=rx,scale=m_SC,position=p)
		s.collider=BoxCollider(s,center=(s.x,s.y,s.z+100),size=Vec3(500,700,200))
		cc.set_val_npc(s,di=d)
	def update(self):
		if not st.gproc():
			s=self
			cc.npc_action(s)
			an.npc_walking(s)
			if distance(s,LC.ACTOR) < 2:
				s.x=lerp(s.x,LC.ACTOR.x,time.dt*2)

class SewerMine(Entity):
	def __init__(self,p,d):
		s=self
		nN='sewer_mine'
		s.vnum=13
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation_x=rx,scale=m_SC,position=p)
		s.collider=BoxCollider(s,size=Vec3(500,700,500))
		cc.set_val_npc(s,di=d)
		s.move_speed=1.2
	def floating_y(self):
		s=self
		if s.turn == 0:
			s.y-=time.dt/2
			if s.y <= s.spawn_pos[1]-.8:
				s.turn=1
			return
		s.y+=time.dt/2
		if s.y > s.spawn_pos[1]+.8:
			s.turn=0
	def floating_x(self):
		s=self
		if s.turn == 0:
			s.x-=time.dt/2
			if s.x <= s.spawn_pos[0]-.8:
				s.turn=1
			return
		s.x+=time.dt/2
		if s.x > s.spawn_pos[0]+.8:
			s.turn=0
	def update(self):
		if not st.gproc():
			s=self
			an.npc_walking(s)
			if s.m_direction == 0:
				s.floating_y()
				return
			s.floating_x()

class Gorilla(Entity):
	def __init__(self,p,d):
		s=self
		nN='gorilla'
		self.vnum=14
		rmo={0:0,1:90,2:180,3:-90}
		super().__init__(model=npf+nN+'/'+nN+'.ply',texture=npf+nN+'/'+nN+'.tga',rotation=(rx,rmo[d],0),position=p,scale=m_SC)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y,s.z+450),size=Vec3(400,400,800))
		s.throw_act={0:lambda:an.gorilla_take(s),1:lambda:an.gorilla_throw(s)}
		cc.set_val_npc(s,di=d)
		s.t_sleep=.5
		s.t_mode=0
		s.f_frame=0
		s.t_frame=0
	def throw_log(self):
		s=self
		invoke(lambda:objects.LogDanger(pos=(s.x,s.y+.6,s.z),ro_y=s.rotation_y),delay=.1)
	def update(self):
		if not st.gproc():
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