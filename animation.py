import status,_core,_loc
from ursina import *

npc_anim={'amadillo':7,'turtle':12,'saw_turtle':12,'penguin':15,
		'hedgehog':12,'seal':14,'eating_plant':13,'rat':10,
		'lizard':11,'scrubber':3,'mouse':8,'vulture':13}

cf='res/crate/anim/'
nf='res/npc/'
af='res/pc/'
t=19

## player animation
def idle(d):
	if status.LV_CLEAR_PROCESS:
		d=None
		return
	d.idle_anim+=time.dt*15
	if d.idle_anim > 10.75:
		d.idle_anim=0
	d.texture=af+'idle/crash.tga'
	d.model=af+'idle/'+str(int(d.idle_anim))+'.ply'

def run(d):
	if status.LV_CLEAR_PROCESS:
		d=None
		return
	d.run_anim+=time.dt*t
	if d.run_anim >= 10.85:
		d.run_anim=0
	d.texture=af+'run/crash.tga'
	d.model=af+'run/'+str(int(d.run_anim))+'.ply'

def run_s(d):
	d.run_s_anim+=time.dt*t
	if d.run_s_anim > 6.75:
		d.run_s_anim=0
	d.texture=af+'slide_start/crash.tga'
	d.model=af+'slide_start/'+str(int(d.run_s_anim))+'.ply'

def slide_stop(d):
	d.anim_slide_stop+=time.dt*t
	if d.anim_slide_stop > 3.75:
		d.anim_slide_stop=3
	d.texture=af+'slide_stop/crash.tga'
	d.model=af+'slide_stop/'+str(int(d.anim_slide_stop))+'.ply'

def jup(d):
	d.jump_anim+=time.dt*t
	if d.jump_anim > 2.75:
		d.jump_anim=2
	d.texture=af+'jmup/crash.tga'
	d.model=af+'jmup/'+str(int(d.jump_anim))+'.ply'

def spin(d):
	d.spin_anim+=time.dt*25
	if d.spin_anim > 11.75:
		d.spin_anim=0
	d.texture=af+'spn/crash.tga'
	d.model=af+'spn/'+str(int(d.spin_anim))+'.ply'

def land(d):
	d.land_anim+=time.dt*t
	if d.land_anim > 12.75:
		d.is_landing=False
		d.land_anim=0
		return
	d.texture=af+'lnd/crash.tga'
	d.model=af+'lnd/'+str(int(d.land_anim))+'.ply'

def land_s(d):
	d.land_s_anim+=time.dt*t
	if d.land_s_anim > 7.75:
		d.land_s_anim=0
	d.texture=af+'slide_land/crash.tga'
	d.model=af+'slide_land/'+str(int(d.land_anim))+'.ply'

def fall(d):
	d.fall_anim+=time.dt*t
	if d.fall_anim > 7.75:
		d.fall_anim=7
	d.texture=af+'fall/crash.tga'
	d.model=af+'fall/'+str(int(d.fall_anim))+'.ply'

def flip(d):
	d.flip_anim+=time.dt*t
	if d.flip_anim > 16.75:
		d.flip_anim=0
		d.is_flip=False
	d.texture=af+'flp/crash.tga'
	d.model=af+'flp/'+str(int(d.flip_anim))+'.ply'

def player_death(d):
	d.death_anim+=time.dt*15
	d.y+=time.dt/1.25
	if d.death_anim > 20.75:
		status.is_dying=False
		d.death_anim=0
		_core.death_event(d)
	d.texture=af+'death/crash_death.tga'
	d.model=af+'death/'+str(int(d.death_anim))+'.ply'

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
			self.frame_break+=time.dt*20
			if self.frame_break > 13.75:
				self.frame_break=0
				self.parent=None
				self.disable()
				return
			self.model=cf+'brk/'+str(int(self.frame_break))+'.ply'

## Effects
class WarpVortex(FrameAnimation3d):
	def __init__(self,pos):
		super().__init__('res/objects/warp_vortex/vortex.obj',color=color.yellow,scale=.1,position=pos,fps=30,loop=True)

class WarpRingEffect(Entity): ## spawn animation
	def __init__(self,pos):
		self.omf='res/objects/ev/'
		super().__init__(model=self.omf+'warp_rings/0.ply',texture=self.omf+'warp_rings/ring.tga',scale=.0016/2,rotation_x=-90,position=pos,color=color.white,alpha=.8,unlit=False)
		self.ta=_loc.ACTOR
		self.rings=0
		self.times=0
	def update(self):
		if _core.level_ready:
			self.rings+=time.dt*30
			if self.rings > 8.75:
				self.rings=0
				self.times+=1
			if self.times > 5:
				self.ta.warped=True
				self.disable()
				return
			self.model=self.omf+'warp_rings/'+str(int(self.rings))+'.ply'

## npc animation
def npc_walking(m):
	if status.pause:
		return
	m.anim_frame+=time.dt*t
	if m.anim_frame > npc_anim[str(m)]+.75:
		m.anim_frame=0
	m.model=nf+str(m)+'/'+str(int(m.anim_frame))+'.ply'

def plant_bite(m):
	m.is_attacking=True
	m.atk_frame+=time.dt*t
	if m.atk_frame > 18.75:
		m.is_attacking=False
		m.is_bite=False
		m.atk_frame=0
		m.atk_wait=1
	m.texture=nf+str(m)+'/attack/plant.tga'
	m.model=nf+str(m)+'/attack/'+str(int(m.atk_frame))+'.ply'

def hedge_defend(m):
	m.def_frame+=time.dt*t
	if m.def_frame > 6.75:
		m.def_frame=0
	m.texture=nf+str(m)+'/attack/attack.tga'
	m.model=nf+str(m)+'/attack/'+str(int(m.def_frame))+'.ply'

def hippo_wait(m):
	m.a_frame+=time.dt*t
	if m.a_frame > 23.75:
		m.a_frame=0
		return
	m.model=nf+'hippo/'+str(int(m.a_frame))+'.ply'
def hippo_dive(m):
	m.a_frame+=time.dt*t
	if m.a_frame > 57.75:
		m.a_frame=0
		m.is_uw=True
		return
	m.model=nf+'hippo/'+str(int(m.a_frame))+'.ply'
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