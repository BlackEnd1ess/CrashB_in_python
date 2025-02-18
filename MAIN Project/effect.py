from ursina import Entity,Vec2,Vec3,color,Shader,Func,load_texture
from ursina.ursinastuff import destroy
import status,_core,_loc,time,random

trpv='res/objects/ev/teleport/warp_effect'
ef='res/effects/'
st=status
cc=_core
LC=_loc

class WarpVortex(Entity):
	def __init__(self,pos,sca,drc,col):
		s=self
		super().__init__(name='wvpx',position=pos,color=col,scale=sca,rotation_x=90,alpha=.5,unlit=False)
		s.spd=600
		s.drc=drc
		del pos,sca,drc,col
	def update(self):
		if st.gproc():
			return
		if LC.ACTOR.indoor > 0:
			s=self
			if s.texture != trpv+'.png':
				s.model=trpv+'.ply'
				s.texture=trpv+'.png'
			if s.drc == 1:
				s.rotation_y+=time.dt*s.spd
				return
			s.rotation_y-=time.dt*s.spd

class Sparkle(Entity):
	def __init__(self,pos):
		super().__init__(model='quad',texture=ef+'sparkle.tga',position=pos,scale=.04,color=color.gold,unlit=False)
		self.mode=0
	def update(self):
		if st.gproc():
			return
		s=self
		if s.mode == 0:
			s.scale+=Vec3(time.dt/2,time.dt/2,0)
			if s.scale_x > .1:
				s.mode=1
			return
		s.scale-=Vec3(time.dt/2,time.dt/2,0)
		if s.scale_x <= 0:
			destroy(s)

class JumpDust(Entity):
	def __init__(self,pos):
		super().__init__(model='quad',texture=ef+'fire_ball.png',position=pos,scale=.1,color=color.gray)
	def update(self):
		if st.gproc():
			return
		s=self
		s.scale+=(time.dt,time.dt)
		if s.scale_x > .6:
			destroy(s)

prsv='res/crate/anim/exp_wave/'
class PressureWave(Entity):
	def __init__(self,pos,col):
		s=self
		super().__init__(model=prsv+'0.ply',texture=prsv+'0.png',position=pos,scale=.0008,color=col,rotation_x=90,alpha=.8,unlit=False)
		s.frm=0
		del pos,col
	def update(self):
		if st.gproc():
			return
		s=self
		s.frm=min(s.frm+time.dt*15,4.999)
		if s.frm > 4.99:
			s.frm=0
			destroy(s)
			return
		s.model=prsv+f'{int(s.frm)}.ply'

frb='res/crate/anim/exp_fire/'
class Fireball(Entity):
	def __init__(self,cr):
		s=self
		nC=color.red
		if cr.name == 'ldmn':
			nC=color.orange
		if cc.is_crate(cr) and cr.vnum == 12:
			nC=color.green
		super().__init__(model='quad',texture=frb+'0.png',position=(cr.x,cr.y+.1,cr.z+random.uniform(-.1,.1)),color=nC,scale=.75,unlit=False)
		PressureWave(pos=s.position,col=nC)
		s.ex_step=0
		del cr,nC
	def update(self):
		if st.gproc():
			return
		s=self
		s.ex_step=min(s.ex_step+time.dt*25,14.999)
		s.texture=frb+f'{int(s.ex_step)}.png'
		s.visible=(s.ex_step < 14.99)
		if (s.ex_step > 14.99):
			destroy(s)

class FireThrow(Entity):
	def __init__(self,pos,ro_y):
		s=self
		super().__init__(model='quad',name='fthr',texture=ef+'fire_ball.png',position=(pos[0],pos[1]+.25,pos[2]),scale=.2,collider='box',unlit=False,color=random.choice([color.orange,color.red]))
		s.life_time=.4
		s.direc=ro_y
		s.mvs=4
		if ro_y in {90,-90}:
			s.z=s.z+random.uniform(-.1,.1)
	def fly_away(self):
		s=self
		mt=time.dt*s.mvs
		ddi={90:lambda:setattr(s,'x',s.x-mt),-90:lambda:setattr(s,'x',s.x+mt),
			180:lambda:setattr(s,'z',s.z+mt),0:lambda:setattr(s,'z',s.z-mt)}
		ddi[s.direc]()
	def update(self):
		if st.gproc():
			return
		s=self
		tdf=time.dt*1.1
		s.life_time=max(s.life_time-time.dt,0)
		if s.intersects(LC.ACTOR):
			cc.get_damage(LC.ACTOR,rsn=4)
		if s.life_time <= 0:
			destroy(s)
			return
		s.scale+=(tdf,tdf,tdf)
		s.fly_away()

class ElectroBall(Entity):
	def __init__(self,pos):
		super().__init__(model='quad',texture=ef+'sparkle.tga',name='eball',position=pos,scale=.8,collider='box',color=color.rgb32(0,60,255),unlit=False,alpha=.75)
		self.spawn_y=self.y
	def update(self):
		if not st.gproc():
			s=self
			s.rotation_z+=time.dt*500
			s.y-=time.dt*2
			if s.intersects(LC.ACTOR):
				cc.get_damage(LC.ACTOR,rsn=6)
			if s.y <= s.spawn_y-LC.ltth:
				destroy(s)