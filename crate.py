import item,status,_core,animation,player,sound,npc
from ursina.shaders import *
from ursina import *

pp='res/crate/crate_'
b='box'
ic=(.15,.2)
cs=0.16
cc=_core
sn=sound

##spawn/remove event
def place_crate(p,ID,m=None,l=None,pse=None):
	CRATES={0:lambda:Iron(pos=p,pse=pse),
			1:lambda:Normal(pos=p,pse=pse),
			2:lambda:QuestionMark(pos=p,pse=pse),
			3:lambda:Bounce(pos=p,pse=pse),
			4:lambda:ExtraLife(pos=p,pse=pse),
			5:lambda:AkuAku(pos=p,pse=pse),
			6:lambda:Checkpoint(pos=p,pse=pse),
			7:lambda:SpringWood(pos=p,pse=pse),
			8:lambda:SpringIron(pos=p,pse=pse),
			9:lambda:SwitchEmpty(pos=p,m=m,pse=pse),
			10:lambda:SwitchNitro(pos=p,pse=pse),
			11:lambda:TNT(pos=p,pse=pse),
			12:lambda:Nitro(pos=p,pse=pse),
			13:lambda:Air(pos=p,m=m,l=l,pse=pse)}
	CRATES[ID]()
	if not ID in [0,8,9,10] and not pse == 1:
		status.crates_in_level+=1
		if p[1] < -10:
			status.crates_in_bonus+=1
		if ID == 13 and l in [0,8]:
			status.crates_in_level-=1

def destroy_event(c):
	status.d_delay=.1
	c.collider=None
	if not c.poly == 1:
		status.C_RESET.append(c)
	if status.bonus_round:
		status.crate_bonus+=1
	else:
		status.crate_to_sv+=1
		status.crate_count+=1
		status.show_crates=5
	Audio(sn.snd_break)
	animation.crate_break(c)
	cc.check_crates_over(c)

def block_destroy(c):
	if not c.p_snd:
		c.p_snd=True
		Audio(sn.snd_steel)
		invoke(lambda:setattr(c,'p_snd',False),delay=.5)

def spawn_ico(c):
	sound.snd_switch()
	ico=Entity(model='quad',texture='res/ui/icon/trigger.png',position=(c.x,c.y,c.z),scale=ic)
	ico.animate_y(c.y+1,duration=1.2)
	invoke(ico.disable,delay=3)

##Crate Logics
class Iron(Entity):
	def __init__(self,pos,pse):
		_in='iron'
		super().__init__(model=pp+_in+'.obj',texture=pp+_in+'.png',scale=cs,position=pos,collider=b)
		self.spawn_pos=pos
		self.poly=pse
		self.p_snd=False
		self.vnum=0
	def destroy(self):
		block_destroy(self)

class Normal(Entity):
	def __init__(self,pos,pse):
		_in='normal'
		super().__init__(model=pp+_in+'.obj',texture=pp+'wooden.png',scale=cs,collider=b,position=pos,shader=lit_with_shadows_shader)
		self.spawn_pos=pos
		self.poly=pse
		self.vnum=1
	def destroy(self):
		item.WumpaFruit(pos=self.position)
		destroy_event(self)

class QuestionMark(Entity):
	def __init__(self,pos,pse):
		_in='sup'
		super().__init__(model=pp+_in+'.obj',texture=pp+_in+'.png',scale=cs,collider=b,position=pos)
		self.spawn_pos=pos
		self.poly=pse
		self.vnum=2
	def destroy(self):
		for _w in range(random.randint(5,10)):
			item.WumpaFruit(pos=(self.x+random.uniform(-.1,.1),self.y,self.z+random.uniform(-.1,.1)))
		destroy_event(self)

class Bounce(Entity):
	def __init__(self,pos,pse):
		_in='bounce'
		super().__init__(model=pp+_in+'.obj',texture=pp+_in+'.png',scale=cs,collider=b,position=pos)
		self.spawn_pos=pos
		self.poly=pse
		self.vnum=3
		self.ltime=0
		self._empty=5
	def empty_destroy(self):
		destroy_event(self)
	def destroy(self):
		if self._empty <= 0:
			self.empty_destroy()
			return
		self.ltime+=1
		cc.wumpa_count(2)
		animation.crate_bounce(self)
		b_snd=Audio(sn.snd_bounc)
		b_snd.pitch=1+self.ltime/10
		self._empty=5
		if self.ltime > 4:
			self.hide()
			destroy_event(self)
			return
	def update(self):
		if self.ltime > 0 and self._empty > 0:
			self._empty-=time.dt

class ExtraLife(Entity):
	def __init__(self,pos,pse):
		_in='live'
		super().__init__(model=pp+_in+'.obj',texture=pp+_in+'.png',scale=cs,collider=b,position=pos)
		self.spawn_pos=pos
		self.poly=pse
		self.vnum=4
	def destroy(self):
		item.ExtraLive(pos=(self.x,self.y+.25,self.z))
		destroy_event(self)

class AkuAku(Entity):
	def __init__(self,pos,pse):
		_in='aku'
		super().__init__(model=pp+_in+'.obj',texture=pp+_in+'.png',scale=cs,collider=b,position=pos)
		self.spawn_pos=pos
		self.poly=pse
		self.vnum=5
	def destroy(self):
		if status.aku_hit < 3:
			status.aku_hit+=1
		if not status.aku_exist:
			npc.AkuAkuMask(pos=(self.x,self.y,self.z))
		Audio(sn.snd_aku_m,pitch=1.2)
		destroy_event(self)

class Checkpoint(Entity):
	def __init__(self,pos,pse):
		_in='checkp'
		super().__init__(model=pp+_in+'.obj',texture=pp+_in+'.png',scale=cs,collider=b,position=pos)
		self.spawn_pos=pos
		self.poly=pse
		self.vnum=6
	def destroy(self):
		status.checkpoint=(self.x,self.y+1,self.z)
		sn.snd_checkp()
		destroy_event(self)
		CheckpointAnimation(p=self.position)
		status.NPC_RESET.clear()
		_core.collect_reset()

class SpringWood(Entity):
	def __init__(self,pos,pse):
		_in='spring'
		super().__init__(model=pp+_in+'.obj',texture=pp+_in+'.png',scale=cs,collider=b,position=pos)
		self.spawn_pos=pos
		self.poly=pse
		self.vnum=7
	def destroy(self):
		item.WumpaFruit(pos=self.position)
		destroy_event(self)

class SpringIron(Entity):
	def __init__(self,pos,pse):
		_in='spring_iron'
		super().__init__(model=pp+_in+'.obj',texture=pp+_in+'.png',scale=cs,collider=b,position=pos)
		self.spawn_pos=pos
		self.poly=pse
		self.p_snd=False
		self.vnum=8
	def destroy(self):
		block_destroy(self)

class SwitchEmpty(Entity):
	def __init__(self,pos,m,pse):
		self._in='switch'
		super().__init__(model=pp+self._in+'.obj',texture=pp+self._in+'.png',scale=cs,collider=b,position=pos)
		self.spawn_pos=pos
		self.poly=pse
		self.p_snd=False
		self.activ=False
		self.vnum=9
		self.mark=m
	def c_reset(self):
		self.texture=pp+self._in+'.png'
		self.activ=False
	def destroy(self):
		block_destroy(self)
		if not self.activ:
			self.activ=True
			self.texture=pp+'iron.png'
			ccount=0
			status.C_RESET.append(self)
			for _air in scene.entities[:]:
				if isinstance(_air,Air) and _air.mark == self.mark:
					invoke(_air.destroy,delay=ccount/3.5)
					ccount+=.8
			spawn_ico(self)

class SwitchNitro(Entity):
	def __init__(self,pos,pse):
		self._in='switch_n'
		super().__init__(model=pp+self._in+'.obj',texture=pp+self._in+'.png',scale=cs,collider=b,position=pos)
		self.spawn_pos=pos
		self.p_snd=False
		self.vnum=10
		self.activ=False
		self.poly=pse
	def c_reset(self):
		self.texture=pp+self._in+'.png'
		self.color=color.white
		self.activ=False
	def destroy(self):
		block_destroy(self)
		if not self.activ:
			self.activ=True
			self.color=color.green
			self.texture=pp+'iron.png'
			spawn_ico(self)
			status.C_RESET.append(self)
			for ni in scene.entities[:]:
				if isinstance(ni,Nitro):
					ni.destroy()

class TNT(Entity):
	def __init__(self,pos,pse):
		_in='tnt'
		super().__init__(model=pp+_in+'.obj',texture=pp+_in+'.png',scale=cs,collider=b,position=pos,shader=None)
		self.spawn_pos=pos
		self.vnum=11
		self.c_audio=Audio(sn.snd_c_tnt,autoplay=False)
		self.activ=False
		self.countdown=0
		self.poly=pse
	def destroy(self):
		self.activ=True
		self.color=color.hsv(0,0,2,1)
		self.c_audio.play()
		self.countdown=3.99
		self.shader=unlit_shader
	def empty_destroy(self):
		self.c_audio.fade_out()
		self.countdown=0
		Explosion(p=self.position,c=color.red)
		destroy_event(self)
	def update(self):
		if self.countdown > 0 and self.activ:
			self.countdown-=time.dt/1.15
			ctnt=int(self.countdown)
			self.texture='res/crate/crate_tnt_'+str(ctnt)+'.png'
			if self.countdown <= 0:
				self.empty_destroy()

class Nitro(Entity):
	def __init__(self,pos,pse):
		_in='nitro'
		super().__init__(model=pp+_in+'.obj',texture=pp+_in+'.png',scale=cs,collider=b,position=pos,shadows=False,color=color.hsv(0,0,1,1),shader=unlit_shader)
		self.spawn_pos=pos
		self.vnum=12
		self.acustic=False
		self.start_y=self.y
		self.snd_time=1
		self.poly=pse
	def destroy(self):
		Explosion(p=self.position,c=color.green)
		destroy_event(self)
	def update(self):
		dst=distance(cc.playerInstance[0].position,self.position)
		self.snd_time-=time.dt
		if self.snd_time <= 0:
			rh=random.uniform(0.1,0.2)
			self.snd_time=random.randint(2,3)
			if dst <= 1:
				Audio(sn.snd_nitro,volume=0.2)
			self.animate_position((self.x,self.y+rh,self.z),duration=0.02)
			invoke(lambda:self.animate_position((self.x,self.start_y,self.z),duration=0.2),delay=0.15)

class Air(Entity):
	def __init__(self,pos,m,l,pse):
		_in='air'
		super().__init__(model=pp+_in+'.obj',texture=pp+_in+'.png',scale=cs,collider=None,position=pos)
		self.spawn_pos=pos
		self.vnum=13
		self.mark=m
		self.c_ID=l
		self.poly=pse
	def destroy(self):
		status.C_RESET.append(self)
		place_crate(p=self.position,ID=self.c_ID,pse=1)
		Audio(sn.snd_c_air)
		scene.entities.remove(self)
		self.disable()

##crate effects
class Explosion(Entity):
	def __init__(self,p,c):
		super().__init__(model='sphere',position=p,color=c,collider='sphere',alpha=0.4,scale=0.1)
		Audio(sn.snd_explo,volume=1.5)
		if c == color.green:
			invoke(lambda:Audio(sn.snd_glass,volume=1.5),delay=.1)
	def update(self):
		for dest in scene.entities:
			if cc.is_crate(dest) and self.intersects(dest):
				do=dest.vnum
				if cc.is_crate(dest):
					if do in [3,11]:
						dest.empty_destroy()
					elif do == 13:
						return
					else:
						dest.destroy()
		self.scale_x+=0.4
		self.scale_y+=0.4
		self.scale_z+=0.4
		if self.scale > 1.6:
			self.scale=0
			self.parent=None
			self.disable()

class CheckpointAnimation(Entity):
	def __init__(self,p):
		super().__init__(position=(p[0],p[1]+1,p[2]))
		self.c_text='CHECKPOINT'
		self.wtime=0
		self.index=0
		self.run=True
	def update(self):
		if self.run:
			self.wtime+=time.dt
			if self.wtime >= 0.05:
				self.wtime=0
				letter=self.c_text[self.index]
				ct=Text(letter,font='res/ui/font.ttf',position=(self.x+self.index/10,self.y,self.z),scale=7,parent=scene,color=color.rgb(255,255,0))
				invoke(ct.disable,delay=1.5)
				self.index+=1
				if self.index >= 10:
					self.run=False
					self.disable()