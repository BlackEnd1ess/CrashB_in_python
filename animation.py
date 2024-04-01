from ursina import *
import status,_core

t=18
af='res/character/'
cf='res/crate/actions/'
nf='res/npc/'
gr=color.light_gray

## player animation
def idle(d):
	d.idle_anim+=time.dt*15
	if d.idle_anim > 10.75:
		d.idle_anim=0
	d.texture=af+'idle/crash.tga'
	d.model=af+'idle/'+str(int(d.idle_anim))+'.ply'

def run(d):
	d.run_anim+=time.dt*20
	if d.run_anim > 10.75:
		d.run_anim=0
	d.texture=af+'run/crash.tga'
	d.model=af+'run/'+str(int(d.run_anim))+'.ply'

def jup(d):
	d.jump_anim+=time.dt*t
	if d.jump_anim > 2.75:
		d.jump_anim=2
	d.texture=af+'_jup/crash.tga'
	d.model=af+'_jup/'+str(int(d.jump_anim))+'.ply'

def spin(d):
	d.spin_anim+=time.dt*25
	if d.spin_anim > 11.75:
		d.spin_anim=0
		d.is_attack=False
	d.texture=af+'_spn/crash.tga'
	d.model=af+'_spn/'+str(int(d.spin_anim))+'.ply'

def land(d):
	d.land_anim+=time.dt*t
	if d.land_anim > 12.75:
		d.land_anim=0
	d.texture=af+'_lnd/crash.tga'
	d.model=af+'_lnd/'+str(int(d.land_anim))+'.ply'

def fall(d):
	d.fall_anim+=time.dt*t
	if d.fall_anim > 7.75:
		d.fall_anim=7
	d.texture=af+'_fall/crash.tga'
	d.model=af+'_fall/'+str(int(d.fall_anim))+'.ply'

def flip(d):
	d.flip_anim+=time.dt*t
	if d.flip_anim > 16.75:
		d.flip_anim=0
		d.is_flip=False
	d.texture=af+'_flp/crash.tga'
	d.model=af+'_flp/'+str(int(d.flip_anim))+'.ply'

def player_death(d):
	d.death_anim+=time.dt*15
	d.y+=time.dt/1.25
	if d.death_anim > 20.75:
		status.is_dying=False
		d.death_anim=0
		_core.p_death_event(d)
	d.texture=af+'death/crash_death.tga'
	d.model=af+'death/'+str(int(d.death_anim))+'.ply'

## crate animation
bT=20
def crate_bounce(c):
	if not c.is_bounc and c.b_cnt < 5:
		c.is_bounc=True
		c.color=color.light_gray
		invoke(lambda:setattr(c,'model',cf+'bnc/bnc0.obj'),delay=0)
		invoke(lambda:setattr(c,'model',cf+'bnc/bnc1.obj'),delay=1/bT)
		invoke(lambda:setattr(c,'model',cf+'bnc/bnc2.obj'),delay=2/bT)
		invoke(lambda:setattr(c,'model',cf+'bnc/bnc3.obj'),delay=3/bT)
		invoke(lambda:setattr(c,'model',cf+'bnc/bnc4.obj'),delay=4/bT)
		invoke(lambda:setattr(c,'model',cf+'bnc/bnc5.obj'),delay=5/bT)
		invoke(lambda:setattr(c,'model',cf+'bnc/bnc6.obj'),delay=6/bT)
		invoke(lambda:setattr(c,'model',cf+'bnc/bnc7.obj'),delay=7/bT)
		invoke(lambda:setattr(c,'model',cf+'bnc/bnc8.obj'),delay=8/bT)
		invoke(lambda:setattr(c,'model',cf+'bnc/bnc9.obj'),delay=9/bT)
		invoke(lambda:setattr(c,'model',cf+'bnc/bnc10.obj'),delay=10/bT)
		invoke(lambda:setattr(c,'model',cf+'bnc/bnc11.obj'),delay=11/bT)
		invoke(lambda:setattr(c,'model',cf+'bnc/bnc12.obj'),delay=12/bT)
		invoke(lambda:setattr(c,'model',cf+'bnc/bnc13.obj'),delay=13/bT)
		invoke(lambda:setattr(c,'model',cf+'bnc/bnc14.obj'),delay=14/bT)
		invoke(lambda:setattr(c,'model',cf+'bnc/bnc0.obj'),delay=15/bT)
		invoke(lambda:setattr(c,'is_bounc',False),delay=15/bT)

def spring_animation(c):
	c.hide()
	W=.45
	anim=FrameAnimation3d(cf+'sw/sw_',texture=c.texture,fps=40,scale=c.scale,position=c.position,color=gr)
	invoke(anim.disable,delay=W)
	invoke(c.show,delay=W-.017)

class CrateBreak(Entity):
	def __init__(self,cr):
		if cr.vnum == 12:
			bco=color.green
		if cr.vnum == 11:
			bco=color.red
		else:
			bco=color.orange
		super().__init__(model=cf+'break/0.ply',texture=cf+'break/break.tga',rotation=(-90,cr.rotation_y,0),scale=.4/1000,color=bco,position=cr.position,unlit=False,collider=None)
		self.frame_break=0
	def update(self):
		if not status.pause or status.loading:
			self.frame_break+=time.dt*20
			if self.frame_break > 13.75:
				self.frame_break=0
				self.parent=None
				self.disable()
				return
			self.model=cf+'break/'+str(int(self.frame_break))+'.ply'

class WarpVortex(FrameAnimation3d):
	def __init__(self,pos):
		super().__init__('res/objects/warp_vortex/vortex.obj',color=color.yellow,scale=.1,position=pos,fps=30,loop=True)

## npc animation
def npc_walking(m):
	if status.pause:
		return
	m.anim_frame+=time.dt*t
	if m.anim_frame > status.npc_anim[str(m)]+.75:
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


## object animations
def door_open(do):
	if do.door_time < 3.9:
		ddt=int(do.door_time)
		do.door_time+=time.dt*8
		do.door.model='res/objects/door1/'+str(ddt)+'.ply'
		do.door1.model='res/objects/door/'+str(ddt)+'.ply'
		if do.door_time >= 3.9:
			do.door.hide()
			do.door1.hide()
			do.door.collider=None
			do.door1.collider=None
			do.door_move=False

def warp_vortex(d):
	print(d)