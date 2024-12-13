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
		16:10}#lumberjack

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

## player animation
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
#def dig_attack(d,sp):

## crash death animationsa
def angel_fly(c):
	DTH=13
	ATF=af+'death/angel/'
	c.model=ATF+'0.ply'
	c.texture=ATF+'crash_death.tga'
	c.animate_y(c.y+1.7,duration=2)
	invoke(lambda:setattr(c,mo,ATF+'1.ply'),delay=1/DTH)
	invoke(lambda:setattr(c,mo,ATF+'2.ply'),delay=2/DTH)
	invoke(lambda:setattr(c,mo,ATF+'3.ply'),delay=3/DTH)
	invoke(lambda:setattr(c,mo,ATF+'4.ply'),delay=4/DTH)
	invoke(lambda:setattr(c,mo,ATF+'5.ply'),delay=5/DTH)
	invoke(lambda:setattr(c,mo,ATF+'6.ply'),delay=6/DTH)
	invoke(lambda:setattr(c,mo,ATF+'7.ply'),delay=7/DTH)
	invoke(lambda:setattr(c,mo,ATF+'8.ply'),delay=8/DTH)
	invoke(lambda:setattr(c,mo,ATF+'9.ply'),delay=9/DTH)
	invoke(lambda:setattr(c,mo,ATF+'10.ply'),delay=10/DTH)
	invoke(lambda:setattr(c,mo,ATF+'11.ply'),delay=11/DTH)
	invoke(lambda:setattr(c,mo,ATF+'12.ply'),delay=12/DTH)
	invoke(lambda:setattr(c,mo,ATF+'13.ply'),delay=13/DTH)
	invoke(lambda:setattr(c,mo,ATF+'14.ply'),delay=14/DTH)
	invoke(lambda:setattr(c,mo,ATF+'15.ply'),delay=15/DTH)
	invoke(lambda:setattr(c,mo,ATF+'16.ply'),delay=16/DTH)
	invoke(lambda:setattr(c,mo,ATF+'17.ply'),delay=17/DTH)
	invoke(lambda:setattr(c,mo,ATF+'18.ply'),delay=18/DTH)
	invoke(lambda:setattr(c,mo,ATF+'19.ply'),delay=19/DTH)
	invoke(lambda:setattr(c,mo,ATF+'20.ply'),delay=20/DTH)
	invoke(lambda:cc.reset_state(c),delay=3)

def water_swim(c):
	DTW=18
	sn.pc_audio(ID=10)
	ATW=af+'death/water/'
	c.model=ATW+'0.ply'
	c.texture=ATW+'0.tga'
	invoke(lambda:setattr(c,mo,ATW+'1.ply'),delay=1/DTW)
	invoke(lambda:setattr(c,mo,ATW+'2.ply'),delay=2/DTW)
	invoke(lambda:setattr(c,mo,ATW+'3.ply'),delay=3/DTW)
	invoke(lambda:setattr(c,mo,ATW+'4.ply'),delay=4/DTW)
	invoke(lambda:setattr(c,mo,ATW+'5.ply'),delay=5/DTW)
	invoke(lambda:setattr(c,mo,ATW+'6.ply'),delay=6/DTW)
	invoke(lambda:setattr(c,mo,ATW+'7.ply'),delay=7/DTW)
	invoke(lambda:setattr(c,mo,ATW+'8.ply'),delay=8/DTW)
	invoke(lambda:setattr(c,mo,ATW+'9.ply'),delay=9/DTW)
	invoke(lambda:setattr(c,mo,ATW+'10.ply'),delay=10/DTW)
	invoke(lambda:setattr(c,mo,ATW+'11.ply'),delay=11/DTW)
	invoke(lambda:setattr(c,mo,ATW+'12.ply'),delay=12/DTW)
	invoke(lambda:setattr(c,mo,ATW+'13.ply'),delay=13/DTW)
	invoke(lambda:setattr(c,mo,ATW+'14.ply'),delay=14/DTW)
	invoke(lambda:setattr(c,mo,ATW+'15.ply'),delay=15/DTW)
	invoke(lambda:setattr(c,mo,ATW+'16.ply'),delay=16/DTW)
	invoke(lambda:setattr(c,mo,ATW+'17.ply'),delay=17/DTW)
	invoke(lambda:setattr(c,mo,ATW+'18.ply'),delay=18/DTW)
	invoke(lambda:setattr(c,mo,ATW+'19.ply'),delay=19/DTW)
	invoke(lambda:setattr(c,mo,ATW+'20.ply'),delay=20/DTW)
	invoke(lambda:setattr(c,mo,ATW+'21.ply'),delay=21/DTW)
	invoke(lambda:setattr(c,mo,ATW+'22.ply'),delay=22/DTW)
	invoke(lambda:setattr(c,mo,ATW+'23.ply'),delay=23/DTW)
	invoke(lambda:setattr(c,mo,ATW+'24.ply'),delay=24/DTW)
	invoke(lambda:setattr(c,mo,ATW+'25.ply'),delay=25/DTW)
	invoke(lambda:cc.reset_state(c),delay=3)

def fire_ash(c):
	DTE=18
	ATA=af+'death/fire/'
	c.model=ATA+'0.ply'
	c.texture=ATA+'0.tga'
	invoke(lambda:setattr(c,mo,ATA+'1.ply'),delay=1/DTE)
	invoke(lambda:setattr(c,mo,ATA+'2.ply'),delay=2/DTE)
	invoke(lambda:setattr(c,mo,ATA+'3.ply'),delay=3/DTE)
	invoke(lambda:setattr(c,mo,ATA+'4.ply'),delay=4/DTE)
	invoke(lambda:setattr(c,mo,ATA+'5.ply'),delay=5/DTE)
	invoke(lambda:setattr(c,mo,ATA+'6.ply'),delay=6/DTE)
	invoke(lambda:setattr(c,mo,ATA+'7.ply'),delay=7/DTE)
	invoke(lambda:setattr(c,mo,ATA+'8.ply'),delay=8/DTE)
	invoke(lambda:setattr(c,mo,ATA+'9.ply'),delay=9/DTE)
	invoke(lambda:setattr(c,mo,ATA+'10.ply'),delay=10/DTE)
	invoke(lambda:setattr(c,mo,ATA+'11.ply'),delay=11/DTE)
	invoke(lambda:setattr(c,mo,ATA+'12.ply'),delay=12/DTE)
	invoke(lambda:setattr(c,mo,ATA+'13.ply'),delay=13/DTE)
	invoke(lambda:setattr(c,mo,ATA+'14.ply'),delay=14/DTE)
	invoke(lambda:setattr(c,mo,ATA+'15.ply'),delay=15/DTE)
	invoke(lambda:setattr(c,mo,ATA+'16.ply'),delay=16/DTE)
	invoke(lambda:setattr(c,mo,ATA+'17.ply'),delay=17/DTE)
	invoke(lambda:setattr(c,mo,ATA+'18.ply'),delay=18/DTE)
	invoke(lambda:setattr(c,mo,ATA+'19.ply'),delay=19/DTE)
	invoke(lambda:setattr(c,mo,ATA+'20.ply'),delay=20/DTE)
	invoke(lambda:setattr(c,mo,ATA+'21.ply'),delay=21/DTE)
	invoke(lambda:setattr(c,mo,ATA+'22.ply'),delay=22/DTE)
	invoke(lambda:setattr(c,mo,ATA+'23.ply'),delay=23/DTE)
	invoke(lambda:setattr(c,mo,ATA+'24.ply'),delay=24/DTE)
	invoke(lambda:cc.reset_state(c),delay=3)

def electric(c):
	ATV=af+'death/volt/'
	c.model=ATV+'0.ply'
	c.texture=ATV+'0.tga'
	invoke(lambda:cc.reset_state(c),delay=3)

def eat_by_plant(c):
	c.visible=False
	invoke(lambda:cc.reset_state(c),delay=3)

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
		elif cr.vnum == 11:
			s.color=color.rgb32(190,0,0)
		elif cr.vnum == 12:
			s.color=color.rgb32(0,190,0)
		elif cr.vnum == 16:
			s.color=color.rgb32(160,0,160)
		del cr
	def update(self):
		if st.gproc():
			return
		s=self
		s.frame_break=min(s.frame_break+time.dt*t,13.999)
		if s.frame_break > 13.99:
			s.frame_break=0
			destroy(s)
			return
		s.model=cf+'brk/'+str(int(s.frame_break))+'.ply'

class CollapseFloor(Entity):
	def __init__(self,t,pos):
		s=self
		dc=.01/15
		super().__init__(model=cl+f'{t}/0.ply',texture=cl+f'{t}/0.tga',position=pos,scale=(-dc,dc,dc),rotation=(-90,-270,0))
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