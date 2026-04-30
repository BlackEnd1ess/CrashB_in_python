import status,_core,_loc,sound,time,random
from ursina.ursinastuff import destroy
from ursina import Entity,color,invoke

cl='res/objects/l5/loose_ptf/'
cf='res/crate/anim/'
nf='res/npc/'
af='res/pc/'
mo='model'

labt='res/objects/l7/lab_taser/'
labp='res/objects/l7/e_pad/'
tki='res/objects/l6/tikki/'
hpf='res/objects/l6/hive/'
ldm='res/objects/l6/lmine/'
dpw='res/objects/ev/door/'

atp=f'{af}spin/crash.png'
dtp=f'{af}crash.png'

frg=f'{nf}frog/'
lbh=f'{nf}lumberjack/smash/'
lbas=f'{nf}lab_assistant/'
peng=f'{nf}penguin/'
plt=f'{nf}eating_plant/'
hdg=f'{nf}hedgehog/'
rti=f'{nf}rat/idle/'
btf=f'{nf}butterfly/'
hpo=f'{nf}hippo/'
go=f'{nf}gorilla/'
brd=f'{nf}bird/'

st=status
sn=sound
cc=_core
LC=_loc

ps=.3
qs=.5
bT=50
gp=20
t=18
## animator classes
class BoxBreak(Entity):
	def __init__(self,pos,ID):
		s=self
		s.vcol={3:color.rgb32(140,70,0),11:color.red,12:color.green,15:color.gold,16:color.rgb32(180,0,180)}
		col=color.orange if not (ID in s.vcol) else s.vcol[ID]
		super().__init__(model=f'{cf}brk/0.ply',texture=f'{cf}brk/0.png',rotation=(-90,0,0),scale=.4/1000,position=(pos[0],pos[1]-.16,pos[2]),color=col,unlit=False)
		sn.crate_audio(ID=2)
		s.frm=0
		del pos,ID,s,col
	def update(self):
		if st.gproc():
			return
		s=self
		s.frm+=.4
		if s.frm > 13.99:
			destroy(s)
			return
		s.model=f'{cf}brk/{int(s.frm)}.ply'

class BoxAnimation(Entity):
	def __init__(self,c):
		s=self
		if not c:
			super().__init__()
			destroy(self)
			return
		s.frm_path=f'{cf}prt/' if c.vnum == 14 else f'{cf}bn/'
		super().__init__(model=f'{s.frm_path}0.ply',texture=c.texture,position=c.position,scale=c.scale,color=c.color)
		s.max_frm=12.99
		s.frm_spd=.9
		s.box=c
		s.frm=0
		del c,s
	def update(self):
		if st.gproc():
			return
		s=self
		if not s.box:
			destroy(s)
			return
		s.frm+=s.frm_spd
		if s.frm > s.max_frm:
			s.visible=False
			s.box.visible=True
			destroy(s)
			return
		s.visible=True
		s.box.visible=False
		if s.model != f'{s.frm_path}{int(s.frm)}.ply':
			s.model=f'{s.frm_path}{int(s.frm)}.ply'

class NPCAnimator(Entity):
	def __init__(self,ID,pos,sca,rot,max_frm,col):
		s=self
		super().__init__(position=pos,scale=sca,rotation=rot,color=col)
		s.max_frame=max_frm
		s.unlit=False
		s.anm_sp=14
		s.vnum=ID
		s.frm=0
	def update(self):
		if st.gproc():
			return
		s=self
		s.frm+=time.dt*s.anm_sp
		if s.frm >= s.max_frame+.99:
			destroy(s)
			return
		if s.vnum == 14:
			s.model=f'{go}fall/{int(s.frm)}.ply'
		if s.vnum == 19:
			s.model=f'{lbas}fall/{int(s.frm)}.ply'

class CollapseFloor(Entity):
	def __init__(self,t,pos):
		s=self
		dc=.01/15
		super().__init__(model=f'{cl}{t}/0.ply',texture=f'{cl}{t}/0.png',position=pos,scale=(-dc,dc,dc),rotation=(-90,-270,0))
		s.spd=20
		s.frm=0
		s.typ=t
		del t,pos,dc,s
	def update(self):
		if st.gproc():
			return
		s=self
		s.frm+=time.dt*s.spd
		if s.frm > 32.99:
			s.visible=False
			destroy(s)
			return
		s.model=f'{cl}{s.typ}/{int(s.frm)}.ply'

class PlayerDeathAnimator(Entity):
	def __init__(self,pos,typ):
		s=self
		s.tex_info={2:f'{af}death/angel/0',
					3:f'{af}death/water/0',
					4:f'{af}death/fire/0',
					6:f'{af}death/volt/0',
					7:f'{af}death/sting/0',
					8:f'{af}death/buried/0'}
		if typ in s.tex_info:
			s.pre_tex=s.tex_info[typ]
		else:
			s.pre_tex=f'{af}idle/0'
		s.snd_info={
			2:lambda:sn.pc_audio(ID=15,pit=.35),
			3:lambda:sn.pc_audio(ID=10,pit=.75),
			4:lambda:sn.pc_audio(ID=19,pit=1.2),
			6:lambda:sn.pc_audio(ID=20)}
		if typ in s.snd_info:
			s.snd_info[typ]()
		s.dsc_x=.1/115 if typ != 8 else -.1/115
		super().__init__(model=f'{s.pre_tex}.ply',texture=f'{s.pre_tex}.png',position=pos,rotation=(-90,0,0),scale=(s.dsc_x,.1/115,.1/115),color=LC.ACTOR.color,unlit=False)
		s.dth_done=False
		s.dth_duration=5
		s.dthfr=0
		s.typ=typ
		if typ == 8:
			s.y-=.3
	def dth_angelfly(self):
		s=self
		s.y+=time.dt
		s.dthfr+=ps
		if s.dthfr > 20.99:
			s.dthfr=0
			sn.pc_audio(ID=16)
		s.model=f'{af}death/angel/{int(s.dthfr)}.ply'
	def dth_water(self):
		self.dthfr+=ps
		if self.dthfr > 25.99:
			return
		self.model=f'{af}death/water/{int(self.dthfr)}.ply'
	def dth_fire(self):
		self.dthfr+=ps
		if self.dthfr > 24.99:
			self.dthfr=24
		self.model=f'{af}death/fire/{int(self.dthfr)}.ply'
	def dth_electric(self):
		s=self
		s.dthfr+=ps
		if s.dthfr > 1.99:
			s.dthfr=0
		if s.model != f'{af}death/volt/{int(s.dthfr)}.ply':
			s.model=f'{af}death/volt/{int(s.dthfr)}.ply'
			s.texure=f'{af}death/volt/{int(s.dthfr)}.png'
	def dth_beesting(self):
		self.dthfr+=ps
		if self.dthfr > 47.99:
			self.dthfr=47
		self.model=f'{af}death/sting/{int(self.dthfr)}.ply'
	def dth_buried(self):
		self.dthfr+=ps
		if self.dthfr > 10.99:
			self.dthfr=10
		self.model=f'{af}death/buried/{int(self.dthfr)}.ply'
	def dth_shrink(self):
		fv=time.dt/1000
		if self.scale_x > .1/400:
			self.scale-=(fv,fv,fv)
	def finish_dth_event(self):
		if not self.dth_done:
			self.dth_done=True
			cc.reset_state(LC.ACTOR)
			destroy(self)
	def refr_animation(self):
		s=self
		if s.typ == 2:
			s.dth_angelfly()
			return
		if s.typ == 3:
			s.dth_water()
			return
		if s.typ == 4:
			s.dth_fire()
			return
		if s.typ == 6:
			s.dth_electric()
			return
		if s.typ == 7:
			s.dth_beesting()
			return
		if s.typ == 8:
			s.dth_buried()
			return
		if s.typ == 9:
			s.dth_shrink()
	def update(self):
		if st.gproc():
			return
		self.dth_duration-=time.dt
		if self.dth_duration <= 0:
			self.finish_dth_event()
			return
		self.refr_animation()

##player animation logic
def refr_animation(c):
	if c.is_spin:
		c_animation(c,5)#spin
		return
	if c.is_flip:
		c_animation(c,8)#flip
		return
	if c.stun:
		c_animation(c,12)#stun fly
		return
	if c.pushed:
		c_animation(c,13)#push back
		return
	if c.standup:
		c_animation(c,11)#stand up from b smash
		return
	if c.is_landing and c.landed and c.b_smash and not c.standup:
		c_animation(c,10)#belly smash land
		return
	if c.jumping:
		if c.air_time < .1 and c.walking and not (c.is_flip or c.falling):
			c.is_flip=True
			c.frm=0
			return
		c_animation(c,4)#jump up
		return
	if c.landed:
		if st.p_idle(c) or c.freezed:
			if c.is_slp:
				c_animation(c,3)#idle ice slippery
				return
			c_animation(c,0)#idle stand
			return
		if c.walking and not c.jumping:
			if c.is_slp:
				c_animation(c,2)#slippery walk
				return
			c_animation(c,1)#walk normal
			return
		if c.is_landing and not c.jumping:
			c_animation(c,6)#normal landing
			return
		return
	if c.falling:
		if c.b_smash:
			c_animation(c,9)#b smash
			return
		c_animation(c,7)#fall

frm_info={0:(10,f'{af}idle/'),
		1:(10,f'{af}run/'),
		2:(6,f'{af}slide_start/'),
		3:(3,f'{af}slide_stop/'),
		4:(2,f'{af}jump_up/'),
		5:(11,f'{af}spin/'),##error
		6:(12,f'{af}land/'),
		7:(7,f'{af}fall/'),
		8:(16,f'{af}flip/'),
		9:(2,f'{af}belly_smash/'),
		10:(3,f'{af}belly_smash_land/'),
		11:(8,f'{af}stand_up/'),
		12:(14,f'{af}stun/'),
		13:(4,f'{af}push_back/')}
def c_animation(c,n):
	if c.anim_idx != n:
		c.anim_idx=n
		c.frm=0
		c.texture=atp if n == 5 else dtp
	if c.frm > frm_info[n][0]+.99:
		cc.c_anim_flag(n)
		if n in (3,4,6,7,9,10,11):
			return
		c.frm=0
	c.frm=min(c.frm+(ps if n != 5 else .4),frm_info[n][0]+.999)
	mdl=f'{frm_info[n][1]}{int(c.frm)}.ply'
	if c.model != mdl:
		c.model=mdl

##npc animation
def refresh_npc_animation(m):
	if m.vnum == 16 and not m.walking:
		if m.is_atk:
			lmbjack_smash(m)
		return
	if m.vnum == 7:
		if m.eat:
			plant_eat(m)
			return
		if m.atk:
			plant_bite(m)
			return
	if m.vnum == 8 and not m.can_move:
		rat_idle(m)
		return
	if m.vnum == 5:
		if m.def_mode:
			hedge_defend(m)
			return
	npc_walking(m)

def npc_walking(m):
	m.anim_frame+=ps
	if m.anim_frame > m.max_frm+.99:
		m.anim_frame=0
	m.model=f'{nf}{m}/{m.typ}/{int(m.anim_frame)}.ply' if m.vnum == 17 else f'{nf}{m}/{int(m.anim_frame)}.ply'

def plant_bite(m):
	m.atk_frame+=time.dt*t
	if m.atk_frame > 18.99:
		m.atk_frame=0
		m.atk=False
	m.model=f'{plt}attack/{int(m.atk_frame)}.ply'

def plant_eat(m):
	m.eat_frame+=time.dt*t
	if m.eat_frame > 30.99:
		m.eat_frame=0
		m.eat=False
		m.atk=False
		return
	m.model=f'{plt}eat/{int(m.eat_frame)}.ply'

def hedge_defend(m):
	m.def_frame+=time.dt*t
	if m.def_frame > 6.99:
		m.def_frame=0
	m.model=f'{hdg}attack/{int(m.def_frame)}.ply'

def rat_idle(m):
	cc.incr_frm(m,t)
	m.model=f'{rti}{int(m.frm)}.ply'

def penguin_dizzy(m):
	m.anim_frame+=time.dt*m.spd
	if m.anim_frame > 24.99:
		m.anim_frame=0
		m.is_dizzy=False
	mdl=f'{peng}dizzy/{int(m.anim_frame)}.ply'
	if m.model != mdl:
		m.model=mdl

def hippo_wait(m):
	m.a_frame+=time.dt*t
	if m.a_frame > 23.99:
		m.a_frame=0
		return
	m.model=f'{hpo}{int(m.a_frame)}.ply'

def hippo_dive(m):
	m.a_frame+=time.dt*t
	if m.a_frame > 57.99:
		m.active=False
		m.is_dive=True
		m.a_frame=0
		m.col.collider=None
		return
	m.model=f'{hpo}{int(m.a_frame)}.ply'

def gorilla_take(m):
	m.frm+=time.dt*gp
	if m.frm > 32.99:
		m.frm=0
		m.t_mode=1
		m.do_throw=True
		return
	m.model=f'{go}{int(m.frm)}.ply'
def gorilla_throw(m):
	m.t_frame+=time.dt*gp
	if m.t_frame > 10.99:
		m.wait_next=False
		m.t_frame=0
		m.t_mode=0
		return
	m.model=f'{go}act/{int(m.t_frame)}.ply'

def lba_push(m):
	m.anim_frame=min(m.anim_frame+time.dt*12,4.999)
	if m.anim_frame > 4.99:
		m.anim_frame=0
		m.do_push=False
	m.model=lbas+f'push/{int(m.anim_frame)}.ply'

def hive_awake(h):
	h.frm+=time.dt*h.spd
	if h.frm > h.max_frm:
		h.frm=0
		h.active=True
		h.spawn_bee()
	md=f'{hpf}{h.typ}/{int(h.frm)}.ply'
	if h.model != md:
		h.model=md

def tikki_rotate(t,sp):
	if t.an_mode == 0:
		t.frm=min(t.frm+time.dt*sp,10.999)
		if t.frm > 10.99:
			t.an_pause=1
			t.an_mode=1
	else:
		t.frm=max(t.frm-time.dt*sp,0)
		if t.frm <= 0:
			t.an_pause=1
			t.an_mode=0
	t.model=f'{tki}{int(t.frm)}.ply'
	del t,sp

def lmbjack_smash(m):
	m.sma_frm+=time.dt*m.spd
	if m.sma_frm > 35.99:
		m.sma_frm=0
		sn.npc_audio(ID=9)
		m.is_atk=False
		return
	m.model=f'{lbh}{int(m.sma_frm)}.ply'

def frog_jump(m):
	m.frm+=time.dt*m.spd
	if m.frm > m.max_frm:
		m.frm=0
		m.is_jmp=False
	if m.model != f'{frg}{int(m.frm)}.ply':
		m.model=f'{frg}{int(m.frm)}.ply'

def btfly_fly(m):
	cc.incr_frm(m,m.spd)
	if m.model != f'{btf}/{m.typ}/{int(m.frm)}.ply':
		m.model=f'{btf}/{m.typ}/{int(m.frm)}.ply'

def bird_idle(m):
	m.frm+=time.dt*m.spd
	if m.frm > 7.99:
		m.frm=0
	mdl=f'{brd}{int(m.frm)}.ply'
	if m.model != mdl:
		m.model=mdl
def bird_fly(m):
	m.frm+=time.dt*m.spd
	if m.frm > 8.99:
		m.frm=0
	mdl=f'{brd}/fly/{int(m.frm)}.ply'
	if m.model != mdl:
		m.model=mdl

def land_mine(m,sp):
	m.frm+=time.dt*sp
	if m.frm > 10.99:
		m.frm=0
	m.model=f'{ldm}{int(m.frm)}.ply'

def mine_destroy(m,sp):
	m.frm=min(m.frm+time.dt*sp,10.999)
	if m.frm > 10.99:
		m.frm=0
		m.purge()
		return
	m.model=f'{ldm}expl/{int(m.frm)}.ply'

## lab pad
def pad_refr(lp):
	lp.frm=min(lp.frm+time.dt*10,3.999)
	if lp.frm > 3.99:
		lp.frm=3
	lp.model=labp+f'{lp.mode}/{int(lp.frm)}.ply'
def taser_rotation(t):
	t.frm+=time.dt*15
	if t.frm > 6.99:
		t.frm=0
	t.model=labt+f'/{int(t.frm)}.ply'

## door animation
def door_open(d):
	d.d_frm=min(d.d_frm+time.dt*15,3.999)
	if d.d_frm > 3.99:
		d.d_opn=True
		d.door_part.collider=None
		d.collider=None
		d.d_frm=3
		sn.obj_audio(ID=1)
	d.model=f'{dpw}u{int(d.d_frm)}.ply'
	d.door_part.model=f'{dpw}d{int(d.d_frm)}.ply'
def door_close(d):
	d.d_frm=max(d.d_frm-time.dt*15,0)
	if d.d_frm <= 0:
		d.d_opn=False
		d.door_part.collider='box'
		d.collider='box'
		d.d_frm=0
		sn.obj_audio(ID=1,pit=.85)
	fk=f'{int(d.d_frm)}.ply'
	d.model=f'{dpw}u{int(d.d_frm)}.ply'
	d.door_part.model=f'{dpw}d{int(d.d_frm)}.ply'