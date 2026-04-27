import _core,status,animation,sound,_loc,settings,_debug_
from effect import WarpRingEffect
from math import atan2
from ursina import *

debg=_debug_
an=animation
sg=settings
st=status
sn=sound
cc=_core
LC=_loc

class pShadow(Entity):## shadow point
	def __init__(self):
		super().__init__(model='quad',texture='res/pc/shdw.png',color=color.black,rotation_x=90,scale=.25,origin_z=.01,alpha=.9)
		LC.IGNORE.append(self)
		_loc.shdw=self
	def update(self):
		if st.gproc():
			return
		s=self
		krf=raycast(LC.ACTOR.world_position,-Vec3(0,1,0),distance=2,ignore=LC.IGNORE,debug=False)
		s.visible=not(LC.ACTOR.freezed)
		s.x,s.z=LC.ACTOR.x,LC.ACTOR.z
		if krf.hit:
			if not str(krf.entity) in LC.item_lst|LC.trigger_lst:
				s.y=krf.world_point.y+.1/10

class CrashB(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=LC.ctx+'.ply',texture=LC.ctx+'.png',scale=.1/115,rotation_x=-90,position=pos,unlit=False)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+500),size=Vec3(300,300,500))
		cc.set_val(s)
		WarpRingEffect()
		pShadow()
		s.KEY_ACT={sg.MNU_KEY:lambda:cc.game_pause(),sg.JMP_KEY:lambda:s.check_jump(),sg.IFC_KEY:lambda:cc.show_status_ui(),sg.ATK_KEY:lambda:s.spin_attack(),sg.BLY_KEY:lambda:s.belly_smash(),sg.FWD_KEY:lambda:setattr(s,'CMS',2.9),sg.BCK_KEY:lambda:setattr(s,'CMS',3.6)}
		if sg.debg:
			debg.PlayerDBG()
			s.dev_act={sg.DEV_WARP:lambda:setattr(s,'position',(4.2,3,31.7)),
						sg.DEV_INFO:lambda:_debug_.pos_info(s),
						sg.DEV_COLL:_debug_.complete_level,
						sg.DEV_INFO:lambda:_debug_.show_instance_count(),
						sg.DEV_ECAM:lambda:EditorCamera(),
						sg.DEV_TERM:lambda:_debug_.dev_console()}
		LC.IGNORE.append(s)
		del pos
	def input(self,key):
		s=self
		if not st.p_rst(s):
			if key in s.KEY_ACT:
				s.KEY_ACT[key]()
			if sg.debg:
				if key in s.dev_act:
					s.dev_act[key]()
		del key
	def belly_smash(self):
		s=self
		if s.jumping or not s.landed:
			if not s.b_smash:
				s.b_smash=True
				s.landing=False
				s.jumping=False
				s.is_flip=False
				s.animate_y(s.y+.45,.2)
	def spin_attack(self):
		s=self
		if not s.is_attack and s.atk_cooldown <= 0:
			s.is_attack=True
			s.is_spin=True
			s.atk_cooldown=.35
			s.atk_duration=.25
			s.is_flip=False
			s.is_landing=False
			s.standup=False
			sn.pc_audio(ID=3)
			return
		sn.pc_audio(ID=4)
	def move(self):
		s=self
		mvx=held_keys[sg.RGT_KEY]-held_keys[sg.LFT_KEY]
		mvz=held_keys[sg.FWD_KEY]-held_keys[sg.BCK_KEY]
		if mvx != 0 or mvz != 0:
			length=math.sqrt(mvx*mvx+mvz*mvz)
			mvx/=length
			mvz/=length
			mvD=Vec3(mvx,0,mvz)
		else:
			mvD=Vec3(0,0,0)
		s.direc=mvD
		cc.wall_hit_idle(s)
		if s.is_slp:
			cc.c_slide(s)
		if mvD.x != 0 or mvD.z != 0:
			cc.wall_hit_walk(s)
			return
		s.wksn=0
		s.walking=False
	def walk_event(self):
		s=self
		s.walking=True
		if not s.landed:
			return
		if s.is_landing:
			s.is_landing=False
		s.wksn=max(s.wksn-time.dt,0)
		if s.wksn <= 0:
			s.wksn=.5 if s.is_slp else .35
			if not s.jumping:
				sn.footstep(s)
	def jump_typ(self,typ):
		s=self
		s.vpos=s.y+s.jmp_hgt[typ]
		s.jmp_typ=typ
		s.fall_time=0
		s.frst_lnd=True
		s.jumping=True
		if typ == 3:
			s.b_smash=False
	def jump(self):
		s=self
		if held_keys[settings.JMP_KEY]:
			s.space_time+=time.dt
			if s.space_time > .2:
				s.vpos+=.25*time.dt
		s.y=lerp(s.y,s.vpos,time.dt*s.jmp_pwr[s.jmp_typ])
		if abs(s.y-s.vpos) < .1:
			s.space_time=0
			s.jumping=False
	def check_jump(self):
		s=self
		if s.landed and not (s.jumping or s.falling):
			s.landed=False
			sn.pc_audio(ID=1)
			s.jump_typ(0)
	def anim_land(self):
		s=self
		s.is_flip=False
		s.is_landing=True
		s.jmp_typ=0
	def death_action(self):
		s=self
		if not s.dth_block:
			s.dth_block=True
			s.visible=False
			an.PlayerDeathAnimator(pos=s.position,typ=s.dth_cause)
	def hurt_visual(self):
		for vkh in range(7):
			invoke(lambda:cc.hurt_blink(self),delay=vkh/3)
		del vkh
	def c_physic(self):
		s=self
		cc.various_val(s)
		cc.check_ceiling(s)
		if not s.jumping:
			cc.check_floor(s)
	def c_interact(self):
		s=self
		s.move()
		if not st.death_event:
			s.c_camera()
		if s.jumping:
			s.jump()
		if s.b_smash:
			cc.c_smash(s)
		if s.is_attack:
			cc.c_spin(s)
		if st.aku_hit >= 3:
			cc.c_shield()
	def c_camera(self):
		s=self
		if st.bonus_round:
			cc.cam_bonus(s)
			return
		if s.indoor > 0:
			cc.cam_indoor(s)
			return
		cc.cam_level(s)
	def update(self):
		if st.gproc():
			return
		s=self
		if st.death_event:
			s.death_action()
			return
		s.c_physic()
		if not st.p_rst(s):
			s.c_interact()
		an.refr_animation(s)