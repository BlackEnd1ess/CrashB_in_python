import _core,status,animation,sound,_loc,settings,_debug_
from math import atan2
from ursina import *

debg=_debug_
an=animation
sg=settings
st=status
sn=sound
cc=_core
LC=_loc

jmh={1:.8,2:1,3:1.1,4:1.5}

hgt={True:.3,False:.1}
fgt={True:2.2,False:2}

atp='res/pc/spin/crash.png'
dtp='res/pc/crash.png'

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
		an.WarpRingEffect(pos=s.position)
		pShadow()
		s.KEY_ACT={sg.MNU_KEY:lambda:cc.game_pause(),
					sg.JMP_KEY:lambda:s.check_jump(),
					sg.IFC_KEY:lambda:cc.show_status_ui(),
					sg.ATK_KEY:lambda:s.spin_attack(),
					sg.BLY_KEY:lambda:s.belly_smash(),
					sg.FWD_KEY:lambda:setattr(s,'CMS',2.9),
					sg.BCK_KEY:lambda:setattr(s,'CMS',3.6)}
		if sg.debg:
			debg.PlayerDBG()
			s.dev_act={
					sg.DEV_WARP:lambda:setattr(s,'position',(4.2,3,31.7)),
					sg.DEV_INFO:lambda:_debug_.pos_info(s),
					sg.DEV_COLL:_debug_.complete_level,
					sg.DEV_INFO:lambda:_debug_.chck_mem(),
					sg.DEV_ECAM:lambda:EditorCamera()}
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
		if s.is_slp:
			an.run_s(s)
		else:
			if s.is_landing:
				s.is_landing=False
			an.run(s)
		s.wksn=max(s.wksn-time.dt,0)
		if s.wksn <= 0:
			s.wksn=.5 if s.is_slp else .35
			if not s.jumping:
				sn.footstep(s)
	def jump_typ(self,t):
		s=self
		s.gravity={1:(2.6),2:(2.9),3:(3.1),4:(2.8)}[t]#fall speed
		s.vpos=s.y+jmh[t]#jump height limit
		s.fall_time=0
		s.frst_lnd=True
		s.jumping=True
		if t == 4:
			s.b_smash=False
	def jump(self):
		s=self
		s.frst_lnd=True
		kt=bool(s.space_time > .09)
		s.y=lerp(s.y,s.vpos+hgt[kt]+.1,(time.dt*s.gravity)*fgt[kt])
		if s.walking and not s.is_attack:
			s.is_flip=True
		if not s.is_flip:
			an.jump_up(s)
		if s.y >= s.vpos+hgt[kt]:
			s.space_time=0
			s.jumping=False
	def check_jump(self):
		s=self
		if s.landed and not (s.jumping or s.falling):
			s.landed=False
			sn.pc_audio(ID=1)
			s.jump_typ(t=1)
	def anim_land(self):
		s=self
		s.is_flip=False
		s.flfr,s.ldfr,s.jmfr=0,0,0
		s.is_landing=True
	def anim_fall(self):
		s=self
		if s.is_flip or s.is_attack or s.stun or st.death_event:
			return
		if s.b_smash:
			an.belly_smash(s)
			return
		an.fall(s)
	def death_action(self):
		s=self
		dtc=s.dth_cause
		s.dth_timer-=time.dt
		if s.dth_timer <= 0:
			s.dth_timer=4
			cc.reset_state(s)
			return
		if dtc in (1,5):
			s.visible=False
			return
		{2:lambda:an.dth_angelfly(s),
		3:lambda:an.dth_wtr_swim(s),
		4:lambda:an.dth_fire_ash(s),
		6:lambda:an.dth_el_shock(s),
		7:lambda:an.dth_beesting(s),
		8:lambda:an.dth_c_buried(s),
		9:lambda:an.dth_shrink(s)}[dtc]()
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
		if s.jumping:s.jump()
		if s.b_smash:cc.c_smash(s)
		if s.is_attack:
			cc.c_spin(s)
		if held_keys[settings.JMP_KEY]:s.space_time+=time.dt/2
		if st.aku_hit >= 3:cc.c_shield()
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
		an.c_animation(s)
		s.texture=atp if (s.is_spin and atp != s.texture) else dtp