import status,_core,_loc,time,random
from ursina import Entity,Vec3,color

st=status
cc=_core
LC=_loc
ef='res/effects/'

class Sparkle(Entity):
	def __init__(self,pos):
		super().__init__(model='quad',texture=ef+'sparkle.tga',position=pos,scale=.04,color=color.gold,unlit=False)
		self.mode=0
	def update(self):
		if not st.gproc():
			s=self
			if s.mode == 0:
				s.scale+=Vec3(time.dt/2,time.dt/2,0)
				if s.scale_x > .1:
					s.mode=1
				return
			s.scale-=Vec3(time.dt/2,time.dt/2,0)
			if s.scale_x <= 0:
				cc.purge_instance(s)

class JumpDust(Entity):
	def __init__(self,pos):
		super().__init__(model='quad',texture=ef+'fire_ball.png',position=pos,scale=.1,color=color.gray)
	def update(self):
		if st.gproc():
			return
		s=self
		s.scale+=(time.dt,time.dt)
		if s.scale_x > .6:
			cc.purge_instance(s)

class FireThrow(Entity):
	def __init__(self,pos,ro_y):
		s=self
		super().__init__(model='quad',name='fthr',texture=ef+'fire_ball.png',position=(pos[0],pos[1]+.25,pos[2]),scale=.2,collider='box',unlit=False,color=random.choice([color.orange,color.red]))
		s.life_time=.5
		s.direc=ro_y
		s.mvs=4
		if ro_y in [90,-90]:
			s.z=s.z+random.uniform(-.1,.1)
	def fly_away(self):
		s=self
		mt=time.dt*s.mvs
		ddi={90:lambda:setattr(s,'x',s.x-mt),-90:lambda:setattr(s,'x',s.x+mt),
			180:lambda:setattr(s,'z',s.z+mt),0:lambda:setattr(s,'z',s.z-mt)}
		ddi[s.direc]()
	def update(self):
		if not st.gproc():
			s=self
			tdf=time.dt*1.1
			s.life_time=max(s.life_time-time.dt,0)
			if s.intersects(LC.ACTOR):
				cc.get_damage(LC.ACTOR,rsn=3)
			if s.life_time <= 0:
				cc.purge_instance(s)
				return
			s.scale+=(tdf,tdf,tdf)
			s.fly_away()