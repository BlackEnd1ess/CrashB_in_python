import status,_core,_loc,sound
from ursina import *

npc_anim={0:7,#amadillo
		1:12,#turtle
		2:12,#saw turtle
		3:13,#vulture
		4:15,#penguin
		5:12,#hedgehog
		6:14,#seal
		7:13,#eating plant
		8:10,#rat
		9:11,#lizard
		10:3,#scrubber
		11:8,#mouse
		12:12,#eel
		13:16}#sewer mine

cf='res/crate/anim/'
nf='res/npc/'
af='res/pc/'
mo='model'
sn=sound
cc=_core
t=18

## player animation
def idle(d,sp):
	d.idfr+=time.dt*sp
	if d.idfr > 10.75:
		d.idfr=0
	d.texture=af+'idle/crash.tga'
	d.model=af+'idle/'+str(int(d.idfr))+'.ply'

def run(d,sp):
	d.rnfr+=time.dt*sp
	if d.rnfr > 10.9:
		d.rnfr=0
	d.texture=af+'run/crash.tga'
	d.model=af+'run/'+str(int(d.rnfr))+'.ply'

def run_s(d,sp):
	d.srfr+=time.dt*sp
	if d.srfr > 6.75:
		d.srfr=0
	d.texture=af+'slide_start/crash.tga'
	d.model=af+'slide_start/'+str(int(d.srfr))+'.ply'

def slide_stop(d,sp):
	d.ssfr+=time.dt*sp
	if d.ssfr > 3.9:
		d.ssfr=3
	d.texture=af+'slide_stop/crash.tga'
	d.model=af+'slide_stop/'+str(int(d.ssfr))+'.ply'

def jup(d,sp):
	d.jmfr+=time.dt*sp
	if d.jmfr > 2.9:
		return
	d.texture=af+'jmup/crash.tga'
	d.model=af+'jmup/'+str(int(d.jmfr))+'.ply'

def spin(d,sp):
	d.spfr+=time.dt*sp
	if d.spfr > 11.9:
		d.spfr=0
	d.texture=af+'spn/crash.tga'
	d.model=af+'spn/'+str(int(d.spfr))+'.ply'

def land(d,sp):
	d.ldfr+=time.dt*sp
	if d.ldfr > 12.9:
		d.is_landing=False
		d.ldfr=0
		return
	d.texture=af+'lnd/crash.tga'
	d.model=af+'lnd/'+str(int(d.ldfr))+'.ply'

def land_s(d,sp):
	d.land_s_anim+=time.dt*sp
	if d.land_s_anim > 7.9:
		d.land_s_anim=0
	d.texture=af+'slide_land/crash.tga'
	d.model=af+'slide_land/'+str(int(d.land_anim))+'.ply'

def fall(d,sp):
	if d.fafr < 7.99:
		d.fafr=1
	d.fafr+=time.dt*sp
	d.texture=af+'fall/crash.tga'
	d.model=af+'fall/'+str(int(d.fafr))+'.ply'

def flip(d,sp):
	d.flfr+=time.dt*sp
	if d.flfr > 16.9:
		d.is_flip=False
		d.flfr=0
		return
	d.texture=af+'flp/crash.tga'
	d.model=af+'flp/'+str(int(d.flfr))+'.ply'

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
bT=40
def bnc_animation(c):
	invoke(lambda:setattr(c,'model',cf+'bn/0.ply'),delay=0)
	invoke(lambda:setattr(c,'model',cf+'bn/1.ply'),delay=1/bT)
	invoke(lambda:setattr(c,'model',cf+'bn/2.ply'),delay=2/bT)
	invoke(lambda:setattr(c,'model',cf+'bn/3.ply'),delay=3/bT)
	invoke(lambda:setattr(c,'model',cf+'bn/4.ply'),delay=4/bT)
	invoke(lambda:setattr(c,'model',cf+'bn/5.ply'),delay=5/bT)
	invoke(lambda:setattr(c,'model',cf+'bn/6.ply'),delay=6/bT)
	invoke(lambda:setattr(c,'model',cf+'bn/7.ply'),delay=7/bT)
	invoke(lambda:setattr(c,'model',cf+'bn/8.ply'),delay=8/bT)
	invoke(lambda:setattr(c,'model',cf+'bn/9.ply'),delay=9/bT)
	invoke(lambda:setattr(c,'model',cf+'bn/10.ply'),delay=10/bT)
	invoke(lambda:setattr(c,'model',cf+'bn/11.ply'),delay=11/bT)
	invoke(lambda:setattr(c,'model',cf+'bn/12.ply'),delay=12/bT)
	invoke(lambda:setattr(c,'model',cf+'bn/0.ply'),delay=13/bT)
	invoke(lambda:setattr(c,'is_bounc',False),delay=13/bT)

def prtc_anim(c):
	invoke(lambda:setattr(c,'model',cf+'prt/0.ply'),delay=0)
	invoke(lambda:setattr(c,'model',cf+'prt/1.ply'),delay=1/bT)
	invoke(lambda:setattr(c,'model',cf+'prt/2.ply'),delay=2/bT)
	invoke(lambda:setattr(c,'model',cf+'prt/3.ply'),delay=3/bT)
	invoke(lambda:setattr(c,'model',cf+'prt/4.ply'),delay=4/bT)
	invoke(lambda:setattr(c,'model',cf+'prt/5.ply'),delay=5/bT)
	invoke(lambda:setattr(c,'model',cf+'prt/6.ply'),delay=6/bT)
	invoke(lambda:setattr(c,'model',cf+'prt/7.ply'),delay=7/bT)
	invoke(lambda:setattr(c,'model',cf+'prt/8.ply'),delay=8/bT)
	invoke(lambda:setattr(c,'model',cf+'prt/9.ply'),delay=9/bT)
	invoke(lambda:setattr(c,'model',cf+'prt/10.ply'),delay=10/bT)
	invoke(lambda:setattr(c,'model',cf+'prt/11.ply'),delay=11/bT)
	invoke(lambda:setattr(c,'model',cf+'prt/12.ply'),delay=12/bT)
	invoke(lambda:setattr(c,'model',cf+'prt/0.ply'),delay=13/bT)
	invoke(lambda:setattr(c,'hitten',False),delay=20/bT)

class CrateBreak(Entity):
	def __init__(self,cr):
		if cr.vnum in [11,12,15,16]:
			vco={11:color.red,12:color.green,15:color.gold,16:color.violet}
			bco=vco[cr.vnum]
		else:
			bco=color.orange
		anP=cr.position
		super().__init__(model=cf+'brk/0.ply',texture=cf+'brk/break.tga',rotation=(-90,random.randint(0,360),0),scale=.4/1000,color=bco,position=(anP[0],anP[1]-.16,anP[2]),unlit=False,collider=None)
		self.frame_break=0
	def update(self):
		if not status.gproc():
			self.frame_break+=time.dt*t
			if self.frame_break > 13.9:
				self.frame_break=0
				cc.purge_instance(self)
				return
			self.model=cf+'brk/'+str(int(self.frame_break))+'.ply'

##warp rings 
class WarpRingEffect(Entity): ## spawn animation
	def __init__(self,pos):
		self.omf='res/objects/ev/'
		super().__init__(model=self.omf+'warp_rings/0.ply',texture=self.omf+'warp_rings/ring.tga',scale=.0016/2,rotation_x=-90,position=pos,color=color.white,alpha=.8,unlit=False)
		self.activ=False
		self.ta=_loc.ACTOR
		self.rings=0
		self.times=0
	def update(self):
		if not status.gproc() and cc.level_ready:
			s=self
			if not s.activ:
				s.activ=True
				sn.obj_audio(ID=0)
			s.rings+=time.dt*30
			if s.rings > 8.9:
				s.rings=0
				s.times+=1
				sn.pc_audio(ID=1,pit=.35)
			s.model=s.omf+'warp_rings/'+str(int(s.rings))+'.ply'
			if s.times > 7:
				s.ta.warped=True
				cc.purge_instance(s)

## npc animation
def npc_walking(m):
	if status.pause:
		return
	m.anim_frame+=time.dt*t
	if m.anim_frame > npc_anim[m.vnum]+.9:
		m.anim_frame=0
	m.model=nf+str(m)+'/'+str(int(m.anim_frame))+'.ply'

#plant
def plant_bite(m):
	m.atk_frame+=time.dt*t
	if m.atk_frame > 18.9:
		m.atk_frame=0
	m.texture=nf+str(m)+'/attack/plant.tga'
	m.model=nf+str(m)+'/attack/'+str(int(m.atk_frame))+'.ply'
def plant_eat(m):
	m.eat_frame+=time.dt*t
	if m.eat_frame > 30.9:
		m.eat_frame=0
		m.eat=False
		return
	m.model=nf+str(m)+'/eat/'+str(int(m.eat_frame))+'.ply'

#hedge
def hedge_defend(m):
	m.def_frame+=time.dt*t
	if m.def_frame > 6.9:
		m.def_frame=0
	m.texture=nf+str(m)+'/attack/attack.tga'
	m.model=nf+str(m)+'/attack/'+str(int(m.def_frame))+'.ply'

#hippo
def hippo_wait(m):
	m.a_frame+=time.dt*18
	if m.a_frame > 23.9:
		m.a_frame=0
		return
	m.model=nf+'hippo/'+str(int(m.a_frame))+'.ply'
def hippo_dive(m):
	m.a_frame+=time.dt*18
	if m.a_frame > 57.9:
		m.a_frame=0
		return
	m.model=nf+'hippo/'+str(int(m.a_frame))+'.ply'

#gorilla
gsp=30
def gorilla_take(m):
	m.anim_frame+=time.dt*20
	if m.anim_frame > 32.9:
		m.anim_frame=0
		m.t_mode=1
		m.throw_log()
		return
	m.model=nf+str(m)+'/'+str(int(m.anim_frame))+'.ply'
def gorilla_throw(m):
	m.t_frame+=time.dt*20
	if m.t_frame > 10.9:
		m.t_frame=0
		m.t_mode=0
		return
	m.model=nf+str(m)+'/act/'+str(int(m.t_frame))+'.ply'
def gorilla_fall(m):
	m.f_frame+=time.dt*20
	if m.f_frame > 10.9:
		m.f_frame=0
		cc.purge_instance(m)
		return
	m.model=nf+str(m)+'/fall/'+str(int(m.f_frame))+'.ply'

## object animations
def door_open(d):
	invoke(lambda:setattr(d,'model',d.dPA+'u0.ply'),delay=0/t)
	invoke(lambda:setattr(d.door_part,'model',d.dPA+'d0.ply'),delay=0/t)
	invoke(lambda:setattr(d,'model',d.dPA+'u1.ply'),delay=1/t)
	invoke(lambda:setattr(d.door_part,'model',d.dPA+'d1.ply'),delay=1/t)
	invoke(lambda:setattr(d,'model',d.dPA+'u2.ply'),delay=2/t)
	invoke(lambda:setattr(d.door_part,'model',d.dPA+'d2.ply'),delay=2/t)
	invoke(lambda:setattr(d,'model',d.dPA+'u3.ply'),delay=3/t)
	invoke(lambda:setattr(d.door_part,'model',d.dPA+'d3.ply'),delay=3/t)
	d.door_part.collider=None
	d.collider=None

def door_close(d):
	invoke(lambda:setattr(d,'model',d.dPA+'u3.ply'),delay=0/t)
	invoke(lambda:setattr(d.door_part,'model',d.dPA+'d3.ply'),delay=0/t)
	invoke(lambda:setattr(d,'model',d.dPA+'u2.ply'),delay=1/t)
	invoke(lambda:setattr(d.door_part,'model',d.dPA+'d2.ply'),delay=1/t)
	invoke(lambda:setattr(d,'model',d.dPA+'u1.ply'),delay=2/t)
	invoke(lambda:setattr(d.door_part,'model',d.dPA+'d1.ply'),delay=2/t)
	invoke(lambda:setattr(d,'model',d.dPA+'u0.ply'),delay=3/t)
	invoke(lambda:setattr(d.door_part,'model',d.dPA+'d0.ply'),delay=3/t)
	d.door_part.collider='box'
	d.collider='box'

def warp_vortex(d):
	print(d)