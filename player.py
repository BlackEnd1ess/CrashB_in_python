import _core,status,animation,sound,_loc,map_tools
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
		s=self
		s.x=s.ta.x
		s.z=s.ta.z
		vSH=raycast(s.ta.world_position,-Vec3(0,1,0),distance=2,ignore=[self,self.ta],debug=False)
		if (s.ta.landed and not s.ta.jumping):
			s.y=(s.ta.y)
			return
		if vSH.normal:
			if not (str(vSH.entity) in LC.item_lst+LC.trigger_lst):
				s.y=vSH.world_point.y
	def update(self):
		if not st.gproc():
			self.flw_p()

class pShield(Entity):
	def __init__(self):
		super().__init__(model='cube',collider='box',scale=(4,3,4),position=(0,-5,0),visible=False)
	def check_block(self):
		wt=self.intersects(ignore=[LC.ACTOR,LC.shdw])
		we=wt.entity
		if wt:
			if cc.is_enemie(we) and not (we.is_hitten or we.is_purge):
				if (we.vnum == 1) or (we.vnum == 5 and we.def_mode):
					cc.get_damage(LC.ACTOR,rsn=1)
				cc.bash_enemie(we,h=LC.ACTOR)
				return
			if str(we) in LC.item_lst:
				we.collect()
				return
			if cc.is_crate(we):
				if we.vnum in [3,11]:
					we.empty_destroy()
				else:
					we.destroy()
				return
	def update(self):
		s=self
		if st.aku_hit > 2:
			s.collider='box'
			fv=LC.ACTOR
			s.position=(fv.x,fv.y+.5,fv.z)
			s.check_block()
			return
		s.collider=None

class CrashB(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=cHr+'crash.ply',texture=cHr+'crash.tga',scale=.1/110,rotation_x=-90,position=pos,unlit=False)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+400),size=Vec3(200,200,600))
		cc.set_val(s)
		an.WarpRingEffect(pos=s.position)
		pShadow()
		s.KEY_ACT={'escape':lambda:cc.game_pause(),
				'space':lambda:s.check_jump(),
				'tab':lambda:cc.show_status_ui(),
				'alt':lambda:s.spin_attack(),
				'v':lambda:s.belly_smash(),
				'w':lambda:setattr(s,'CMS',3.2),
				's':lambda:setattr(s,'CMS',4.2),
				#dev inp
				'u':lambda:setattr(s,'position',(4.8,4,31.7)),
				#'b':lambda:print(s.position),
				'e':lambda:EditorCamera()}
	def input(self,key):
		s=self
		if st.p_rst(s):
			return
		if key in s.KEY_ACT:
			s.KEY_ACT[key]()
	def belly_smash(self):
		s=self
		if s.jumping or not s.landed:
			if not s.b_smash:
				s.b_smash=True
				s.landing=False
				s.jumping=False
				s.is_flip=False
				s.animate_y(s.y+.4,.3)
	def spin_attack(self):
		s=self
		if not s.is_attack:
			s.is_attack=True
			s.standup=False
			s.is_landing=False
			sn.pc_audio(ID=3)
			invoke(lambda:setattr(s,'is_attack',False),delay=.6)
			return
		sn.pc_audio(ID=0)
	def move(self):
		s=self
		if s.b_smash or st.p_rst(s):
			return
		mvD=Vec3(held_keys['d']-held_keys['a'],0,held_keys['w']-held_keys['s']).normalized()
		s.direc=mvD
		if s.is_slippery:
			cc.c_slide(s)
		if mvD.length() > 0:
			st.p_last_direc=mvD
			mc=raycast(s.world_position+(0,.1,0),s.direc,distance=.2,ignore=[s,LC.shdw],debug=False)
			me=mc.entity
			mn=str(me)
			if not mc or (mc and mn in LC.item_lst+LC.trigger_lst):
				s.position=lerp(s.position,(s.position+s.direc),time.dt*s.move_speed)
			if (mn == 'fthr'):
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
			sn.footstep(self)
			if s.is_slippery:
				s.walk_snd=.5
				return
			s.walk_snd=.35
	def fall(self):
		s=self
		fsp={False:(time.dt*s.gravity),True:(time.dt*s.gravity)*2}
		s.y-=fsp[s.b_smash]
		s.fall_time+=time.dt
		if (s.is_flip or s.is_attack):
			return
		if s.b_smash:
			an.belly(s,sp=12)
		else:
			an.fall(s,sp=12)
	def jump_typ(self,t):
		s=self
		grv={1:(2.2),2:(2.6),3:(2.9),4:(2.7)}
		jmh={1:s.y+.8,#normal jump
			2:s.y+1,#crate jump
			3:s.y+1.2,#bounce jump
			4:s.y+1.4}#spring jump
		s.gravity=grv[t]#fall speed
		s.vpos=jmh[t]#jump heigt limit
		s.fall_time=0
		s.frst_lnd=True
		s.jumping=True
	def jump(self):
		s=self
		s.frst_lnd=True
		s.y=lerp(s.y,s.vpos+.1,(time.dt*s.gravity)*2)
		if s.walking:
			s.is_flip=True
		if not s.is_flip:
			an.jup(s,sp=16)
		if s.y >= s.vpos:
			s.jumping=False
	def check_jump(self):
		if self.landed:
			sn.pc_audio(ID=1)
			self.jump_typ(t=1)
	def c_camera(self):
		if not st.death_event:
			if st.bonus_round:
				cc.cam_bonus(self)
				return
			cc.cam_follow(self)
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
		if (s.standup):
			an.stand_up(s,sp=16)
			return
		if (s.is_attack):
			an.spin(s,sp=20)
			return
		if s.is_flip and not (s.landed and s.is_attack):
			an.flip(s,sp=18)
			return
		if (s.landed and s.is_landing) and not (s.walking and s.jumping and s.is_attack):
			if s.b_smash:
				an.belly_land(s,sp=12)
			else:
				an.land(s,sp=18)
			return
		if st.p_idle(s) or self.freezed:
			if s.is_slippery:
				an.slide_stop(s,sp=8)
			else:
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
			cc.various_val(s)
			cc.check_ceiling(s)
			if not st.p_rst(s):
				s.move()
				s.c_camera()
				if not (s.landed or s.jumping):
					s.fall()
				if s.jumping:
					s.jump()
				if s.b_smash:
					cc.c_smash(s)
				if s.is_attack:
					cc.c_attack(s)
			if not st.death_event:
				s.refr_anim()