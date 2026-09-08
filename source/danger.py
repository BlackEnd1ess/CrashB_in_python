from ursina import Audio,Entity,color,time,distance,distance_xz,invoke,BoxCollider,Vec3,scene,Vec3,lerp,load_texture
import _core,status,item,sound,animation,player,_loc,settings,effect,npc,random,math,objects
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
dtsm={0:f'{omf}l2/wood_log/wood_log.glb',
	1:f'{omf}l2/stone_log/stone_log.glb',
	2:f'{omf}l7/piston/piston.glb'}
class DeathSmasher(Entity):#level 2
	def __init__(self,pos,typ,speed=1,wait=1,turn=0):
		if typ > 2:
			typ=2
		s=self
		s.glb_model=dtsm[typ]
		super().__init__(name='wdlg',position=pos,scale=(.3,.4,.3),rotation=(0 if typ != 2 else 180,180 if typ != 2 else 0,0))
		s.collider=BoxCollider(s,center=Vec3(0,-2.4,0) if typ != 2 else Vec3(0,2.4,0),size=Vec3(1,3,1))
		an.set_glb_value(s,fps=0,sca=.002)
		an.set_glb_color(s,col=color.white,UNLIT=True,brightness=1.5)
		if typ != 2:
			sbcx=.5 if typ == 0 else .7
			sctt=f'{trn}bricks.png'
			Entity(model='cube',texture=sctt,name=s.name,position=(s.x,s.y+.8,s.z-.075),scale=(sbcx,2,.5),texture_scale=(1,1))
			Entity(model='cube',texture=sctt,name=s.name,position=(s.x,s.y-.1,s.z+.6),scale=(sbcx,3,.5),texture_scale=(1,2))
			del sbcx,sctt
		s.limit_y=s.y+1.5
		s.spawn_y=s.y
		s.speed=speed
		s.reset_wait=wait
		s.wait=wait
		s.stat=turn
		s.typ=typ
		del pos,s,typ,speed,turn,wait
	def refr_function(self):
		s=self
		if s.stat == 0:
			if s.y > s.spawn_y:
				if s.intersects(LC.ACTOR):
					cc.get_damage(LC.ACTOR,rsn=2)
				s.y-=time.dt*s.speed
				return
			if s.stat != 1:
				s.stat=1
				s.wait=s.reset_wait
				if distance(s,LC.ACTOR) < 3:
					if s.typ != 2:
						sn.obj_audio(ID=3)
					else:
						sn.obj_audio(ID=11,pit=.85)
			return
		if s.y < s.limit_y:
			s.y+=time.dt*s.speed
			return
		if s.stat != 0:
			s.stat=0
			s.wait=s.reset_wait
			if s.typ == 2:
				if distance(s,LC.ACTOR) < 5:
					sn.obj_audio(ID=11,pit=.6)
	def update(self):
		s=self
		if st.gproc():
			return
		if st.aku_hit > 2:
			s.stat=1
			s.reset_pos()
			return
		if s.wait > 0:
			s.wait-=time.dt
			return
		s.refr_function()

rol=f'{omf}l2/role/role'
class Role(Entity):
	def __init__(self,pos,di):
		s=self
		super().__init__(model=f'{rol}.ply',texture=f'{rol}.png',rotation=(-90,90,90),position=pos,scale=.01,collider=b)
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

class IceIcle(Entity):
	def __init__(self,pos,fall_speed):
		s=self
		s.glb_model='res/objects/l2/iceicle/iceicle.glb'
		super().__init__(position=pos,scale=.4,collider=b)
		an.set_glb_value(s,fps=30,sca=.0018)
		an.set_glb_color(s,col=color.white,UNLIT=True,brightness=1.5)
		s.fall_speed=fall_speed
		s.on_ground=False
		s.falling=False
		s.target_y=None
		s.danger=True
		s.spawn_pos=pos
		del pos,fall_speed
	def refr_animation(self):
		s=self
		s.new_index+=time.dt*s.fps
		if s.new_index >= len(s.frames):
			if s.on_ground:
				destroy(s)
				return
			return
		an.set_glb_frame(s)
	def refr_function(self):
		s=self
		s.refr_animation()
		if s.on_ground:
			return
		if s.y > s.target_y:
			s.y-=time.dt*s.fall_speed
			lps=s.intersects()
			if lps.entity == LC.ACTOR:
				cc.get_damage(LC.ACTOR,rsn=4)
			return
		if not s.on_ground:
			s.on_ground=True
			sn.crate_audio(ID=10,pit=1.1)
	def update(self):
		if st.gproc():
			return
		s=self
		if s.falling:
			s.refr_function()
			return
		if distance_xz(s,LC.ACTOR) < 1:
			s.falling=True
			s.target_y=LC.ACTOR.y+.1
			sn.pc_audio(ID=1,pit=2)

class SewerGlowIron(Entity):
	def __init__(self,pos,sca):
		super().__init__(model='cube',texture=f'{trn}swr_iron.png',position=pos,scale=sca,color=color.rgb32(255,50,0),texture_scale=(sca[0],sca[2]),unlit=False,collider=b)
		del pos,sca
	def update(self):
		s=self
		if st.gproc():
			return
		if s.intersects(LC.ACTOR):
			cc.get_damage(LC.ACTOR,rsn=4)

class EletricWater(Entity):
	def __init__(self,pos,sca,sw_delay=8):
		s=self
		super().__init__(model='cube',texture=LC.wtr_texture[0],name='elwt',position=pos,scale=(sca[0],.1,sca[1]),texture_scale=(sca[0],sca[1]),color=color.rgb32(0,180,180),alpha=.9,collider=b)
		s.max_frm=len(LC.wtr_texture)-1+.99
		s.tx=(sca[0],sca[1])
		s.electric=False
		s.sw_delay=sw_delay
		s.elc_time=0
		s.matr='wtr'
		s.nr=False
		s.frm=0
		s.tme=.1 if s.x > 180 else 8
		s.spd=8
		del pos,sca,s,sw_delay
	def switch_state(self,state):
		s=self
		if state == 0:
			s.electric=False
			s.color=color.rgb32(0,125,125)
			s.unlit=True
			s.alpha=.9
			return
		s.electric=True
		s.elc_time=1.5
		s.color=color.yellow
		s.unlit=False
		s.alpha=.8
		if LC.ACTOR.warped and not st.bonus_round:
			if s.nr:
				sn.obj_audio(ID=7)
	def refr_texture(self):
		s=self
		cc.incr_frm(s,s.spd)
		if s.texture != LC.wtr_texture[int(s.frm)]:
			s.texture=LC.wtr_texture[int(s.frm)]
	def check_p(self):
		s=self
		fq=s.intersects(LC.ACTOR)
		LC.ACTOR.in_water=fq
		if fq and s.electric:
			cc.get_damage(LC.ACTOR,rsn=6)
	def update(self):
		if st.gproc():
			return
		s=self
		s.nr=st.wtr_dist(w=s,p=LC.ACTOR)
		if s.nr:
			s.check_p()
			s.refr_texture()
			if s.electric and s.elc_time > 0:
				s.elc_time-=time.dt
				if s.elc_time <= 0:
					s.switch_state(0)
				return
			s.tme=max(s.tme-time.dt,0)
			if s.tme <= 0:
				s.tme=random.uniform(.1,.2) if s.x > 180 else s.sw_delay
				s.switch_state(1)

class ToxicBarrel(Entity):
	def __init__(self,pos):
		s=self
		s.glb_model=f'{omf}l4/barrel/barrel.glb'
		super().__init__(position=(pos[0],pos[1]+.275,pos[2]),scale=.4,rotation=(0,90,90),collider=b)
		an.set_glb_value(s,fps=0,sca=.0015)
		an.set_glb_color(s,col=color.white,UNLIT=True,brightness=1.5)
		s.active=False
		s.danger=True
		del pos,s
	def purge(self):
		if not self.active:
			self.active=True
			sn.crate_audio(ID=9,pit=1.25)
			sn.crate_audio(ID=10,pit=2.25)
			ef.Fireball(self)
			cc.get_damage(LC.ACTOR,rsn=4)
			destroy(self)

swrp=f'{omf}l4/heat_pipe/heat_pipe'
class HeatPipe(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=f'{swrp}.ply',texture=f'{swrp}.png',name='hotp',position=pos,scale=.75,rotation=(0,90,0),color=color.red,unlit=False)
		s.collider=BoxCollider(s,size=Vec3(.5,.5,5))
		s.danger=True
		del pos
	def update(self):
		if st.gproc():
			return
		if self.intersects(LC.ACTOR):
			cc.get_damage(LC.ACTOR,rsn=4)

class MonkeySculpture(Entity):
	def __init__(self,pos,ro_y,p_count=25,p_wait=1,typ=0,rotation_speed=1):
		s=self
		s.glb_model=f'res/objects/l5/m_sculpt/monkey_sculpture.glb'
		super().__init__(name='mnks',position=pos,rotation_y=ro_y,scale=.4)
		an.set_glb_value(s,fps=0,sca=.0018)
		an.set_glb_color(s,col=color.white,UNLIT=True,brightness=2.25)
		s.rotation_speed=rotation_speed
		s.p_count_reset=p_count
		s.p_count=p_count
		s.p_snd=False
		s.wait=p_wait
		s.tme=p_wait
		s.typ=typ
		objects.spw_block(ID=4,ro_y=-90,p=s.position,vx=[1,1])
		del pos,ro_y,p_count,p_wait,typ,rotation_speed
	def refr_function(self):
		s=self
		if s.tme > 0:
			s.tme-=time.dt
			return
		if not s.p_snd:
			s.p_snd=True
			if distance(s,LC.ACTOR) < 3:
				sn.obj_audio(ID=8,pit=1)
		ef.FireThrow(pos=s.position,ro_y=s.rotation_y)
		if s.p_count > 0:
			s.p_count-=1
			s.tme=.075
			return
		s.tme=s.wait
		s.p_count=s.p_count_reset
		s.p_snd=False
	def update(self):
		if st.gproc() or self.typ == 0:
			return
		s=self
		if s.typ == 1:
			cc.rotate_to_target(s,LC.ACTOR.position)
			return
		if s.typ == 2:
			if s.p_count_reset > 0:
				s.refr_function()
			return
		s.rotation_y+=time.dt*s.rotation_speed
		if s.p_count_reset > 0:
			s.refr_function()

ftf=f'{omf}l5/fire_trap/fire_trap'
class FireTrap(Entity):
	def __init__(self,pos):
		s=self
		super().__init__(model=f'{ftf}.obj',texture=f'{ftf}.png',position=pos,scale=.2,color=color.yellow,collider=b,double_sided=True)
		ef.LightFire(pos=(s.x,s.y+.2,s.z))
		del pos

ldg=f'{omf}l5/log_danger/log_danger'
class LogDanger(Entity):
	def __init__(self,pos,ro_y):
		s=self
		super().__init__(model=f'{ldg}.ply',texture=f'{ldg}.png',position=pos,scale=.001,rotation=(-90,ro_y,0),collider=b,unlit=False)
		s.spawn_pos=s.position
		s.stop_throw=False
		s.is_purge=False
		s.start_delay=0
		s.life_time=3
		s.fly_time=0
		s.direc_y=0
		s.fsp=2.75
		s.rtf=175
		del pos,ro_y
	def fly(self):
		s=self
		{180:lambda:setattr(s,'z',s.z-time.dt*s.fsp),
		-90:lambda:setattr(s,'x',s.x-time.dt*s.fsp),
		0:lambda:setattr(s,'z',s.z+time.dt*s.fsp),
		90:lambda:setattr(s,'x',s.x+time.dt*s.fsp)}[s.rotation_y]()
		s.rotation_x-=time.dt*s.rtf
	def fly_away(self,di):
		s=self
		s.position+=di*time.dt*40
		s.fly_time+=time.dt
		if s.fly_time > .5:
			cc.destroy_entity(s)
	def hit_ground(self):
		s=self
		if s.direc_y == 0:
			s.y-=time.dt*3
			if s.y <= s.spawn_pos[1]-.4:
				s.direc_y=1
				if distance(s,LC.ACTOR) < 5:
					sn.obj_audio(ID=9)
			return
		s.y+=time.dt*3
		if s.y >= s.spawn_pos[1]+.3:
			s.direc_y=0
	def update(self):
		if not st.gproc():
			ac=LC.ACTOR
			s=self
			s.life_time=max(s.life_time-time.dt,0)
			if s.life_time <= 0 or s.is_purge:
				cc.destroy_entity(s)
				return
			if s.stop_throw:
				s.fly_away(di=Vec3(s.x-ac.x,0,s.z-ac.z))
				return
			s.fly()
			s.start_delay+=time.dt
			if s.start_delay > .4:
				s.hit_ground()
				if s.intersects(ac):
					s.collider=None
					if LC.ACTOR.is_attack:
						sn.pc_audio(ID=17)
						s.stop_throw=True
						return
					cc.get_damage(LC.ACTOR,rsn=2)
					s.is_purge=True

class Hive(Entity):
	def __init__(self,pos,bID,bMAX,typ):
		s=self
		s.glb_model=f'{omf}l6/hive/{typ}/hive.glb'
		super().__init__(position=pos,scale=.3)
		an.set_glb_value(s,fps=16,sca=.0024)
		an.set_glb_color(s,col=color.white,UNLIT=False,brightness=3)
		s.bMAX=bMAX if (typ == 1) else 1
		s.locked=False
		s.bees_out=0
		s.bID=bID
		s.typ=typ
		s.tme=0
		del pos,bID,bMAX
	def is_own_bee(self):
		cnt_bee=[b for b in scene.entities if (isinstance(b,npc.Bee) and b.bID == self.bID)]
		self.bees_out=len(cnt_bee)
		self.locked=self.bees_out >= self.bMAX
	def spawn_bee(self):
		npc.Bee(pos=self.position,bID=self.bID,typ=0)
	def refr_anim(self):
		s=self
		s.new_index+=time.dt*s.fps
		if s.new_index >= len(s.frames):
			s.new_index=0
			s.spawn_bee()
		an.set_glb_frame(s)
	def update(self):
		if st.gproc() or st.death_event:
			return
		s=self
		s.tme+=time.dt
		if s.tme > .3:
			s.tme=0
			s.is_own_bee()
		if (LC.ACTOR.z < s.z+10) and (LC.ACTOR.z > s.z-1.5):
			if not s.locked:
				s.refr_anim()

class TikkiSculpture(Entity):
	def __init__(self,pos,spd,rng):
		s=self
		s.glb_model=f'{omf}l6/tikki/tikki.glb'
		super().__init__(position=pos,scale=.5,name='tksc',collider=b)
		an.set_glb_value(s,fps=20,sca=.001)
		an.set_glb_color(s,col=color.white,UNLIT=True,brightness=2)
		s.is_moving=False
		s.move_speed=spd
		s.move_point=pos
		s.spawn_pos=pos
		s.an_pause=0
		s.an_mode=0
		s.danger=True
		s.tme=1
		s.rng=rng
		del pos,spd,rng
	def move_to_point(self):
		s=self
		if distance(s.position,s.move_point) < .1:
			s.is_moving=False
			return
		s.position=lerp(s.position,s.move_point,time.dt*s.move_speed)
	def refr_anim(self):
		s=self
		if s.an_mode == 0:
			s.new_index+=time.dt*s.fps
			if s.new_index >= len(s.frames):
				s.new_index=len(s.frames)-1
				s.an_pause=0
				s.an_mode=1
			return
		s.new_index-=time.dt*s.fps
		if s.new_index <= 0:
			s.new_index=0
			s.an_pause=0
			s.an_mode=0
	def update(self):
		if st.gproc():
			return
		s=self
		if s.intersects(LC.ACTOR):
			cc.get_damage(LC.ACTOR,rsn=2)
		s.an_pause+=time.dt
		if s.an_pause > 1:
			s.refr_anim()
			an.set_glb_frame(s)
		if s.is_moving:
			s.move_to_point()
			return
		s.tme=max(s.tme-time.dt,0)
		if s.tme <= 0:
			s.tme=1/s.move_speed
			ksp=s.spawn_pos
			s.move_point=random.choice([(ksp[0]+s.rng,ksp[1],ksp[2]),(ksp[0]-s.rng,ksp[1],ksp[2]),(ksp[0],ksp[1],ksp[2]+s.rng),(ksp[0],ksp[1],ksp[2]-s.rng)])
			s.is_moving=True

class WaterMine(Entity):
	def __init__(self,pos,spd,drc=0):
		s=self
		self.lst={0:f'{omf}l3/water_mine/idle.glb',1:f'{omf}l3/water_mine/explode.glb'}
		super().__init__(name='wtmn',position=pos,scale=.4,collider=b)
		an.set_switch_glb_value(s,fps=22,sca=.002,lst=s.lst)
		an.set_glb_color(s,col=color.white,UNLIT=True,brightness=1.5)
		s.danger=True
		s.speed=spd
		s.direc=drc
		s.minetyp=1
		s.status=0
		del pos,spd,drc
	def switch_model(self,n):
		s=self
		s.root.hide()
		s.root=s.models[n]
		s.frames=s.frames_all[n]
		s.new_index=0
		s.frame_index=0
		for frame in s.frames:
			frame.hide()
		an.set_glb_color(s,col=color.white,UNLIT=True,brightness=1.5)
		s.frames[0].show()
		s.root.show()
	def refr_function(self):
		s=self
		if distance(s,LC.ACTOR) < .4:
			if s.status != 1:
				s.status=1
				s.switch_model(s.status)
				sn.crate_audio(ID=9)
				cc.get_damage(LC.ACTOR,rsn=4)
				ef.Fireball(s)
		if s.direc == 0:
			s.x+=math.sin(time.time()*s.speed)*.015
			return
		s.z+=math.sin(time.time()*s.speed)*.015
	def refr_anim(self):
		s=self
		s.new_index+=time.dt*s.fps
		if s.new_index >= len(s.frames):
			LC.LDM_POS.append((s.minetyp,s.position,s.speed,s.direc))
			destroy(s)
			return
		an.set_glb_frame(s)
	def update(self):
		if st.gproc():
			return
		if self.status == 0:
			self.refr_function()
			return
		self.refr_anim()

class LandMine(Entity):
	def __init__(self,pos):##mem
		s=self
		s.glb_model=f'{omf}l6/lmine/landmine_normal.glb'
		s.second_glb_model=f'{omf}l6/lmine/landmine_explode.glb'
		super().__init__(name='ldmn',position=pos,scale=.2)
		an.set_glb_value(s,fps=20,sca=.003)
		an.set_glb_color(s,col=color.white,UNLIT=True,brightness=1.5)
		s.explode=False
		s.danger=True
		s.p_snd=False
		s.minetyp=0
		del pos
	def purge(self):
		LC.LDM_POS.append((self.minetyp,self.position))
		destroy(self)
	def refr_anim(self):
		s=self
		s.new_index+=time.dt*s.fps
		if s.new_index >= len(s.frames):
			if s.explode:
				s.purge()
				return
			s.new_index=0
			sn.obj_audio(ID=10,pit=random.uniform(.8,1))
		an.set_glb_frame(s)
	def switch_status(self):
		self.glb_model=self.second_glb_model
		an.set_glb_value(self,fps=20,sca=.004)
		sn.crate_audio(ID=9)
		ef.Fireball(self)
		if st.aku_hit < 3:
			LC.ACTOR.stun_time=2
	def update(self):
		if st.gproc():
			return
		s=self
		dta=distance(s,LC.ACTOR)
		if dta < 2:
			s.refr_anim()
			if dta < .3:
				if not s.explode:
					s.explode=True
					s.switch_status()

def multi_heat_tile(p,typ,ro_y,sca,CNT):
	for mhx in range(CNT[0]):
		for mhz in range(CNT[1]):
			HeatTile(pos=(p[0]+mhx,p[1],p[2]+mhz),typ=typ,ro_y=ro_y,sca=sca)
	del mhx,mhz,p,typ,ro_y,sca,CNT

lbcb=f'{omf}l7/lab_ptf/lab_ptf'
class HeatTile(Entity):
	def __init__(self,pos,ro_y=0,typ=0,sca=(.5,.8,.5)):
		s=self
		super().__init__(model=f'{lbcb}.obj',texture=f'{lbcb}.png',name='labt',position=pos,scale=sca,collider=b,rotation_y=ro_y,color=color.red,unlit=False)
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

class Piston(Entity):
	def __init__(self,pos,spd,wait=1):##mem
		s=self
		s.glb_model=f'{omf}l7/piston/piston.glb'
		super().__init__(position=pos,scale=.4,rotation=(180,0,0))
		s.collider=BoxCollider(s,size=Vec3(1.8,4,1.8),center=Vec3(0,3.1,0))
		an.set_glb_value(s,fps=0,sca=.0025)
		an.set_glb_color(s,col=color.white,UNLIT=True,brightness=1.25)
		s.spawn_y=s.y
		s.mvspd=spd
		s.wait=wait
		s.tme=wait
		s.mode=0
		del pos,spd,wait
	def switch_mode(self,m):
		s=self
		if s.mode == m:
			return
		s.mode=m
		s.tme=s.wait
		if distance(s,LC.ACTOR) < 8:
			sn.obj_audio(ID=11,pit=.85 if m == 1 else .6)
	def refr_position(self):
		s=self
		if s.y > s.spawn_y-2:
			if st.aku_hit > 2:
				return
			vc=s.intersects()
			if vc and vc.entity == LC.ACTOR:
				if vc.normal == Vec3(0,1,0):
					cc.get_damage(LC.ACTOR,rsn=2)
			s.y-=time.dt*s.mvspd
			return
		s.switch_mode(1)
	def reset_position(self):
		s=self
		if s.y < s.spawn_y:
			s.y+=time.dt*s.mvspd
			return
		s.switch_mode(0)
	def update(self):
		if st.gproc():
			return
		s=self
		if s.tme > 0:
			s.tme-=time.dt
			return
		if s.mode == 0:
			s.refr_position()
			return
		s.reset_position()

class LabPad(Entity):
	def __init__(self,pos,ID,ltth=1.75):
		s=self
		s.lst={0:f'{omf}l7/e_pad/0.glb',1:f'{omf}l7/e_pad/1.glb'}
		super().__init__(name='epad',position=pos,rotation_y=90,scale=.5,collider=b)
		s.collider=BoxCollider(s,center=Vec3(0,-.1,0),size=Vec3(1.6,.2,1.6))
		an.set_switch_glb_value(s,fps=20,sca=.002,lst=s.lst)
		an.set_glb_color(s,col=color.white,UNLIT=False,brightness=1.5)
		s.active=False
		s.locked=False
		s.matr='metal'
		s.tme=0
		s.ID=ID
		LabTaser(pos=(s.x,s.y,s.z),ID=s.ID,height=ltth)
		del pos,ID,ltth
	def switch_model(self,n):
		s=self
		s.root.hide()
		s.root=s.models[n]
		s.frames=s.frames_all[n]
		s.new_index=0
		s.frame_index=0
		for frame in s.frames:
			frame.hide()
		s.frames[0].show()
		s.root.show()
	def refr_pad(self,mode):
		s=self
		if mode == 0:
			s.new_index+=time.dt*s.fps
			if s.new_index >= len(s.frames):
				if not s.locked:
					s.locked=True
					sn.obj_audio(ID=12)
					s.trigger_taser()
					s.switch_model(1)
		else:
			s.new_index-=time.dt*s.fps
			if s.new_index <= 0:
				s.new_index=0
				if s.locked:
					s.locked=False
					s.active=False
					s.tme=0
					s.switch_model(0)
				return
		an.set_glb_frame(s)
	def trigger_taser(self):
		for lpo in scene.entities[:]:
			if isinstance(lpo,LabTaser) and lpo.ID == self.ID:
				lpo.shoot_laser()
	def update(self):
		if st.gproc():
			return
		s=self
		if not s.active:
			return
		if not s.locked:
			s.refr_pad(mode=0)
			return
		s.tme+=time.dt
		if s.tme >= 2:
			s.refr_pad(mode=1)

class LabTaser(Entity):
	def __init__(self,pos,ID,height):
		self.glb_model=f'{omf}l7/lab_taser/lab_taser.glb'
		super().__init__(name='ltts',position=(pos[0],pos[1]+height,pos[2]),scale=.1)
		an.set_glb_value(self,fps=20,sca=.0075)
		an.set_glb_color(self,col=color.white,UNLIT=True,brightness=1.5)
		self.height=height
		self.ID=ID
		del pos,ID,height
	def shoot_laser(self):
		sn.obj_audio(ID=13,pit=.5)
		ef.ElectroBall(pos=self.position,height=self.height)
	def update(self):
		if st.gproc():
			return
		s=self
		s.new_index+=time.dt*s.fps
		if s.new_index >= len(s.frames):
			s.new_index=0
		an.set_glb_frame(s)

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

bldr=f'{omf}l8/boulder/boulder'
class Boulder(Entity):
	def __init__(self,pos,fldd):
		s=self
		super().__init__(model=f'{bldr}.ply',texture=f'{bldr}.png',position=pos,scale=.0016,rotation_x=-90,unlit=False)
		s.imp_snd=Audio(sn.BLD_ROLL,loop=True,autoplay=False,volume=settings.SFX_VOLUME)
		s.move_speed=1.8
		s.ffly_drc=fldd
		s.rs_delay=3.5
		s.is_reset=False
		s.is_done=False
		s.active=False
		s.p_snd=False
		s.spawn_pos=pos
		s.way_index=0
		s.mode=0
		del s,pos,fldd
	def npc_pathfinding(self):
		s=self
		if s.way_index < len(s.ffly_drc):
			ddrc=(Vec3(s.ffly_drc[s.way_index])-s.position).normalized()
			s.position+=ddrc*(time.dt*s.move_speed)
			if distance(Vec3(s.position),s.ffly_drc[s.way_index]) < .3:
				s.way_index+=1
			return
		if not s.is_done:
			s.is_done=True
			s.path_fin()
	def path_fin(self):
		s=self
		s.active=False
		s.rotation_x=0
		s.collider=b
		sn.obj_audio(ID=18)
		s.imp_snd.stop()
		s.imp_snd.fade_out()
	def reset_state(self):
		s=self
		s.is_reset=False
		s.position=s.spawn_pos
		s.way_index=0
		s.collider=None
		s.p_snd=False
		s.imp_snd.stop()
		s.imp_snd.fade_out()
	def refr(self):
		self.rotation_x-=time.dt*70
		for blh in scene.entities:
			if not blh:
				continue
			if distance(self,blh) < 1.8 and blh.collider:
				if blh == LC.ACTOR and not st.death_event:
					cc.dth_event(LC.ACTOR,rsn=2)
					return
				if cc.is_box(blh):
					if blh.vnum in (3,11):
						blh.empty_destroy()
					else:
						blh.box_destroy()
				if cc.is_enemie(blh):
					if not (blh.is_purge or blh.is_hitten):
						cc.bash_enemie(blh,LC.ACTOR)
	def check_dst(self):
		s=self
		z_dist=s.z-LC.ACTOR.z
		x_dist=abs(s.x-LC.ACTOR.x)
		if z_dist > 5 and z_dist < 12 and x_dist < 4:
			s.active=True
	def update(self):
		if st.gproc():
			return
		s=self
		if s.way_index >= len(s.ffly_drc):
			if not s.is_done:
				s.is_done=True
				s.path_fin()
				return
		if s.is_done:
			if st.death_event and st.checkpoint[2] > s.z:
				s.is_done=False
				if not s.is_reset:
					s.is_reset=True
					invoke(s.reset_state,delay=s.rs_delay)
			return
		if st.death_event:
			s.active=False
			if not s.is_reset:
				s.is_reset=True
				invoke(s.reset_state,delay=s.rs_delay)
			return
		if s.active:
			if not s.p_snd:
				s.p_snd=True
				sn.obj_audio(ID=16)
				s.imp_snd.fade_in()
				s.imp_snd.play()
				return
			s.npc_pathfinding()
			s.refr()
			return
		s.check_dst()