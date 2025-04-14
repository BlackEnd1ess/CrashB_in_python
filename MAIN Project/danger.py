from ursina import Entity,color,time,distance,invoke,BoxCollider,Vec3,scene,Vec3,lerp
import _core,status,item,sound,animation,player,_loc,settings,effect,npc,random
from ursina.ursinastuff import destroy

wfc='wireframe_cube'
omf='res/objects/'
trn='res/terrain/'
b='box'

an=animation
st=status
ef=effect
sn=sound
cc=_core
LC=_loc

## classes for dangerous objects ingame where causes player damage or death event ###
inp=omf+'l2/wood_log/wood_log'
class WoodLog(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=inp+'.ply',texture=inp+'.png',name='wdlg',position=pos,scale=(.001,.001,.0015),rotation=(-90,0,0),collider=b)
		Entity(model='cube',texture=trn+'bricks.png',name=s.name,position=(s.x,s.y+.8,s.z-.075),scale=(.5,2,.5),collider=b)
		Entity(model='cube',texture=trn+'bricks.png',name=s.name,position=(s.x,s.y-.1,s.z+.6),scale=(.5,3,.5),texture_scale=(1,2),collider=b)
		s.danger=True
		s.or_pos=s.y
		s.stat=0
		del pos,s
	def reset_pos(self):
		s=self
		s.y=min(s.y+time.dt,s.or_pos+1.31)
		if s.y > (s.or_pos+1.3):
			s.danger=True
			s.stat=1
	def stomp(self):
		s=self
		s.y=max(s.y-time.dt*4,s.or_pos)
		if s.y <= s.or_pos:
			if distance(s,LC.ACTOR) < 2:
				sn.obj_audio(ID=3)
			s.danger=False
			s.stat=0
	def update(self):
		s=self
		if st.gproc():
			return
		if st.aku_hit > 2:
			s.stat=1
			s.reset_pos()
			return
		if s.intersects(LC.ACTOR) and s.danger:
			cc.get_damage(LC.ACTOR,rsn=2)
		{0:s.reset_pos,1:s.stomp}[s.stat]()

rol=omf+'l2/role/role'
class Role(Entity):
	def __init__(self,pos,di):
		s=self
		super().__init__(model=rol+'.ply',texture=rol+'.png',rotation=(-90,90,90),position=pos,scale=.01,collider=b)
		s.main_pos=s.position
		s.is_rolling=False
		s.danger=False
		s.roll_wait=1
		s.direc=di
		if st.level_index == 8:
			s.color=color.dark_gray
			s.unlit=False
		del pos,di,s
	def roll_right(self):
		s=self
		s.x+=time.dt*2
		s.rotation_x+=time.dt*80
		if s.x >= s.main_pos[0]+1.5:
			s.roll_wait=1
			s.direc=1
			invoke(s.p_snd,delay=.5)
	def roll_left(self):
		s=self
		s.x-=time.dt*2
		s.rotation_x-=time.dt*80
		if s.x <= s.main_pos[0]-1.5:
			s.roll_wait=1
			s.direc=0
			invoke(s.p_snd,delay=.5)
	def p_snd(self):
		if distance(self,LC.ACTOR) < 4:
			sn.obj_audio(ID=4)
	def update(self):
		s=self
		if not st.gproc():
			if (s.intersects(LC.ACTOR) and s.danger):
				cc.get_damage(LC.ACTOR,rsn=2)
			s.roll_wait=max(s.roll_wait-time.dt,0)
			if s.roll_wait <= 0:
				s.is_rolling=True
				s.danger=True
				rdi={0:s.roll_right,1:s.roll_left}
				rdi[s.direc]()
				return
			s.is_rolling=False
			s.danger=False

class SewerGlowIron(Entity):
	def __init__(self,pos,sca):
		super().__init__(model='cube',texture=trn+'swr_iron.png',position=pos,scale=sca,color=color.rgb32(255,50,0),texture_scale=(sca[0],sca[2]),unlit=False,collider=b)
		del pos,sca
	def update(self):
		s=self
		if st.gproc():
			return
		if s.intersects(LC.ACTOR):
			cc.get_damage(LC.ACTOR,rsn=4)

wtt=omf+'l4/wtr/'
class EletricWater(Entity):
	def __init__(self,pos,sca):
		s=self
		super().__init__(model='cube',texture=wtt+'0.png',name='elwt',position=pos,scale=(sca[0],.1,sca[1]),texture_scale=(sca[0],sca[1]),color=color.rgb32(0,180,180),alpha=.9,collider=b)
		s.tx=(sca[0],sca[1])
		s.electric=False
		s.nr=False
		s.splash=0
		s.frm=0
		s.tme=8
		del pos,sca,s
	def wtr_danger(self):
		s=self
		if not s.electric:
			s.electric=True
			s.color=color.yellow
			s.unlit=False
			s.alpha=.9
			if LC.ACTOR.warped and not st.bonus_round:
				if s.nr:
					sn.obj_audio(ID=7)
			invoke(s.wtr_normal,delay=1.5)
	def wtr_normal(self):
		s=self
		if not s:
			del s
			return
		s.electric=False
		s.color=color.rgb32(0,125,125)
		s.unlit=True
		s.alpha=.9
	def check_p(self):
		s=self
		ta=LC.ACTOR
		if ta.inwt <= 0:
			s.splash=max(s.splash-time.dt,0)
		if s.intersects(ta):
			ta.inwt=.3
			if s.electric:
				cc.get_damage(ta,rsn=6)
			if s.splash <= 0:
				s.splash=.3
				sn.pc_audio(ID=10)
	def update(self):
		if st.gproc():
			return
		s=self
		s.nr=st.wtr_dist(w=s,p=LC.ACTOR)
		if s.nr:
			s.check_p()
			cc.incr_frm(s,31,8)
			s.texture=wtt+f'{int(s.frm)}.png'
			s.tme=max(s.tme-time.dt,0)
			if s.tme <= 0:
				s.tme=random.uniform(.1,.2) if s.x > 180 else 8
				s.wtr_danger()

swrp=omf+'l4/heat_pipe/heat_pipe'
class HeatPipe(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=swrp+'.ply',texture=swrp+'.png',name='hotp',position=pos,scale=.75,rotation=(0,90,0),color=color.red,unlit=False)
		s.collider=BoxCollider(s,size=Vec3(.5,.5,5))
		s.danger=True
		del pos
	def update(self):
		if st.gproc():
			return
		if self.intersects(LC.ACTOR):
			cc.get_damage(LC.ACTOR,rsn=4)

rmsc=omf+'l5/m_sculpt/m_sculpt'
class MonkeySculpture(Entity):
	def __init__(self,pos,r,d,ro_y=90):
		s=self
		super().__init__(name='mnks',position=pos,scale=.003,rotation=(-90,ro_y,0))
		s.model=rmsc+'1.ply'
		if r:
			s.model=rmsc+'.ply'
			s.podium=Entity(model='cube',texture=trn+'moss.png',name=s.name,scale=(.5,1,.5),texture_scale=(1,2),position=(s.x,s.y-.5,s.z))
		s.texture=rmsc+'.png'
		s.f_pause=False
		s.s_audio=False
		s.danger=d
		s.f_cnt=0
		s.tme=.08
		s.rot=r
		del ro_y,pos,r,d,s
	def f_reset(self):
		s=self
		s.f_pause=False
		s.f_cnt=0
	def fire_throw(self):
		s=self
		if (distance(s,LC.ACTOR) < 8 and not st.gproc()):
			if s.f_cnt >= 30:
				if not s.f_pause:
					s.f_pause=True
					invoke(s.f_reset,delay=5)
				return
			ef.FireThrow(pos=s.position,ro_y=s.rotation_y)
			s.f_cnt+=1
			if not s.s_audio:
				s.s_audio=True
				sn.obj_audio(ID=10,pit=1)
				invoke(lambda:setattr(s,'s_audio',False),delay=3)
	def rot_to_crash(self):
		s=self
		if distance(s,LC.ACTOR) < 2:
			cc.rotate_to_crash(s)
	def update(self):
		if st.gproc():
			return
		s=self
		if s.danger:
			s.tme=max(s.tme-time.dt,0)
			if s.tme <= 0:
				s.tme=.08
				s.fire_throw()
		if s.rot:
			s.rot_to_crash()

ftf=omf+'l5/fire_trap/fire_trap'
class FireTrap(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=ftf+'.obj',texture=ftf+'.png',position=pos,scale=.2,color=color.yellow,collider=b,double_sided=True)
		ef.LightFire(pos=(s.x,s.y+.2,s.z))
		del pos

ldg=omf+'l5/log_danger/log_danger'
class LogDanger(Entity):
	def __init__(self,pos,ro_y):
		s=self
		super().__init__(model=ldg+'.ply',texture=ldg+'.png',position=pos,scale=.001,rotation=(-90,ro_y,0),collider=b,unlit=False)
		s.spawn_pos=s.position
		s.stop_throw=False
		s.fly_time=0
		s.start_delay=.3
		s.life_time=3
		s.direc_y=0
		del pos,ro_y
	def fly(self):
		s=self
		fsp=3.2
		fdi={0:lambda:setattr(s,'z',s.z-time.dt*fsp),
			90:lambda:setattr(s,'x',s.x-time.dt*fsp),
			180:lambda:setattr(s,'z',s.z+time.dt*fsp),
			-90:lambda:setattr(s,'x',s.x+time.dt*fsp)}
		fdi[s.rotation_y]()
		s.rotation_x-=time.dt*100
		del fsp,fdi
	def fly_away(self,di):
		s=self
		s.position+=di*time.dt*40
		s.fly_time+=time.dt
		if s.fly_time > .5:
			cc.purge_instance(s)
			return
	def hit_ground(self):
		s=self
		if s.direc_y == 0:
			s.y-=time.dt*3
			if s.y <= s.spawn_pos[1]-.4:
				s.direc_y=1
				if distance(s,LC.ACTOR) < 5:
					sn.obj_audio(ID=11)
			return
		s.y+=time.dt*3
		if s.y >= s.spawn_pos[1]+.3:
			s.direc_y=0
	def update(self):
		if not st.gproc():
			ac=LC.ACTOR
			s=self
			s.life_time=max(s.life_time-time.dt,0)
			if s.life_time <= 0:
				cc.purge_instance(s)
				return
			if s.stop_throw:
				s.fly_away(di=Vec3(s.x-ac.x,0,s.z-ac.z))
				return
			s.fly()
			s.start_delay=max(s.start_delay-time.dt,0)
			if s.start_delay <= 0:
				s.hit_ground()
				if s.intersects(ac):
					if LC.ACTOR.is_attack:
						sn.obj_audio(ID=8)
						s.stop_throw=True
						return
					cc.get_damage(LC.ACTOR,rsn=2)

behv=omf+'l6/hive/0'
class Hive(Entity):
	def __init__(self,pos,bID,bMAX):
		s=self
		super().__init__(model=behv+'.ply',texture=behv+'.tga',position=pos,scale=.1/150,rotation_x=-90)
		s.locked=False
		s.bees_out=0
		s.bMAX=bMAX
		s.bID=bID
		s.tme=.3
		s.frm=0
		del pos,bID,bMAX
	def is_own_bee(self):
		s=self
		s.bees_out=0
		for qv in scene.entities[:]:
			if isinstance(qv,npc.Bee) and qv.bID == s.bID:
				s.bees_out+=1
				s.locked=(s.bees_out >= s.bMAX)
	def spawn_bee(self):
		s=self
		npc.Bee(pos=s.position,bID=s.bID)
	def update(self):
		if st.gproc():
			return
		s=self
		s.tme=min(s.tme-time.dt,0)
		if s.tme <= 0:
			s.tme=.3
			s.is_own_bee()
		if (LC.ACTOR.z < s.z+10) and (LC.ACTOR.z > s.z-1.5):
			if not s.locked:
				an.hive_awake(s,sp=12)

tk=omf+'l6/tikki/'
class TikkiSculpture(Entity):
	def __init__(self,pos,spd,rng):
		s=self
		super().__init__(model=tk+'0.ply',texture=tk+'0.tga',position=pos,scale=.0004,rotation_x=-90,name='tksc',collider=b)
		s.is_moving=False
		s.move_speed=spd
		s.move_point=pos
		s.spawn_pos=pos
		s.an_pause=0
		s.an_mode=0
		s.tme=1
		s.frm=0
		s.rng=rng
		del pos,spd,rng
	def move_to_point(self):
		s=self
		if distance(s.position,s.move_point) < .1:
			s.is_moving=False
			return
		s.position=lerp(s.position,s.move_point,time.dt*s.move_speed)
	def update(self):
		if st.gproc():
			return
		s=self
		s.an_pause=max(s.an_pause-time.dt,0)
		if s.intersects(LC.ACTOR):
			cc.get_damage(LC.ACTOR,rsn=2)
		if s.an_pause <= 0:
			an.tikki_rotate(s,sp=14)
		if s.is_moving:
			s.move_to_point()
			return
		s.tme=max(s.tme-time.dt,0)
		if s.tme <= 0:
			s.tme=1/s.move_speed
			ksp=s.spawn_pos
			s.move_point=random.choice([(ksp[0]+s.rng,ksp[1],ksp[2]),(ksp[0]-s.rng,ksp[1],ksp[2]),(ksp[0],ksp[1],ksp[2]+s.rng),(ksp[0],ksp[1],ksp[2]-s.rng)])
			s.is_moving=True
			del ksp

lm=omf+'l6/lmine/'
class LandMine(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=lm+'0.ply',name='ldmn',texture=lm+'0.tga',position=pos,rotation_x=-90,scale=.00065)
		s.explode=False
		s.p_snd=False
		s.frm=0
		s.tme=1
		del pos
	def purge(self):
		s=self
		LC.LDM_POS.append(s.position)
		destroy(s)
	def m_audio(self):
		s=self
		s.tme=max(s.tme-time.dt,0)
		if s.tme <= 0:
			s.tme=random.randint(1,2)
			sn.obj_audio(ID=12,pit=random.uniform(.8,1))
	def explosion(self):
		s=self
		s.frm=0
		LC.ACTOR.stun,s.explode=True,True
		if not s.p_snd:
			s.p_snd=True
			ef.Fireball(s)
			sn.crate_audio(ID=10)
	def update(self):
		if not st.gproc():
			s=self
			if s.explode:
				LC.ACTOR.y=lerp(LC.ACTOR.y,s.y+1,time.dt*12)
				an.mine_destroy(s,sp=12)
				return
			lmd=distance(s,LC.ACTOR)
			an.land_mine(s,sp=12)
			if lmd < .3:
				s.explosion()
				return
			if lmd < 2:
				s.m_audio()

def multi_heat_tile(p,typ,ro_y,sca,CNT):
	for mhx in range(CNT[0]):
		for mhz in range(CNT[1]):
			HeatTile(pos=(p[0]+mhx,p[1],p[2]+mhz),typ=typ,ro_y=ro_y,sca=sca)
	del mhx,mhz,p,typ,ro_y,sca,CNT

lbcb=omf+'l7/lab_ptf/lab_ptf'
class HeatTile(Entity):
	def __init__(self,pos,ro_y=0,typ=0,sca=(.5,.8,.5)):
		s=self
		super().__init__(model=lbcb+'.obj',texture=lbcb+'.png',name='labt',position=pos,scale=sca,collider=b,rotation_y=ro_y,color=color.red,unlit=False)
		s.matr='metal'
		s.danger=True
		if typ == 1:
			s.is_heat=True
			s.heat_color=0
			s.refr=0
		s.typ=typ
		del pos,typ,ro_y,sca
	def update(self):
		s=self
		if st.gproc():
			return
		if s.typ == 1:
			s.danger=(s.heat_color <= 0)
			s.color=color.rgb32(255,int(s.heat_color),int(s.heat_color))
			s.refr=max(s.refr-time.dt,0)
			rtu=time.dt*80
			if s.refr <= 0:
				if s.is_heat:
					s.heat_color=min(s.heat_color+rtu,255)
					if s.heat_color >= 255:
						s.refr=1
						s.is_heat=False
					return
				s.heat_color=max(s.heat_color-rtu,0)
				if s.heat_color <= 0:
					s.refr=1
					s.is_heat=True

lbpi=omf+'l7/piston/piston'
class Piston(Entity):
	def __init__(self,pos,typ,spd):
		s=self
		super().__init__(model=lbpi+'.ply',texture=lbpi+'.png',position=(pos[0],pos[1],pos[2]),scale=(.1/110,.1/110,.1/100),rotation=(-90,0,0),collider=b)
		s.collider=BoxCollider(s,center=Vec3(0,0,-1100),size=Vec3(900,900,1800))
		s.danger=True
		s.spawn_y=s.y
		s.mvspd=spd
		s.tme=spd
		s.typ=typ
		s.mode=0
		del pos,typ,spd
	def stomp(self):
		s=self
		s.y=max(s.y-time.dt*s.mvspd,s.spawn_y-2.051)
		if s.y <= s.spawn_y-2.05:
			jg=s.intersects(LC.ACTOR)
			if jg and s.danger:
				if jg.normal == Vec3(0,-1,0):
					cc.get_damage(LC.ACTOR,rsn=2)
			s.danger=False
			if distance(s,LC.ACTOR) < 8:
				sn.obj_audio(ID=13,pit=.8)
			s.mode=1
			s.tme=.5
	def reset(self):
		s=self
		s.y=min(s.y+time.dt*s.mvspd,s.spawn_y+.1)
		if s.y >= s.spawn_y:
			s.danger=True
			if distance(s,LC.ACTOR) < 8 and st.aku_hit < 3:
				sn.obj_audio(ID=13,pit=.5)
			s.mode=0
			s.tme=1-(1/s.mvspd)
	def update(self):
		if st.gproc():
			return
		s=self
		if st.aku_hit > 2:
			s.mode=1
			s.reset()
			return
		s.tme=max(s.tme-time.dt,0)
		if s.tme <= 0:
			pva={0:lambda:s.stomp(),1:lambda:s.reset()}
			pva[s.mode]()
			del pva

lpad=omf+'l7/e_pad/'
class LabPad(Entity):
	def __init__(self,pos,ID):
		s=self
		super().__init__(model=lpad+'0/0.ply',texture=lpad+'0/0.tga',name='epad',position=pos,scale=.1/85,rotation_x=-90,collider=b)
		s.active=False
		s.locked=False
		s.matr='metal'
		s.mode=0
		s.frm=0
		s.tme=1
		s.ID=ID
		LabTaser(pos=(s.x,s.y+LC.ltth,s.z),ID=s.ID)
		del pos,ID
	def trigger_taser(self):
		for lpo in scene.entities[:]:
			if isinstance(lpo,LabTaser) and lpo.ID == self.ID:
				lpo.shoot_laser()
	def disable_pad(self):
		s=self
		s.mode=0
		s.unlit,s.locked=True,False
		s.texture=lpad+'0/0.tga'
	def enable_pad(self):
		s=self
		s.tme=.5
		if not s.locked:
			sn.obj_audio(ID=15,pit=.5)
			s.locked=True
			s.trigger_taser()
		s.mode=1
		s.texture=lpad+'1/0.tga'
		s.unlit=False
	def update(self):
		if st.gproc():
			return
		s=self
		an.pad_refr(s)
		s.tme=max(s.tme-time.dt,0)
		if s.active:
			s.active=False
			s.enable_pad()
			return
		if s.tme <= 0:
			s.disable_pad()

lbts=omf+'l7/lab_taser/'
class LabTaser(Entity):
	def __init__(self,pos,ID):
		s=self
		super().__init__(model=lbts+'0.ply',texture=lbts+'0.tga',name='ltts',position=pos,scale=.1/150,rotation_x=-90)
		s.frm=0
		s.ID=ID
		del pos,ID
	def shoot_laser(self):
		sn.obj_audio(ID=14)
		ef.ElectroBall(pos=self.position)
	def update(self):
		if not st.gproc():
			an.taser_rotation(self)

class WaterHit(Entity):## collider for water
	def __init__(self,p,sc):
		super().__init__(model=wfc,name='wtrh',collider=b,position=p,scale=(sc[0],.2,sc[1]),visible=False)
		del p,sc

class FallingZone(Entity):## falling
	def __init__(self,pos,s,v=False):
		super().__init__(model='cube',name='fllz',collider=b,scale=s,position=pos,color=color.black,visible=v)
		del pos,s,v
	def update(self):
		if self.intersects(LC.ACTOR):
			cc.dth_event(LC.ACTOR,rsn=1)

bldr=omf+'l8/boulder/boulder'
class Boulder(Entity):
	def __init__(self,pos,fldd):
		s=self
		super().__init__(model=bldr+'.ply',texture=bldr+'.png',position=pos,scale=.002,rotation_x=-90,unlit=False)
		s.follow_speed=4
		s.ffly_drc=fldd
		s.spawn_pos=pos
		s.active=True
		s.way_index=0
		del s,pos,fldd
	def update(self):
		if st.gproc():
			return
		s=self
		if s.active:
			s.rotation_x+=time.dt*60
			cc.npc_pathfinding(s)