import _core,ui,status,animation,sound,_loc,map_tools
from ursina.shaders import *
from math import atan2
from ursina import *

sn=sound
an=animation
cc=_core
LC=_loc

cHr='res/pc/'
class pShadow(Entity):## shadow point
	def __init__(self):
		super().__init__(model=Circle(16,thickness=1,radius=.09),color=color.black,rotation_x=90,alpha=.6,origin_z=.01,collider='box')
		self.ta=LC.ACTOR
		_loc.shdw=self
	def flw_p(self):
		self.x=self.ta.x
		self.z=self.ta.z
	def check_obj(self):
		vSH=raycast(self.ta.world_position,-Vec3(0,1,0),distance=2,ignore=[self,self.ta],debug=False)
		if not cc.is_enemie(vSH.entity):
			if vSH.normal and not str(vSH.entity) in LC.item_lst:
				self.y=vSH.world_point.y
	def update(self):
		if not status.gproc() and LC.ACTOR != None:
			self.flw_p()
			if not self.ta.landed:
				self.check_obj()
				return
			self.y=self.ta.y

class CrashB(Entity):
	def __init__(self,pos):
		super().__init__(model=cHr+'crash.ply',texture=cHr+'crash.tga',scale=.1/110,rotation_x=-90,position=pos,unlit=False)
		self.collider=BoxCollider(self,center=Vec3(self.x,self.y+50,self.z+400),size=Vec3(200,200,600))
		self.fall_speed={0:2.9,1:2.9,2:3,3:2.8}
		self.jump_speed={0:2.7,1:2.7,2:3,3:3}
		cc.set_val(self)
		ui.PauseMenu()
		ui.WumpaCounter()
		ui.CrateCounter()
		ui.LiveCounter()
		ui.CollectedGem()
		an.WarpRingEffect(pos=self.position)
		pShadow()
	def input(self,key):
		if status.p_rst(self):
			return
		if key == 'space' and self.landed:
			sn.pc_audio(ID=1)
			if self.landed:
				cc.set_jump_type(self,typ=0)
		if key == 'alt':
			if not self.is_attack:
				self.is_landing=False
				self.is_attack=True
				sn.pc_audio(ID=3)
				invoke(lambda:setattr(self,'is_attack',False),delay=.6)
			else:
				sn.pc_audio(ID=0)
		if key == 'tab':
			status.show_wumpas=5
			status.show_crates=5
			status.show_lives=5
			status.show_gems=5
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
			print('Entities: '+str(len(scene.entities)))
			print('CRATE reset: '+str(len(status.C_RESET)))
			print(scene.entities[-1])
			print(self.position)
		if key == 'e':
			EditorCamera()
		if key == 'j':
			scene.fog_color=color.random_color()
			print(scene.fog_color)
		if key == 'u':
			self.position=(43,6,28)
	def move(self):
		mvD=Vec3(held_keys['d']-held_keys['a'],0,held_keys['w']-held_keys['s']).normalized()
		self.direc=mvD
		if self.is_slippery:
			cc.c_slide(self)
		if mvD.length() > 0:
			status.p_last_direc=mvD
			cc.obj_walls(self)
			self.rotation_y=atan2(-mvD.x,-mvD.z)*180/math.pi
			self.walk_event()
			return
		self.walk_snd=0
		self.walking=False
	def walk_event(self):
		self.walking=True
		self.is_landing=False#stop the remaining landing frames after run
		if self.landed:
			if self.is_slippery:
				an.run_s(self)
			else:
				an.run(self)
		self.walk_snd=max(self.walk_snd-time.dt,0)
		if self.walk_snd <= 0:
			if self.is_slippery:
				self.walk_snd=.5
				sn.pc_audio(ID=8,pit=1.5)
			else:
				self.walk_snd=.35
				sn.pc_audio(ID=0)
	def fall(self):
		s=self
		if s.landed or s.jumping:
			self.fall_time=0
			return
		self.y-=time.dt*self.fall_speed[self.jmp_typ]
		self.fall_time+=time.dt
		if s.fall_time > 2 and not (s.is_attack or s.freezed):
			s.is_flip=False
			an.fall(s)
	def jump(self):
		self.first_land=True
		self.y+=time.dt*self.jump_speed[self.jmp_typ]
		if self.y >= self.vpos:
			self.jumping=False
			return
		if self.walking:
			self.is_flip=True
		if not self.is_flip:
			an.jup(self)
	def c_camera(self):
		if not status.is_dying:
			cc.cam_rotate(self)
			cc.cam_follow(self)
			#camera.y=lerp(camera.y,self.y+1.2,time.dt*2)
	def basic_animation(self):
		if not status.gproc():
			if status.is_dying:
				an.p_death(self)
				return
			if self.is_attack:
				an.spin(self)
				return
			if self.is_flip and not self.landed:
				an.flip(self)
			if (self.landed and self.is_landing) and not self.walking:
				an.land(self)
				return
			if status.p_idle(self) or self.freezed:
				if self.is_slippery:
					an.slide_stop(self)
				else:
					an.idle(self)
	def hurt_blink(self):
		self.blink_time=max(self.blink_time-time.dt,0)
		if self.blink_time <= 0:
			self.blink_time=.1
			if self.alpha == 1:
				self.alpha=0
				return
			self.alpha=1
	def update(self):
		if not status.gproc():
			cc.obj_grnd(self)
			if not status.p_rst(self):
				self.move()
				self.fall()
				self.c_camera()
				cc.c_item(self)
				if self.is_attack:
					cc.c_attack(self)
				if self.jumping:
					self.jump()
			self.basic_animation()
			cc.various_val(self)
			if not self.landed:
				cc.obj_ceiling(self)