from ursina import Entity,camera,scene,invoke,Vec3,color,distance,distance_xz,boxcast,raycast,window,load_texture
import ui,crate,item,status,sound,npc,settings,_loc,warproom,environment,time,random,json,math,objects
from effect import JumpDust,PressureWave,Fireball,ExclamationMark
from animation import NPCAnimator,BoxBreak,BoxAnimation
from math import atan2,sqrt,pi,sin,cos,radians,degrees
from ursina.ursinastuff import destroy
from danger import LandMine

kmw={7:5,15:7,16:8,17:6}
kpp=.3

level_ready=False
env=environment
st=status
sn=sound
LC=_loc

o=objects
C=crate
N=npc

## player
def set_val(c):
	for _v in {'aq_bonus','walking','jumping','landed','frst_lnd','is_landing','is_attack','is_flip','is_spin','warped','freezed','injured','b_smash','standup','falling','stun','is_slp','pushed','in_water','dth_block'}:
		setattr(c,_v,False)#flags
	for _a in {'frm','anim_idx','wksn','fall_time','slide_fwd','dth_cause','jmp_typ','space_time','crt_wait','sld_wait','atk_cooldown','atk_duration','air_time'}:
		setattr(c,_a,0)#values
	c.jmp_hgt={0:0.8, 1:1.0, 2:1.2, 3:1.5}
	c.jmp_pwr={0:4.0, 1:4.0, 2:6.0, 3:5.0}
	c.gravity={0:3.0, 1:3.9, 2:3.0, 3:3.1}
	c.move_speed=LC.dfsp
	c.direc=(0,0,0)
	c.indoor=.5
	c.vpos=c.y
	c.CMS=3
	LC.ACTOR=c
	if st.level_index == 8:
		c.color=color.dark_gray
	del _a,_v
def get_damage(c,rsn):
	if st.aku_hit > 2 or settings.debg_gm:
		return
	if not (c.injured or st.death_event):
		if st.aku_hit > 0:
			st.aku_hit-=1
			c.injured=True
			c.hurt_visual()
			sn.pc_audio(ID=21)
			sn.pc_audio(ID=6,pit=.8)
			invoke(lambda:setattr(c,'injured',False),delay=2)
			invoke(lambda:setattr(c,'alpha',1),delay=2)
			return
		dth_event(c,rsn=rsn)
def hurt_blink(c):
	c.visible=False
	invoke(lambda:setattr(c,'visible',True),delay=.2)
def dth_event(c,rsn):
	if not st.death_event:
		if rsn == 1:
			sn.pc_audio(ID=14,pit=.8)
		else:
			sn.pc_audio(ID=7,pit=.8)
		st.death_event=True
		c.freezed=True
		c.dth_cause=rsn
	del rsn,c
def reset_state(c):
	ui.BlackScreen()
	st.crate_count-=st.crate_to_sv
	if st.relic_challange:
		st.relic_challange=False
		st.level_relic_time=0
		item.TimeTrialClock(pos=LC.CLOCK_POSITION[st.level_index])
	if st.death_route and st.checkpoint[0] < 198.5:
		st.death_route=False
		sn.BackgroundMusic(m=0)
	if st.bonus_round:
		st.wumpa_bonus=0
		st.crate_bonus=0
		st.lives_bonus=0
		st.bonus_round=False
		sn.BackgroundMusic(m=0)
	else:
		if not (settings.debg_gm or st.relic_challange):
			st.extra_lives-=1
		st.fails+=1
		if st.level_index == 2:
			st.gem_death=True
	if st.extra_lives < 0:
		st.game_over=True
		game_over()
		return
	st.aku_hit=0
	if st.fails > 2:
		st.aku_hit=1
		if not st.aku_exist:
			sn.crate_audio(ID=12,pit=1.2)
			npc.AkuAkuMask(pos=(c.x,c.y,c.z))
	purge_wumpa()
	reset_crates()
	reset_wumpas()
	reset_npc()
	if st.level_index == 6:
		reset_mines()
	c.position=status.checkpoint
	env.set_fog()
	camera.position=c.position
	camera.rotation=(15,0,0)
	c.dth_block=False
	c.is_slp=False
	c.in_water=False
	st.death_event=False
	c.visible=True
	c.stun=False
	invoke(lambda:setattr(c,'freezed',False),delay=3)
def c_anim_flag(n):
	if n == 5:
		LC.ACTOR.is_spin=False
	if n == 6:
		LC.ACTOR.is_landing=False
	if n == 8:
		LC.ACTOR.is_flip=False
	if n == 10:
		LC.ACTOR.standup=True
		LC.ACTOR.b_smash=False
	if n == 11:
		LC.ACTOR.is_landing=False
		LC.ACTOR.standup=False
	if n == 12:
		LC.ACTOR.stun=False
	if n == 13:
		LC.ACTOR.pushed=False
def various_val(c):
	st.show_gems=max(st.show_gems-time.dt,0)
	c.crt_wait=max(c.crt_wait-time.dt,0)
	c.sld_wait=max(c.sld_wait-time.dt,0)
	c.indoor=max(c.indoor-time.dt,0)
	st.wu_sn=max(st.wu_sn-time.dt,0)
	st.br_sn=max(st.br_sn-time.dt,0)
	st.ex_sn=max(st.ex_sn-time.dt,0)
	st.ni_sn=max(st.ni_sn-time.dt,0)
	c.air_time=c.air_time+time.dt if not c.landed else 0
	if not c.is_attack and c.atk_cooldown > 0:
		c.atk_cooldown=max(c.atk_cooldown-time.dt,0)
	c.atk_duration=max(c.atk_duration-time.dt,0)
	if c.atk_duration <= 0:
		c.is_attack=False
	if c.falling and c.fall_time > .3:
		c.frst_lnd=True
	if not c.is_slp:
		c.move_speed=LC.dfsp
	if st.bonus_solved and not st.wait_screen:
		c.aq_bonus=bool(st.wumpa_bonus > 0 or st.crate_bonus > 0 or st.lives_bonus > 0)
def c_slide(c):
	if not c.walking:
		if c.slide_fwd > 0 and st.p_last_direc:
			if c.move_speed > 0:
				c.move_speed=max(c.move_speed-time.dt,0)
			c.position+=st.p_last_direc*time.dt*c.slide_fwd
			c.slide_fwd-=time.dt
			if c.sld_wait <= 0:
				c.sld_wait=.5
				if not c.jumping:
					sn.pc_audio(ID=9)
			if c.slide_fwd <= 0:
				c.slide_fwd=0
				st.p_last_direc=None
		return
	c.is_landing=False
	c.move_speed=min(c.move_speed+time.dt/2,3)
	if c.move_speed > 0:
		c.slide_fwd=c.move_speed
def c_spin(c):
	for qd in scene.entities[:]:
		if not qd or not qd.collider:
			continue
		if distance_xz(c,qd) < .5 and abs(c.y-qd.y) < .4:
			if is_box(qd) and qd.vnum != 13:
				if qd.vnum in (3,11):
					qd.empty_destroy()
				else:
					qd.destroy()
			if is_enemie(qd):
				if not (qd.is_purge or qd.is_hitten):
					if qd.vnum in (1,11) or (qd.vnum == 5 and qd.def_mode):
						get_damage(c,rsn=2)
						return
					if qd.vnum == 17 and qd.ro_mode == 0:
						get_damage(c,rsn=6)
						return
					if qd.vnum != 13:
						bash_enemie(qd,c)
	del qd
def c_smash(c):
	for sw in scene.entities:
		if not sw or not sw.collider:
			continue
		if (is_box(sw) or is_enemie(sw)) and bool(distance(c.position,sw.position) < .4 and sw.collider):
			if is_box(sw):
				if sw.vnum in (3,11):
					sw.empty_destroy()
				if sw.vnum == 14:
					sw.c_destroy()
				else:
					sw.destroy()
			if is_enemie(sw) and sw.vnum != 13:
				sw.is_purge=True
	del sw
def c_bounce(c):
	if c.vnum == 8 and LC.ACTOR.b_smash:
		LC.ACTOR.b_smash=False
	LC.ACTOR.is_flip=False
	LC.ACTOR.jump_typ(2 if (c.vnum == 3) else 3)
	if c.vnum == 3:
		c.destroy()
	else:
		sn.crate_audio(ID=4)
	BoxAnimation(c)
def c_shield():
	if st.aku_hit < 3:
		return
	for rf in scene.entities:
		if rf and rf.collider:
			if distance(rf,LC.ACTOR) < 1.5:
				if rf.name in LC.item_lst:
					rf.collect()
					sn.pc_audio(ID=21)
				if is_enemie(rf):
					bash_enemie(rf,LC.ACTOR)
				if is_box(rf) and not rf.vnum in (0,8,13):
					if rf.vnum == 14:
						rf.c_destroy()
					if not (rf.vnum in (9,10) and rf.active):
						rf.destroy()
					if rf.vnum in (3,11):
						rf.empty_destroy()

## camera actor
def cam_indoor(c):
	ftt=time.dt*2
	cm=camera
	cm.fov=lerp(cm.fov,57.5,ftt)
	cm.z=lerp(cm.z,c.z-3,ftt)
	cm.x=lerp(cm.x,c.x,ftt)
	cm.rotation_x=lerp(cm.rotation_x,14,ftt)
	if c.landed and c.walking:
		cm.y=lerp(cm.y,c.y+1,ftt)
def cam_level(c):
	ftt=time.dt
	cm=camera
	cm.z=lerp(cm.z,c.z-c.CMS,ftt*3)
	cm.x=lerp(cm.x,c.x,ftt*2.5)
	camera.fov=cm.fov=lerp(cm.fov,64,ftt)
	if c.jumping or c.falling:
		if cm.rotation_x > 20:
			cm.rotation_x=lerp(cm.rotation_x,c.y,ftt/5)
		return
	if c.landed and not (c.jumping or c.freezed):
		cm.rotation_x=lerp(cm.rotation_x,25,ftt)
		cm.y=lerp(cm.y,c.y+1.8,time.dt*2)
def cam_bonus(c):
	ftt=time.dt*3
	camera.z=(c.z-3.2)
	camera.x=lerp(camera.x,c.x,ftt)
	camera.y=lerp(camera.y,c.y+1.4,time.dt*1.5)
	camera.rotation_x=15

## world, misc
def spawn_level_crystal(idx):
	if idx > 5 or idx == 0:
		return
	item.EnergyCrystal(pos={1:(0,1.5,-13),2:(35.5,6.4,28.5),3:(0,2.5,60.5),4:(14,4.25,66),5:(12,.8,-7)}[idx])
def spawn_trial_clock(idx):
	if check_best_relic(idx):
		return
	if idx in st.CRYSTAL or idx > 5:
		item.TimeTrialClock(pos=LC.CLOCK_POSITION[idx])
def spawn_color_gem(idx):
	if idx == st.DEV_LEVEL_INDEX:
		return
	cgem_pos=LC.gem_pod_position
	if idx == 4:
		cgem_pos=(200,0,28.9)
	if idx == 5:
		cgem_pos=(194.4,-2,37.7)
	item.GemStone(pos=cgem_pos,c=idx)
def collect_reset():
	st.BOX_RESET.clear()
	st.WMP_RESET.clear()
	st.crate_to_sv=0
	st.fails=0
	if level_ready:
		st.NPC_RESET.clear()
def c_subtract(cY):
	if cY < -20:
		st.crates_in_bonus-=1
	st.crates_in_level-=1
def reset_crates():
	for sr in scene.entities[:]:
		if not sr:
			continue
		if is_box(sr):
			if sr.poly or sr.vnum == 15:
				sr.enabled=False
				destroy(sr)
			else:
				sr.position=sr.spawn_pos
	del sr
	if len(st.SWI_RESET) > 0:
		for ssw in st.SWI_RESET[:]:
			ssw.c_reset()
		del ssw
	if len(st.BOX_RESET) > 0:
		for cv in st.BOX_RESET[:]:
			if not (cv[0] == 13 and cv[4] == 0) and not (cv[0] == 16):
				c_subtract(cY=cv[1][1])
			C.spawn(ID=cv[0],p=cv[1],pse=cv[2],m=cv[3],l=cv[4])
		del cv
	st.BOX_RESET.clear()
	st.SWI_RESET.clear()
	check_nitro_stack()
	st.crate_to_sv=0
def reset_wumpas():
	for wres in st.WMP_RESET[:]:
		item.WumpaFruit(p=wres,c_prg=False)
	st.WMP_RESET.clear()
def reset_npc():
	if len(st.NPC_RESET) > 0:
		for NP in st.NPC_RESET[:]:
			npc.spawn(ID=NP[0],POS=NP[1],DRC=NP[2],RNG=NP[3],RTYP=NP[4],CMV=NP[5])
		del NP
	st.NPC_RESET.clear()
def jmp_lv_fin():
	if not st.LEVEL_CLEAN:
		destroy(LC.ACTOR)
		st.LEVEL_CLEAN=True
		clear_level(passed=True)
def clear_level(passed):
	st.LV_CLEAR_PROCESS=True
	scene.clear()
	if passed:
		window.color=color.gray
		collect_rewards()
		ui.WhiteScreen()
		return
	st.loading=True
	delete_states()
	invoke(lambda:warproom.level_select(),delay=3)
def delete_states():
	st.color_gem_id=None
	unload_textures(st.level_index)
	st.level_index=0
	st.crates_in_bonus=0
	st.crates_in_level=0
	st.level_relic_time=0
	st.wumpas_in_level=0
	st.npc_in_level=0
	st.crate_bonus=0
	st.crate_count=0
	st.crate_to_sv=0
	st.fails=0
	st.aku_inv_time=20
	if st.aku_hit > 2:
		st.aku_hit=2
	st.NPC_RESET.clear()
	st.WMP_RESET.clear()
	st.BOX_RESET.clear()
	st.SWI_RESET.clear()
	st.is_invincible=False
	st.level_crystal=False
	st.level_col_gem=False
	st.level_cle_gem=False
	st.RELIC_TRIAL_DONE=False
	st.relic_challange=False
	st.gem_path_solved=False
	st.death_route=False
	st.bonus_solved=False
	st.bonus_round=False
	st.LEVEL_CLEAN=False
	st.death_event=False
	st.gem_death=False
	st.pause=False
	level_ready=False
	LC.IGNORE.clear()
def collect_rewards():
	cdx=st.level_index
	if st.level_crystal:
		if not cdx in st.CRYSTAL:
			st.CRYSTAL.append(cdx)
	if st.level_cle_gem:
		if not cdx in st.CLEAR_GEM:
			st.CLEAR_GEM.append(cdx)
	if st.relic_challange:
		jtv=(st.level_index,st.relic_rank)
		if not jtv in st.RELIC:
			st.RELIC.append(jtv)
	if st.level_col_gem:
		if st.level_index != 9:
			if st.color_gem_id != st.DEV_LEVEL_INDEX:
				if not st.color_gem_id in st.COLOR_GEM:
					st.COLOR_GEM.append(st.color_gem_id)
	delete_states()
	invoke(lambda:warproom.level_select(),delay=2)
def destroy_entity(v):
	if isinstance(v,N.AkuAkuMask):
		st.aku_exist=False
	v.visible=False
	v.enabled=False
	scene.entities.remove(v)
	destroy(v)
	del v
def game_pause():
	st.pause=not st.pause
def game_over():
	invoke(lambda:ui.GameOverScreen(),delay=2)
def is_obj_scene(o):
	return (hasattr(o,'idf') and o.idf == 'mo')
def purge_wumpa():
	for wf in scene.entities[:]:
		if wf:
			if (isinstance(wf,item.WumpaFruit) and wf.c_purge):
				wf.destroy()
def gem_challange_fail(gemID):
	if gemID == 1 and (st.level_index == 1 and st.crate_count > 0):#blue gem
		return True
	if gemID == 2 and (st.level_index == 2 and st.gem_death):#red gem
		return True
	if gemID == 3 and (st.level_index == 3 and st.gem_death):#yellow gem
		return True
	return False
def refresh_relic_rank(idx):
	relic_time_limit=LC.RELIC_TIME_LIMIT_LEVEL[idx]
	if st.level_relic_time <= relic_time_limit[0]:
		return 0
	if st.level_relic_time > relic_time_limit[0] and st.level_relic_time < relic_time_limit[2]:
		return 1
	return 2
def check_best_relic(idx):
	for lpr in st.RELIC:
		if idx == lpr[0]:
			if lpr[1] == 0:
				return True
		return False

## collisions
def check_ceiling(c):
	vc=c.intersects(ignore=LC.IGNORE)
	ve=vc.entity
	if ve and ve.collider:
		if vc.normal == Vec3(0,-1,0):
			if not ve.name in LC.item_lst|LC.trigger_lst:
				if is_box(ve):
					if c.crt_wait <= 0:
						c.crt_wait=.1
						ve.destroy()
						if ve.vnum == 3:
							BoxAnimation(ve)
				c.y=c.y
				c.jumping=False
def check_floor(c):
	fwd_drc=Vec3(-sin(radians(c.rotation_y))*.05,0,-cos(radians(c.rotation_y))*.05)
	vj=boxcast(Vec3(c.x,c.y,c.z)+fwd_drc,Vec3(0,1,0),distance=.01,thickness=(.12,.12),ignore=LC.IGNORE,debug=settings.debg)
	stm=bool(vj.hit and vj.normal) and not (vj.entity.name in LC.item_lst|LC.dangers|LC.trigger_lst)
	c.falling=bool(not stm)
	c.landed=stm
	if stm:
		c.y=vj.world_point.y
		if c.frst_lnd:
			c.frst_lnd=False
			land_act(c,vj.entity)
		if bool(vj.entity and vj.entity.collider):
			spc_floor(vj.entity)
		c.fall_time=0
		return
	c.y=c.y-time.dt*6 if c.b_smash else c.y-time.dt*c.gravity[c.jmp_typ]
	c.fall_time=min(c.fall_time+time.dt,1)
def land_act(c,vp):
	c.stun=False
	c.space_time=0
	sn.landing_sound(vp)
	c.anim_land()
	if is_box(vp):
		if LC.ACTOR.fall_time > .01:
			box_jump_action(vp)
		return
	if is_enemie(vp):
		npc_jump_action(vp)
		return
	if c.b_smash:
		PressureWave(pos=c.position,col=color.light_gray)
def spc_floor(e):
	if not e.name:
		del e
		return
	LC.ACTOR.is_slp=(e.name == 'obj_type__floor' and e.vnum == 0)
	if e.name in ('bnpt','gmpt'):
		ptf_up(e,LC.ACTOR)
		return
	if e.name in ('swpt','HPP','epad'):
		e.active=True
		return
	if (e.name == 'plnk' and e.typ == 1) or e.name == 'loos':
		e.pl_touch()
		return
	if (e.name == 'obj_type__deco' and e.vnum == 4):
		get_damage(LC.ACTOR,rsn=2)
		return
	if (e.name == 'swpi' and e.typ == 3) or (e.name == 'labt' and e.danger):
		get_damage(LC.ACTOR,rsn=4)
		return
	if e.name == 'wtrh':
		dth_event(LC.ACTOR,rsn=3)
		return
	if e.name in ('mptf','lbbt') and not (LC.ACTOR.walking or LC.ACTOR.jumping):
		e.mv_player()
def ptf_up(e,c):
	if not c.freezed:
		c.freezed=True
		c.position=(e.x,c.y,e.z)
		c.rotation_y=0
	e.y+=time.dt/1.5
	if e.y > e.start_y+3:
		e.y=e.start_y
		{'bnpt':lambda:load_bonus(c),'gmpt':lambda:load_gem_route(c)}[e.name]()
def wall_hit_walk(c):
	if c.stun or c.b_smash or c.pushed or st.p_rst(c):
		return
	mc=raycast(c.world_position+(0,.2,0),c.direc,distance=.25,ignore=LC.IGNORE,debug=settings.debg)
	c.rotation_y=atan2(-c.direc.x,-c.direc.z)*180/math.pi
	st.p_last_direc=c.direc
	c.walk_event()
	if not mc or str(mc.entity) in LC.item_lst|LC.trigger_lst:
		c.position+=c.direc*(time.dt*c.move_speed)
	if mc and is_box(mc.entity) and mc.entity.vnum == 12:
		mc.entity.destroy()
def wall_hit_idle(c):
	hT=c.intersects(ignore=LC.IGNORE,debug=settings.debg)
	if hT:
		if hT.entity.name in LC.item_lst:
			hT.entity.collect()
			return
		if hT.entity.name == 'fthr':
			get_damage(LC.ACTOR,rsn=4)
			return
		if hT.entity.name in LC.trigger_lst:
			return
		if not hT.normal in (Vec3(0,-1,0),Vec3(0,1,0)):
			c.position+=hT.world_normal*(time.dt*c.move_speed)
			if hT.entity.collider:
				if is_box(hT.entity) and hT.entity.vnum == 12:
					hT.entity.destroy()
					return
				if is_enemie(hT.entity) and not (hT.entity.is_purge or hT.entity.is_hitten):
					RS=kmw[hT.entity.vnum] if hT.entity.vnum in kmw else 2
					if not LC.ACTOR.is_attack:
						get_damage(LC.ACTOR,rsn=RS)

## interface,collectables
def wumpa_count(n):
	if st.wu_sn <= 0:
		st.wu_sn=.1
		sn.ui_audio(ID=2)
		invoke(lambda:sn.ui_audio(ID=1),delay=.5)
	if st.bonus_round:
		st.wumpa_bonus+=n
	else:
		st.wumpa_fruits+=n
		st.show_wumpas=5
	sc_ps=LC.ACTOR.screen_position
	if not LC.ACTOR.aq_bonus:
		if n > 1:
			ui.WumpaCollectAnim(pos=(sc_ps[0],sc_ps[1]))
		ui.WumpaCollectAnim(pos=(sc_ps[0],sc_ps[1]+.1))
def give_extra_live():
	sn.ui_audio(ID=3)
	if st.bonus_round:
		st.lives_bonus+=1
		return
	if st.extra_lives < 99:
		st.extra_lives+=1
	ui.LiveCollectAnim()
	st.show_lives=5
def show_status_ui():
	st.show_wumpas=5
	if not st.relic_challange:
		st.show_crates=5
		st.show_lives=5
	st.show_gems=5

## crate actions
def box_set_val(cR,Cpos,Cpse,Cmk,Ctl):
	cR.idf='cr'
	cR.texture=f'res/crate/15_t{cR.time_stop}.png' if (cR.vnum == 15) else f'res/crate/{cR.vnum}.png'
	cR.org_tex=cR.texture if (cR.vnum in (9,10)) else None
	cR.spawn_pos=Cpos
	cR.position=Cpos
	cR.collider='box'
	cR.c_fall=False
	cR.poly=Cpse
	cR.c_ID=Ctl
	cR.mark=Cmk
	cR.scale=.16
	if st.level_index == 8 and cR.vnum != 12:
		cR.color=color.dark_gray
		cR.unlit=False
	del cR,Cpos,Cpse,Ctl,Cmk
def box_stack(c_pos):
	sdi=0
	for wm in scene.entities:
		if (is_box(wm) and not wm.vnum in (3,13)) and (wm.x == c_pos[0] and wm.z == c_pos[2]):
			if (wm.y > c_pos[1]) and abs(wm.y-c_pos[1]) <= sdi*.32:
				if wm.vnum == 12:
					wm.new_y-=.32
				wm.c_fall=True
				box_move(wm)
		sdi+=1
	del wm
def box_move(c):
	c.animate_y(c.y-.32,duration=.2)
	invoke(lambda:setattr(c,'c_fall',False),delay=.25)
def check_nitro_stack():
	nitro_boxes=[e for e in scene.entities if (is_box(e) and e.vnum == 12)]
	if len(nitro_boxes) > 0:
		for np in nitro_boxes:
			box_above=False
			for op in scene.entities[:]:
				if not is_box(op) or op is np:
					continue
				if np.x == op.x and np.z == op.z:
					if op.y > np.y:
						box_above=True
						break
			if not box_above:
				np.can_jmp=True
def block_destroy(c):
	if not c.p_snd:
		c.p_snd=True
		if c.vnum == 14:
			BoxAnimation(c)
			sn.crate_audio(ID=1)
		else:
			if LC.ACTOR.is_attack:
				sn.crate_audio(ID=0)
		invoke(lambda:setattr(c,'p_snd',False),delay=.5)
def box_jump_action(c):
	if (c.vnum in (9,10,11) and c.active) or c.vnum == 0:
		return
	if c.vnum in (3,7,8):
		c_bounce(c)
		return
	if c.vnum != 14:
		LC.ACTOR.jump_typ(1)
	c.destroy()
def box_destroy_event(c):
	if c.c_fall or not c:
		return
	c.collider=None
	if c.vnum in (11,12):
		explosion(c)
	if not (c.poly or st.relic_challange):
		st.BOX_RESET.append((c.vnum,c.spawn_pos,c.poly,c.mark,c.c_ID))
	if c.vnum != 13:
		if c.visible:
			BoxBreak(c.position,c.vnum)
		if st.bonus_round:
			st.crate_bonus+=1
		else:
			if not (c.vnum in (15,16) or st.relic_challange):
				st.crate_to_sv+=1
				st.crate_count+=1
				st.show_crates=5
		box_stack(c.position)
	destroy_entity(c)
def is_box(e):
	return bool(hasattr(e,'idf') and e.idf == 'cr')
def explosion(c):
	if c.visible:
		Fireball(c)
	if c.vnum == 11:
		sn.crate_audio(ID=9)
	if c.vnum == 12:
		sn.crate_audio(ID=10,pit=2.05)
		invoke(lambda:sn.crate_audio(ID=9),delay=.075)
	for nbc in scene.entities[:]:
		if not nbc or not nbc.collider:
			continue
		if distance(c,nbc) < 1:
			if is_box(nbc) and nbc.vnum != 6:
				if nbc.vnum in (3,11):
					nbc.empty_destroy()
				else:
					nbc.destroy()
			if is_enemie(nbc) and not nbc.is_hitten:
				bash_enemie(nbc,c)
			if nbc == LC.ACTOR:
				get_damage(LC.ACTOR,rsn=4)
	del c,nbc
def spawn_ico(cr_pos):
	for exm in range(5):
		ExclamationMark(pos=cr_pos,ID=exm)
	del exm,cr_pos

class AirBoxReplacer(Entity):
	def __init__(self,mark):
		s=self
		s.AB_ID=mark
		super().__init__()
		s.air_box_list=[abx for abx in scene.entities if (isinstance(abx,C.Air) and abx.mark == s.AB_ID)]
		s.index=0
		s.tme=0
		if len(s.air_box_list) <= 0:
			destroy(s)
	def switch_boxes(self):
		s=self
		s.tme+=time.dt
		if s.tme >= .2:
			s.tme=0
			if s.index >= len(s.air_box_list):
				s.air_box_list.clear()
				destroy(s)
				return
			tbox=s.air_box_list[s.index]
			if tbox and tbox.enabled:
				tbox.destroy()
			s.index+=1
	def update(self):
		if st.gproc():
			return
		s=self
		if st.death_event:
			destroy(s)
			return
		s.switch_boxes()

## bonus level
def load_b_ui():
	ui.WumpaBonus()
	ui.BoxBonus()
	ui.LiveBonus()
def load_bonus(c):
	st.loading=True
	st.checkpoint=LC.bonus_checkp[st.level_index]
	collect_reset()
	if st.bonus_round:
		invoke(lambda:back_to_level(c),delay=.5)
		return
	invoke(lambda:enter_bonus(c),delay=.5)
def enter_bonus(c):
	ui.BlackScreen()
	st.bonus_round=True
	load_b_ui()
	sn.BackgroundMusic(m=1)
	ui.BonusText()
	c.position=(0,-35,-3)
	env.set_fog()
	camera.y=-35
	st.loading,c.freezed=False,False
def clear_bonus():
	for brd in scene.entities[:]:
		if brd and brd.y < -15:
			if isinstance(brd,(o.ObjType_Block,o.ObjType_Wall,o.ObjType_Water)):
				destroy(brd)
	del brd
def back_to_level(c):
	ui.BlackScreen()
	c.position=st.checkpoint
	if st.death_route:
		st.death_route=False
		st.gem_path_solved=True
		clear_gem_route()
	if st.bonus_round:
		st.bonus_round=False
		st.bonus_solved=True
		clear_bonus()
	c.freezed=False
	sn.BackgroundMusic(m=0)
	env.set_fog()
	camera.y=c.y+.5
	st.loading=False

## gem route
def load_gem_route(c):
	st.loading=True
	if st.death_route:
		invoke(lambda:back_to_level(c),delay=.5)
		return
	invoke(lambda:load_droute(c),delay=.5)
def load_droute(c):
	ui.BlackScreen()
	if st.death_route:
		c.back_to_level(c)
		return
	st.death_route=True
	c.position=(200,2.3,-3)
	sn.BackgroundMusic(m=2)
	camera.position=(200,.5,-3)
	st.loading,c.freezed=False,False
def clear_gem_route():
	for grd in scene.entities[:]:
		if grd.parent == scene and grd.x > 180:
			if not (is_box(grd) or grd in (LC.shdw,LC.ACTOR) or isinstance(grd,N.AkuAkuMask) or grd.name == 'firefly' or grd.name == 'point_light'):
				destroy(grd)
	del grd

## npc
di={0:'x',1:'y',2:'z'}
npf='res/npc/'
def set_val_npc(m,drc=None,rng=None,rtyp=0,cmv=True,typ=0):
	m.idf='np'
	m.anim_frame=0
	m.fly_time=0
	m.turn=0
	m.is_hitten,m.is_purge=False,False
	m.is_defeated=False
	m.spawn_pos=m.position
	m.fly_direc=None
	m.mov_range=rng
	m.mov_direc=drc
	m.can_move=cmv
	m.ro_mode=rtyp
	m.typ=typ
	if rtyp > 0:
		m.angle=rng
	m.rotation_x=-90
	m.scale=.8/1200
	vnn=f'{m.name}/{typ}' if m.vnum == 17 else m.name
	m.model=f'{npf}{vnn}/0.ply'
	m.texture=f'{npf}{vnn}/0.png'
	m.collider.visible=settings.debg
	if st.level_index == 8:
		m.color=color.dark_gray
		m.unlit=False
	del m,drc,rng,vnn,cmv,rtyp,typ
def npc_walk(m):
	pdv={0:m.spawn_pos[0],1:m.spawn_pos[1],2:m.spawn_pos[2]}
	mm=m.mov_direc
	mt=m.turn
	ox=m.x
	oz=m.z
	step=time.dt*m.move_speed
	kv=getattr(m,di[mm])
	if mt == 0:
		setattr(m,di[mm],kv+step)
	else:
		setattr(m,di[mm],kv-step)
	if (mt == 0 and kv >= pdv[mm]+m.mov_range) or (mt == 1 and kv <= pdv[mm]-m.mov_range):
		m.turn=1 if mt == 0 else 0
	m.rotation_y=degrees(atan2(m.x-ox,m.z-oz))+180
def circle_move(m):
	if m.ro_mode == 1:
		m.angle-=time.dt*m.move_speed
		m.angle%=(2*math.pi)
		new_x=m.spawn_pos[0]-m.mov_range*math.cos(m.angle)
		new_z=m.spawn_pos[2]-m.mov_range*math.sin(m.angle)
		m.position=Vec3(new_x,m.y,new_z)
		rot=math.degrees(math.atan2(new_z-m.spawn_pos[2],new_x-m.spawn_pos[0]))
		m.rotation_y=-rot
		return
	m.angle+=time.dt*m.move_speed
	m.angle%=(2*math.pi)
	new_x=m.spawn_pos[0]+m.mov_range*math.cos(m.angle)
	new_y=m.spawn_pos[1]+m.mov_range*math.sin(m.angle)
	m.position=Vec3(new_x,new_y,m.z)
	rot=math.degrees(math.atan2(new_y-m.spawn_pos[1],new_x-m.spawn_pos[0]))
	m.rotation_x=rot
	m.rotation_y=-90
def refresh_npc_function(m):
	if m.is_hitten:
		fly_away(m)
		return
	if m.is_purge:
		JumpDust(m.position)
		npc_destroy_event(m)
		return
	if not m.can_move:
		if distance(m,LC.ACTOR) < 3:
			rotate_to_target(m,LC.ACTOR.position)
		return
	if m.ro_mode > 0:
		circle_move(m)
		return
	npc_walk(m)
def rotate_to_target(m,target_pos):
	rtp=(target_pos-m.position)
	m.rotation_y=atan2(rtp.x,rtp.z)*(180/pi)+180
	m.rotation_x=-90
def fly_away(n):
	n.position+=n.fly_direc*(time.dt*LC.NPC_FLY_SPEED)
	n.fly_time+=time.dt
	npc_fly_hit(n)
	if n.fly_time > .5:
		npc_destroy_event(n)
def npc_fly_hit(n):
	for nh in scene.entities:
		if not nh or not nh.collider or n is nh:
			continue
		if is_box(nh) and nh.vnum != 6:
			if distance(n,nh) < .3:
				if nh.vnum in (3,11):
					nh.empty_destroy()
				else:
					nh.destroy()
		if is_enemie(nh) and not nh.is_hitten:
			if distance(n,nh) < .3:
				nh.is_purge=True
				wumpa_count(1)
	del nh
def is_enemie(n):
	return bool(hasattr(n,'idf') and n.idf == 'np')
def bash_enemie(e,h):
	e.is_hitten=True
	e.fly_direc=Vec3(e.x-h.x,0,e.z-h.z)
	sn.pc_audio(ID=17)
def npc_pathfinding(m):
	if m.way_index < len(m.ffly_drc):
		ddrc=(Vec3(m.ffly_drc[m.way_index])-m.position).normalized()
		m.position+=ddrc*(time.dt*m.follow_speed)
		if distance(Vec3(m.position),m.ffly_drc[m.way_index]) < .3:
			m.way_index+=1
		return
	if m.name == 'boulder':
		if not m.is_done:
			m.is_done=True
			m.path_fin()
def npc_jump_action(m):
	if not (m.is_hitten or m.is_purge):
		if m.vnum in (2,9,13) or (m.vnum == 5 and m.def_mode):
			get_damage(LC.ACTOR,rsn=2)
		m.is_purge=bool(m.vnum != 13)
		LC.ACTOR.jump_typ(1)
def npc_destroy_event(m):
	if m.vnum in (14,19):
		NPCAnimator(ID=m.vnum,pos=m.position,sca=m.scale,rot=m.rotation,max_frm=m.max_frm,col=m.color)
	m.collider=None
	MW=True if getattr(m,'can_move',True) else False
	RW=m.ro_mode if (hasattr(m,'ro_mode') and m.ro_mode > 0) else 0
	st.NPC_RESET.append((m.vnum,m.spawn_pos,m.mov_direc,m.mov_range,RW,MW))
	m.visible=False
	m.enabled=False
	scene.entities.remove(m)
	destroy(m)
	del m,MW,RW

## game progress
save_file='savegame.json'
def save_game():
	save_data={
		'SV_WU':st.wumpa_fruits,#wumpa fruits
		'SV_LF':st.extra_lives,#extra lives
		'SV_AK':st.aku_hit,#aku mask
		'LS_CR':st.CRYSTAL,#Lv ID crystal
		'LS_CL':st.CLEAR_GEM,#Lv ID clear gem
		'LS_CG':st.COLOR_GEM,#Color Gem ID
		'LS_RL':st.RELIC,#time relic
		'M_IDX':st.WARP_ROOM_MUSIC,
		'M_VOL':settings.MUSIC_VOLUME,
		'S_VOL':settings.SFX_VOLUME,
		'CRD_W':st.crd_seen}
	with open(save_file,'w') as f:
		json.dump(save_data,f)
def load_game():
	with open(save_file,'r') as f:
		save_data=json.load(f)
	st.wumpa_fruits=save_data['SV_WU']
	st.extra_lives=save_data['SV_LF']
	st.aku_hit=save_data['SV_AK']
	st.CRYSTAL=[(x) for x in save_data['LS_CR']]
	st.WARP_ROOM_MUSIC=save_data['M_IDX']
	st.RELIC=[(x) for x in save_data['LS_RL']]
	st.CLEAR_GEM=[(x) for x in save_data['LS_CL']]
	st.COLOR_GEM=[(x) for x in save_data['LS_CG']]
	settings.SFX_VOLUME=save_data['S_VOL']
	settings.MUSIC_VOLUME=save_data['M_VOL']
	st.crd_seen=save_data['CRD_W']

##entity-frames+ : ENTITY/FRAME_COUNT/SPEED
def incr_frm(o,sp):
	o.frm=min(o.frm+time.dt*sp,o.max_frm)
	if o.frm >= o.max_frm:
		o.frm=0

def reset_mines():
	for rsm in LC.LDM_POS[:]:
		LandMine(pos=rsm)
	LC.LDM_POS.clear()

##preload animation
def preload_animator():
	print('test')

##preload global texture
def preload_ui_texture():
	LC.wmp_texture=[load_texture(f'res/ui/icon/wumpa/w{cbx}.png') for cbx in range(13+1)]
	LC.box_texture=[load_texture(f'res/ui/icon/box/anim_crt_{cbx}.png') for cbx in range(63+1)]
	LC.crystal_texture=[load_texture(f'res/ui/icon/crystal/{cbx}.png') for cbx in range(32+1)]
	LC.normal_gem_texture=[load_texture(f'res/ui/icon/gem0/{cbx}.png') for cbx in range(64+1)]
	LC.green_gem_texture=[load_texture(f'res/ui/icon/gem1/{cbx}.png') for cbx in range(64+1)]
	LC.purple_gem_texture=[load_texture(f'res/ui/icon/gem2/{cbx}.png') for cbx in range(64+1)]
	LC.relic_texture=[load_texture(f'res/ui/icon/relic/{cbx}.png') for cbx in range(16+1)]
def preload_water_texture(ID):
	if len(LC.wtr_texture) > 0:
		LC.wtr_texture.clear()
	if ID == 0:
		LC.wtr_texture=[load_texture(f'res/objects/ev/wtr/{cbx}.png') for cbx in range(31+1)]
	if ID == 1:
		LC.wtr_texture=[load_texture(f'res/objects/l3/water_flow/water_flow{cbx}.png') for cbx in range(3+1)]
	if ID == 2:
		LC.wtr_texture='res/objects/l8/polar_water/0.png'
def unload_textures(idx):
	if settings.debg:
		print('depending object textures unloaded')
	if idx == 3:
		LC.wtf_texture.clear()
		LC.wff_texture.clear()
	if idx == 4:
		LC.drp_texture.clear()
	if idx == 5:
		LC.fre_texture.clear()