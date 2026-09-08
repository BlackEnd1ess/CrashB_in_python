from ursina import BoxCollider,Vec3,Entity,Audio,distance,distance_xz,lerp,invoke,color,scene,time
import settings,_core,math,animation,status,sound,_loc,effect,random,objects
from math import radians,cos,sin,pi,degrees,atan2
from ursina.ursinastuff import destroy
from panda3d.core import NodePath
from danger import LogDanger
import gltf

npf='res/npc/'
an=animation
st=status
sn=sound
cc=_core
LC=_loc

npc_scale=.4
b='box'

def spawn(ID,POS,DRC=0,RTYP=0,RNG=1,CMV=True,MTYP=0,PTH=None):
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
	14:lambda:Gorilla(pos=POS,drc=DRC),
	15:lambda:Bee(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP,cmv=CMV,typ=MTYP),
	16:lambda:Lumberjack(pos=POS),
	17:lambda:SpiderRobot(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP,cmv=CMV,typ=MTYP),
	18:lambda:WalkerRobot(pos=POS,drc=DRC,rng=RNG,rtyp=RTYP,cmv=CMV),
	19:lambda:LabAssistant(pos=POS,drc=DRC),
	20:lambda:Frog(pos=POS,cmv=CMV,ffld=PTH)}[ID]()
	st.npc_in_level+=1
	del ID,POS,DRC,RTYP,RNG,CMV,MTYP,PTH

## Enemies
class Amadillo(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=0
		s.glb_model=f'{npf}amadillo/walk.glb'
		super().__init__(position=pos,scale=npc_scale)
		s.collider=BoxCollider(s,center=Vec3(0,.25,0),size=(.8,.5,1.5))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		an.set_glb_value(s,fps=22,sca=.0018)
		an.set_glb_color(s,col=color.white,UNLIT=True,brightness=1.25)
		s.move_speed=1
		del s,pos,drc,rng,rtyp,cmv
	def update(self):
		if st.gproc():
			return
		s=self
		if not (s.is_purge or s.is_hitten):
			an.refr_npc_animation(s)
		cc.refresh_npc_function(s)

class Turtle(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=1
		s.glb_model=f'{npf}turtle/walk.glb'
		super().__init__(position=pos,scale=npc_scale)
		s.collider=BoxCollider(s,center=Vec3(0,.25,0),size=(1.3,.5,1.8))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		an.set_glb_value(s,fps=22,sca=.0018)
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=2)
		s.move_speed=.7
		del s,pos,drc,rng,rtyp,cmv
	def update(self):
		if st.gproc():
			return
		s=self
		if not (s.is_purge or s.is_hitten):
			an.refr_npc_animation(s)
		cc.refresh_npc_function(s)

class SawTurtle(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=2
		s.glb_model=f'{npf}saw_turtle/walk.glb'
		super().__init__(position=pos,scale=npc_scale)
		s.collider=BoxCollider(s,center=Vec3(0,.25,0),size=(.8,.5,1.5))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		an.set_glb_value(s,fps=22,sca=.0018)
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=2)
		s.move_speed=1
		del s,pos,drc,rng,rtyp,cmv
	def update(self):
		if st.gproc():
			return
		s=self
		if not (s.is_purge or s.is_hitten):
			an.refr_npc_animation(s)
		cc.refresh_npc_function(s)

class Vulture(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=3
		s.glb_model=f'{npf}vulture/idle.glb'
		super().__init__(position=pos,scale=npc_scale)
		s.collider=BoxCollider(s,center=Vec3(0,1.5,0),size=(.75,.75,1.5))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		an.set_glb_value(s,fps=22,sca=.0018)
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=2)
		s.move_speed=1.2
		del s,pos,drc,rng,rtyp,cmv
	def update(self):
		if st.gproc():
			return
		s=self
		if not (s.is_purge or s.is_hitten):
			an.refr_npc_animation(s)
		cc.refresh_npc_function(s)

class Penguin(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=4
		s.lst={0:f'{npf}penguin/walk.glb',1:f'{npf}penguin/attack.glb',2:f'{npf}penguin/idle.glb'}
		super().__init__(position=pos,scale=npc_scale)
		s.collider=BoxCollider(s,center=Vec3(0,.25,0),size=(.75,1.5,.75))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		an.set_switch_glb_value(s,fps=22,sca=.0018,lst=s.lst)
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=2)
		s.is_dizzy=False
		s.is_spin=False
		s.move_speed=1.1
		s.rot_speed=800
		s.spin_time=3
		s.wait_time=3
		del s,pos,drc,rng,rtyp,cmv
	def switch_model(self,n):
		s=self
		s.root.hide()
		s.root=s.models[n]
		s.frames=s.frames_all[n]
		s.new_index=0
		s.frame_index=0
		for frame in s.frames:
			frame.hide()
		s.frames[0].show()
		s.root.show()
	def refr_function(self):
		s=self
		if s.is_dizzy:
			s.dizzy_action()
			return
		if s.is_spin:
			s.spin_attack()
			return
		s.wait_time-=time.dt
		if s.wait_time <= 0:
			s.wait_time=3
			if distance(s,LC.ACTOR) < LC.NPC_SND_DISTANCE:
				sn.npc_audio(ID=21)
			s.is_spin=True
			s.switch_model(1)
	def spin_attack(self):
		s=self
		s.rotation_y+=time.dt*s.rot_speed
		s.spin_time-=time.dt
		if s.spin_time <= 0:
			s.is_spin=False
			s.is_dizzy=True
			s.spin_time=1
			sn.npc_audio(ID=22)
			s.switch_model(2)
	def dizzy_action(self):
		s=self
		s.wait_time-=time.dt
		if s.wait_time <= 0:
			s.wait_time=3
			s.is_dizzy=False
			s.switch_model(0)
	def update(self):
		if st.gproc():
			return
		s=self
		if s.is_purge or s.is_hitten:
			cc.refresh_npc_function(s)
			return
		s.refr_function()
		if not (s.is_purge or s.is_hitten):
			an.refr_npc_animation(s)
		if not s.is_spin and not s.is_dizzy:
			cc.refresh_npc_function(s)

class Hedgehog(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=5
		s.lst={0:f'{npf}hedgehog/walk.glb',1:f'{npf}hedgehog/attack.glb'}
		super().__init__(position=pos,scale=npc_scale)
		s.collider=BoxCollider(s,center=Vec3(0,.25,0),size=(.75,.75,.75))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		an.set_switch_glb_value(s,fps=22,sca=.001,lst=s.lst)
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=2)
		s.def_mode=False
		s.move_speed=1.1
		s.def_time=5
		s.wait=0
		del s,pos,drc,rng,rtyp,cmv
	def switch_model(self,n):
		s=self
		s.root.hide()
		s.root=s.models[n]
		s.frames=s.frames_all[n]
		s.new_index=0
		s.frame_index=0
		for frame in s.frames:
			frame.hide()
		s.frames[0].show()
		s.root.show()
	def refr_function(self):
		s=self
		if not s.def_mode:
			if distance(s,LC.ACTOR) < 2:
				s.def_mode=True
				s.switch_model(1)
			return
		if s.def_time > 0:
			s.def_time-=time.dt
			if s.def_time <= 0:
				s.def_mode=False
				s.switch_model(0)
				s.def_time=5
				s.wait=3
	def update(self):
		if st.gproc():
			return
		s=self
		if not (s.is_purge or s.is_hitten):
			if not (s.def_mode and s.new_index == len(s.frames)):
				an.refr_npc_animation(s)
		cc.refresh_npc_function(s)
		if s.wait > 0:
			s.wait-=time.dt
			return
		s.refr_function()

class Seal(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=6
		s.glb_model=f'{npf}seal/walk.glb'
		super().__init__(position=pos,scale=npc_scale)
		s.collider=BoxCollider(s,center=Vec3(0,.25,0),size=(1,.8,1.5))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		an.set_glb_value(s,fps=22,sca=.0018)
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=2)
		s.move_speed=1.1
		s.n_snd=False
		s.snID=3
		s.tme=1
		del s,pos,drc,rng,rtyp,cmv
	def update(self):
		if st.gproc():
			return
		s=self
		if not (s.is_purge or s.is_hitten):
			if distance(s,LC.ACTOR) < LC.NPC_SND_DISTANCE:
				sn.npc_loop_audio(n=s,PIT=random.uniform(.36,.38),tme_r=random.uniform(1,2))
			an.refr_npc_animation(s)
		cc.refresh_npc_function(s)

class EatingPlant(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=7
		s.lst={0:f'{npf}eating_plant/idle.glb',1:f'{npf}eating_plant/attack.glb',2:f'{npf}eating_plant/eat.glb'}
		super().__init__(position=pos,scale=npc_scale,rotation_y=180)
		s.collider=BoxCollider(s,center=Vec3(0,.9,0),size=(1.3,1.8,1.3))
		an.set_switch_glb_value(s,fps=22,sca=.0024,lst=s.lst)
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=2)
		cc.set_val_npc(s)
		s.can_move=False
		s.mdl_index=0
		s.atk_pause=0
		s.atk=False
		s.eat=False
		del s,pos,drc,rng,rtyp,cmv
	def switch_model(self,n):
		s=self
		s.root.hide()
		s.root=s.models[n]
		s.frames=s.frames_all[n]
		s.new_index=0
		s.frame_index=0
		for frame in s.frames:
			frame.hide()
		s.frames[0].show()
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=2)
		s.root.show()
	def refr_func(self):
		s=self
		ddc=distance(LC.ACTOR,s)
		if ddc < 3:
			cc.rotate_to_target(s,LC.ACTOR.position)
		if ddc < 1.5:
			if s.atk_pause > 0:
				s.atk_pause-=time.dt
				return
			if not s.atk:
				s.atk=True
				sn.npc_audio(ID=0)
				s.switch_model(1)
	def npc_attack(self):
		s=self
		if distance(LC.ACTOR,s) > 1:
			return
		if not LC.ACTOR.is_attack:
			cc.get_damage(LC.ACTOR,rsn=5)
		if st.aku_hit == 0:
			if not s.eat:
				s.eat=True
				s.switch_model(2)
	def refr_anim_frame(self):
		s=self
		s.new_index+=time.dt*s.fps
		if s.new_index > len(s.frames):
			s.atk_pause=1 if s.atk or s.eat else 0
			s.new_index=0
			if s.atk:
				s.atk=False
				s.switch_model(0)
				return
			if s.eat:
				s.eat=False
				s.switch_model(0)
				return
		an.set_glb_frame(s)
	def update(self):
		if st.gproc():
			return
		s=self
		if s.is_purge or s.is_hitten:
			cc.refresh_npc_function(s)
			return
		s.refr_anim_frame()
		if st.death_event or LC.ACTOR.injured:
			return
		if s.atk:
			s.npc_attack()
			return
		s.refr_func()

class Rat(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=8
		s.glb_model=f'{npf}rat/walk.glb' if cmv else f'{npf}rat/idle.glb'
		super().__init__(position=pos,scale=npc_scale,rotation_y=180)
		s.collider=BoxCollider(s,center=Vec3(0,.25,0),size=(.8,.5,1.25))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		an.set_glb_value(s,fps=22,sca=.0018)
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=2)
		s.move_speed=1
		s.snID=4
		s.tme=1
		del s,pos,drc,rng,rtyp,cmv
	def update(self):
		if st.gproc():
			return
		s=self
		if not (s.is_purge or s.is_hitten):
			if distance(s,LC.ACTOR) < LC.NPC_SND_DISTANCE:
				sn.npc_loop_audio(n=s,PIT=random.uniform(.65,.75),tme_r=random.uniform(1,1.5))
			an.refr_npc_animation(s)
		cc.refresh_npc_function(s)

class Lizard(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=9
		s.glb_model=f'{npf}lizard/walk.glb'
		super().__init__(position=pos,scale=npc_scale)
		s.collider=BoxCollider(s,center=Vec3(0,.75,0),size=(1,1.5,1))
		an.set_glb_value(s,fps=22,sca=.0018)
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=2)
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		s.move_speed=1.2
		s.snID=11
		s.tme=1
		del s,pos,drc,rng,rtyp,cmv
	def update(self):
		if st.gproc():
			return
		s=self
		if not (s.is_purge or s.is_hitten):
			if distance(s,LC.ACTOR) < 10:
				sn.npc_loop_audio(s,PIT=random.uniform(.8,1.1),tme_r=random.uniform(.9,1.1))
			an.refr_npc_animation(s)
		cc.refresh_npc_function(s)

class Scrubber(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv,mtyp=0):
		s=self
		s.inner_pipe=False
		if mtyp == 1:
			s.inner_pipe=True
		s.vnum=10
		s.glb_model=f'{npf}scrubber/walk.glb'
		super().__init__(position=pos,scale=npc_scale)
		s.collider=BoxCollider(s,center=Vec3(0,.5,0),size=(1.25,1,1.25))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		an.set_glb_value(s,fps=22,sca=.0018)
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=1.5)
		s.move_speed=1.2
		s.angle=0
		s.snID=1
		s.tme=.5
		del s,pos,drc,rng,rtyp,cmv,mtyp
	def update(self):
		if st.gproc():
			return
		s=self
		if not (s.is_purge or s.is_hitten):
			if distance(s,LC.ACTOR) < LC.NPC_SND_DISTANCE:
				sn.npc_loop_audio(s,PIT=1,tme_r=1.5)
			an.refr_npc_animation(s)
		cc.refresh_npc_function(s)

class Mouse(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=11
		s.glb_model=f'{npf}mouse/walk.glb'
		super().__init__(position=pos,scale=npc_scale)
		s.collider=BoxCollider(s,center=Vec3(0,.25,0),size=(1.2,.5,1.5))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		an.set_glb_value(s,fps=22,sca=.0018)
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=1.5)
		s.move_speed=1.2
		s.angle=0
		s.snID=2
		s.tme=1
		del s,pos,drc,rng,rtyp,cmv
	def update(self):
		if st.gproc():
			return
		s=self
		if not (s.is_purge or s.is_hitten):
			if distance(s,LC.ACTOR) < LC.NPC_SND_DISTANCE:
				sn.npc_loop_audio(s,PIT=1,tme_r=1)
			an.refr_npc_animation(s)
		cc.refresh_npc_function(s)

class Eel(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=12
		s.glb_model=f'{npf}eel/walk.glb'
		super().__init__(position=pos,scale=npc_scale)
		s.collider=BoxCollider(s,center=Vec3(0,.3,0),size=(.5,.5,1.8))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		an.set_glb_value(s,fps=22,sca=.0018)
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=2)
		s.move_speed=1
		del s,pos,drc,rng,rtyp,cmv
	def update(self):
		if st.gproc():
			return
		s=self
		if not (s.is_purge or s.is_hitten):
			an.refr_npc_animation(s)
		cc.refresh_npc_function(s)

class SewerMine(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=13
		s.glb_model=f'{npf}sewer_mine/walk.glb'
		super().__init__(position=pos,scale=npc_scale)
		s.collider=BoxCollider(s,center=Vec3(0,0,0),size=(1,1,1))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		an.set_glb_value(s,fps=22,sca=.0018)
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=2)
		s.move_speed=.75
		del s,pos,drc,rng,rtyp,cmv
	def update(self):
		if st.gproc():
			return
		s=self
		if not (s.is_purge or s.is_hitten):
			an.refr_npc_animation(s)
		cc.refresh_npc_function(s)

class Gorilla(Entity):
	def __init__(self,pos,drc):
		s=self
		s.vnum=14
		s.lst={0:f'{npf}gorilla/0.glb',1:f'{npf}gorilla/1.glb',2:f'{npf}gorilla/2.glb'}
		super().__init__(position=pos,rotation_y={0:0,1:90,2:180,3:-90}[drc],scale=npc_scale)
		s.collider=BoxCollider(s,center=Vec3(0,1,0),size=(1.25,2,1.25))
		cc.set_val_npc(s,drc)
		an.set_switch_glb_value(s,fps=22,sca=.0018,lst=s.lst)
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=2)
		s.wait_next=False
		s.do_throw=False
		s.mode=0
		s.tme=0
		del pos,drc
	def cleanup(self):
		if self.root:
			self.root.removeNode()
			self.root=None
		cc.npc_destroy_event(self)
	def switch_model(self,n):
		s=self
		if s.mode == n:
			return
		s.root.hide()
		s.mode=n
		s.root=s.models[n]
		s.frames=s.frames_all[n]
		s.new_index=0
		s.frame_index=0
		for frame in s.frames:
			frame.hide()
		s.frames[0].show()
		s.root.show()
	def refr_function(self):
		s=self
		s.new_index+=time.dt*s.fps
		if s.new_index >= len(s.frames):
			if s.mode == 2:
				s.cleanup()
				return
			s.new_index=0
			if s.mode == 0:
				s.switch_model(1)
				LogDanger(pos=(s.x,s.y+.6,s.z),ro_y=s.rotation_y)
				return
			if s.mode == 1:
				s.switch_model(0)
				return
		an.set_glb_frame(s)
	def update(self):
		if st.gproc():
			return
		s=self
		s.refr_function()
		if s.is_purge or s.is_hitten:
			s.collision=False
			if s.mode != 2:
				s.switch_model(2)

class Bee(Entity):
	def __init__(self,pos,drc=0,rng=0,rtyp=0,typ=0,cmv=True,bID=0):
		s=self
		s.vnum=15
		s.glb_model=f'{npf}bee/bee.glb'
		super().__init__(position=pos,scale=npc_scale)
		s.collider=BoxCollider(s,center=Vec3(0,0,0),size=(.5,.5,.5))
		s.buzz_snd=Audio(sn.BE,pitch=random.uniform(1,2),loop=True,volume=settings.SFX_VOLUME)
		if typ == 0:
			cc.set_val_npc(s)
		else:
			cc.set_val_npc(s,drc,rng,cmv,typ=typ)
		an.set_glb_value(s,fps=22,sca=.0016)
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=2)
		s.play_sfx()
		s.is_hunt=False
		s.is_home=False
		s.move_speed=2
		s.snd_pit=1
		s.bID=bID
		s.pgt=0
		s.tme=0
		del s,pos,drc,rng,rtyp,cmv,bID,typ
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
		cc.rotate_to_target(s,LC.ACTOR.position)
	def purge(self):
		self.stop_sfx()
		destroy(self)
	def check_near_npc(self):
		s=self
		jbc=s.intersects()
		ksc=time.dt*10
		if jbc:
			if jbc.entity.name == s.name and not jbc.entity is s:
				s.y+=time.dt
	def depending_home(self):
		s=self
		if abs(s.z-s.spawn_pos[2]) > 10.1 or st.death_event or s.is_home:
			s.purge()
			return
		s.fly_event()
		s.check_near_npc()
	def update(self):
		if st.gproc():
			return
		s=self
		if s.is_purge or s.is_hitten:
			s.stop_sfx()
			cc.refresh_npc_function(s)
			return
		an.refr_npc_animation(s)
		if s.typ == 0:
			s.depending_home()
			return
		cc.refresh_npc_function(s)

class Lumberjack(Entity):
	def __init__(self,pos):
		s=self
		s.vnum=16
		s.lst={0:f'{npf}lumberjack/walk.glb',1:f'{npf}lumberjack/attack.glb'}
		super().__init__(position=pos,scale=npc_scale,rotation_y=180)
		s.collider=BoxCollider(s,center=Vec3(0,1,0),size=(.75,2,.75))
		cc.set_val_npc(s)
		an.set_switch_glb_value(s,fps=22,sca=.0018,lst=s.lst)
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=2)
		s.move_speed=1.6
		s.follow_range=3
		s.is_back=True
		s.atk=False
		del pos,s
	def switch_model(self,n):
		s=self
		s.root.hide()
		s.root=s.models[n]
		s.frames=s.frames_all[n]
		s.new_index=0
		s.frame_index=0
		for frame in s.frames:
			frame.hide()
		s.frames[0].show()
		s.root.show()
	def back_to_spawn(self):
		s=self
		s.position+=(s.spawn_pos-s.position).normalized()*s.move_speed*time.dt
		if abs(s.position-s.spawn_pos) < .01:
			s.position=s.spawn_pos
			s.rotation_y=180
			s.new_index=0
			s.is_back=True
			s.atk=False
	def follow_player(self):
		s=self
		if not st.death_event:
			s.position+=(Vec3(LC.ACTOR.x,s.y,LC.ACTOR.z)-s.position).normalized()*s.move_speed*time.dt
	def refr_frame(self):
		s=self
		s.new_index+=time.dt*s.fps
		if s.new_index >= len(s.frames):
			s.new_index=0
			if s.atk:
				s.atk=False
				s.switch_model(0)
		an.set_glb_frame(s)
	def refr_function(self):
		s=self
		ddc=distance(LC.ACTOR,s)
		if not s.is_back:
			s.refr_frame()
		if ddc > s.follow_range:
			s.back_to_spawn()
			return
		if ddc <= s.follow_range:
			cc.rotate_to_target(s,LC.ACTOR.position)
		if ddc <= 2:
			if not s.atk:
				if not st.death_event:
					s.follow_player()
					if s.is_back:
						s.is_back=False
					if ddc < .75:
						s.atk=True
						s.switch_model(1)
						if not LC.ACTOR.is_attack:
							cc.get_damage(LC.ACTOR,rsn=8)
	def update(self):
		if st.gproc():
			return
		s=self
		if s.is_hitten or s.is_purge:
			cc.refresh_npc_function(s)
			return
		s.refr_function()

class SpiderRobot(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv,typ):
		s=self
		s.vnum=17
		if typ > 1:
			typ=1
		s.glb_model=f'{npf}robot_spider/{typ}.glb'
		super().__init__(position=pos,scale=npc_scale)
		s.collider=BoxCollider(s,center=Vec3(0,.3,0) if typ == 0 else Vec3(0,.5,0),size=(1.2,.6,1.5) if typ == 0 else (1.2,1,1.2))
		cc.set_val_npc(s,drc,rng,rtyp,cmv,typ)
		an.set_glb_value(s,fps=22,sca=.0018)
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=2)
		s.move_speed=1
		s.snID=6
		s.tme=1
		del s,pos,drc,rng,rtyp,cmv,typ
	def update(self):
		if st.gproc():
			return
		s=self
		if not (s.is_purge or s.is_hitten):
			if distance(s,LC.ACTOR) < LC.NPC_SND_DISTANCE:
				sn.npc_loop_audio(n=s,PIT=1,tme_r=.26)
			an.refr_npc_animation(s)
		cc.refresh_npc_function(s)

class WalkerRobot(Entity):
	def __init__(self,pos,drc,rng,rtyp,cmv):
		s=self
		s.vnum=18
		s.glb_model=f'{npf}robot_walker/walk.glb'
		super().__init__(position=pos,scale=npc_scale)
		s.collider=BoxCollider(s,center=Vec3(0,.8,0),size=(1.2,1.6,1.2))
		cc.set_val_npc(s,drc,rng,rtyp,cmv)
		an.set_glb_value(s,fps=22,sca=.0018)
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=2)
		s.move_speed=1.8
		s.p_snd=False
		s.tme=0
		del s,pos,drc,rng,rtyp,cmv
	def snd_action(self):
		s=self
		s.tme+=time.dt
		if s.tme > .6:
			if not s.p_snd:
				s.p_snd=True
				sn.pc_audio(ID=12)
			if s.tme > 1:
				s.tme=0
				s.p_snd=False
				sn.pc_audio(ID=12,pit=.8)
	def update(self):
		if st.gproc():
			return
		s=self
		if not (s.is_purge or s.is_hitten):
			if distance(s,LC.ACTOR) < 5:
				s.snd_action()
			an.refr_npc_animation(s)
		cc.refresh_npc_function(s)

class LabAssistant(Entity):
	def __init__(self,pos,drc):
		s=self
		s.vnum=19
		s.lst={0:f'{npf}lab_assistant/idle.glb',1:f'{npf}lab_assistant/fall.glb'}
		super().__init__(position=pos,rotation_y={0:90,1:180,2:270,3:0}[drc],scale=npc_scale)
		s.collider=BoxCollider(s,center=Vec3(0,1,0),size=(1,2,.75))
		cc.set_val_npc(s,drc)
		an.set_switch_glb_value(s,fps=22,sca=.0018,lst=s.lst)
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=2)
		s.is_fall=False
		s.do_push=False
		s.p_snd=False
		s.move_speed=1
		s.tme=1
		del s,pos,drc
	def cleanup(self):
		if self.root:
			self.root.removeNode()
			self.root=None
		cc.npc_destroy_event(self)
	def switch_model(self,n):
		s=self
		s.root.hide()
		s.mode=n
		s.root=s.models[n]
		s.frames=s.frames_all[n]
		s.new_index=0
		s.frame_index=0
		for frame in s.frames:
			frame.hide()
		s.frames[0].show()
		s.root.show()
	def refr_anim_frame(self):
		s=self
		s.new_index+=time.dt*s.fps
		if s.new_index >= len(s.frames):
			if s.is_fall:
				s.cleanup()
				return
			s.new_index=0
			s.do_push=False
		an.set_glb_frame(s)
	def refr_function(self):
		s=self
		s.is_fall=(s.is_hitten or s.is_purge)
		if s.is_fall:
			if not s.p_snd:
				s.p_snd=True
				s.collision=False
				sn.npc_audio(ID=8)
				s.rotation_y+=90
				s.switch_model(1)
			s.refr_anim_frame()
			return
		s.tme-=time.dt
		dv=distance(s,LC.ACTOR)
		LC.ACTOR.pushed=dv < .6 and s.do_push
		if s.do_push:
			s.refr_anim_frame()
		if s.tme <= 0:
			if dv < 6:
				sn.npc_audio(ID=7)
			s.tme=random.randint(1,3)
			s.do_push=True
	def update(self):
		if st.gproc():
			return
		self.refr_function()

class Frog(Entity):
	def __init__(self,pos,cmv,ffld):
		s=self
		s.vnum=20
		if not ffld or len(ffld) <= 0:
			s.mvo_drc=[(pos[0],pos[1],pos[2]-2),(pos[0],pos[1],pos[2]-1),(pos[0],pos[1],pos[2]),(pos[0],pos[1],pos[2]+1),(pos[0],pos[1],pos[2]+2)]
		else:
			s.mvo_drc=ffld
		s.glb_model=f'{npf}frog/walk.glb'
		super().__init__(position=pos,scale=npc_scale)
		s.collider=BoxCollider(s,center=Vec3(0,.25,0),size=(1,.5,1))
		cc.set_val_npc(s,cmv)
		an.set_glb_value(s,fps=22,sca=.01)
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=2)
		s.can_move=bool(len(s.mvo_drc) > 0)
		s.mode,s.tme,s.tme_st,s.frm=0,0,0,0
		s.lst_reverse=False
		s.tg_position=None
		s.max_frm=20.99
		s.move_speed=2.5
		s.is_jmp=False
		s.jmp_done=False
		s.p_snd=False
		s.way_index=0
		s.spd=24
		del pos,cmv,ffld
	def frog_sound_effect(self):
		if distance(self,LC.ACTOR) < LC.NPC_SND_DISTANCE:
			dsd=max(0,1-(distance(self,LC.ACTOR)/10))
			sn.npc_audio(ID=10,vol=dsd)
	def next_way_index(self):
		s=self
		if not s.lst_reverse:
			if s.way_index < len(s.mvo_drc)-1:
				s.way_index+=1
			else:
				s.lst_reverse=True
				s.way_index=max(len(s.mvo_drc)-2,0)
			return
		if s.way_index > 0:
			s.way_index-=1
		else:
			s.lst_reverse=False
			s.way_index=1 if len(s.mvo_drc) > 1 else 0
	def refr_func(self):
		s=self
		if not s.p_snd:
			s.p_snd=True
			if settings.SFX_VOLUME > 0:
				s.frog_sound_effect()
			s.rotation_y=degrees(atan2(s.mvo_drc[s.way_index][0]-s.x,s.mvo_drc[s.way_index][2]-s.z))
		if s.tme > 0:
			if s.tme < s.tme_st/5:
				s.is_jmp=True
			s.tme-=time.dt
			return
		s.tg_position=s.mvo_drc[s.way_index]
		s.position=lerp(s.position,s.tg_position,time.dt*s.move_speed)
		if distance(Vec3(s.position),s.tg_position) <= .1:
			s.next_way_index()
			s.tme=random.uniform(.5,2)
			s.tme_st=s.tme
			s.p_snd=False
	def refr_anim_frame(self):
		s=self
		s.new_index+=time.dt*s.fps
		if s.new_index >= len(s.frames):
			s.is_jmp=False
			s.new_index=0
			return
		an.set_glb_frame(s)
	def update(self):
		if st.gproc():
			return
		s=self
		if s.is_hitten or s.is_purge:
			cc.refresh_npc_function(s)
			return
		if not s.can_move:
			return
		if s.is_jmp:
			s.refr_anim_frame()
		s.refr_func()

## passive NPC
class AkuAkuMask(Entity):
	def __init__(self,pos):
		s=self
		s.glb_model=f'{npf}akuaku/idle.glb'
		super().__init__(position=pos,scale=npc_scale)
		an.set_glb_value(s,fps=22,sca=.0018)
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=2)
		s.status_changed=0
		st.aku_exist=True
		s.sparking=False
		s.spark_delay=0
		s.rot_speed=16
		s.mov_speed=10
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
		s.sparking=bool(skin == 2)
		s.scale=npc_scale if skin != 3 else .8
		if skin in (2,3):
			s.new_index=1
			an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=2)
		else:
			s.new_index=0
			an.set_glb_color(s,col=color.light_gray,UNLIT=True,brightness=2)
		an.set_glb_frame(s)
	def cover_player(self):
		mk_pos=LC.ACTOR.position+Vec3(sin(radians(LC.ACTOR.rotation_y)),0,cos(radians(LC.ACTOR.rotation_y)))*.25
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

class Hippo(Entity):
	def __init__(self,POS):
		s=self
		s.glb_model=f'{npf}hippo/hippo.glb'
		super().__init__(position=POS,scale=(.6,.5,1),name='HPP',rotation_y=180,collider=b)
		an.set_glb_value(s,fps=22,sca=(.001,.001,.0006))
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=2)
		s.frame_max={0:23,1:len(s.frames)}
		s.dive_y=s.y-.32
		s.active=False
		s.locked=False
		s.p_snd=False
		s.spawn_y=s.y
		s.tme=3
		del POS,s
	def reset_position(self):
		s=self
		if s.tme > 0:
			s.tme-=time.dt
			return
		if s.y < s.spawn_y:
			s.y+=time.dt/2
			return
		if not s.collision:
			s.collision=True
			s.locked=False
			s.p_snd=False
			s.tme=3
	def refr_anim_frame(self,mode):
		s=self
		s.new_index+=time.dt*s.fps
		if s.new_index > s.frame_max[mode]:
			if mode == 1:
				if not s.p_snd:
					s.p_snd=True
					sn.pc_audio(ID=10,pit=.85)
				return
			s.new_index=0
		an.set_glb_frame(s)
	def dive_down(self):
		s=self
		s.refr_anim_frame(1)
		if s.tme > 0:
			s.tme-=time.dt
			return
		if s.collision:
			s.collision=False
		if not s.collision:
			if s.y > s.dive_y:
				s.y-=time.dt/2
				return
		if s.active:
			s.active=False
			s.locked=True
			s.tme=5
	def update(self):
		if st.gproc():
			return
		s=self
		if s.active:
			s.dive_down()
			return
		s.refr_anim_frame(0)
		if s.locked:
			s.reset_position()

class Bird(Entity):
	def __init__(self,pos):
		s=self
		s.lst={0:f'{npf}bird/idle.glb',1:f'{npf}bird/fly.glb'}
		super().__init__(position=(pos[0],pos[1],pos[2]),scale=npc_scale,rotation_y=random.uniform(135,225))
		an.set_switch_glb_value(s,fps=22,sca=.006,lst=s.lst)
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=1.5)
		s.wait_min_max=(.5,2)
		s.rand_wait=True
		s.spawn_pos=pos
		s.active=False
		s.p_snd=False
		s.tme=0
		del pos,s
	def refr_function(self):
		s=self
		if distance(s,LC.ACTOR) < 2:
			s.active=True
			sn.npc_audio(ID=19)
			s.switch_model(1)
	def refr_position(self):
		s=self
		an.refr_npc_animation(s)
		if not s.p_snd:
			s.p_snd=True
			sn.npc_audio(ID=20)
		s.z+=time.dt*.5
		s.y+=time.dt*1.5
		if s.y > s.spawn_pos[1]+3:
			destroy(s)
	def switch_model(self,n):
		s=self
		s.root.hide()
		s.root=s.models[n]
		s.frames=s.frames_all[n]
		s.new_index=0
		s.frame_index=0
		for frame in s.frames:
			frame.hide()
		s.frames[0].show()
		s.root.show()
	def update(self):
		if st.gproc():
			return
		s=self
		if s.active:
			s.refr_position()
			return
		s.refr_function()
		if s.tme > 0:
			s.tme-=time.dt
			return
		an.refr_npc_animation(s)

class Butterfly(Entity):
	def __init__(self,pos,typ=0,rng=1):
		s=self
		if typ > 5:
			typ=5
		s.glb_model=f'{npf}butterfly/butterfly{typ}.glb'
		super().__init__(position=pos,scale=.4)
		an.set_glb_value(s,fps=22,sca=.0018)
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=2)
		s.angle=random.uniform(0,360)
		s.height_limit=s.y
		s.mov_range=rng
		s.spawn_pos=pos
		s.rng_swap=.1
		s.typ=typ
	def refr_function(self):
		s=self
		an.refr_npc_animation(s)
		prev=Vec3(s.position)
		s.angle+=time.dt*60
		#radius
		radius=s.mov_range+sin(time.time()*.5)*s.rng_swap
		s.x=s.spawn_pos[0]+cos(radians(s.angle))*radius
		s.z=s.spawn_pos[2]+sin(radians(s.angle))*radius
		#rotation_y
		dr=s.position-prev
		s.rotation_y=degrees(atan2(dr[0],dr[2]))+180
		#height
		s.y=s.spawn_pos[1]+(sin(time.time()*1.52)*.3+.3)*s.height_limit
	def update(self):
		if st.gproc():
			return
		self.refr_function()

class Firefly(Entity):
	def __init__(self,pos):
		s=self
		s.glb_model=f'{npf}firefly/idle.glb'
		super().__init__(position=pos,scale=npc_scale)
		an.set_glb_value(s,fps=22,sca=.002)
		an.set_glb_color(s,col=color.light_gray,UNLIT=False,brightness=2)
		s.start_checkp=st.checkpoint
		s.spawn_pos=pos
		s.active=False
		s.move_speed=8
		s.glow_mode=0
		s.mov_range=1
		s.ro_mode=0
		s.angle=0
		objects.ObjectLight(target=s,col=color.rgb32(255,200,180),pulse=True)
		del pos
	def respawn(self):
		s=self
		if st.checkpoint == s.start_checkp:
			s.active=False
			s.position=s.spawn_pos
			return
		s.position=st.checkpoint
	def m_idle(self):
		s=self
		s.mov_range=.3+abs(sin(time.time()))*.4
		s.y=s.spawn_pos[1]+sin(time.time()*3)*.2
	def update(self):
		if st.gproc():
			return
		s=self
		if distance(s,LC.ACTOR) < .8:
			s.active=not st.death_event
		if st.death_event:
			s.respawn()
			return
		if s.active:
			cc.rotate_to_target(s,LC.ACTOR.position)
			if st.bonus_round:
				s.position=lerp(s.position,(LC.ACTOR.x+.2,LC.ACTOR.y+.5,LC.ACTOR.z),time.dt*2)
			if st.death_route:
				s.position=lerp(s.position,(LC.ACTOR.x,LC.ACTOR.y+.5,LC.ACTOR.z-.5),time.dt*2)
			else:
				s.position=lerp(s.position,(LC.ACTOR.x,LC.ACTOR.y+.5,LC.ACTOR.z+.8),time.dt*2)
			return
		s.m_idle()