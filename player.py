import _core,ui,status,animation,sound,_loc
from ursina.shaders import *
from math import atan2
from ursina import *

snd=sound
an=animation
cc=_core
LC=_loc

class pShadow(Entity):## shadow point
	def __init__(self):
		super().__init__(model=Circle(16,thickness=1,radius=.08),rotation_x=90,color=color.black,alpha=.7,origin_z=.01,collider='box')
		self.target=cc.playerInstance[0]
		_loc.shdw=self
	def flw_p(self):
		self.x=self.target.x
		self.z=self.target.z
	def check_obj(self):
		vSH=raycast(self.target.world_position,-Vec3(0,1,0),distance=2,ignore=[self,self.target],debug=False)
		if not cc.is_enemie(vSH.entity):
			if vSH.normal and not str(vSH.entity) in LC.item_lst:
				self.y=vSH.world_point.y
	def update(self):
		if not status.gproc():
			self.flw_p()
			if not self.target.landed:
				self.check_obj()
				return
			self.y=self.target.y

class CrashB(Entity):
	def __init__(self,pos):
		cHr='res/character/'
		super().__init__(model=cHr+'crash.ply',texture=cHr+'crash.tga',scale=.001,rotation_x=-90,position=pos,unlit=False)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+400),size=Vec3(200,200,700))
		self.gnd_c=Entity(model='cube',scale=.1,position=self.position,visible=False)
		cc.set_val(self)
		ui.PauseMenu()
		ui.WumpaCounter()
		ui.CrateCounter()
		ui.LiveCounter()
		ui.CollectedGem()
		an.WarpRingEffect(pos=self.position)
		pShadow()
	def input(self,key):
		if self.freezed or status.is_dying:
			return
		if key == 'space' and not self.block_input:
			if not self.warped:
				return
			Audio(snd.snd_jump)
			self.block_input=True
			if not status.p_in_air(self):
				cc.set_jump_type(d=self,t=1)
			return
		if key == 'alt':
			if not self.is_attack:
				self.is_attack=True
				Audio(snd.snd_attk)
			else:
				Audio(snd.snd_atkw)
		if key == 'tab':
			status.show_wumpas=5
			status.show_crates=5
			status.show_lives=5
			status.show_gems=5
			return
		if key == 'w':
			self.CMS=3
		if key == 's':
			self.CMS=4
		if key in ['p','escape']:
			if not status.pause:
				status.pause=True
				return
			status.pause=False
		##dev input
		if key == 'b':
			#print(f"c.place_crate(ID=1,p=({self.x},{self.y+.16},{self.z})")
			print(self.position)
		if key == 'e':
			EditorCamera()
		if key == 'j':
			scene.fog_color=color.random_color()
			print(scene.fog_color)
		if key == 'u':
			self.position=(-.8,7,49.7)
	def move(self):
		mvD=Vec3(held_keys['d']-held_keys['a'],0,held_keys['w']-held_keys['s']).normalized()
		self.direc=mvD
		if self.is_slippery:
			cc.c_slide(self)
		if mvD.length() > 0:
			status.p_last_direc=mvD
			self.walking=True
			self.walk_event()
			cc.obj_walls(self)
			if not status.gproc():#avoid sys error by missing ursina entity
				self.rotation_y=atan2(-mvD.x,-mvD.z)*180/math.pi
			return
		self.walk_snd=0
		self.walking=False
	def walk_event(self):
		if self.landed:
			self.is_landing=False##stop the remaining landing frames after run
			if not self.is_attack:
				if self.is_slippery:
					an.run_s(self)
				else:
					an.run(self)
		if self.walk_snd <= 0 and not status.p_in_air(self):
			if self.is_slippery:
				self.walk_snd=.5
				Audio(snd.snd_icew,pitch=1.5)
			else:
				self.walk_snd=.35
				Audio(snd.snd_walk,volume=.3)
	def fall(self):
		s=self
		if (s.landed or s.jumping or s.freezed or status.is_dying) or not s.warped:
			self.fall_time=0
			return
		self.y-=time.dt*1.5
		self.fall_time+=time.dt
		if s.fall_time > 2 and not (s.is_attack or s.freezed):
			s.is_flip=False
			an.fall(s)
	def jump(self):
		self.first_land=True
		self.y+=time.dt*2.4
		if self.walking:
			self.is_flip=True
		if self.y >= self.lpos:
			self.jumping=False
		if not self.is_flip:
			an.jup(self)
	def c_camera(self):
		if not status.is_dying:
			cc.cam_rotate(self)
			cc.cam_follow(self)
			camera.y=lerp(camera.y,self.y+1.2,time.dt*2)
	def basic_animation(self):
		if status.is_dying:
			an.player_death(self)
			return
		if self.is_attack:
			an.spin(self)
			return
		if self.is_flip and status.p_in_air(self):
			an.flip(self)
		if self.is_landing and not self.walking and not status.p_in_air(self):
			an.land(self)
			return
		if self.freezed or status.p_idle(self) and not self.is_landing or not self.warped:
			if self.is_slippery:
				an.slide_stop(self)
			else:
				an.idle(self)
	def char_misc(self):
		if not status.is_dying and self.warped and not self.freezed:
			self.move()
		if self.intersects().normal == Vec3(0,-1,0):
			cc.obj_ceiling(c=self,e=self.intersects().entity)
		self.fall()
		if self.is_attack:
			cc.c_attack(self)
		self.basic_animation()
		self.c_camera()
		cc.c_item(self)
		cc.various_val(self)
	def hurt_blink(self):
		if self.blink_time <= 0:
			self.blink_time=.1
			if self.alpha == 1:
				self.alpha=0
			else:
				self.alpha=1
	def update(self):
		if status.pause or status.level_solved or status.gproc():
			return
		cc.obj_grnd(self)
		self.char_misc()
		if self.jumping:
			self.jump()
		if cc.level_ready and not status.is_dying:
			self.fall()