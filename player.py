import _core,status,animation,sound,_loc,map_tools,npc
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
		if vSH.hit:
			if str(vSH.entity) in LC.item_lst:
				pass
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
		self.KEY_ACT={'escape':lambda:cc.game_pause(),
				'tab':lambda:cc.show_status_ui(),
				'alt':lambda:self.spin_attack(),
				'w':lambda:setattr(self,'CMS',3),
				's':lambda:setattr(self,'CMS',4),
				#dev inp
				'u':lambda:setattr(self,'position',(9+.75*6,1.5,-22)),
				'b':lambda:print(self.position),
				'e':lambda:EditorCamera()}
		cc.set_val(self)
		an.WarpRingEffect(pos=self.position)
		pShadow()
		if st.aku_hit > 0:
			npc.AkuAkuMask(pos=(self.x-.3,self.y+.3,self.z+.5))
	def input(self,key):
		if st.p_rst(self):
			return
		if key in self.KEY_ACT:
			self.KEY_ACT[key]()
	def spin_attack(self):
		if not self.is_attack:
			self.is_landing=False
			self.is_attack=True
			sn.pc_audio(ID=3)
			invoke(lambda:setattr(self,'is_attack',False),delay=.6)
			return
		sn.pc_audio(ID=0)
	def move(self):
		s=self
		mvD=Vec3(held_keys['d']-held_keys['a'],0,held_keys['w']-held_keys['s']).normalized()
		s.direc=mvD
		if s.is_slippery:
			cc.c_slide(s)
		if mvD.length() > 0:
			st.p_last_direc=mvD
			mc=raycast(s.world_position+(0,.1,0),s.direc,distance=.2,ignore=[s,LC.shdw],debug=False)
			if not mc or (mc and str(mc.entity) in LC.item_lst or mc and str(mc.entity) in LC.trigger_lst):
				s.position+=s.direc*time.dt*s.move_speed
			if (str(mc.entity) == 'sewer_pipe' and mc.entity.danger) or (str(mc.entity) == 'fire_throw'):
				cc.get_damage(s,rsn=3)
			s.rotation_y=atan2(-mvD.x,-mvD.z)*180/math.pi
			s.walk_event()
			return
		s.walk_snd=0
		s.walking=False
	def walk_event(self):
		s=self
		if st.death_event:
			return
		s.walking=True
		s.is_landing=False#stop the remaining landing frames after run
		if s.landed:
			if s.is_slippery:
				an.run_s(s)
			else:
				an.run(s)
		s.walk_snd=max(s.walk_snd-time.dt,0)
		if s.walk_snd <= 0 and s.landed:
			if s.is_slippery:
				s.walk_snd=.5
				sn.pc_audio(ID=8,pit=1.5)
				return
			if s.in_water > 0:
				sn.pc_audio(ID=11,pit=random.uniform(.9,1))
			else:
				if st.level_index == 4:
					sn.pc_audio(ID=12)
				else:
					sn.pc_audio(ID=0)
			self.walk_snd=.35
	def fall(self):
		s=self
		s.y-=time.dt*s.fall_speed[s.jmp_typ]
		s.fall_time+=time.dt
		if s.fall_time > .8 and not (s.is_attack or s.freezed):
			s.is_flip=False
			an.fall(s)
	def jump(self):
		s=self
		s.first_land=True
		s.y+=time.dt*s.jump_speed[s.jmp_typ]
		if s.y >= s.vpos:
			s.jumping=False
			return
		if s.walking:
			s.is_flip=True
		if not s.is_flip:
			an.jup(s)
	def check_jump(self):
		if held_keys['space'] and self.landed:
			sn.pc_audio(ID=1)
			if self.landed:
				cc.set_jump_type(self,typ=0)
	def c_camera(self):
		if not st.death_event:
			cc.cam_rotate(self)
			cc.cam_follow(self)
			#camera.y=lerp(camera.y,self.y+1.2,time.dt*2)
	def death_action(self,rsn):
		s=self
		if rsn > 0:
			dca={1:lambda:an.angel_fly(s),
				2:lambda:an.water_swim(s),
				3:lambda:an.fire_ash(s),
				4:lambda:an.electric(s),
				5:lambda:an.eat_by_plant(s)}
			dca[rsn]()
			return
		invoke(lambda:cc.reset_state(s),delay=2)
	def basic_animation(self):
		s=self
		if not st.LV_CLEAR_PROCESS:
			if s.is_attack:
				an.spin(s)
				return
			if s.is_flip and not s.landed:
				an.flip(s)
			if (s.landed and s.is_landing) and not s.walking:
				an.land(s)
				return
			if status.p_idle(s) or s.freezed:
				if s.is_slippery:
					an.slide_stop(s)
				else:
					an.idle(s)
	def hurt_visual(self):
		for vkh in range(7):
			invoke(lambda:cc.hurt_blink(self),delay=vkh/3)
	def update(self):
		if not st.gproc():
			s=self
			cc.obj_grnd(s)
			cc.obj_walls(s)
			if not s.landed:
				cc.obj_ceiling(s)
			cc.various_val(s)
			if not st.p_rst(s):
				s.check_jump()
				s.move()
				if not (s.landed or s.jumping):
					s.fall()
				s.c_camera()
				if s.is_attack:
					cc.c_attack(s)
				if s.jumping:
					s.jump()
			if not st.death_event:
				s.basic_animation()