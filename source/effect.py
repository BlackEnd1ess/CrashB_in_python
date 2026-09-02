from animation import set_glb_value,set_glb_frame,set_glb_color,set_memory_glb_value,set_switch_glb_value
from ursina import Entity,Text,Vec3,color,load_texture,scene,invoke,camera
import status,_loc,time,random,_core,math
from ursina.ursinastuff import destroy
from sound import pc_audio,obj_audio
from math import sin,radians,cos

trpv='res/objects/ev/teleport/warp_effect'
ef='res/effects/'
q='quad'

st=status
cc=_core
LC=_loc

def spawn_glitter(pos,cnt):
	for ggt in range(cnt):
		invoke(lambda:GlitterStar(pos=(pos[0]+random.uniform(-.32,.32),pos[1]+random.uniform(-.08,.32),pos[2]+random.uniform(-.32,.32))),delay=ggt/15)
	del ggt

class WarpVortex(Entity):
	def __init__(self,pos,sca,drc,col):
		s=self
		super().__init__(model=f'{trpv}.ply',texture=f'{trpv}.png',name='wvpx',position=pos,color=col,scale=sca,rotation_x=90,alpha=.5,unlit=False)
		s.spd=600
		s.drc=drc
		del pos,sca,drc,col,s
	def update(self):
		if st.gproc():
			return
		if LC.ACTOR.indoor > 0:
			s=self
			if s.drc == 1:
				s.rotation_y+=time.dt*s.spd
				return
			s.rotation_y-=time.dt*s.spd

class WaterDrips(Entity):
	def __init__(self,pos,sca,rot):
		s=self
		if len(LC.drp_texture) <= 0:
			LC.drp_texture=[load_texture(f'res/effects/drips/{cbx}.png') for cbx in range(7+1)]
		super().__init__(model='quad',texture=LC.drp_texture[0],position=pos,scale=sca,rotation=rot)
		s.max_frm=len(LC.drp_texture)-1
		s.spd=10
		s.frm=0
		del pos,sca,rot,s
	def update(self):
		if st.gproc():
			return
		s=self
		cc.set_instance_texture(s,LC.drp_texture[int(s.frm)])
		cc.incr_frm(s,s.spd)

class ExclamationMark(Entity):
	def __init__(self,pos,ID):
		super().__init__(model=q,texture=ef+'trigger.png',position=pos,scale=(.15,.2),unlit=False)
		self.vnum=ID
		self.lft=1
		del pos,ID
	def update(self):
		if st.gproc():
			return
		s=self
		s.lft=max(s.lft-time.dt,0)
		if s.lft <= 0:
			destroy(s)
			return
		tv=time.dt*4
		{0:lambda:setattr(s,'x',s.x+tv),
		1:lambda:setattr(s,'x',s.x-tv),
		2:lambda:setattr(s,'z',s.z+tv),
		3:lambda:setattr(s,'z',s.z-tv),
		4:lambda:setattr(s,'y',s.y+tv/4)}[s.vnum]()

##aku typ 2 floating effect
class Sparkle(Entity):
	def __init__(self,pos):
		super().__init__(model=q,texture=f'{ef}sparkle.png',position=pos,scale=.04,color=color.gold,unlit=False)
		self.mode=0
		del pos
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

##aku box break effect
class GlitterStar(Entity):
	def __init__(self,pos):
		super().__init__(model=q,texture=f'{ef}sparkle.png',position=pos,scale=.01,color=color.yellow,unlit=False)
		del pos
	def update(self):
		if st.gproc():
			return
		s=self
		s.scale+=Vec3(time.dt/3,time.dt/3,0)
		if s.scale_x > .25:
			destroy(s)

class GemFirework(Entity):
	def __init__(self,col,pos):
		self.glb_model=f'{ef}firework/firework.glb'
		super().__init__(scale=.5,rotation_y=60,position=pos,color=col,unlit=False)
		set_glb_value(self,fps=20,sca=.0125)
		set_glb_color(self,col=self.color,UNLIT=True,brightness=2)
	def refr_anim(self):
		s=self
		s.new_index+=time.dt*s.fps
		if s.new_index >= len(s.frames):
			destroy(s)
			return
		set_glb_frame(s)
	def update(self):
		if st.gproc():
			return
		s=self
		s.visible=not st.pause
		s.refr_anim()

class JumpDust(Entity):
	def __init__(self,pos):
		super().__init__(model=q,texture=LC.explode_anim_texture[4],position=pos,scale=.1,color=color.light_gray,unlit=False,alpha=.5)
		del pos
	def update(self):
		if st.gproc():
			return
		self.scale+=(time.dt,time.dt)
		if self.scale_x > .6:
			destroy(self)

class WarpRingEffect(Entity):
	def __init__(self):
		s=self
		s.glb_model=f'{ef}warp_rings/warp_rings.glb'
		super().__init__(position=LC.ACTOR.position,color=color.white,alpha=.9,unlit=False)
		set_glb_value(s,fps=40,sca=.00125)
		set_glb_color(s,col=s.color,UNLIT=False,brightness=2)
		s.activ=False
		s.max_rings=7
		s.rings=0
		s.times=0
		del s
	def cleanup(self):
		s=self
		if s.root:
			s.root.removeNode()
			s.root=None
		destroy(s)
	def refr_anim(self):
		s=self
		s.new_index+=time.dt*s.fps
		if s.new_index >= len(s.frames):
			s.new_index=0
			s.rings+=1
			pc_audio(ID=1,pit=.35)
			if s.rings >= s.max_rings:
				LC.ACTOR.warped=True
				s.cleanup()
				return
		set_glb_frame(s)
	def update(self):
		if st.gproc() or not cc.level_ready:
			return
		s=self
		if not s.activ:
			s.activ=True
			obj_audio(ID=0)
		s.refr_anim()

class TrialTimeStopInfo(Entity):
	def __init__(self,pos,n):
		s=self
		super().__init__()
		s.text_info=Text(str(n),font='res/ui/font.ttf',color=color.gold,position=(pos[0]+random.uniform(-.2,.2),pos[1]+random.uniform(-.2,.2),pos[2]+random.uniform(-.2,.2)),parent=scene,unlit=False,scale=6)
		s.is_done=False
		s.lftime=0
	def update(self):
		if st.gproc():
			return
		s=self
		s.text_info.y+=time.dt*.75
		s.lftime+=time.dt
		if s.lftime > 2:
			if not s.is_done:
				s.is_done=True
				destroy(s.text_info)
				destroy(s)

class PressureWave(Entity):
	def __init__(self,pos,col):
		s=self
		super().__init__(position=pos)
		set_memory_glb_value(s,fps=16,sca=.001,model=LC.explode_wave_anim)
		set_glb_color(s,col=col,UNLIT=False,brightness=1.5)
		s.y+=random.uniform(-.1,.1)
		s.alpha=.75
		del pos,col,s
	def refr_anim(self):
		s=self
		s.new_index+=time.dt*s.fps
		if s.new_index >= len(s.frames):
			destroy(s)
			return
		set_glb_frame(s)
	def update(self):
		if st.gproc():
			return
		self.refr_anim()

class JungleLeaf(Entity):
	def __init__(self,pos,sca,typ,col=color.white):
		if typ > 1:
			typ=random.randint(0,1)
		self.glb_model=f'res/objects/l1/leaf/{typ}.glb'
		super().__init__(position=pos,scale=sca)
		set_glb_value(self,fps=0,sca=.001)
		set_glb_color(self,col=col,UNLIT=True,brightness=2)
		self.fall_speed=.25
		self.wait=random.uniform(.75,2)
		self.ready=False
		del pos,sca,typ,col
	def fall_down(self):
		s=self
		s.y-=time.dt*s.fall_speed
		s.x+=math.sin(time.time()*1.7)*.015
		if s.y < LC.ACTOR.y-5:
			s.wait=random.uniform(.75,2)
			s.rotation_x=random.randint(0,360)
			s.rotation_y=random.randint(0,180)
			s.ready=False
	def check_player_position(self):
		s=self
		if s.wait > 0:
			s.wait-=time.dt
			return
		if not s.ready:
			s.ready=True
			s.position=(LC.ACTOR.x+random.uniform(-1,1),LC.ACTOR.y+3,LC.ACTOR.z+random.uniform(1,2.5))
	def update(self):
		if st.gproc() or st.death_event:
			return
		s=self
		if st.LEVEL_CLEAN:
			destroy(s)
			return
		if not s.ready:
			if LC.ACTOR.indoor > 0:
				return
			s.check_player_position()
			return
		s.fall_down()

class Fireball(Entity):
	def __init__(self,cr):
		s=self
		if cr.name in ('ldmn','wtmn'):
			nC=color.orange
		elif cr.name == 'toxic_barrel':
			nC=color.blue
		elif cc.is_box(cr) and cr.vnum == 12:
			nC=color.green
		else:
			nC=color.red
		super().__init__(model=q,texture=LC.explode_anim_texture[0],position=(cr.x,cr.y+.1,cr.z+random.uniform(-.1,.1)),color=nC,scale=.75,unlit=False)
		PressureWave(pos=s.position,col=nC)
		s.ex_step=0
		del cr,nC,s
	def update(self):
		if st.gproc():
			return
		s=self
		cc.set_instance_texture(s,LC.explode_anim_texture[int(s.ex_step)])
		s.ex_step=min(s.ex_step+time.dt*25,14.999)
		s.visible=bool(s.ex_step < 14.99)
		if s.ex_step > 14.99:
			destroy(s)

class LightFire(Entity):
	def __init__(self,pos,lft=None):
		s=self
		if len(LC.fre_texture) <= 0:
			LC.fre_texture=[load_texture(f'res/effects/fire/fire_{cbx}.png') for cbx in range(31+1)]
		super().__init__(model=q,texture=LC.fre_texture[0],position=pos,scale=.4,unlit=False)
		s.max_frm=len(LC.fre_texture)-1
		s.life_time=lft
		s.spd=12
		s.frm=0
		del pos,lft,s
	def update(self):
		if st.gproc():
			return
		s=self
		if s.life_time:
			s.life_time-=time.dt
			if s.life_time <= 0:
				destroy(s)
				return
		cc.incr_frm(s,s.spd)
		cc.set_instance_texture(s,LC.fre_texture[int(s.frm)])

class FireThrow(Entity):
	def __init__(self,pos,ro_y):
		s=self
		super().__init__(model=q,name='fthr',texture=LC.explode_anim_texture[4],position=(pos[0],pos[1]+.25,pos[2]),scale=.2,collider='box',unlit=False,color=random.choice([color.orange,color.red]))
		s.life_time=.4
		s.mvs=4
		a=radians(ro_y)
		s.direc=Vec3(sin(a),0,cos(a))
	def fly_away(self):
		s=self
		s.position+=s.direc*(time.dt*s.mvs)
	def update(self):
		s=self
		if st.gproc():
			return
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
	def __init__(self,pos,height):##mem
		super().__init__(model=q,texture=f'{ef}sparkle.png',name='eball',position=pos,scale=.9,collider='box',color=color.rgb32(0,60,255),unlit=False,alpha=.75)
		self.spawn_y=self.y
		self.height=height
		del pos,height
	def update(self):
		if st.gproc():
			return
		s=self
		s.rotation_z+=time.dt*500
		s.y-=time.dt*2
		if s.intersects(LC.ACTOR):
			cc.get_damage(LC.ACTOR,rsn=6)
		if s.y <= s.spawn_y-s.height:
			destroy(s)

class WeatherSnow(Entity):
	def __init__(self,p_count,p_speed):
		super().__init__()
		self.particles=[Entity(model=q,texture=LC.snow_particle[0],scale=0,position=(LC.ACTOR.x+random.uniform(-5.5,5.5),camera.y+random.uniform(.7,1.4),LC.ACTOR.z+random.uniform(.5,4))) for _ in range(p_count)]
		self.speed=1.25
		for mpp in self.particles:
			mpp.scale=0
			mpp.lifetime=random.uniform(2,4)
		del mpp,p_count,p_speed
	def update(self):
		if st.gproc():
			return
		s=self
		for pptc in s.particles:
			pptc.lifetime-=time.dt
			pptc.y-=time.dt*s.speed
			pptc.x+=time.dt/2
			pptc.z-=time.dt
			if pptc.lifetime <= 0:
				pptc.lifetime=random.uniform(2,4)
				pptc.scale=random.uniform(.025,.05)
				pptc.position=(LC.ACTOR.x+random.uniform(-5.5,5.5),camera.y+random.uniform(.7,1.4),LC.ACTOR.z+random.uniform(.5,4))