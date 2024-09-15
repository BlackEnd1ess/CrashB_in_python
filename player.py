import _core,status,animation,sound,_loc,map_tools,npc
from ursina.shaders import *
from math import atan2
from ursina import *

an=animation
sn=sound
cc=_core
st=status
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
		vSH=raycast(self.ta.world_position,-Vec3(0,1,0),distance=2,ignore=[self,self.ta],debug=False)
		if vSH.normal:
			if not str(vSH.entity) in LC.item_lst:
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
		self.KEY_ACT={'escape':lambda:cc.game_pause(),
				'space':lambda:self.check_jump(),
				'tab':lambda:cc.show_status_ui(),
				'alt':lambda:self.spin_attack(),
				'w':lambda:setattr(self,'CMS',3.2),
				's':lambda:setattr(self,'CMS',4.4),
				#dev inp
				'u':lambda:setattr(self,'position',(194,0,31)),
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
			self.is_attack=True
			self.is_landing=False
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
			me=mc.entity
			mn=str(me)
			if not mc or (mc and mn in LC.item_lst,LC.trigger_lst):
				s.position+=s.direc*time.dt*s.move_speed
			if (mn == 'swpi' and me.danger) or (mn == 'fthr'):
				cc.get_damage(s,rsn=3)
			if (cc.is_crate(me) and me.vnum == 12):
				me.destroy()
			s.rotation_y=atan2(-mvD.x,-mvD.z)*180/math.pi
			s.walk_event()
			return
		s.walk_snd=0
		s.walking=False
	def walk_event(self):
		s=self
		s.walking=True
		if not s.landed:
			return
		if s.is_slippery:
			an.run_s(s,sp=16)
		else:
			if s.is_landing:
				s.is_landing=False
			an.run(s,sp=18)
		s.walk_snd=max(s.walk_snd-time.dt,0)
		if s.walk_snd <= 0:
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
			s.walk_snd=.35
	def fall(self):
		s=self
		s.y-=time.dt*s.gravity
		s.fall_time+=time.dt
		if (s.is_flip or s.is_attack):
			return
		an.fall(s,sp=12)
	def jump_typ(self,t):
		s=self
		grv={1:(2.1),2:(2.7),3:(2.8),4:(2.6)}
		jmt={1:s.y+.9,#normal jump
			2:s.y+1.15,#crate jump
			3:s.y+1.25,#bounce jump
			4:s.y+1.5}#spring jump
		s.gravity=grv[t]
		s.vpos=jmt[t]
		s.fall_time=0
		s.frst_lnd=True
		s.jumping=True
	def jump(self):
		s=self
		s.frst_lnd=True
		s.y+=time.dt*s.gravity
		if s.walking:
			s.is_flip=True
		if not s.is_flip:
			an.jup(s,sp=12)
		if s.y > s.vpos:
			s.jumping=False
	def check_jump(self):
		if self.landed:
			sn.pc_audio(ID=1)
			self.jump_typ(t=1)
	def c_camera(self):
		if not st.death_event:
			cc.cam_rotate(self)
			cc.cam_follow(self)
			camera.y=lerp(camera.y,self.y+1.2,time.dt*2)
	def death_action(self,rsn):
		s=self
		if rsn > 0:#0 is falling
			dca={1:lambda:an.angel_fly(s),
				2:lambda:an.water_swim(s),
				3:lambda:an.fire_ash(s),
				4:lambda:an.electric(s),
				5:lambda:an.eat_by_plant(s)}
			dca[rsn]()
			return
		invoke(lambda:cc.reset_state(s),delay=2)
	def refr_anim(self):
		s=self
		if (s.is_attack):
			an.spin(s,sp=20)
			return
		if s.is_flip and not (s.landed and s.is_attack):
			an.flip(s,sp=18)
			return
		if (s.landed and s.is_landing) and not (s.walking and s.jumping and s.is_attack):
			an.land(s,sp=18)
			return
		if st.p_idle(s):
			an.idle(s,sp=16)
			return
	def hurt_visual(self):
		for vkh in range(7):
			invoke(lambda:cc.hurt_blink(self),delay=vkh/3)
	def update(self):
		if not st.gproc():
			s=self
			cc.check_floor(s)
			cc.check_wall(s)
			if not s.landed:
				cc.check_ceiling(s)
			cc.various_val(s)
			if not st.p_rst(s):
				s.move()
				if not (s.landed or s.jumping):
					s.fall()
				s.c_camera()
				if s.is_attack:
					cc.c_attack(s)
				if s.jumping:
					s.jump()
			if not st.death_event:
				s.refr_anim()