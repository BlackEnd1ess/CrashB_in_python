import ui,crate,item,status,sound,npc,settings,_loc,math
from math import atan2,sqrt
from ursina import *

level_ready=False
sn=sound
st=status
LC=_loc
C=crate
N=npc

## player
def set_val(c):
	for _a in ['run_anim','jmp_typ','jump_anim','idle_anim','spin_anim','land_anim','fall_anim','flip_anim','anim_slide_stop','run_s_anim','attack_time','walk_snd','fall_time','death_anim','slide_fwd','in_water']:
		setattr(c,_a,0)
	for _v in ['aq_bonus','walking','jumping','landed','tcr','first_land','is_landing','is_attack','is_flip','warped','freezed','injured','is_slippery','wall_stop']:
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
def get_damage(c,rsn):
	if not (c.injured or st.death_event):
		if st.aku_hit > 0:
			status.aku_hit-=1
			c.injured=True
			c.hurt_blink()
			sn.pc_audio(ID=6,pit=.8)
			invoke(lambda:setattr(c,'injured',False),delay=2)
			invoke(lambda:setattr(c,'alpha',1),delay=2)
			del rsn
			return
		dth_event(c,rsn=rsn)
def dth_event(c,rsn):
	if not st.death_event:
		if rsn == 0:
			sn.pc_audio(ID=14,pit=.8)
		else:
			sn.pc_audio(ID=7,pit=.8)
		status.death_event=True
		c.freezed=True
		c.death_action(rsn=rsn)
def reset_state(c):
	ui.BlackScreen()
	status.crate_count-=st.crate_to_sv
	if st.is_death_route:
		status.is_death_route=False
	if st.bonus_round:
		status.wumpa_bonus=0
		status.crate_bonus=0
		status.lives_bonus=0
		status.bonus_round=False
	else:
		status.extra_lives-=1
		status.fails+=1
		if st.level_index == 2:
			status.gem_death=True
	if st.extra_lives <= 0:
		game_over()
		return
	if st.fails < 3:
		status.aku_hit=0
	else:
		status.aku_hit=1
		if not st.aku_exist:
			sn.crate_audio(ID=14,pit=1.2)
			npc.AkuAkuMask(pos=(c.x,c.y,c.z))
	reset_crates()
	rmv_wumpas()
	reset_npc()
	check_cstack()
	c.position=status.checkpoint
	camera.position=c.position
	camera.rotation=(15,0,0)
	status.death_event=False
	c.visible=True
	invoke(lambda:setattr(c,'freezed',False),delay=3)
def game_over():
	clear_level(passed=False)
	invoke(lambda:ui.GameOverScreen(),delay=1)
def various_val(c):
	c.indoor=max(c.indoor-time.dt,0)
	c.in_water=max(c.in_water-time.dt,0)
	if not c.is_slippery:c.move_speed=2.4
	if st.bonus_solved and not st.wait_screen:
		c.aq_bonus=(st.wumpa_bonus > 0 or st.crate_bonus > 0 or st.lives_bonus > 0)
def c_attack(c):
	for e in scene.entities[:]:
		if distance(c,e) < .5:
			if is_crate(e):
				if e.vnum in [3,11]:
					e.empty_destroy()
				else:
					if not e.falling and not e.vnum == 13:
						e.destroy()
			if is_enemie(e) and not e.is_hitten:
				if (e.vnum in [1,9]) or (e.vnum == 5 and e.def_mode):
					get_damage(c,rsn=1)
				e.is_hitten=True
				e.fly_direc=Vec3(e.x-c.x,0,e.z-c.z)
				sn.obj_audio(ID=8)
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
		if c.landed:
			camera.y=lerp(camera.y,c.y+1,time.dt)
		camera.rotation_x=12
		return
	if (st.bonus_round or st.is_death_route) and not c.freezed:
		camera.y=lerp(camera.y,c.y+1,time.dt)

## world, misc
def collect_reset():
	status.C_RESET.clear()
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
				purge_instance(ca)
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
def rmv_wumpas():
	for wu in scene.entities[:]:
		if isinstance(wu,item.WumpaFruit) and wu.auto_purge:
			wu.destroy()
def reset_npc():
	for NP in st.NPC_RESET[:]:
		if NP.vnum in [10,11]:
			npc.spawn(mID=NP.vnum,pos=NP.spawn_pos,mDirec=NP.m_direction,mTurn=0,ro_mode=NP.ro_mode)
		else:
			npc.spawn(mID=NP.vnum,pos=NP.spawn_pos,mDirec=NP.m_direction,mTurn=0)
	status.NPC_RESET.clear()
def clear_level(passed):
	st.LV_CLEAR_PROCESS=True
	scene.clear()
	if passed:
		collect_rewards()
		ui.WhiteScreen()
		return
	ui.BlackScreen()
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
def purge_instance(v):
	v.parent=None
	scene.entities.remove(v)
	v.disable()
	del v

## collisions
def obj_ceiling(c):
	vc=c.intersects(ignore=[c,LC.shdw])
	if vc and vc.normal == Vec3(0,-1,0):
		e=vc.entity
		if not (str(e) in LC.item_lst or str(e) in LC.trigger_lst):
			if is_crate(e) and not c.tcr:
				c.tcr=True
				e.destroy()
				invoke(lambda:setattr(c,'tcr',False),delay=.1)
			c.y=c.y
			c.jumping=False
def obj_grnd(c):
	vj=boxcast(c.world_position,Vec3(0,1,0),distance=.01,thickness=(.13,.13),ignore=[c,LC.shdw],debug=False)
	vp=vj.entity
	if vj.normal and not (str(vp) in LC.item_lst or str(vp) in LC.dangers or str(vp) in LC.trigger_lst):
		if (is_crate(vp) and not vp.vnum == 0) and not (is_crate(vp) and vp.vnum in [9,10,11] and vp.activ) and c.fall_time > .1:
			crate_action(e=vp)
			return
		if is_enemie(vp) and not vp.is_hitten:
			jump_enemy(c=c,e=vp)
			return
		landing(c,e=vj.world_point.y,o=vp)
		if str(vp.name) == 'mptf':
			vp.mv_player()
		if str(vp) == 'water_hit':
			dth_event(c,rsn=2)
			return
		c.is_slippery=(str(vp.name) == 'iceg')
		return
	c.landed=False
def obj_walls(c):
	if st.LV_CLEAR_PROCESS:
		del c
		return
	hT=c.intersects(ignore=[c,LC.shdw])
	jV=hT.entity
	xa=str(jV)
	if hT and hT.normal != Vec3(0,1,0):
		if isinstance(jV,crate.Nitro) and jV.collider != None:
			jV.destroy()
			return
		if xa in LC.trigger_lst:
			jV.do_act()
			return
		if xa in LC.item_lst:
			jV.collect()
			return
		if (is_enemie(jV) and not c.is_attack):
			if jV.vnum == 7:
				get_damage(c,rsn=5)
				return
			get_damage(c,rsn=1)
			return
		c.position-=c.direc*time.dt*c.move_speed
def obj_act(e):
	u=str(e)
	e.catch_p=(u in ['bonus_platform','gem_platform'])
	e.active=(u == 'HPP')
	if (u == 'plank' and e.typ == 1):e.pl_touch()
	if u == 'falling_zone':dth_event(c=LC.ACTOR,rsn=0)
	if u == 'loose_platform':e.active=True
	if u == 'swim_platform':e.active=True
def landing(c,e,o):
	c.landed=True
	if c.y < e and not c.jumping:
		c.y=e
	if c.first_land:
		c.first_land=False
		c.is_landing=True
		c.land_anim=0
		if str(o) in ['sewer_platform','swim_platform']:
			sn.pc_audio(ID=13)
		elif c.in_water > 0:
			sn.pc_audio(ID=10)
		else:
			sn.pc_audio(ID=2)
		obj_act(o)
	c.is_flip=False
	c.flip_anim=0
def ptf_up(p,c):
	if not c.freezed:
		c.freezed=True
		c.position=(p.x,c.y,p.z)
		c.rotation_y=0
	p.y+=time.dt/1.5
	if p.y >= p.start_y+3:
		p.catch_p=False
		p.y=p.start_y
		if str(p) == 'bonus_platform':
			load_bonus(c)
			return
		load_gem_route(c)
def jump_enemy(c,e):
	if (e.vnum in [2,9]) or (e.vnum == 5 and e.def_mode):
		get_damage(c,rsn=1)
		return
	kill_by_jump(m=e,c=c)
def jmp_lv_fin():
	if not st.LEVEL_CLEAN:
		status.LEVEL_CLEAN=True
		clear_level(passed=True)

## interface,collectables
def wumpa_count(n):
	sn.ui_audio(ID=2)
	invoke(lambda:sn.ui_audio(ID=1),delay=.5)
	if st.bonus_round:
		st.wumpa_bonus+=n
		return
	st.wumpa_fruits+=n
	st.show_wumpas=5
	sc_ps=LC.ACTOR.screen_position
	if st.wumpa_bonus <= 0 and not LC.ACTOR.aq_bonus:
		if n > 1:
			ui.WumpaCollectAnim(pos=(sc_ps[0],sc_ps[1]))
		ui.WumpaCollectAnim(pos=(sc_ps[0],sc_ps[1]+.1))
def give_extra_live():
	ui.live_get_anim()
	sn.ui_audio(ID=3)
	if st.bonus_round:
		st.lives_bonus+=1
	else:
		st.extra_lives+=1
		st.show_lives=5

## crate actions
def crate_set_val(cR,Cpos,Cpse):
	if cR.vnum == 15:
		cR.texture='res/crate/crate_t'+str(cR.time_stop)+'.png'
	else:
		cR.texture='res/crate/'+str(cR.vnum)+'.png'
	cR.org_tex=cR.texture
	cR.fall_down=False
	cR.is_stack=False
	cR.falling=False
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
def crate_action(e):
	A=LC.ACTOR
	if e.vnum in [7,8]:
		set_jump_type(A,typ=2)
		e.c_action()
		return
	if e.vnum != 14:
		if e.vnum == 3:
			set_jump_type(A,typ=3)
		else:
			set_jump_type(A,typ=1)
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
def crate_fall_state(co):
	invoke(lambda:setattr(co,'falling',False),delay=.2)
def check_crates_over(c):
	if c.vnum in [3,7,8]:
		return
	for co in scene.entities[:]:
		if is_crate(co) and (co.x == c.x and co.z == c.z) and co.is_stack:
			if co.y > c.y:
				co.falling=True
				co.animate_y(co.y-(co.scale_y*2),duration=.2)
				crate_fall_state(co)

## bonus level
def load_b_ui():
	ui.WumpaBonus()
	ui.CrateBonus()
	ui.LiveBonus()
def load_bonus(c):
	status.loading=True
	status.checkpoint=LC.bonus_checkpoint[st.level_index]
	collect_reset()
	if st.bonus_round:
		invoke(lambda:back_to_level(c),delay=.5)
		return
	invoke(lambda:enter_bonus(c),delay=.5)
def enter_bonus(c):
	ui.BlackScreen()
	status.bonus_round=True
	load_b_ui()
	status.day_mode='bonus'
	sn.BonusMusic(T=st.level_index)
	ui.BonusText()
	c.position=(0,-35,-3)
	camera.y=-35
	status.loading=False
	c.freezed=False
def back_to_level(c):
	ui.BlackScreen()
	if st.is_death_route:
		status.is_death_route=False
		status.gem_path_solved=True
	if st.bonus_round:
		status.bonus_round=False
		status.bonus_solved=True
	dMN=_loc.day_m
	st.day_mode=dMN[st.level_index]
	c.position=st.checkpoint
	c.freezed=False
	camera.y=c.y+.5
	status.loading=False

## gem route
def load_gem_route(c):
	status.loading=True
	if st.is_death_route:
		invoke(lambda:back_to_level(c),delay=.5)
		return
	invoke(lambda:load_droute(c),delay=.5)
def load_droute(c):
	ui.BlackScreen()
	if st.is_death_route:
		c.back_to_level(c)
		return
	status.is_death_route=True
	c.position=(200,1,-3)
	camera.position=(200,.5,-3)
	status.loading=False
	c.freezed=False
	sn.SpecialMusic(T=st.level_index)

## npc
def set_val_npc(m,tu,di,cm=True):
	if m.vnum in [3,7,8]:
		cm=False
	m.can_move=cm
	m.spawn_pos=m.position
	m.is_hitten=False
	m.fly_direc=None
	m.is_purge=False
	m.m_direction=di
	m.anim_frame=0
	m.unlit=False
	m.fly_time=0
	m.turn=tu
def npc_action(m):
	if m.is_purge:
		npc_purge(m)
		return
	if not m.is_hitten:
		if m.vnum in [10,11] and m.ro_mode > 0:
			ro_di={1:lambda:npc_circle_move_xz(m),2:lambda:npc_circle_move_y(m)}
			ro_di[m.ro_mode]()
		else:
			if m.vnum != 12:
				npc_walk(m)
		return
	fly_away(m)
def npc_purge(m):
	m.collider=None
	m.can_move=False
	m.fly_time=0
	m.scale_z=max(m.scale_z-time.dt/100,0)
	if m.scale_z <= 0 or m.is_hitten:
		status.NPC_RESET.append(m)
		purge_instance(m)
def npc_walk(m):
	if status.gproc():
		return
	if m.can_move:
		s=m.move_speed
		m_D=m.m_direction
		if m.m_direction == 0:
			if m.turn == 0:
				m.x+=time.dt*s
				if m.x >= m.spawn_pos[0]+1:
					m.rotation_y=90
					m.turn=1
			elif m.turn == 1:
				m.x-=time.dt*s
				if m.x <= m.spawn_pos[0]-1:
					m.rotation_y=270
					m.turn=0
			return
		if m.m_direction == 1:
			if m.turn == 0:
				m.z+=time.dt*s
				if m.z >= m.spawn_pos[2]+1:
					m.turn=1
					m.rotation_y=0
			elif m.turn == 1:
				m.z-=time.dt*s
				if m.z <= m.spawn_pos[2]-1:
					m.rotation_y=180
					m.turn=0
def npc_circle_move_xz(m):
	m.angle-=time.dt*2
	m.angle%=(2*math.pi)
	new_x=m.spawn_pos[0]-1*math.cos(m.angle)
	new_z=m.spawn_pos[2]-1*math.sin(m.angle)
	m.position=Vec3(new_x,m.y,new_z)
	rot=math.degrees(math.atan2(new_z-m.spawn_pos[2],new_x-m.spawn_pos[0]))
	m.rotation_y=-rot
def npc_circle_move_y(m):
	m.angle+=time.dt*2
	m.angle%=(2*math.pi)
	new_x=m.spawn_pos[0]+1.7*math.cos(m.angle)
	new_y=m.spawn_pos[1]+1.7*math.sin(m.angle)
	m.position=Vec3(new_x,new_y,m.z)
	rot=math.degrees(math.atan2(new_y-m.spawn_pos[1],new_x-m.spawn_pos[0]))
	m.rotation_x=rot
	m.rotation_y=-90
def rotate_to_crash(m):
	relative_position=LC.ACTOR.position-m.position
	angle=atan2(relative_position.x,relative_position.z)*(180/pi)+180
	m.rotation_y=angle
	m.rotation_x=-90
def fly_away(n):
	n.position+=n.fly_direc*time.dt*40
	n.fly_time+=time.dt
	if n.fly_time > .5:
		npc_purge(n)
		return
	if n.intersects():
		PNL=n.intersects().entity
		if is_crate(PNL):
			if PNL.vnum in [3,11]:
				PNL.empty_destroy()
			else:
				if PNL.vnum != 6:# avoid checkp accidentally
					PNL.destroy()
		if is_enemie(PNL):
			PNL.fly_direc=n.fly_direc
			PNL.is_hitten=True
			wumpa_count(1)
			npc_purge(n)
def kill_by_jump(m,c):
	m.is_purge=True
	set_jump_type(c,typ=1)
	sn.pc_audio(ID=5)
def is_enemie(n):
	nnk=[N.Amadillo,N.Turtle,N.SawTurtle,
		N.Penguin,N.Hedgehog,N.Seal,
		N.EatingPlant,N.Rat,N.Lizard,
		N.Eel,N.Scrubber,N.Mouse,N.SewerMine,
		N.Vulture,N.Hippo]
	if any(isinstance(n,npc_class) for npc_class in nnk):
		return True
	return False