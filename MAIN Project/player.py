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

atp='res/pc/spn/crash.png'
dtp='res/pc/crash.png'

class pShadow(Entity):## shadow point
	def __init__(self):
		super().__init__(model='quad',texture='res/pc/shdw.png',color=color.black,rotation_x=90,scale=.25,origin_z=.01,alpha=.9)
		_loc.shdw=self
	def update(self):
		if st.gproc():
			return
		s=self
		krf=raycast(LC.ACTOR.world_position,-Vec3(0,1,0),distance=2,ignore=[s,LC.ACTOR],debug=False)
		s.visible=not(LC.ACTOR.freezed)
		s.x,s.z=LC.ACTOR.x,LC.ACTOR.z
		if krf.hit:
			if not str(krf.entity) in LC.item_lst|LC.trigger_lst:
				s.y=krf.world_point.y+.1/10

class CrashB(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=LC.ctx+'.ply',texture=LC.ctx+'.png',scale=.1/114,rotation_x=-90,position=pos,unlit=False)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+400),size=Vec3(200,200,600))
		cc.set_val(s)
		an.WarpRingEffect(pos=s.position)
		pShadow()
		s.KEY_ACT={
				sg.MNU_KEY:lambda:cc.game_pause(),
				sg.JMP_KEY:lambda:s.check_jump(),
				sg.IFC_KEY:lambda:cc.show_status_ui(),
				sg.ATK_KEY:lambda:s.spin_attack(),
				sg.BLY_KEY:lambda:s.belly_smash(),
				sg.FWD_KEY:lambda:setattr(s,'CMS',2.9),
				sg.BCK_KEY:lambda:setattr(s,'CMS',3.6)}
		if sg.debg:
			debg.PlayerDBG()
			s.dev_act={
					sg.DEV_WARP:lambda:setattr(s,'position',(60.5,4,139)),
					sg.DEV_INFO:lambda:_debug_.pos_info(s),
					#sg.DEV_INFO:lambda:_debug_.chck_mem(),
					sg.DEV_ECAM:lambda:EditorCamera()}
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
		if not s.is_attack:
			s.is_attack=True
			s.standup,s.is_landing=False,False
			sn.pc_audio(ID=3)
			return
		sn.pc_audio(ID=4)
	def move(self):
		s=self
		uq=[s,LC.shdw]
		mvD=Vec3(held_keys[sg.RGT_KEY]-held_keys[sg.LFT_KEY],0,held_keys[sg.FWD_KEY]-held_keys[sg.BCK_KEY]).normalized()
		hT=s.intersects(ignore=uq,debug=False)
		s.direc=mvD
		if hT.hit and not hT.normal in {Vec3(0,1,0),Vec3(0,-1,0)}:
			if not str(hT.entity) in LC.item_lst|LC.trigger_lst:
				s.position+=hT.normal*time.dt*s.move_speed
			if hT.entity:
				cc.wall_hit(hT.entity)
		if s.is_slp:
			cc.c_slide(s)
		if mvD.length() > 0:
			if any([s.stun,s.b_smash,s.pushed,st.p_rst(s)]):
				return
			mc=raycast(s.world_position+(0,.2,0),mvD,distance=.25,ignore=uq,debug=False)
			s.rotation_y=atan2(-mvD.x,-mvD.z)*180/math.pi
			st.p_last_direc=mvD
			s.walk_event()
			if not mc or str(mc.entity) in LC.item_lst|LC.trigger_lst:
				s.position+=mvD*(time.dt*s.move_speed)
			if mc.entity:
				cc.wall_hit(mc.entity)
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
			sn.footstep(self)
			if s.is_slp:
				s.wksn=.5
				return
			s.wksn=.35
	def jump_typ(self,t):
		s=self
		grv={1:(2.5),2:(2.8),3:(3.0),4:(2.7)}
		jmh={1:s.y+.8,#		normal jump
			2:s.y+1,#		crate jump
			3:s.y+1.1,#		bounce jump
			4:s.y+1.5}#		spring jump
		s.gravity=grv[t]#	fall speed
		s.vpos=jmh[t]#		jump heigt limit
		s.fall_time=0
		s.frst_lnd=True
		s.jumping=True
		if t == 4:
			s.b_smash=False
		del jmh,grv
	def jump(self):
		s=self
		s.frst_lnd=True
		hgt={True:.3,False:.1}
		fgt={True:2.2,False:2}
		kt=(s.space_time > .09)
		s.y=lerp(s.y,s.vpos+hgt[kt]+.1,(time.dt*s.gravity)*fgt[kt])
		if s.walking:
			s.is_flip=True
		if not s.is_flip:
			an.jump_up(s)
		if (s.y >= s.vpos+hgt[kt]):
			s.space_time=0
			s.jumping=False
			del hgt,fgt,kt
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
		if s.stun:
			return
		if st.death_event or (s.is_flip or s.is_attack):
			return
		if s.b_smash:
			an.belly_smash(s)
			return
		an.fall(s)
	def c_camera(self):
		s=self
		if not st.death_event:
			if st.bonus_round:
				cc.cam_bonus(s)
				return
			if s.indoor > 0:
				cc.cam_indoor(s)
				return
			cc.cam_level(s)
	def death_action(self):
		s=self
		dtc=s.dth_cause
		s.dth_timer-=time.dt
		if s.dth_timer <= 0:
			s.dth_timer=4
			cc.reset_state(s)
			return
		if dtc in [1,5]:
			s.visible=False
			return
		cbda={2:lambda:an.dth_angelfly(s),
			3:lambda:an.dth_wtr_swim(s),
			4:lambda:an.dth_fire_ash(s),
			6:lambda:an.dth_el_shock(s),
			7:lambda:an.dth_beesting(s),
			8:lambda:an.dth_c_buried(s),
			9:lambda:an.dth_shrink(s)}
		cbda[dtc]()
		del cbda
	def refr_tex(self):
		s=self
		if s.is_attack:
			if not atp in {s.texture,s.cur_tex}:
				s.texture,s.cur_tex=atp,atp
			return
		if not dtp in {s.texture,s.cur_tex}:
			s.texture,s.cur_tex=dtp,dtp
	def refr_anim(self):
		s=self
		anim={(s.pushed,an.c_push_back),
			(s.landed and s.is_landing and not any([s.walking,s.jumping,s.is_attack,s.falling,s.standup]),an.land if not s.b_smash else an.belly_land),
			(s.stun,an.c_stun),
			(s.standup,an.stand_up),
			(s.is_attack,an.spin),
			(s.is_flip and not (s.landed and s.is_attack),an.flip),
			((st.p_idle(s) or s.freezed),an.slide_stop if s.is_slp else an.idle)}
		for cds,do_anim in anim:
			if cds:
				do_anim(s)
				del anim,cds
				return
	def hurt_visual(self):
		for vkh in range(7):
			invoke(lambda:cc.hurt_blink(self),delay=vkh/3)
	def c_physic(self):
		s=self
		cc.various_val(s)
		cc.check_ceiling(s)
		if not s.jumping:
			cc.check_floor(s)
	def c_interact(self):
		s=self
		s.move()
		s.c_camera()
		if s.jumping:s.jump()
		if s.b_smash:cc.c_smash(s)
		if s.is_attack:cc.c_attack(s)
		if held_keys[settings.JMP_KEY]:s.space_time+=time.dt/2
		if st.aku_hit >= 3:cc.c_shield()
	def update(self):
		if not st.gproc():
			s=self
			if st.death_event:
				s.death_action()
				return
			s.c_physic()
			if not st.p_rst(s):
				s.c_interact()
			s.refr_tex(),s.refr_anim()