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

lbh=f'{nf}lumberjack/smash/'
lbas=f'{nf}lab_assistant/'
plt=f'{nf}eating_plant/'
hdg=f'{nf}hedgehog/'
rti=f'{nf}rat/idle/'
hpo=f'{nf}hippo/'
go=f'{nf}gorilla/'

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

##player animation logic
def c_animation(c):
	if c.stun:
		c_stun(c)
		return
	if c.pushed:
		c_push_back(c)
		return
	if c.standup:
		stand_up(c)
		return
	if c.is_spin:
		spin(c)
		return
	if c.is_flip and not (c.landed and c.is_spin):
		flip(c)
		return
	if (c.landed and c.is_landing) and not (c.walking or c.jumping or c.is_spin or c.falling):
		if c.b_smash:
			belly_land(c)
			return
		land(c)
		return
	if st.p_idle(c) or c.freezed:
		if c.is_slp:
			slide_stop(c)
			return
		idle(c)

##player animations
def idle(c):
	c.idfr+=ps
	if c.idfr > 10.99:
		c.idfr=0
	if c.model != f'{af}idle/{int(c.idfr)}.ply':
		c.model=f'{af}idle/{int(c.idfr)}.ply'

def run(c):
	c.rnfr+=ps
	if c.rnfr > 10.99:
		c.rnfr=0
	if c.model != af+f'run/{int(c.rnfr)}.ply':
		c.model=af+f'run/{int(c.rnfr)}.ply'

def run_s(d):
	d.srfr+=ps
	if d.srfr > 6.99:
		d.srfr=0
	d.model=af+f'slide_start/{int(d.srfr)}.ply'

def slide_stop(d):
	d.ssfr+=ps
	if d.ssfr > 3.99:
		d.ssfr=3
	d.model=af+f'slide_stop/{int(d.ssfr)}.ply'

def jump_up(d):
	d.jmfr+=ps
	if d.jmfr > 2.99:
		return
	d.model=af+f'jump_up/{int(d.jmfr)}.ply'

def spin(d):
	d.spfr+=.45
	if d.spfr > 11.99:
		d.spfr=0
		d.is_spin=False
	d.model=f'{af}spin/{int(d.spfr)}.ply'

def land(d):
	d.ldfr+=ps
	if d.ldfr > 12.99:
		d.is_landing=False
		d.ldfr=0
		return
	d.model=af+f'land/{int(d.ldfr)}.ply'

def fall(d):
	if d.fafr < 7.99:
		d.fafr=min(d.fafr+ps,7.999)
	d.model=af+f'fall/{int(d.fafr)}.ply'

def flip(d):
	d.flfr+=ps
	if d.flfr > 16.99:
		d.is_flip=False
		d.flfr=0
		return
	d.model=af+f'flip/{int(d.flfr)}.ply'

def belly_smash(d):
	d.smfr+=ps
	if d.smfr > 2.99:
		d.smfr=2
		return
	d.model=af+f'belly_smash/{int(d.smfr)}.ply'

def belly_land(d):
	d.blfr+=ps
	if d.blfr > 3.99:
		d.blfr=0
		d.standup=True
		d.b_smash=False
		return
	d.model=af+f'belly_smash_land/{int(d.blfr)}.ply'

def stand_up(d):
	d.sufr+=ps
	if d.sufr > 8.99:
		d.sufr=0
		d.blfr=0
		d.is_landing=False
		d.standup=False
		return
	d.model=af+f'stand_up/{int(d.sufr)}.ply'

def diggin_in(d):
	d.dgifr+=ps
	if d.dgifr > 7.99:
		d.dig_in=False
		d.digged=True
		d.visible=False
		return
	d.model=f'{af}dig_in/{int(d.dgifr)}.ply'

def diggin_out(d):
	d.dgofr+=ps
	if d.dgofr > 2.99:
		d.dig_out,d.dig_in,d.digged=False,False,False
		d.visible=True
		return
	d.model=f'{af}dig_out/{int(d.dgofr)}.ply'

def c_stun(c):
	c.position+=(0,time.dt*3,time.dt*4.5)
	c.stnfr+=ps
	if c.stnfr > 14.99:
		c.stnfr=0
		c.stun=False
		return
	c.model=af+f'stun/{int(c.stnfr)}.ply'

def c_push_back(c):
	c.x-=time.dt*4
	c.pshfr+=ps
	if c.pshfr > 4.99:
		c.pshfr=0
		c.pushed=False
		return
	c.model=af+f'push_back/{int(c.pshfr)}.ply'

##player death animations
def dth_angelfly(c):
	c.y+=time.dt
	c.dthfr+=ps
	if c.texture != f'{af}death/angel/0.png':
		c.texture=f'{af}death/angel/0.png'
	if not c.dth_snd:
		c.dth_snd=True
		sn.pc_audio(ID=15,pit=.35)
	if c.dthfr > 20.99:
		c.dthfr=0
		sn.pc_audio(ID=16)
	c.model=af+f'death/angel/{int(c.dthfr)}.ply'

def dth_wtr_swim(c):
	if not c.dth_snd:
		c.dth_snd=True
		sn.pc_audio(ID=10,pit=.75)
	c.dthfr+=ps
	if c.dthfr > 25.99:
		return
	c.model=af+f'death/water/{int(c.dthfr)}.ply'

def dth_fire_ash(c):
	if not c.dth_snd:
		c.dth_snd=True
		sn.pc_audio(ID=19,pit=1.2)
	c.dthfr+=ps
	if c.dthfr > 24.99:
		c.dthfr=24
	c.model=af+f'death/fire/{int(c.dthfr)}.ply'

def dth_el_shock(c):
	if not c.dth_snd:
		c.dth_snd=True
		sn.obj_audio(ID=16)
	c.dthfr+=ps
	if c.dthfr > 1.99:
		c.dthfr=0
	c.texure=af+f'death/volt/{int(c.dthfr)}.png'
	c.model=af+f'death/volt/{int(c.dthfr)}.ply'

def dth_beesting(c):
	if not c.landed:
		c.y=(c.y-c.y)
	c.rotation_y=0
	c.dthfr+=ps
	if c.dthfr > 47.99:
		c.dthfr=47
	c.model=af+f'death/sting/{int(c.dthfr)}.ply'

def dth_c_buried(c):
	c.scale_x=c.inv_sc
	c.rotation_y=0
	if not c.sma_dth:#flag for mirror anim
		c.sma_dth=True
		c.y-=.3
	if c.texture != f'{af}death/buried/0.png':
		c.texture=f'{af}death/buried/0.png'
	c.dthfr+=ps
	if c.dthfr > 10.99:
		c.dthfr=10
	c.model=af+f'death/buried/{int(c.dthfr)}.ply'

def dth_shrink(c):
	fv=time.dt/1000
	idle(c)
	if c.scale > (.1/400,.1/400,.1/400):
		c.scale-=(fv,fv,fv)

##npc animation
def npc_walking(m):
	m.anim_frame+=ps
	if m.anim_frame > m.max_frm+.99:
		m.anim_frame=0
	m.model=f'{nf}{m}/{int(m.anim_frame)}.ply' if m.vnum != 17 else f'{nf}{m}/{m.ro_mode}/{int(m.anim_frame)}.ply'

def plant_bite(m):
	m.atk_frame=min(m.atk_frame+time.dt*t,18.999)
	if m.atk_frame > 18.99:
		m.atk_frame=0
		m.atk=False
	m.model=f'{plt}attack/{int(m.atk_frame)}.ply'
def plant_eat(m):
	m.eat_frame=min(m.eat_frame+time.dt*t,30.999)
	if m.eat_frame > 30.99:
		m.eat_frame=0
		m.eat,m.atk=False,False
		return
	m.model=f'{plt}eat/{int(m.eat_frame)}.ply'

def hedge_defend(m):
	m.def_frame=min(m.def_frame+time.dt*t,6.999)
	if m.def_frame > 6.99:
		m.def_frame=0
	m.model=f'{hdg}attack/{int(m.def_frame)}.ply'

def rat_idle(m):
	cc.incr_frm(m,t)
	m.model=f'{rti}{int(m.frm)}.ply'

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

def hive_awake(h,sp):
	h.frm=min(h.frm+time.dt*sp,8.999)
	if h.frm > 8.99:
		h.frm=0
		h.active=True
		h.spawn_bee()
	h.model=f'{hpf}{int(h.frm)}.ply'
	del h,sp

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

def lmbjack_smash(m,sp):
	m.sma_frm=min(m.sma_frm+time.dt*sp,35.999)
	if m.sma_frm > 35.99:
		m.sma_frm=0
		m.is_atk=False
	m.model=f'{lbh}{int(m.sma_frm)}.ply'

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