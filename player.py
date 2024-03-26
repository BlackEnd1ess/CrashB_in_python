import _core,crate,objects,ui,status,animation,debugger,sound,npc
from ursina.shaders import *
from math import atan2
from ursina import *

snd=sound
an=animation
cc=_core
s=5#cam_speed
class CrashB(Entity):
	def __init__(self,pos):
		super().__init__(model='res/crash.ply',texture='res/crash.tga',scale=0.001,rotation_x=-90,collider='box',position=pos,unlit=False)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+400),size=Vec3(200,200,700))
		self.DEFAUL_COLLIDER=self.collider
		self.aku_y=None
		cc.set_val(self)
		ui.WumpaCounter()
		ui.CrateCounter()
		ui.LiveCounter()
		ui.CollectedGem()
		invoke(lambda:objects.WarpRingEffect(pos=self.position),delay=3)
	def input(self,key):
		if self.freezed or status.is_dying:
			return
		if key == 'space' and not self.block_input:
			if not self.warped or status.p_in_air(self):
				return
			Audio(snd.snd_jump)
			self.block_input=True
			cc.set_jump_type(d=self,t=1)
			self.first_land=True
		if key == 'alt' and not self.is_attack:
			self.is_attack=True
			Audio(snd.snd_attk)
		if key == 'tab':
			status.show_wumpas=5
			status.show_crates=5
			status.show_lives=5
			status.show_gems=5
		if key in ['p','escape']:
			if not status.pause:
				status.pause=True
				return
			status.pause=False
		if key == 'b':
			EditorCamera()
		if key == 'u':
			self.move_speed=5
	def move(self):
		if status.is_dying or not self.warped:
			return
		mdi=Vec3(held_keys['d']-held_keys['a'],0,held_keys['w']-held_keys['s']).normalized()
		if mdi.length() > 0:
			self.walking=True
			self.rotation_y=atan2(-mdi.x,-mdi.z)*180/math.pi
			if self.landed:
				an.run(self)
			if self.walk_snd <= 0 and not status.p_in_air(self):
				self.walk_snd=.36
				Audio(snd.snd_walk,volume=.3)
		else:
			self.walk_snd=0
			self.walking=False
		self.x+=mdi.x*time.dt*self.move_speed
		self.z+=mdi.z*time.dt*self.move_speed
	def fall(self):
		if status.LEVEL_CLEAN:
			return
		if self.landed or self.jumping or not self.warped:
			self.fall_time=0
			return
		self.y-=time.dt*2.1
		self.fall_time+=time.dt
		if self.fall_time > 1:
			if not self.is_attack and not self.freezed:
				an.fall(self)
	def jump(self):
		self.y+=time.dt*2.4
		an.jup(self)
		if status.p_walk(self):
			self.is_flip=True
		if self.y >= self.lpos:
			self.jumping=False
	def c_camera(self):
		if not status.is_dying:
			camera.x=lerp(camera.x,self.x,time.dt*s)
			if status.c_indoor:
				camera.y=lerp(camera.y,self.y+.9,time.dt*s)
				camera.z=lerp(camera.z,self.z-3,time.dt*s)
			else:
				camera.y=lerp(camera.y,self.y+1.2,time.dt*s)
				camera.z=lerp(camera.z,self.z-3.2,time.dt*s)
	def basic_animation(self):
		if status.is_dying:
			an.player_death(self)
			return
		if self.is_flip and status.p_in_air(self):
			an.flip(self)
		if self.is_landing and not self.walking:
			an.land(self)
		if self.freezed or status.p_idle(self) and not self.is_landing or not self.warped:
			an.idle(self)
		if self.is_attack:
			cc.p_attack(self)
			an.spin(self)
	def char_misc(self):
		self.c_camera()
		if not status.is_dying:
			self.move()
		self.basic_animation()
		cc.check_ground(self)
		cc.check_wall(self)
		cc.various_val(self)
		cc.wumpa_LOD()
	def hurt_blink(self):
		if self.blink_time <= 0:
			self.blink_time=.1
			if self.alpha == 1:
				self.alpha=0
			else:
				self.alpha=1
	def update(self):
		if status.pause or status.level_solved:
			return
		self.aku_y=self.y+.5
		if self.jumping:
			self.jump()
		self.char_misc()
		if cc.level_ready and not status.is_dying:
			self.fall()