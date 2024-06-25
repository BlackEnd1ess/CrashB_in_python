import ui,crate,item,status,sound,npc,settings,_loc,math
from math import atan2,sqrt
from ursina import *

level_ready=False
snd=sound
st=status
LC=_loc
C=crate
N=npc

## player
def set_val(c):
	for _a in ['run_anim','jmp_typ','jump_anim','idle_anim','spin_anim','land_anim','fall_anim','flip_anim','anim_slide_stop','run_s_anim','attack_time','walk_snd','count_time','fall_time',
			'blink_time','death_anim','slide_fwd']:
		setattr(c,_a,0)
	for _v in ['aq_bonus','walking','jumping','landed','is_touch_crate','first_land','is_landing','is_attack','is_flip','warped','freezed','injured','is_slippery','wall_stop']:
		setattr(c,_v,False)
	c.move_speed=2.4
	c.direc=(0,0,0)
	c.vpos=None
	c.indoor=.5
	c.CMS=4
	_loc.ACTOR=c
def set_jump_type(c,typ):
	c.jmp_typ=typ
	jmp_h={0:c.y+1.3,1:c.y+1,2:c.y+1.7,3:c.y+1.1}
	c.vpos=jmp_h[typ]
	c.jumping=True
def get_damage(c):
	if not c.injured and not status.is_dying and status.aku_hit < 3:
		if st.aku_hit > 0:
			status.aku_hit-=1
			c.injured=True
			Audio(snd.snd_damg,pitch=.8)
			invoke(lambda:setattr(c,'injured',False),delay=2)
			invoke(lambda:setattr(c,'alpha',1),delay=2)
		else:
			status.is_dying=True
			Audio(snd.snd_woah,pitch=.8)
def death_event(d):
	if not st.death_event:
		status.death_event=True
		d.freezed=True
		ui.BlackScreen()
		status.crate_count-=status.crate_to_sv
		if st.is_death_route:
			status.is_death_route=False
		if st.bonus_round:
			status.wumpa_bonus=0
			status.crate_bonus=0
			status.lives_bonus=0
			status.bonus_round=False
		else:
			if not st.is_time_trial:
				status.extra_lives-=1
				status.fails+=1
				if status.level_index == 2:
					status.gem_death=True
		if st.fails < 3:
			status.aku_hit=0
		else:
			status.aku_hit=1
			if not st.aku_exist:
				Audio(sound.snd_aku_m,pitch=1.2,volume=settings.SFX_VOLUME)
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
	if st.bonus_solved and not st.wait_screen:
		if st.wumpa_bonus > 0 or st.crate_bonus > 0 or st.lives_bonus > 0:
			bonus_reward(c)
		else:
			c.aq_bonus=False
	if c.blink_time > 0:c.blink_time-=time.dt
	if c.walk_snd > 0:c.walk_snd-=time.dt
	if c.indoor > 0:c.indoor-=time.dt
	if c.injured:c.hurt_blink()
def c_attack(c):
	for e in scene.entities[:]:
		if is_nearby_pc(e,DX=.5,DY=.5):
			if is_crate(e):
				if e.vnum in [3,11]:
					e.empty_destroy()
				else:
					e.destroy()
			if is_enemie(e) and not e.is_hitten:
				e.is_hitten=True
				a=Vec3(e.x-c.x,0,e.z-c.z)
				e.fly_direc=a
				Audio(snd.snd_nbeat)
def c_slide(c):
	if not c.walking:
		if c.slide_fwd > 0 and status.p_last_direc != None:
			if c.move_speed > 0:
				c.move_speed-=time.dt
			c.position+=status.p_last_direc*time.dt*c.slide_fwd
			c.slide_fwd-=time.dt
			if c.slide_fwd <= 0:
				c.slide_fwd=0
				status.p_last_direc=None
		return
	if c.move_speed < 4:
		c.move_speed+=time.dt
		if c.move_speed > 0:
			c.slide_fwd=c.move_speed

## camera actor
def cam_rotate(c):
	ftt=time.dt*1.5
	if c.jumping:
		camera.rotation_x-=ftt
		return
	if camera.rotation_x < 15:
		camera.rotation_x+=ftt
def cam_follow(c):
	if st.LV_CLEAR_PROCESS:
		c=None
		return
	ftr=time.dt*3
	camera.z=lerp(camera.z,c.z-c.CMS,ftr)
	camera.x=lerp(camera.x,c.x,ftr)
	if c.indoor > 0:
		if not status.p_in_air(c):
			camera.y=lerp(camera.y,c.y+1,time.dt)
		camera.rotation_x=12
		return
	if (st.bonus_round or st.is_death_route) and not c.freezed:
		camera.y=lerp(camera.y,c.y+1,time.dt)

## world, misc
def collect_reset():
	status.C_RESET.clear()
	status.W_RESET.clear()
	status.crate_to_sv=0
	status.fails=0
	if level_ready:status.NPC_RESET.clear()
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
	for cv in st.C_RESET[:]:
		if cv.vnum in [9,10]:
			cv.c_reset()
		elif cv.vnum == 13:
			if not cv.c_ID == 0:
				c_subtract(cY=cv.y)
			C.place_crate(p=cv.spawn_pos,ID=cv.vnum,m=cv.mark,l=cv.c_ID,pse=cv.poly)
		else:
			if cv.vnum == 11:
				cv.activ=False
				cv.countdown=0
			c_subtract(cY=cv.y)
			C.place_crate(p=cv.spawn_pos,ID=cv.vnum)
	status.C_RESET.clear()
	status.crate_to_sv=0
def reset_wumpas():
	for wu in st.W_RESET[:]:
		wu.destroy()
	status.W_RESET.clear()
def reset_npc():
	for NP in st.NPC_RESET[:]:
		npc.spawn(mID=NP.vnum,pos=NP.spawn_pos,mDirec=NP.m_direction,mTurn=0)
	status.NPC_RESET.clear()
def clear_level(passed):
	st.LV_CLEAR_PROCESS=True
	scene.clear()
	if passed:
		collect_rewards()
	ui.WhiteScreen()
def collect_rewards():
	if st.level_crystal:
		status.CRYSTAL.append(status.level_index)
		status.collected_crystals+=1
	if st.level_col_gem:
		status.COLOR_GEM.append(status.level_index)
		status.color_gems+=1
	if st.level_col_gem:
		status.CLEAR_GEM.append(status.level_index)
		status.clear_gems+=1
def reset_audio():
	status.e_audio=False
	status.n_audio=False
	status.b_audio=False

## collisions
def obj_ceiling(c):
	vc=c.intersects(ignore=[c,LC.shdw])
	if vc and vc.normal == Vec3(0,-1,0):
		e=vc.entity
		if not str(e) in LC.item_lst:
			if is_crate(e) and not c.is_touch_crate:
				c.is_touch_crate=True
				e.destroy()
				invoke(lambda:setattr(c,'is_touch_crate',False),delay=.1)
			if str(e) in LC.dangers or (is_enemie(e) and not c.is_attack):
				get_damage(c)
			c.jumping=False
			c.y=c.y
def obj_grnd(c):
	vj=boxcast(c.world_position,Vec3(0,1,0),distance=.01,thickness=(.1,.1),ignore=[c,LC.shdw],debug=False)
	vp=vj.entity
	if vj.normal and not (str(vp) in LC.item_lst or str(vp) in LC.dangers):
		if (is_crate(vp) and not vp.vnum == 0) and not (is_crate(vp) and vp.vnum in [9,10,11] and vp.activ) and c.fall_time > .1:
			crate_action(c=c,e=vp)
		if is_enemie(vp) and not vp.is_hitten:
			jump_enemy(c=c,e=vp)
		else:
			landing(c=c,e=vj.world_point.y)
			obj_act(c=c,e=vp)
		return
	c.landed=False
def obj_walls(c):
	if status.LV_CLEAR_PROCESS:
		c=None
		return
	ig=[c,LC.shdw]
	vT=raycast(c.world_position+(0,.1,0),c.direc,distance=.2,ignore=ig,debug=False)
	hT=c.intersects(ignore=ig)
	for jF in [hT,vT]:
		jV=jF.entity
		if jF and jF.normal != Vec3(0,1,0):
			if isinstance(jV,crate.Nitro) and jV.collider != None:jV.destroy()
			if (is_enemie(jV) and not c.is_attack) or (str(jV) in LC.dangers and jV.danger):
				get_damage(c)
				return
			else:
				if not str(jV) in LC.item_lst:return
	#avoid sys error by missing ursina entity
	c.position+=c.direc*time.dt*c.move_speed
def obj_act(c,e):
	u=str(e)
	if u in LC.d_zone:
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
		c.is_slippery=True
		return
	if u == 'MO_PL' and not c.walking and e.movable:
		c.x=e.x
		c.z=e.z
		return
	if u == 'plank' and e.typ == 1:
		e.pl_touch()
		return
	c.is_slippery=False
	c.move_speed=2.2
def landing(c,e):
	c.landed=True
	if c.y < e and not c.jumping:
		c.y=e
	if c.first_land:
		c.first_land=False
		c.is_landing=True
		c.land_anim=0
		Audio(snd.snd_land)
	c.is_flip=False
	c.flip_anim=0
def platform_floating(m,c):
	m.air_time+=time.dt/1.5
	m.y+=time.dt/1.5
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
	if (e.vnum in [2,8]) or (e.vnum == 4 and e.def_mode):
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
	j=c.intersects(ignore=[c,LC.shdw])
	if str(j.entity) in LC.item_lst:
		j.entity.collect()

## interface,collectables
def wumpa_count(n):
	if status.bonus_round:
		status.wumpa_bonus+=n
	else:
		status.wumpa_fruits+=n
		status.show_wumpas=5
		sc_ps=LC.ACTOR.screen_position
		if status.wumpa_bonus <= 0 and not LC.ACTOR.aq_bonus:
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
		cR.texture='res/crate/crate_t'+str(cR.time_stop)+'.png'
	else:
		cR.texture='res/crate/'+str(cR.vnum)+'.png'
	cR.org_tex=cR.texture
	cR.fall_down=False
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
		set_jump_type(c,typ=2)
		e.c_action()
		return
	elif e.vnum == 3:
		set_jump_type(c,typ=3)
	else:
		if not e.vnum == 14:
			set_jump_type(c,typ=1)
	e.destroy()
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
	if c.vnum in [3,7,8]:
		return
	for co in scene.entities[:]:
		if is_crate(co) and co.is_stack:
			if (c.x == co.x and co.z == c.z) and c.y < co.y:
				if co.y > co.y-.32:
					co.animate_y(co.y-.32,duration=.1,unscaled=True)

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
	ui.BlackScreen()
	status.bonus_round=True
	status.day_mode='bonus'
	snd.BonusMusic(T=status.level_index)
	ui.BonusText()
	c.position=(0,-35,-3)
	camera.y=-35
	status.loading=False
	c.freezed=False
def back_to_level(c):
	ui.BlackScreen()
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
	p.aq_bonus=True
	p.count_time+=time.dt
	if p.count_time >= .075:
		p.count_time=0
		if status.wumpa_bonus > 0:
			status.wumpa_bonus-=1
			ui.WumpaCollectAnim(pos=(-.2,-.4))
			wumpa_count(1)
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
	ui.BlackScreen()
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
	if m.vnum in [6,7,11]:
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
def npc_action(m):
	if m.is_purge:
		npc_purge(m)
		return
	if not m.is_hitten:
		npc.walk_frames(m)
		if m.vnum == 9 and m.ro_mode:
			npc_circle_move(m)
		else:
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
	if status.gproc():
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
def npc_circle_move(m):
	m.angle+=time.dt*3
	m.angle%=(2*math.pi)
	new_x=m.spawn_pos[0]+1*math.cos(m.angle)
	new_y=m.spawn_pos[1]+1*math.sin(m.angle)
	m.position=Vec3(new_x,new_y,m.z)
	#direction_to_center=m.spawn_pos-m.position
	#self.rotation = Vec3(0, -math.degrees(math.atan2(direction_to_center.z, direction_to_center.x)) + 90, 0)
def rotate_to_crash(m):
	relative_position=LC.ACTOR.position-m.position
	angle=atan2(relative_position.x,relative_position.z)*(180/pi)+180
	m.rotation_y=angle
	m.rotation_x=-90
def fly_away(n):
	fSP=time.dt*40
	n.position+=n.fly_direc*fSP
	n.fly_time-=time.dt
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
			PNL.fly_direc=n.fly_direc
			PNL.is_hitten=True
			wumpa_count(1)
			npc_purge(n)
			return
	if abs(n.fly_time) > .3:npc_purge(n)
def kill_by_jump(m,c):
	m.is_purge=True
	set_jump_type(c,typ=1)
	Audio(snd.snd_jmph)
def is_nearby_pc(n,DX,DY):
	if LC.ACTOR:
		dist_y=abs(LC.ACTOR.y-n.y)
		dist_x=distance_xz(LC.ACTOR,n)
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
	return
#	status.preload_phase=True
#	settings.SFX_VOLUME=0
#def end_preload():
#	status.preload_phase=False
#	settings.SFX_VOLUME=2