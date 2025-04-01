import status,_core,_loc,sound,time,random
from ursina.ursinastuff import destroy
from ursina import Entity,color,invoke

cl='res/objects/l5/loose_ptf/'
cf='res/crate/anim/'
nf='res/npc/'
af='res/pc/'
mo='model'

LC=_loc
st=status
sn=sound
cc=_core

bT=50
t=18

##animation logic
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
	if c.is_attack:
		spin(c)
		return
	if c.is_flip and not (c.landed and c.is_attack):
		flip(c)
		return
	if (c.landed and c.is_landing) and not any([c.walking,c.jumping,c.is_attack,c.falling]):
		if c.b_smash:
			belly_land(c)
		else:
			land(c)
		return
	if st.p_idle(c) or c.freezed:
		if c.is_slp:
			slide_stop(c)
		else:
			idle(c)

##animations
def idle(c):
	c.idfr=0 if c.idfr > 10.99 else min(c.idfr+time.dt*17,10.999)
	c.model=af+f'idle/{int(c.idfr)}.ply'

def run(c):
	c.rnfr=0 if c.rnfr > 10.99 else min(c.rnfr+time.dt*17,10.999)
	c.model=af+f'run/{int(c.rnfr)}.ply'

def run_s(d):
	d.srfr=0 if d.srfr > 6.99 else min(d.srfr+time.dt*16,6.999)
	d.model=af+f'slide_start/{int(d.srfr)}.ply'

def slide_stop(d):
	d.ssfr=3 if d.ssfr > 3.99 else min(d.ssfr+time.dt*18,3.999)
	d.model=af+f'slide_stop/{int(d.ssfr)}.ply'

def jump_up(d):
	d.jmfr=min(d.jmfr+time.dt*16,2.999)
	if d.jmfr > 2.99:
		return
	d.model=af+f'jmup/{int(d.jmfr)}.ply'

def spin(d):
	d.spfr=min(d.spfr+time.dt*24,11.999)
	if d.spfr > 11.99:
		d.spfr=0
		d.is_attack=False
	d.model=af+'spn/'+str(int(d.spfr))+'.ply'

def land(d):
	d.ldfr=min(d.ldfr+time.dt*18,12.999)
	if d.ldfr > 12.99:
		d.is_landing=False
		d.ldfr=0
		return
	d.model=af+f'lnd/{int(d.ldfr)}.ply'

def fall(d):
	d.fafr=min(d.fafr+time.dt*14,7.99) if d.fafr < 7.99 else 7
	d.model=af+'fall/'+str(int(d.fafr))+'.ply'

def flip(d):
	d.flfr=min(d.flfr+time.dt*21,16.999)
	if d.flfr > 16.99:
		d.is_flip=False
		d.flfr=0
		return
	d.model=af+'flp/'+str(int(d.flfr))+'.ply'

def belly_smash(d):
	d.smfr=min(d.smfr+time.dt*14,2.999)
	if d.smfr > 2.99:
		d.smfr=2
		return
	d.model=af+'smash/'+str(int(d.smfr))+'.ply'

def belly_land(d):
	d.blfr=min(d.blfr+time.dt*16,3.999)
	if d.blfr > 3.99:
		d.blfr=0
		d.standup=True
		d.b_smash=False
		return
	d.model=af+'smash_land/'+str(int(d.blfr))+'.ply'

def stand_up(d):
	d.sufr=min(d.sufr+time.dt*17,8.999)
	if d.sufr > 8.99:
		d.sufr=0
		d.blfr=0
		d.is_landing=False
		d.standup=False
		return
	d.model=af+'stand_up/'+str(int(d.sufr))+'.ply'

def diggin_in(d):
	d.dgifr=min(d.dgifr+time.dt*16,7.999)
	if d.dgifr > 7.99:
		d.dig_in=False
		d.digged=True
		d.visible=False
		return
	d.model=af+'dig_in/'+str(int(d.dgifr))+'.ply'

def diggin_out(d):
	d.dgofr=min(d.dgofr+time.dt*16,2.999)
	if d.dgofr > 2.99:
		d.dig_out,d.dig_in,d.digged=False,False,False
		d.visible=True
		return
	d.model=af+'dig_out/'+str(int(d.dgofr))+'.ply'

def c_stun(c):
	c.position+=(0,time.dt*3,time.dt*4.5)
	c.stnfr=min(c.stnfr+time.dt*16,14.999)
	if c.stnfr > 14.99:
		c.stnfr=0
		c.stun=False
		return
	c.model=af+f'stun/{int(c.stnfr)}.ply'

def c_push_back(c):
	c.x-=time.dt*4
	c.pshfr=min(c.pshfr+time.dt*12,4.999)
	if c.pshfr > 4.99:
		c.pshfr=0
		c.pushed=False
		return
	c.model=af+f'push/{int(c.pshfr)}.ply'

##death animations
def dth_angelfly(c):
	c.y+=time.dt
	c.dthfr=min(c.dthfr+time.dt*t,20.999)
	if c.texture != af+'death/angel/0.tga':
		c.texture=af+'death/angel/0.tga'
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
	c.dthfr=25 if c.dthfr > 25.99 else min(c.dthfr+time.dt*t,25.999)
	c.model=af+f'death/water/{int(c.dthfr)}.ply'

def dth_fire_ash(c):
	if not c.dth_snd:
		c.dth_snd=True
		sn.obj_audio(ID=16,pit=1.1)
	c.dthfr=min(c.dthfr+time.dt*t,24.999)
	if c.dthfr > 24.99:
		c.dthfr=24
	c.model=af+f'death/fire/{int(c.dthfr)}.ply'

def dth_el_shock(c):
	if not c.dth_snd:
		c.dth_snd=True
		sn.obj_audio(ID=17)
	c.dthfr=min(c.dthfr+time.dt*t,1.999)
	if c.dthfr > 1.99:
		c.dthfr=0
	c.texure=af+f'death/volt/{int(c.dthfr)}.tga'
	c.model=af+f'death/volt/{int(c.dthfr)}.ply'

def dth_beesting(c):
	if not c.landed:
		c.y=(c.y-c.y)
	c.rotation_y=0
	c.dthfr=min(c.dthfr+time.dt*t,47.999)
	if c.dthfr > 47.99:
		c.dthfr=47
	c.model=af+f'death/sting/{int(c.dthfr)}.ply'

def dth_c_buried(c):
	c.scale_x=c.inv_sc
	c.rotation_y=0
	if not c.sma_dth:#flag for mirror anim
		c.sma_dth=True
		c.y-=.3
	if c.texture != af+'death/buried/0.tga':
		c.texture=af+'death/buried/0.tga'
	c.dthfr=min(c.dthfr+time.dt*t,10.999)
	if c.dthfr > 10.99:
		c.dthfr=10
	c.model=af+f'death/buried/{int(c.dthfr)}.ply'

def dth_shrink(c):
	fv=time.dt/1000
	idle(c)
	if c.scale > (.1/400,.1/400,.1/400):
		c.scale-=(fv,fv,fv)

##crate animation
def bnc_anim(c):
	c.frm=min(c.frm+time.dt*bT,12.999)
	if c.frm > 12.99:
		c.frm=0
		c.is_bounc=False
	c.model=cf+f'bn/{int(c.frm)}.ply'

def prtc_anim(c):
	c.frm=min(c.frm+time.dt*bT,12.999)
	if c.frm > 12.99:
		c.frm=0
		c.hitten=False
	c.model=cf+f'prt/{int(c.frm)}.ply'

class CrateBreak(Entity):
	def __init__(self,pos,col):
		s=self
		super().__init__(model=cf+'brk/0.ply',texture=cf+'brk/0.tga',rotation=(-90,0,0),scale=.4/1000,position=(pos[0],pos[1]-.16,pos[2]),color=col,unlit=False)
		s.frm=0
		del pos,col
	def update(self):
		if st.gproc():
			return
		s=self
		s.frm=min(s.frm+time.dt*t,13.999)
		if s.frm > 13.99:
			s.frm=0
			destroy(s)
			return
		s.model=cf+f'brk/{int(s.frm)}.ply'

class CollapseFloor(Entity):
	def __init__(self,t,pos):
		s=self
		dc=.01/15
		super().__init__(model=cl+f'{t}/0.ply',texture=cl+f'{t}/0.png',position=pos,scale=(-dc,dc,dc),rotation=(-90,-270,0))
		s.typ=t
		s.frm=0
		del t,pos,dc,s
	def update(self):
		if st.gproc():
			return
		s=self
		s.frm=min(s.frm+time.dt*18,32.999)
		if s.frm > 32.99:
			s.frm=0
			s.disable()
			destroy(s)
			return
		s.model=cl+f'{s.typ}/{int(s.frm)}.ply'

##warp rings
wrv='res/objects/ev/'
class WarpRingEffect(Entity): ## spawn animation
	def __init__(self,pos):
		s=self
		super().__init__(model=wrv+'warp_rings/0.ply',texture=wrv+'warp_rings/ring.tga',scale=.0016/2,rotation_x=-90,position=pos,color=color.white,alpha=.9,unlit=False)
		s.activ=False
		s.rings=0
		s.times=0
		del pos
	def update(self):
		if not st.gproc() and cc.level_ready:
			s=self
			if not s.activ:
				s.activ=True
				sn.obj_audio(ID=0)
			s.rings=min(s.rings+time.dt*35,8.999)
			if s.rings > 8.99:
				s.rings=0
				s.times+=1
				sn.pc_audio(ID=1,pit=.35)
			s.model=wrv+f'warp_rings/{int(s.rings)}.ply'
			if s.times > 8:
				LC.ACTOR.warped=True
				destroy(s)

##npc animation
def npc_walking(m):
	m.anim_frame=0 if m.anim_frame > m.max_frm+.99 else min(m.anim_frame+time.dt*t,m.max_frm+.999)
	m.model=nf+f'{m}/{int(m.anim_frame)}.ply'

#plant attack
plt=nf+'eating_plant/'
def plant_bite(m):
	m.atk_frame=min(m.atk_frame+time.dt*t,18.999)
	if m.atk_frame > 18.99:
		m.atk_frame=0
		m.atk=False
	m.model=plt+'attack/'+str(int(m.atk_frame))+'.ply'
def plant_eat(m):
	m.eat_frame=min(m.eat_frame+time.dt*t,30.999)
	if m.eat_frame > 30.99:
		m.eat_frame=0
		m.eat,m.atk=False,False
		return
	m.model=plt+'eat/'+str(int(m.eat_frame))+'.ply'

#hedge def
hdg=nf+'hedgehog/'
def hedge_defend(m):
	m.def_frame=0 if m.def_frame > 6.99 else min(m.def_frame+time.dt*t,6.999)
	m.model=hdg+'attack/'+str(int(m.def_frame))+'.ply'

#rat idle
rti=nf+'rat/idle/'
def rat_idle(m):
	m.idl_frm=0 if m.idl_frm > 10.99 else min(m.idl_frm+time.dt*t,10.999)
	m.model=rti+str(int(m.idl_frm))+'.ply'

#hippo
hpo=nf+'hippo/'
def hippo_wait(m):
	m.a_frame=min(m.a_frame+time.dt*t,23.999)
	if m.a_frame > 23.99:
		m.a_frame=0
		return
	m.model=hpo+str(int(m.a_frame))+'.ply'
def hippo_dive(m):
	m.a_frame=min(m.a_frame+time.dt*t,57.999)
	if m.a_frame > 57.99:
		m.a_frame=0
		return
	m.model=hpo+str(int(m.a_frame))+'.ply'

#gorilla
gp=20
go=nf+'gorilla/'
def gorilla_take(m):
	m.anim_frame=min(m.anim_frame+time.dt*gp,32.999)
	if m.anim_frame > 32.99:
		m.anim_frame=0
		m.t_mode=1
		m.throw_log()
		return
	m.model=go+str(int(m.anim_frame))+'.ply'
def gorilla_throw(m):
	m.t_frame=min(m.t_frame+time.dt*gp,10.999)
	if m.t_frame > 10.99:
		m.t_frame=0
		m.t_mode=0
		return
	m.model=go+'/act/'+str(int(m.t_frame))+'.ply'
def gorilla_fall(m):
	m.f_frame=min(m.f_frame+time.dt*gp,10.999)
	if m.f_frame > 10.99:
		m.f_frame=0
		cc.purge_instance(m)
		return
	m.model=go+'/fall/'+str(int(m.f_frame))+'.ply'

lbas=nf+'lab_assistant/'
def lba_push(m):
	m.anim_frame=min(m.anim_frame+time.dt*12,4.999)
	if m.anim_frame > 4.99:
		m.do_push=False
		m.anim_frame=0
	m.model=lbas+f'push/{int(m.anim_frame)}.ply'
def lba_fall(m):
	m.anim_frame=min(m.anim_frame+time.dt*12,5.999)
	if m.anim_frame > 5.99:
		m.enabled=False
		destroy(m)
		return
	m.model=lbas+f'fall/{int(m.anim_frame)}.ply'

#hive
hpf='res/objects/l6/hive/'
def hive_awake(h,sp):
	h.frm=min(h.frm+time.dt*sp,8.999)
	if h.frm > 8.99:
		h.frm=0
		h.active=True
		h.spawn_bee()
	h.model=hpf+str(int(h.frm))+'.ply'
	del h,sp

bb='bee/'
def bee_fly(b,sp):
	b.frm=0 if b.frm > 9.99 else min(b.frm+time.dt*sp,9.999)
	b.model=nf+bb+str(int(b.frm))+'.ply'

tki='res/objects/l6/tikki/'
def tikki_rotate(t,sp):
	if t.an_mode == 0:
		t.frm=min(t.frm+time.dt*sp,10.999)
		if t.frm > 10.99:
			t.an_pause=1
			t.an_mode=1
	else:
		t.frm=max(t.frm-time.dt*sp,0)
		if t.frm == 0:
			t.an_pause=1
			t.an_mode=0
	t.model=tki+f'{int(t.frm)}.ply'
	del t,sp

lbh=nf+'lumberjack/smash/'
def lmbjack_smash(m,sp):
	m.sma_frm=min(m.sma_frm+time.dt*sp,35.999)
	if m.sma_frm > 35.99:
		m.sma_frm=0
		m.is_atk=False
	m.model=lbh+f'{int(m.sma_frm)}.ply'

ldm='res/objects/l6/lmine/'
def land_mine(m,sp):
	m.frm=0 if m.frm > 10.99 else min(m.frm+time.dt*sp,10.999)
	m.model=ldm+str(int(m.frm))+'.ply'

def mine_destroy(m,sp):
	m.frm=min(m.frm+time.dt*sp,10.999)
	if m.frm > 10.99:
		m.frm=0
		m.purge()
		return
	m.model=ldm+'expl/'+str(int(m.frm))+'.ply'

## lab pad
labp='res/objects/l7/e_pad/'
def pad_refr(lp):
	lp.frm=3 if lp.frm > 3.99 else min(lp.frm+time.dt*10,3.999)
	lp.model=labp+f'{lp.mode}/{int(lp.frm)}.ply'

labt='res/objects/l7/lab_taser/'
def taser_rotation(t):
	t.frm=0 if t.frm > 6.99 else min(t.frm+time.dt*15,6.999)
	t.model=labt+f'/{int(t.frm)}.ply'
## door animation
dpw='res/objects/ev/door/'
def door_open(d):
	d.d_frm=min(d.d_frm+time.dt*15,3.9)
	if d.d_frm >= 3.9:
		d.d_opn=True
		d.door_part.collider=None
		d.collider=None
		d.d_frm=3
		sn.obj_audio(ID=1)
	fk=str(int(d.d_frm))+'.ply'
	d.model=dpw+'u'+fk
	d.door_part.model=dpw+'d'+fk
def door_close(d):
	d.d_frm=max(d.d_frm-time.dt*15,0)
	if d.d_frm <= 0:
		d.d_opn=False
		d.door_part.collider='box'
		d.collider='box'
		d.d_frm=0
		sn.obj_audio(ID=1,pit=.85)
	fk=str(int(d.d_frm))+'.ply'
	d.model=dpw+'u'+fk
	d.door_part.model=dpw+'d'+fk