import _core,ui,status,animation,sound,_loc,map_tools
from ursina.shaders import *
from math import atan2
from ursina import *

sn=sound
an=animation
cc=_core
LC=_loc
st=status

cHr='res/pc/'
class pShadow(Entity):## shadow point
	def __init__(self):
		super().__init__(model=Circle(16,thickness=1,radius=.09),color=color.black,rotation_x=90,alpha=.6,origin_z=.01,collider='box')
		self.ta=LC.ACTOR
		_loc.shdw=self
	def flw_p(self):
		self.x=self.ta.x
		self.z=self.ta.z
		vSH=raycast(self.ta.world_position,-Vec3(0,1,0),distance=2,ignore=[self,self.ta],debug=False)
		if vSH.hit and not str(vSH.entity) in LC.item_lst:
			self.y=vSH.world_point.y
	def update(self):
		if not st.gproc():
			self.visible=not(self.ta.landed)
			if self.visible:
				self.flw_p()

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
		if st.p_rst(self):
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
			st.show_wumpas=5
			st.show_crates=5
			st.show_lives=5
			st.show_gems=5
		if key == 'w':
			self.CMS=3
		if key == 's':
			self.CMS=4
		if key in ['p','escape']:
			if not st.pause:
				st.pause=True
				return
			st.pause=False
		##dev input
		if key == 'b':
			#map_tools.pos_info(self)
			#print('Entities: '+str(len(scene.entities)))
			#print('CRATE reset: '+str(len(st.C_RESET)))
			#print(scene.entities[-1])
			print(self.position)
		if key == 'e':
			EditorCamera()
		if key == 'j':
			scene.fog_color=color.random_color()
			print(scene.fog_color)
		if key == 'u':
			#self.position=(0,-35,-3)
			#self.position=(0,2,3)
			#self.position=(14.5,5,48.5)
			self.position=(5,3,30)
	def move(self):
		mvD=Vec3(held_keys['d']-held_keys['a'],0,held_keys['w']-held_keys['s']).normalized()
		self.direc=mvD
		if self.is_slippery:
			cc.c_slide(self)
		if mvD.length() > 0:
			st.p_last_direc=mvD
			mc=raycast(self.world_position+(0,.1,0),self.direc,distance=.2,ignore=[self,LC.shdw],debug=False)
			if not mc or (mc and str(mc.entity) in LC.item_lst):
				self.position+=self.direc*time.dt*self.move_speed
			if (str(mc.entity) == 'sewer_pipe' and mc.entity.danger):
				cc.get_damage(self,rsn=3)
			self.rotation_y=atan2(-mvD.x,-mvD.z)*180/math.pi
			self.walk_event()
			return
		self.walk_snd=0
		self.walking=False
	def walk_event(self):
		if st.death_event:
			return
		self.walking=True
		self.is_landing=False#stop the remaining landing frames after run
		if self.landed:
			if self.is_slippery:
				an.run_s(self)
			else:
				an.run(self)
		self.walk_snd=max(self.walk_snd-time.dt,0)
		if self.walk_snd <= 0 and self.landed:
			if self.is_slippery:
				self.walk_snd=.5
				sn.pc_audio(ID=8,pit=1.5)
				return
			if self.in_water > 0:
				sn.pc_audio(ID=11,pit=random.uniform(.9,1))
			else:
				if st.level_index == 4:
					sn.pc_audio(ID=12)
				else:
					sn.pc_audio(ID=0)
			self.walk_snd=.35
	def fall(self):
		s=self
		if s.landed or s.jumping:
			self.fall_time=0
			return
		self.y-=time.dt*self.fall_speed[self.jmp_typ]
		self.fall_time+=time.dt
		if s.fall_time > .4 and not (s.is_attack or s.freezed):
			s.is_flip=False
			an.fall(s)
		if self.y < -5 and not status.bonus_round:
			cc.dth_event(self,rsn=0)
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
		if not status.death_event:
			cc.cam_rotate(self)
			cc.cam_follow(self)
			#camera.y=lerp(camera.y,self.y+1.2,time.dt*2)
	def hurt_blink(self):
		self.visible=False
		invoke(lambda:setattr(self,'visible',True),delay=.1)
		invoke(lambda:setattr(self,'visible',False),delay=.2)
		invoke(lambda:setattr(self,'visible',True),delay=.3)
		invoke(lambda:setattr(self,'visible',False),delay=.4)
		invoke(lambda:setattr(self,'visible',True),delay=.5)
		invoke(lambda:setattr(self,'visible',False),delay=.6)
		invoke(lambda:setattr(self,'visible',True),delay=.7)
	def death_action(self,rsn):
		if rsn > 0:
			dca={1:lambda:an.angel_fly(self),
				2:lambda:an.water_swim(self),
				3:lambda:an.fire_ash(self),
				4:lambda:an.electric(self),
				5:lambda:an.eat_by_plant(self)}
			dca[rsn]()
			return
		invoke(lambda:cc.reset_state(self),delay=2)
	def basic_animation(self):
		if not st.LV_CLEAR_PROCESS:
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
	def update(self):
		if not status.gproc():
			cc.obj_grnd(self)
			if not status.p_rst(self):
				self.move()
				self.fall()
				self.c_camera()
				cc.obj_walls(self)
				if self.is_attack:
					cc.c_attack(self)
				if self.jumping:
					self.jump()
			if not status.death_event:
				self.basic_animation()
			cc.various_val(self)
			if not self.landed:
				cc.obj_ceiling(self)