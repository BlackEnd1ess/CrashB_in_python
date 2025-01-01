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
		super().__init__(model=trpv+'.ply',texture=trpv+'.png',name='wpvx',position=pos,color=col,scale=sca,rotation_x=90,alpha=.5,unlit=False)
		self.spd=600
		self.drc=drc
		del pos,sca,drc,col
	def update(self):
		if st.gproc():
			return
		s=self
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