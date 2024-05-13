import ui,crate,item,status,sound,npc,settings,_loc
from math import atan2,sqrt
from ursina import *

playerInstance=[]
level_ready=False
snd=sound
LC=_loc
C=crate
N=npc

## player
def set_val(d):
	for _a in ['run_anim','jump_anim','idle_anim','spin_anim','land_anim','fall_anim','flip_anim','anim_slide_stop','run_s_anim','attack_time','walk_snd','count_time','fall_time','blink_time','death_anim']:
		setattr(d,_a,0)
	for _v in ['block_input','walking','jumping','landed','is_touch_crate','first_land','is_landing','is_attack','is_flip','warped','freezed','injured','is_slippery','wall_stop']:
		setattr(d,_v,False)
	d.lpos=None
	d.move_speed=2.2
	d.direc=(0,0,0)
	d.jmp_hgt=0
	d.CMS=4
	playerInstance.append(d)
def set_jump_type(d,t):
	d.jumping=True
	tp={0:1,1:1.2,2:1.5}
	d.lpos=d.y+tp[t]
def get_damage(c):
	if not c.injured and not status.is_dying and status.aku_hit < 3:
		if status.aku_hit > 0:
			status.aku_hit-=1
			c.injured=True
			status.player_protect=2
			Audio(snd.snd_damg,pitch=.8)
		else:
			status.is_dying=True
			Audio(snd.snd_woah,pitch=.8)
def death_event(d):
	if not status.death_event:
		d.freezed=True
		status.death_event=True
		ui.BlackScreen()
		status.crate_count-=status.crate_to_sv
		if status.is_death_route:
			status.is_death_route=False
		if status.bonus_round:
			status.wumpa_bonus=0
			status.crate_bonus=0
			status.lives_bonus=0
			status.bonus_round=False
		else:
			if not status.is_time_trial:
				status.extra_lives-=1
				status.fails+=1
				if status.level_index == 2:
					status.gem_death=True
		if status.fails < 3:
			status.aku_hit=0
		else:
			status.aku_hit=1
			if not status.aku_exist:
				npc.AkuAkuMask(pos=(d.x,d.y,d.z))
		reset_crates()
		reset_wumpas()
		reset_npc()
		check_cstack()
		d.position=status.checkpoint
		camera.position=d.position
		camera.rotation=(15,0,0)
		d.is_reset_phase=False
		status.death_event=False
		invoke(lambda:setattr(d,'freezed',False),delay=2)
def various_val(c):
	if status.bonus_solved:
		if status.wumpa_bonus > 0 or status.crate_bonus > 0 or status.lives_bonus > 0:
			bonus_reward(c)
	if c.walk_snd > 0:
		c.walk_snd-=time.dt
	if c.blink_time > 0:
		c.blink_time-=time.dt
	if c.injured:
		c.hurt_blink()
	if status.c_delay > 0:
		status.c_delay-=time.dt
	if status.d_delay > 0:
		status.d_delay-=time.dt
	if status.player_protect > 0:
		status.player_protect-=time.dt
		if status.player_protect <= 0:
			c.alpha=1
			c.injured=False
def c_attack(c):
	for AC in scene.entities[:]:
		if AC.parent == scene and distance(AC,c) <= .5 and AC.collider != None:
			if is_crate(AC):
				if AC.vnum in [3,11]:
					AC.empty_destroy()
				else:
					AC.destroy()
			if is_enemie(AC) and not AC.is_hitten:
				a=Vec3(c.x-AC.x,0,c.z-AC.z)
				if a.x > 0 and a.x > a.z:
					AC.fly_direc=0
				if a.x < 0 and a.x < a.z:
					AC.fly_direc=1
				if a.z > 0 and a.z > a.x:
					AC.fly_direc=2
				if a.z < 0 and a.z < a.x:
					AC.fly_direc=3
				AC.is_hitten=True
				Audio(snd.snd_nbeat)

## camera actor
def cam_rotate(c):
	ftt=time.dt*1.5
	if c.jumping:
		camera.rotation_x-=ftt
		return
	if camera.rotation_x < 15:
		camera.rotation_x+=ftt
def cam_follow(c):
	if status.LV_CLEAR_PROCESS:
		c=None
		return
	ftr=time.dt*3
	camera.z=lerp(camera.z,c.z-c.CMS,ftr)
	if status.c_indoor:
		if not status.p_in_air(c):
			camera.y=lerp(camera.y,c.y+1,time.dt)
		camera.rotation_x=12
		return
	if (status.bonus_round or status.is_death_route) and not c.freezed:
		camera.y=lerp(camera.y,c.y+1,time.dt)
	camera.x=lerp(camera.x,c.x,ftr)
def free_view_field(o):
	if o.z < playerInstance[0].z-2:
		o.hide()
		return
	o.show()

## world, misc
def collect_reset():
	status.C_RESET.clear()
	status.W_RESET.clear()
	status.crate_to_sv=0
	status.fails=0
	if level_ready:
		status.NPC_RESET.clear()
def c_subtract(cY):
	if cY < -20:
		status.crates_in_bonus-=1
	status.crates_in_level-=1
def reset_crates():
	for ca in scene.entities[:]:
		if is_crate(ca):
			if ca.poly == 1:
				scene.entities.remove(ca)
				ca.disable()
	for cv in status.C_RESET[:]:
		if cv.vnum in [9,10]:
			cv.c_reset()
		elif cv.vnum == 13:
			if not cv.c_ID == 0:
				c_subtract(cY=cv.y)
			C.place_crate(p=cv.spawn_pos,ID=cv.vnum,m=cv.mark,l=cv.c_ID,pse=cv.poly)
		else:
			c_subtract(cY=cv.y)
			C.place_crate(p=cv.spawn_pos,ID=cv.vnum)
	status.C_RESET.clear()
	status.crate_to_sv=0
def reset_wumpas():
	for wu in status.W_RESET[:]:
		wu.destroy()
	status.W_RESET.clear()
def reset_npc():
	for NP in status.NPC_RESET[:]:
		npc.spawn(mID=NP.vnum,pos=NP.spawn_pos,mDirec=NP.m_direction,mTurn=0)
	status.NPC_RESET.clear()
def clear_level(passed):
	status.LV_CLEAR_PROCESS=True
	scene.clear()
	if passed:
		collect_rewards()
	ui.WhiteScreen()
def collect_rewards():
	if status.level_crystal:
		status.CRYSTAL.append(status.level_index)
		status.collected_crystals+=1
	if status.level_col_gem:
		status.COLOR_GEM.append(status.level_index)
		status.color_gems+=1
	if status.level_col_gem:
		status.CLEAR_GEM.append(status.level_index)
		status.clear_gems+=1

## collisions
def obj_ceiling(c):## hit by jump and not move
	cK=c.intersects()
	if cK.normal == Vec3(0,-1,0) and not (str(cK.entity) in LC.item_lst or cK.entity == LC.htBOX):
		if is_crate(cK.entity) and not c.is_touch_crate:
			c.is_touch_crate=True
			cK.entity.destroy()
			invoke(lambda:setattr(c,'is_touch_crate',False),delay=.1)
		c.jumping=False
		c.y=c.y
def obj_walk(c):
	PT=playerInstance[0]
	if LC.map_zone and c.intersects(LC.map_zone):
		landing(c=c,e=terraincast(c.world_position,LC.map_zone,LC.map_height))
		return
	d=boxcast(c.world_position,Vec3(0,1,0),distance=.1,thickness=(.1,.1),ignore=[c,PT,LC.shdw],debug=False)
	dE=d.entity
	if d and not str(dE) in LC.item_lst:
		if (is_crate(dE) and not dE.vnum == 0) and not (is_crate(dE) and dE.vnum in [9,10,11] and dE.activ) and c.fall_time > .1:
			crate_action(c=PT,e=d.entity)
		if is_enemie(dE):
			jump_enemy(c=PT,e=dE)
		else:
			landing(c=PT,e=d.world_point.y)
			obj_act(c=PT,e=d.entity)
		return
	playerInstance[0].landed=False
def obj_walls(c,H):
	hE=H.entity
	if H.normal and H.normal != Vec3(0,1,0):
		if isinstance(hE,crate.Nitro) and hE.collider != None:
			hE.destroy()
		if is_enemie(hE) and not c.is_attack:
			get_damage(c)
		else:
			if not str(hE) in LC.item_lst:
				#if c.direc == c.direc:
				#	c.position-=c.direc*time.dt*3
				return
	c.x+=c.direc.x*time.dt*c.move_speed
	c.z+=c.direc.z*time.dt*c.move_speed
def obj_act(c,e):
	u=str(e)
	if u in LC.dangers:
		death_zone(c=c,e=e)
		return
	if (u == 'bonus_platform' and not status.bonus_solved) or u == 'gem_platform':
		if not c.freezed:
			c.freezed=True
			e.catch_player=True
		return
	if u == 'level_finish':
		jmp_lv_fin(c=c,e=e)
		return
	if u == 'ice_ground':
		e.do_slide(c=c)
	if u == 'plank' and e.typ == 1:
		e.pl_touch()
		return
def landing(c,e):
	c.landed=True
	if c.y != e and not c.jumping:
		c.y=e
		if c.first_land:
			c.first_land=False
			c.is_landing=True
			c.land_anim=0
			Audio(snd.snd_land)
		c.block_input=False
		c.is_flip=False
		c.flip_anim=0
def platform_floating(m,c):
	m.air_time+=time.dt
	m.y+=time.dt
	m.target.x=m.x
	m.target.z=m.z
	c.rotation_y=0
	if m.air_time >= 3:
		m.air_time=0
		m.catch_player=False
		m.position=m.orginal_pos
		if status.level_index == 4:
			c.freezed=False
			return
		if str(m) == 'bonus_platform':
			load_bonus(c=m.target)
		else:
			load_gem_route(c=m.target)
def jump_enemy(c,e):
	e0=str(e)
	if e0 in ['saw_turtle','lizard'] or e0 == 'hedgehog' and e.defend_mode:
		get_damage(c)
		return
	kill_by_jump(m=e,c=c)
def jmp_lv_fin(c,e):
	if not status.LEVEL_CLEAN:
		status.LEVEL_CLEAN=True
		clear_level(passed=True)
def death_zone(c,e):
	if not status.is_dying:
		status.is_dying=True
		Audio(snd.snd_woah,pitch=.8)
def c_item(c):
	vL=c.intersects()
	if vL and str(vL.entity) in LC.item_lst:
		vL.entity.collect()

## interface,collectables
def wumpa_count(n):
	if status.bonus_round:
		status.wumpa_bonus+=n
	else:
		status.wumpa_fruits+=n
		status.show_wumpas=5
		sc_ps=playerInstance[0].screen_position
		if status.wumpa_bonus <= 0:
			if n > 1:
				ui.WumpaCollectAnim(pos=(sc_ps[0],sc_ps[1]))
			ui.WumpaCollectAnim(pos=(sc_ps[0],sc_ps[1]+.1))
	snd.snd_collect()
def give_extra_live():
	ui.live_get_anim()
	Audio(snd.snd_lifes,volume=.5)
	if status.bonus_round:
		status.lives_bonus+=1
	else:
		status.extra_lives+=1
		status.show_lives=5

## crate actions
def crate_set_val(cR,Cpos,Cpse):
	if cR.vnum == 15:
		cR.texture='res/crate/'+str(cR.vnum)+'/crate_t'+str(cR.time_stop)+'.png'
	else:
		cR.texture='res/crate/'+str(cR.vnum)+'/c_tex.png'
	cR.org_tex=cR.texture
	cR.destroy_exp=False
	cR.is_stack=False
	cR.spawn_pos=Cpos
	cR.position=Cpos
	cR.collider='box'
	cR.poly=Cpse
	cR.scale=.16
def is_crate(e):
	cck=[C.Iron,C.Normal,C.QuestionMark,C.Bounce,C.ExtraLife,
		C.AkuAku,C.Checkpoint,C.SpringWood,C.SpringIron,C.SwitchEmpty,
		C.SwitchNitro,C.TNT,C.Nitro,C.Air,C.Protected,C.cTime,C.LvInfo]
	if any(isinstance(e,crate_class) for crate_class in cck):
		return True
	return False
def crate_action(c,e):
	if e.vnum in [7,8]:
		set_jump_type(d=c,t=2)
		e.anim_act()
		return
	e.destroy()
	set_jump_type(d=c,t=0)
def check_cstack():
	for cSD in scene.entities[:]:
		if is_crate(cSD) and not cSD.vnum ==3:
			for cST in scene.entities[:]:
				if is_crate(cST) and not cST.vnum == 3:
					if cST.x == cSD.x and cST.z == cSD.z:
						dsta=round(abs(cST.y-(cSD.y-cSD.scale_y*2)),2)
						if dsta == 0:
							cST.is_stack=True
							cSD.is_stack=True
def check_crates_over(c):
	for co in scene.entities:
		if is_crate(co) and not c.vnum == 3:
			if c.x == co.x and c.z == co.z and co.y > c.y:
				if co.is_stack:
					co.animate_y(co.y-co.scale_y*2,duration=.15)

## bonus level
def load_bonus(c):
	status.loading=True
	status.checkpoint=_loc.bonus_checkpoint[status.level_index]
	collect_reset()
	if status.bonus_round:
		invoke(lambda:back_to_level(c),delay=.5)
	else:
		invoke(lambda:enter_bonus(c),delay=.5)
def enter_bonus(c):
	status.bonus_round=True
	status.day_mode='bonus'
	snd.BonusMusic(T=status.level_index)
	ui.BonusText()
	c.position=(0,-35,-3)
	camera.y=-35
	status.loading=False
	c.freezed=False
def back_to_level(c):
	if status.is_death_route:
		status.is_death_route=False
	if status.bonus_round:
		status.bonus_round=False
		status.bonus_solved=True
	dMN=_loc.day_m
	status.day_mode=dMN[status.level_index]
	c.position=status.checkpoint
	c.freezed=False
	camera.y=c.y+.5
	status.loading=False
def bonus_reward(p):
	p.count_time+=time.dt
	if p.count_time >= .075:
		p.count_time=0
		if status.wumpa_bonus > 0:
			status.wumpa_bonus-=1
			wumpa_count(1)
			ui.wumpa_bonus_anim()
		if status.crate_bonus > 0:
			status.crate_bonus-=1
			status.crate_count+=1
			status.show_crates=1
		if status.lives_bonus > 0:
			status.lives_bonus-=1
			status.extra_lives+=1
			status.show_lives=1
			Audio(sound.snd_lifes)

## gem route
def load_gem_route(c):
	status.loading=True
	if status.is_death_route:
		invoke(lambda:back_to_level(c),delay=.5)
	else:
		invoke(lambda:load_droute(c),delay=.5)
def load_droute(c):
	if not status.is_death_route:
		status.is_death_route=True
		c.position=(200,1,-3)
		camera.position=(200,.5,-3)
		status.loading=False
		c.freezed=False
		snd.SpecialMusic(T=status.level_index)
	else:
		c.back_to_level(c)

## npc
def set_val_npc(m):
	if str(m) in ['rat','eating_plant','vulture']:
		m.can_move=False
	else:
		m.can_move=True
	m.spawn_point=m.position
	m.is_hitten=False
	m.fly_direc=None
	m.is_purge=False
	m.unlit=False
	m.anim_frame=0
	m.fly_time=0
	#m.collider.visible=True
def npc_action(m):
	if m.visible:
		if m.is_purge:
			npc_purge(m)
			return
		if not m.is_hitten:
			npc.walk_frames(m)
			npc_walk(m)
			return
		fly_away(m)
def npc_purge(m):
	u=60
	m.can_move=False
	m.collider=None
	m.fly_time=0
	if m.scale_x > 0:
		m.scale_x-=time.dt/u
	if m.scale_y > 0:
		m.scale_y-=time.dt/u
	if m.scale_z > 0:
		m.scale_z-=time.dt/u
	if m.scale_x <= 0 and m.scale_y <= 0 and m.scale_z <= 0:
		status.NPC_RESET.append(m)
		m.disable()
def npc_walk(m):
	if status.pause:
		return
	if m.can_move:
		s=m.move_speed
		m_D=m.m_direction
		if m.m_direction == 0:
			if m.turn == 0:
				m.x+=time.dt*s
				if m.x >= m.spawn_point[0]+1:
					m.rotation_y=90
					m.turn=1
			elif m.turn == 1:
				m.x-=time.dt*s
				if m.x <= m.spawn_point[0]-1:
					m.rotation_y=270
					m.turn=0
		if m.m_direction == 1:
			if m.turn == 0:
				m.z+=time.dt*s
				if m.z >= m.spawn_point[2]+1:
					m.turn=1
					m.rotation_y=0
			elif m.turn == 1:
				m.z-=time.dt*s
				if m.z <= m.spawn_point[2]-1:
					m.rotation_y=180
					m.turn=0
def rotate_to_crash(m):
	target=playerInstance[0]
	relative_position=target.position-m.position
	angle=atan2(relative_position.x,relative_position.z)*(180/pi)+180
	m.rotation_y=angle
	m.rotation_x=-90
def fly_away(n):
	fSP=time.dt*20
	flD={0:lambda:setattr(n,'x',n.x-fSP),
		1:lambda:setattr(n,'x',n.x+fSP),
		2:lambda:setattr(n,'z',n.z-fSP),
		3:lambda:setattr(n,'z',n.z+fSP)}
	flD[n.fly_direc]()
	n.fly_time+=time.dt
	J=n.intersects()
	if J:
		PNL=J.entity
		if is_crate(PNL):
			if PNL.vnum in [3,11]:
				PNL.empty_destroy()
			else:
				if not PNL.vnum == 6:# avoid checkp accidentally
					PNL.destroy()
		if is_enemie(PNL):
			PNL.is_purge=True
			wumpa_count(1)
	if n.fly_time > .3:
		npc_purge(n)
def kill_by_jump(m,c):
	m.is_purge=True
	set_jump_type(d=c,t=0)
	Audio(snd.snd_jmph)
def is_nearby_pc(n,DX,DY):
	dist_y=abs(playerInstance[0].y-n.y)
	dist_x=distance_xz(playerInstance[0],n)
	if dist_y < DY and dist_x < DX:
		return True
	return False
def is_enemie(n):
	nnk=[N.Amadillo,N.Turtle,N.SawTurtle,
		N.Penguin,N.Hedgehog,N.Seal,
		N.EatingPlant,N.Rat,N.Lizard,
		N.Scrubber,N.Mouse,N.Vulture]
	if any(isinstance(n,npc_class) for npc_class in nnk):
		return True
	return False

## reduce lagg by first spawn
def preload_items():
	status.preload_phase=True
	settings.SFX_VOLUME=0
	FrameAnimation3d('res/crate/anim/bnc/bnc.obj',y=-255,loop=False,scale=.5,fps=20)
	for PRC in range(13):
		C.place_crate(ID=PRC,p=(0+PRC,-255,0),m=99,l=13)
		item.WumpaFruit(pos=(0+PRC,-255,0))
	for DPR in scene.entities:
		if is_crate(DPR) and DPR.collider != None and DPR.y <= -255:
			if DPR.vnum == 3:
				DPR.empty_destroy()
			else:
				DPR.destroy()
	status.C_RESET.clear()
	invoke(end_preload,delay=.3)
def end_preload():
	status.preload_phase=False
	settings.SFX_VOLUME=2