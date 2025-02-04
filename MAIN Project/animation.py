import status,_core,_loc,sound,time,random
from ursina.ursinastuff import destroy
from ursina import Entity,color,invoke

## walk frame count npc
npc_anim={0:7,#amadillo
		1:12,#turtle
		2:12,#saw turtle
		3:13,#vulture
		4:15,#penguin
		5:12,#hedgehog
		6:14,#seal
		7:13,#eating plant
		8:8,#rat
		9:11,#lizard
		10:3,#scrubber
		11:8,#mouse
		12:12,#eel
		13:16,#sewer mine
		14:0,#gorilla
		15:0,#bee
		16:10,#lumberjack
		17:13,#spider robot f
		18:13,#spider robot t
		19:29,#robot
		20:0}#lab assistant

cl='res/objects/l5/loose_ptf/'
cf='res/crate/anim/'
nf='res/npc/'
af='res/pc/'
mo='model'
st=status
sn=sound
cc=_core
bT=50
t=18

## crash play animation
def idle(d,sp):
	d.idfr=min(d.idfr+time.dt*sp,10.999)
	if d.idfr > 10.99:
		d.idfr=0
	d.model=af+'idle/'+str(int(d.idfr))+'.ply'
	del d,sp

def run(d,sp):
	d.rnfr=min(d.rnfr+time.dt*sp,10.999)
	if d.rnfr > 10.99:
		d.rnfr=0
	d.model=af+'run/'+str(int(d.rnfr))+'.ply'
	del d,sp

def run_s(d,sp):
	d.srfr=min(d.srfr+time.dt*sp,6.999)
	if d.srfr > 6.99:
		d.srfr=0
	d.model=af+'slide_start/'+str(int(d.srfr))+'.ply'

def slide_stop(d,sp):
	d.ssfr=min(d.ssfr+time.dt*sp,3.999)
	if d.ssfr > 3.99:
		d.ssfr=3
	d.model=af+'slide_stop/'+str(int(d.ssfr))+'.ply'

def jup(d,sp):
	d.jmfr=min(d.jmfr+time.dt*sp,2.999)
	if d.jmfr > 2.99:
		return
	d.model=af+'jmup/'+str(int(d.jmfr))+'.ply'
	del d,sp

def spin(d,sp):
	d.spfr=min(d.spfr+time.dt*sp,11.999)
	if d.spfr > 11.99:
		d.spfr=0
	d.model=af+'spn/'+str(int(d.spfr))+'.ply'
	del d,sp

def land(d,sp):
	d.ldfr=min(d.ldfr+time.dt*sp,12.999)
	if d.ldfr > 12.99:
		d.is_landing=False
		d.ldfr=0
		return
	d.model=af+'lnd/'+str(int(d.ldfr))+'.ply'
	del d,sp

def fall(d,sp):
	if d.fafr < 7.99:
		d.fafr=min(d.fafr+time.dt*sp,7.99)
	d.model=af+'fall/'+str(int(d.fafr))+'.ply'
	del d,sp

def flip(d,sp):
	d.flfr=min(d.flfr+time.dt*sp,16.999)
	if d.flfr > 16.99:
		d.is_flip=False
		d.flfr=0
		return
	d.model=af+'flp/'+str(int(d.flfr))+'.ply'
	del d,sp

def belly_smash(d,sp):
	d.smfr=min(d.smfr+time.dt*sp,2.999)
	if d.smfr > 2.99:
		d.smfr=2
		return
	d.model=af+'smash/'+str(int(d.smfr))+'.ply'

def belly_land(d,sp):
	d.blfr=min(d.blfr+time.dt*sp,3.999)
	if d.blfr > 3.99:
		d.blfr=0
		d.standup=True
		d.b_smash=False
		return
	d.model=af+'smash_land/'+str(int(d.blfr))+'.ply'

def stand_up(d,sp):
	d.sufr=min(d.sufr+time.dt*sp,8.999)
	if d.sufr > 8.99:
		d.sufr=0
		d.blfr=0
		d.is_landing=False
		d.standup=False
		return
	d.model=af+'stand_up/'+str(int(d.sufr))+'.ply'

def diggin_in(d,sp):
	d.dgifr=min(d.dgifr+time.dt*sp,7.999)
	if d.dgifr > 7.99:
		d.dig_in=False
		d.digged=True
		d.visible=False
		return
	d.model=af+'dig_in/'+str(int(d.dgifr))+'.ply'
	del d,sp

def diggin_out(d,sp):
	d.dgofr=min(d.dgofr+time.dt*sp,2.999)
	if d.dgofr > 2.99:
		d.dig_out,d.dig_in,d.digged=False,False,False
		d.visible=True
		return
	d.model=af+'dig_out/'+str(int(d.dgofr))+'.ply'
	del d,sp

def c_stun(d,sp):
	d.stnfr=min(d.stnfr+time.dt*sp,14.999)
	if d.stnfr > 14.99:
		d.stnfr=0
		return
	d.model=af+'stun/'+str(int(d.stnfr))+'.ply'
	del d,sp


## crash death animations
def dth_angelfly(c):
	c.y+=time.dt
	c.dth_fr=min(c.dth_fr+time.dt*t,20.999)
	if c.texture != af+'death/angel/0.tga':
		c.texture=af+'death/angel/0.tga'
	if not c.dth_snd:
		c.dth_snd=True
		sn.pc_audio(ID=15,pit=.35)
	if c.dth_fr > 20.99:
		c.dth_fr=0
		sn.pc_audio(ID=16)
	c.model=af+f'death/angel/{int(c.dth_fr)}.ply'

def dth_wtr_swim(c):
	c.dth_fr=min(c.dth_fr+time.dt*t,25.999)
	if c.dth_fr > 25.99:
		c.dth_fr=25
	c.model=af+f'death/water/{int(c.dth_fr)}.ply'

def dth_fire_ash(c):
	if not c.dth_snd:
		c.dth_snd=True
		sn.obj_audio(ID=16,pit=1.1)
	c.dth_fr=min(c.dth_fr+time.dt*t,24.999)
	if c.dth_fr > 24.99:
		c.dth_fr=24
	c.model=af+f'death/fire/{int(c.dth_fr)}.ply'

def dth_el_shock(c):
	if not c.dth_snd:
		c.dth_snd=True
		sn.obj_audio(ID=17)
	c.dth_fr=min(c.dth_fr+time.dt*t,1.999)
	if c.dth_fr > 1.99:
		c.dth_fr=0
	c.texure=af+f'death/volt/{int(c.dth_fr)}.tga'
	c.model=af+f'death/volt/{int(c.dth_fr)}.ply'

def dth_beesting(c):
	if not c.landed:
		c.y=(c.y-c.y)
	c.rotation_y=0
	c.dth_fr=min(c.dth_fr+time.dt*t,47.999)
	if c.dth_fr > 47.99:
		c.dth_fr=47
	c.model=af+f'death/sting/{int(c.dth_fr)}.ply'

def dth_c_buried(c):
	c.scale_x=c.inv_sc
	c.rotation_y=0
	if not c.sma_dth:
		c.sma_dth=True
		c.y-=.3
	if c.texture != af+'death/buried/0.tga':
		c.texture=af+'death/buried/0.tga'
	c.dth_fr=min(c.dth_fr+time.dt*t,10.999)
	if c.dth_fr > 10.99:
		c.dth_fr=10
	c.model=af+f'death/buried/{int(c.dth_fr)}.ply'


## crate animation
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

br='brk/0'
class CrateBreak(Entity):
	def __init__(self,cr):
		s=self
		super().__init__(model=cf+br+'.ply',texture=cf+br+'.tga',rotation=(-90,random.randint(0,360),0),scale=.4/1000,position=(cr.x,cr.y-.16,cr.z),unlit=False)
		s.frame_break=0
		s.color=color.rgb32(180,80,0)
		if cr.vnum == 3:
			s.color=color.rgb32(140,70,0)
		if cr.vnum == 11:
			s.color=color.rgb32(190,0,0)
		if cr.vnum == 12:
			s.color=color.rgb32(0,190,0)
		if cr.vnum == 16:
			s.color=color.rgb32(160,0,160)
		del cr
	def update(self):
		if st.gproc():
			return
		s=self
		s.frame_break=min(s.frame_break+time.dt*t,13.999)
		if s.frame_break > 13.99:
			s.frame_break=0
			s.texture=None
			destroy(s)
			return
		s.model=cf+f'brk/{int(s.frame_break)}.ply'

class CollapseFloor(Entity):
	def __init__(self,t,pos):
		s=self
		dc=.01/15
		super().__init__(model=cl+f'{t}/0.ply',texture=cl+f'{t}/0.png',position=pos,scale=(-dc,dc,dc),rotation=(-90,-270,0))
		s.typ=t
		s.frm=0
		del t,pos,dc
	def update(self):
		if st.gproc():
			return
		s=self
		s.frm=min(s.frm+(time.dt*18),32.999)
		if s.frm > 32.99:
			s.frm=0
			s.disable()
			destroy(s)
			return
		s.model=cl+f'{s.typ}/{int(s.frm)}.ply'

##warp rings
class WarpRingEffect(Entity): ## spawn animation
	def __init__(self,pos):
		s=self
		s.omf='res/objects/ev/'
		super().__init__(model=s.omf+'warp_rings/0.ply',texture=s.omf+'warp_rings/ring.tga',scale=.0016/2,rotation_x=-90,position=pos,color=color.white,alpha=.9,unlit=False)
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
			s.rings=min(s.rings+time.dt*30,8.999)
			if s.rings > 8.99:
				s.rings=0
				s.times+=1
				sn.pc_audio(ID=1,pit=.35)
			s.model=s.omf+'warp_rings/'+str(int(s.rings))+'.ply'
			if s.times > 7:
				_loc.ACTOR.warped=True
				destroy(s)

## npc animation
def npc_walking(m):
	m.anim_frame=min(m.anim_frame+time.dt*t,npc_anim[m.vnum]+.999)
	if m.anim_frame > npc_anim[m.vnum]+.99:
		m.anim_frame=0
	m.model=nf+str(m)+'/'+str(int(m.anim_frame))+'.ply'

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
	m.def_frame=min(m.def_frame+time.dt*t,6.999)
	if m.def_frame > 6.99:
		m.def_frame=0
	m.model=hdg+'attack/'+str(int(m.def_frame))+'.ply'

#rat idle
rti=nf+'rat/idle/'
def rat_idle(m):
	m.idl_frm=min(m.idl_frm+time.dt*t,10.999)
	if m.idl_frm > 10.99:
		m.idl_frm=0
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
	b.frm=min(b.frm+time.dt*sp,9.999)
	if b.frm > 9.99:
		b.frm=0
	b.model=nf+bb+str(int(b.frm))+'.ply'
	del b,sp

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
	m.frm=min(m.frm+time.dt*sp,10.999)
	if m.frm > 10.99:
		m.frm=0
	m.model=ldm+str(int(m.frm))+'.ply'
	del m,sp

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
	lp.frm=min(lp.frm+time.dt*10,3.999)
	if lp.frm > 3.99:
		lp.frm=3
	lp.model=labp+f'{lp.mode}/{int(lp.frm)}.ply'

labt='res/objects/l7/lab_taser/'
def taser_rotation(t):
	t.frm=min(t.frm+time.dt*15,6.999)
	if t.frm > 6.99:
		t.frm=0
	t.model=labt+f'/{int(t.frm)}.ply'
## door animation
dpw='res/objects/ev/door/'
def door_open(d):
	if not d.d_opn:
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
	if d.d_opn:
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