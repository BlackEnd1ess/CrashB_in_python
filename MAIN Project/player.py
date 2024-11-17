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

cHr='res/pc/'
atp=cHr+'/spn/crash.tga'
dtp=cHr+'crash.tga'

class pShadow(Entity):## shadow point
	def __init__(self):
		super().__init__(model='quad',texture=cHr+'shdw.png',color=color.black,rotation_x=90,scale=.25,origin_z=.01,alpha=.9,collider='box')
		_loc.shdw=self
	def flw_p(self):
		s=self
		ta=LC.ACTOR
		s.x=ta.x
		s.z=ta.z
		s.visible=not(ta.freezed)
		vSH=raycast(ta.world_position,-Vec3(0,1,0),distance=2,ignore=[s,ta],debug=False)
		if vSH.hit:
			if not (str(vSH.entity) in LC.item_lst|LC.trigger_lst):
				s.y=vSH.world_point.y
			return
		if ta.landed and not (ta.falling or ta.jumping):
			s.y=(ta.y)
	def update(self):
		if not st.gproc():
			self.flw_p()

class CrashB(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=cHr+'crash.ply',texture=cHr+'crash.tga',scale=.1/110,rotation_x=-90,position=pos,unlit=False)
		s.collider=BoxCollider(s,center=Vec3(s.x,s.y+50,s.z+400),size=Vec3(200,200,600))
		cc.set_val(s)
		an.WarpRingEffect(pos=s.position)
		Sequence(cc.c_shield,Wait(.25),loop=True)()
		Sequence(cc.c_attack,Wait(.1),loop=True)()
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
			#_debug_.MemoryTracker(interval=5,threshold=100000)
			debg.PlayerDBG()
			s.dev_act={
					sg.DEV_WARP:lambda:setattr(s,'position',(0,0,0)),
					sg.DEV_INFO:lambda:_debug_.chck_mem(),
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
		if not (s.is_attack or s.atk_ctm):
			s.atk_ctm,s.is_attack=True,True
			s.standup,s.is_landing=False,False
			sn.pc_audio(ID=3)
			invoke(lambda:setattr(s,'is_attack',False),delay=.5)
			invoke(lambda:setattr(s,'atk_ctm',False),delay=.75)
			return
		sn.pc_audio(ID=4)
	def move(self):
		s=self
		if (s.b_smash or st.p_rst(s)):
			return
		mvD=Vec3(held_keys[sg.RGT_KEY]-held_keys[sg.LFT_KEY],0,held_keys[sg.FWD_KEY]-held_keys[sg.BCK_KEY]).normalized()
		s.direc=mvD
		if s.is_slippery:
			cc.c_slide(s)
		if (mvD.length() > 0):
			st.p_last_direc=mvD
			mc=raycast(s.world_position+(0,.1,0),s.direc,distance=.2,ignore=[s,LC.shdw],debug=False)
			me=mc.entity
			mn=str(me)
			if not mc or (mc and mn in LC.item_lst|LC.trigger_lst):
				s.position+=mvD*(time.dt*s.move_speed)
			if (mn == 'fthr'):
				cc.get_damage(s,rsn=3)
			if (cc.is_crate(me) and me.vnum == 12):
				me.destroy()
			s.rotation_y=atan2(-mvD.x,-mvD.z)*180/math.pi
			s.walk_event()
			del mvD
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
			an.jup(s,sp=16)
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
		if st.death_event or (s.is_flip or s.is_attack):
			return
		if s.b_smash:
			an.belly_smash(s,sp=14)
			return
		an.fall(s,sp=14)
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
	def death_action(self,rsn):
		s=self
		if rsn > 0:#0 is falling
			dca={1:lambda:an.angel_fly(s),
				2:lambda:an.water_swim(s),
				3:lambda:an.fire_ash(s),
				4:lambda:an.electric(s),
				5:lambda:an.eat_by_plant(s)}
			dca[rsn]()
			del dca
			return
		invoke(lambda:cc.reset_state(s),delay=2)
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
		if (s.standup):
			an.stand_up(s,sp=18)
			return
		if (s.is_attack):
			an.spin(s,sp=22)
			return
		if s.is_flip and not (s.landed and s.is_attack):
			an.flip(s,sp=18)
			return
		if (s.landed and s.is_landing) and not any([s.walking,s.jumping,s.is_attack,s.falling]):
			if s.b_smash:
				an.belly_land(s,sp=16)
			else:
				an.land(s,sp=18)
			return
		if st.p_idle(s) or s.freezed:
			if s.is_slippery:
				an.slide_stop(s,sp=16)
			else:
				an.idle(s,sp=18)
	def hurt_visual(self):
		for vkh in range(7):
			invoke(lambda:cc.hurt_blink(self),delay=vkh/3)
	def c_physic(self):
		if st.death_event:
			return
		s=self
		cc.check_wall(s)
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
		if held_keys[settings.JMP_KEY]:
			s.space_time+=time.dt/2
	def update(self):
		if not st.gproc():
			s=self
			s.c_physic()
			if not st.p_rst(s):
				s.c_interact()
			if not st.death_event:
				s.refr_tex()
				s.refr_anim()