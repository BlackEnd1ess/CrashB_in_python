import ui,crate,item,status,sound,npc,settings,_loc,warproom,environment,time,random,json,math,objects
from ursina import Entity,Text,camera,scene,invoke,Vec3,color,distance,boxcast,raycast,window
from ursina.ursinastuff import destroy
from math import atan2,sqrt,pi

level_ready=False
env=environment
sn=sound
st=status
LC=_loc
C=crate
N=npc

## player
def set_val(c):#run  jump  idle spin land  fall  flip slidestop standup sliderun smashsmash bellyland walksound					inwater
	for _a in {'rnfr','jmfr','idfr','spfr','ldfr','fafr','flfr','ssfr','sufr','srfr','smfr','blfr','wksn','fall_time','slide_fwd','inwt','space_time','stnfr','stun_tme','dth_cause','dth_fr'}:
		setattr(c,_a,0)#values
	for _v in {'aq_bonus','walking','jumping','landed','tcr','frst_lnd','is_landing','is_attack','is_flip','warped','freezed','injured','is_slippery','b_smash','standup','falling','stun','sma_dth'}:
		setattr(c,_v,False)#flags
	c.move_speed=LC.dfsp
	c.cur_tex=c.texture
	c.gravity=LC.dfsp
	c.inv_sc=-.1/110
	c.nor_sc=.1/110
	c.stun_fd=(0,0,0)
	c.direc=(0,0,0)
	c.vpos=c.y
	c.dth_timer=4
	c.indoor=.5
	c.CMS=3
	_loc.ACTOR=c
	del _a,_v,c
def get_damage(c,rsn):
	if st.aku_hit > 2:
		return
	if not (c.injured or st.death_event):
		if st.aku_hit > 0:
			st.aku_hit-=1
			c.injured=True
			c.hurt_visual()
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
	del rsn
def reset_state(c):
	ui.BlackScreen()
	st.crate_count-=st.crate_to_sv
	if st.death_route:
		st.death_route=False
	if st.bonus_round:
		st.wumpa_bonus=0
		st.crate_bonus=0
		st.lives_bonus=0
		st.bonus_round=False
	else:
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
			sn.crate_audio(ID=14,pit=1.2)
			npc.AkuAkuMask(pos=(c.x,c.y,c.z))
	reset_crates()
	rmv_wumpas()
	reset_wumpas()
	reset_npc()
	if st.level_index == 6:
		c.sma_dth=False
		reset_mines()
		rmv_bees()
	check_nitro_stack()
	c.position=status.checkpoint
	env.set_fog(st.level_index)
	camera.position=c.position
	camera.rotation=(15,0,0)
	c.scale_x=c.nor_sc
	st.death_event=False
	c.dth_fr=0
	c.texture='res/pc/crash.tga'
	c.visible=True
	c.stun=False
	invoke(lambda:setattr(c,'freezed',False),delay=3)
def various_val(c):
	c.inwt=max(c.inwt-time.dt,0)
	c.indoor=max(c.indoor-time.dt,0)
	if not c.is_slippery:
		c.move_speed=LC.dfsp
	if st.bonus_solved and not st.wait_screen:
		c.aq_bonus=(st.wumpa_bonus > 0 or st.crate_bonus > 0 or st.lives_bonus > 0)
def c_slide(c):
	if not c.walking:
		if c.slide_fwd > 0 and status.p_last_direc != None:
			if c.move_speed > 0:
				c.move_speed-=time.dt
			c.position+=status.p_last_direc*time.dt*c.slide_fwd
			c.slide_fwd-=time.dt
			if c.slide_fwd <= 0:
				c.slide_fwd=0
				st.p_last_direc=None
		return
	if c.move_speed < 4:
		c.move_speed+=time.dt
		if c.move_speed > 0:
			c.slide_fwd=c.move_speed
def c_smash(c):
	k=[dp for dp in scene.entities if (distance(c.position,dp.position) < .4 and dp.collider and (is_crate(dp) or is_enemie(dp)))]
	for sw in k:
		if is_crate(sw):
			if sw.vnum in {3,11}:
				sw.empty_destroy()
			if sw.vnum == 14:
				sw.c_destroy()
			else:
				sw.destroy()
		if is_enemie(sw) and sw.vnum != 13:
			sw.is_purge=True
def c_attack(c):
	if not c.is_attack or st.gproc():
		return
	for qd in scene.entities[:]:
		if (qd.collider and distance(qd.position,c.position) < .5):
			if is_crate(qd) and qd.vnum != 13:
				if qd.vnum in {3,11}:
					qd.empty_destroy()
				else:
					qd.destroy()
			if is_enemie(qd):
				if not (qd.is_purge or qd.is_hitten):
					if (qd.vnum in {1,11}) or (qd.vnum == 5 and qd.def_mode):
						get_damage(c,rsn=2)
					if not qd.vnum == 13:
						bash_enemie(qd,h=c)
def c_shield():
	if st.aku_hit < 3 or st.gproc():
		return
	q=LC.ACTOR
	for rf in scene.entities[:]:
		if (rf.collider and rf.enabled):
			if distance(rf.position,q.position) < 1.5:
				if (rf.name in LC.item_lst):
					rf.collect()
				if (is_enemie(rf) and rf.vnum != 13):
					bash_enemie(e=rf,h=q)
				if (is_crate(rf) and not rf.vnum in {0,8,13}):
					if rf.vnum in [3,11]:
						rf.empty_destroy()
					if rf.vnum == 14:
						rf.c_destroy()
					if not (rf.vnum in {9,10} and rf.activ):
						rf.destroy()

## camera actor
def cam_indoor(c):
	ftt=time.dt*2
	cm=camera
	cm.fov=lerp(cm.fov,57.5,ftt)
	cm.z=lerp(cm.z,c.z-3,ftt)
	cm.x=lerp(cm.x,c.x,ftt)
	cm.rotation_x=lerp(cm.rotation_x,14,ftt)
	if (c.landed and c.walking):
		cm.y=lerp(cm.y,c.y+1,ftt)
def cam_level(c):
	ftt=time.dt
	cm=camera
	cm.z=lerp(cm.z,c.z-c.CMS,ftt*3)
	cm.x=lerp(cm.x,c.x,ftt*2.5)
	camera.fov=cm.fov=lerp(cm.fov,64,ftt)
	if (c.jumping or c.falling):
		if cm.rotation_x > 20:
			cm.rotation_x=lerp(cm.rotation_x,c.y,ftt/5)
		del c,cm,ftt
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
	cry_pos={1:(0,1.5,-13),2:(35.5,6.4,28.5),3:(0,2.5,60.5),4:(14,4.25,66),5:(12,.8,-7)}
	if not idx in st.CRYSTAL:
		item.EnergyCrystal(pos=cry_pos[idx])
	del cry_pos
def collect_reset():
	st.C_RESET.clear()
	st.W_RESET.clear()
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
		if is_crate(sr) and sr.poly:
			sr.enabled=False
			sr.parent=None
			scene.entities.remove(sr)
	for cv in st.C_RESET[:]:
		if cv.vnum in {9,10}:
			cv.c_reset()
		elif cv.vnum == 13:
			if not cv.c_ID == 0:
				c_subtract(cY=cv.y)
			C.place_crate(p=cv.spawn_pos,ID=cv.vnum,m=cv.mark,l=cv.c_ID,pse=cv.poly)
		else:
			if cv.vnum == 11:
				cv.activ=False
				cv.countdown=0
			if not cv.vnum == 16:
				c_subtract(cY=cv.y)
			C.place_crate(p=cv.spawn_pos,ID=cv.vnum)
	st.C_RESET.clear()
	st.crate_to_sv=0
def reset_wumpas():
	for wres in status.W_RESET[:]:
		item.WumpaFruit(p=wres,c_prg=False)
	st.W_RESET.clear()
def rmv_wumpas():
	for wu in scene.entities[:]:
		if isinstance(wu,item.WumpaFruit) and wu.c_purge:
			wu.destroy()
def reset_npc():
	for NP in st.NPC_RESET[:]:
		if NP.vnum in {10,11}:
			npc.spawn(ID=NP.vnum,POS=NP.spawn_pos,DRC=NP.mov_direc,RTYP=NP.ro_mode,RNG=NP.mov_range)
		else:
			if NP.vnum == 8:
				npc.spawn(ID=NP.vnum,POS=NP.spawn_pos,DRC=NP.mov_direc,CMV=NP.can_move,RNG=NP.mov_range)
			else:
				npc.spawn(ID=NP.vnum,POS=NP.spawn_pos,DRC=NP.mov_direc,RNG=NP.mov_range)
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
	st.level_index=0
	st.crates_in_bonus=0
	st.crates_in_level=0
	st.crate_bonus=0
	st.crate_count=0
	st.crate_to_sv=0
	st.fails=0
	if st.aku_hit > 2:
		st.aku_hit=2
	st.NPC_RESET.clear()
	st.W_RESET.clear()
	st.C_RESET.clear()
	st.is_invincible=False
	st.level_crystal=False
	st.level_col_gem=False
	st.level_cle_gem=False
	st.gem_path_solved=False
	st.death_route=False
	st.bonus_solved=False
	st.bonus_round=False
	st.LEVEL_CLEAN=False
	st.death_event=False
	st.gem_death=False
	st.pause=False
	level_ready=False
def collect_rewards():
	cdx=st.level_index
	if st.level_crystal:
		st.CRYSTAL.append(cdx)
		st.collected_crystals+=1
	if st.level_cle_gem:
		st.CLEAR_GEM.append(cdx)
		st.clear_gems+=1
	if st.level_col_gem:
		st.color_gems+=1
		if cdx > 5:
			st.COLOR_GEM.append(cdx)
		else:
			wcg={1:4,#lv1#blue
				2:1,#lv2#red
				3:5,#lv3#yellow
				4:2,#lv4#green
				5:3}#lv5#purple
			st.COLOR_GEM.append(wcg[cdx])
			del wcg
	delete_states()
	invoke(lambda:warproom.level_select(),delay=2)
def purge_instance(v):
	if isinstance(v,N.AkuAkuMask):
		st.aku_exist=False
	destroy(v)
def cache_instance(v):
	if str(v) == 'bee':
		destroy(v)
		del v
		return
	if is_enemie(v):
		st.NPC_RESET.append(v)
	v.enabled=False
	v.parent=None
	v.children=None
	scene.entities.remove(v)
	del v
def game_pause():
	if not st.pause:
		st.pause=True
	else:
		st.pause=False
	pa=st.pause
	pm=LC.p_menu
	pm.crystal_counter.visible=(pa)
	pm.game_progress.visible=(pa)
	pm.gem_counter.visible=(pa)
	pm.lvl_name.visible=(pa)
	pm.add_text.visible=(pa)
	pm.cry_anim.visible=(pa)
	pm.select_0.visible=(pa)
	pm.select_1.visible=(pa)
	pm.select_2.visible=(pa)
	pm.col_gem1.visible=(pa)
	pm.col_gem2.visible=(pa)
	pm.col_gem3.visible=(pa)
	pm.col_gem4.visible=(pa)
	pm.col_gem5.visible=(pa)
	pm.cleargem.visible=(pa)
	pm.p_name.visible=(pa)
	pm.ppt.visible=(pa)
	pm.visible=(pa)
	del pm
def game_over():
	invoke(lambda:ui.GameOverScreen(),delay=2)

## collisions
def check_ceiling(c):
	vc=c.intersects(ignore=[c,LC.shdw])
	ve=vc.entity
	if vc and vc.normal == Vec3(0,-1,0):
		if not (ve.name in LC.item_lst|LC.trigger_lst):
			if is_crate(ve):
				if not c.tcr:
					c.tcr=True
					ve.destroy()
					invoke(lambda:setattr(c,'tcr',False),delay=.1)
			c.y=c.y
			c.jumping=False
def check_wall(c):
	hT=c.intersects(ignore=[c,LC.shdw])
	jV=hT.entity
	xa=str(jV)
	if hT and hT.hit and not (hT.normal in {Vec3(0,1,0),Vec3(0,-1,0)}):
		if xa == 'nitro':
			jV.destroy()
			return
		if xa in LC.item_lst:
			jV.collect()
			return
		hit_npc(c,m=jV)
		if not xa in LC.trigger_lst:
			c.position-=c.direc*time.dt*c.move_speed
def check_floor(c):
	lkh={r for r in scene.entities if (str(r) in LC.item_lst|LC.dangers|LC.trigger_lst) or r in [c,LC.shdw]}
	vj=boxcast(c.world_position,Vec3(0,1,0),distance=.01,thickness=(.125,.125),ignore=lkh,debug=False)
	vp=vj.entity
	if not c.landed:
		fall_interact(c,vp)
	if vj and vj.normal:
		c.falling,c.landed=False,True
		if not c.jumping:
			c.y=vj.world_point.y
		if not (is_crate(vp) or is_enemie(vp)):
			spc_floor(c,vp)
		land_act(c,vp)
		return
	c.falling,c.landed=True,False
	fsp={False:(time.dt*c.gravity),True:(time.dt*c.gravity)*2}
	c.y-=fsp[c.b_smash]
	c.fall_time+=time.dt
	c.anim_fall()
	del fsp
def land_act(c,vp):
	if c.frst_lnd:
		c.frst_lnd,c.stun=False,False
		c.space_time,c.fall_time=0,0
		c.anim_land()
		sn.landing_sound(c,vp)
def fall_interact(c,e):
	if (is_crate(e) and c.fall_time > .05):
		if not ((e.vnum == 0) or (e.vnum in {9,10,11} and e.activ)):
			if e.vnum in {7,8}:
				c.jump_typ(t=4)
				e.c_action()
				del c,e
				return
			if e.vnum == 3:
				c.jump_typ(t=3)
			else:
				if not e.vnum == 14:
					c.jump_typ(t=2)
			e.destroy()
			return
	if is_enemie(e) and not (e.is_hitten or e.is_purge):
		if (e.vnum in {2,9,13}) or (e.vnum == 5 and e.def_mode):
			get_damage(c,rsn=2)
		e.is_purge=True
		c.jump_typ(t=2)
		sn.pc_audio(ID=5)
def spc_floor(c,e):
	u=str(e)
	c.is_slippery=(u == 'iceg')
	if u in {'bnpt','gmpt'}:
		ptf_up(p=e,c=c)
		return
	if u in {'swpt','HPP','epad'}:
		e.active=True
		return
	if (u == 'plnk' and e.typ == 1) or u == 'loos':
		e.pl_touch()
		return
	if (u == 'swpi' and e.typ == 3) or (u == 'labt' and e.danger):
		get_damage(c,rsn=4)
		return
	if u == 'wtrh':
		dth_event(c,rsn=3)
		return
	if u == 'mptf' and not c.walking:
		e.mv_player()
def ptf_up(p,c):
	if not c.freezed:
		c.freezed=True
		c.position=(p.x,c.y,p.z)
		c.rotation_y=0
	p.y+=time.dt/1.5
	if p.y > p.start_y+3:
		p.y=p.start_y
		go_to={'bnpt':lambda:load_bonus(c),'gmpt':lambda:load_gem_route(c)}
		go_to[p.name]()
		del go_to
def hit_npc(c,m):
	if is_enemie(m) and m.collider:
		if not (m.is_purge or m.is_hitten):
			RS=2
			if m.vnum == 7:
				RS=5
			elif m.vnum == 15:
				RS=7
			elif m.vnum == 16:
				RS=8
			if not c.is_attack:
				get_damage(c,rsn=RS)

## interface,collectables
def wumpa_count(n):
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
	st.show_crates=5
	st.show_lives=5
	st.show_gems=5

## crate actions
def crate_set_val(cR,Cpos,Cpse):
	cR.texture='res/crate/'+str(cR.vnum)+'.tga'
	if cR.vnum == 15:
		cR.texture='res/crate/crate_t'+str(cR.time_stop)+'.tga'
	if cR.vnum in {9,10}:
		cR.org_tex=cR.texture
	cR.spawn_pos=Cpos
	cR.position=Cpos
	cR.collider='box'
	cR.poly=Cpse
	cR.scale=.16
	del cR,Cpos,Cpse
def crate_stack(c):
	crf={pk for pk in scene.entities if (is_crate(pk) and (pk.x == c.x and pk.z == c.z) and pk.vnum != 3)}
	sdi=0
	for wm in crf:
		sdi+=1
		if (wm.y > c.y) and (wm.y-c.y) <= .33*sdi:
			wm.animate_y(wm.y-.32,duration=.175)
	sdi=0
def check_nitro_stack():
	nit_crt={ct for ct in scene.entities if is_crate(ct) and ct.vnum == 12 and ct.can_jmp}
	all_crt={ct for ct in scene.entities if is_crate(ct)}
	for ni in nit_crt:
		for cra in all_crt:
			if abs(cra.x-ni.x) < .1 and abs(cra.z-ni.z) < .1 and ni.y <= cra.y and not ni is cra:
				ni.can_jmp=False
	del nit_crt,all_crt
def is_crate(e):
	cck={C.Iron,C.Normal,C.QuestionMark,C.Bounce,C.ExtraLife,
		C.AkuAku,C.Checkpoint,C.SpringWood,C.SpringIron,C.SwitchEmpty,
		C.SwitchNitro,C.TNT,C.Nitro,C.Air,C.Protected,C.cTime,C.LvInfo}
	return any(isinstance(e,crate_class) for crate_class in cck)

## bonus level
def load_b_ui():
	ui.WumpaBonus()
	ui.CrateBonus()
	ui.LiveBonus()
def load_bonus(c):
	st.loading=True
	st.checkpoint=LC.bonus_checkpoint[st.level_index]
	collect_reset()
	if st.bonus_round:
		invoke(lambda:back_to_level(c),delay=.5)
		return
	invoke(lambda:enter_bonus(c),delay=.5)
def enter_bonus(c):
	ui.BlackScreen()
	st.bonus_round=True
	load_b_ui()
	sn.BonusMusic(T=st.level_index)
	ui.BonusText()
	c.position=(0,-35,-3)
	env.set_fog(st.level_index)
	camera.y=-35
	st.loading,c.freezed=False,False
def clear_bonus():
	for brd in scene.entities[:]:
		if (brd.parent == scene) and (brd.x > 180):
			if not (is_crate(brd) or brd in {LC.shdw,LC.ACTOR}):
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
	env.set_fog(st.level_index)
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
	c.position=(200,2,-3)
	camera.position=(200,.5,-3)
	st.loading,c.freezed=False,False
	sn.SpecialMusic(T=st.level_index)
def clear_gem_route():
	for grd in scene.entities[:]:
		if (grd.parent == scene) and (grd.x > 180):
			if not (is_crate(grd) or grd in {LC.shdw,LC.ACTOR}):
				destroy(grd)
	del grd

## npc
def set_val_npc(m,drc=None,rng=None):
	m.anim_frame,m.fly_time,m.turn=0,0,0
	m.is_hitten,m.is_purge=False,False
	m.spawn_pos=m.position
	m.fly_direc=None
	m.mov_range=rng
	m.mov_direc=drc
	del m,drc,rng
def circle_move_xz(m):
	m.angle-=time.dt*2
	m.angle%=(2*math.pi)
	new_x=m.spawn_pos[0]-m.mov_range*math.cos(m.angle)
	new_z=m.spawn_pos[2]-m.mov_range*math.sin(m.angle)
	m.position=Vec3(new_x,m.y,new_z)
	rot=math.degrees(math.atan2(new_z-m.spawn_pos[2],new_x-m.spawn_pos[0]))
	m.rotation_y=-rot
def circle_move_y(m):
	m.angle+=time.dt*2
	m.angle%=(2*math.pi)
	new_x=m.spawn_pos[0]+m.mov_range*math.cos(m.angle)
	new_y=m.spawn_pos[1]+m.mov_range*math.sin(m.angle)
	m.position=Vec3(new_x,new_y,m.z)
	rot=math.degrees(math.atan2(new_y-m.spawn_pos[1],new_x-m.spawn_pos[0]))
	m.rotation_x=rot
	m.rotation_y=-90
def rotate_to_crash(m):
	rtp=(LC.ACTOR.position-m.position)
	m.rotation_y=atan2(rtp.x,rtp.z)*(180/pi)+180
	m.rotation_x=-90
def fly_away(n):
	n.position+=n.fly_direc*(time.dt*40)
	n.fly_time=min(n.fly_time+time.dt,.61)
	ke=n.intersects().entity
	if n.fly_time > .6:
		cache_instance(n)
		return
	if (is_crate(ke) and ke.vnum != 6):
		if ke.vnum in {3,11}:
			ke.empty_destroy()
		else:
			ke.destroy()
	if is_enemie(ke):
		if n.vnum == 15:
			destroy(n)
			return
		n.collider=None
		n.enabled=False
		if not ke.is_hitten:
			bash_enemie(e=ke,h=n)
			cache_instance(n)
			wumpa_count(1)
def is_enemie(n):
	ix={0:{},
	1:{N.Amadillo,N.Turtle,N.SawTurtle},
	2:{N.Penguin,N.Hedgehog,N.Seal},
	3:{N.EatingPlant,N.SawTurtle},
	4:{N.Eel,N.Scrubber,N.Mouse,N.SewerMine},
	5:{N.Gorilla,N.Rat,N.Lizard},
	6:{N.Bee,N.Lumberjack},
	7:{N.SpiderRobotFlat,N.SpiderRobotUp,N.Robot}}
	return any(isinstance(n,npc_class) for npc_class in ix[st.level_index])
def bash_enemie(e,h):
	e.is_hitten=True
	e.fly_direc=Vec3(e.x-h.x,0,e.z-h.z)
	sn.obj_audio(ID=8)
	del e,h

## game progress
save_file='savegame.json'
def save_game():
	save_data={
		'SV_WU':st.wumpa_fruits,#wumpa fruits
		'SV_LF':st.extra_lives,#extra lives
		'SV_CR':st.collected_crystals,#crystal count
		'SV_CG':st.color_gems,#color gem count
		'SV_CL':st.clear_gems,#clear gem count
		'SV_AK':st.aku_hit,#aku mask
		'LS_CR':st.CRYSTAL,#Lv ID crystal
		'LS_CL':st.CLEAR_GEM,#Lv ID clear gem
		'LS_CG':st.COLOR_GEM,#Color Gem ID
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
	st.collected_crystals=save_data['SV_CR']
	st.color_gems=save_data['SV_CG']
	st.clear_gems=save_data['SV_CL']
	st.aku_hit=save_data['SV_AK']
	st.CRYSTAL=[(x) for x in save_data['LS_CR']]
	st.CLEAR_GEM=[(x) for x in save_data['LS_CL']]
	st.COLOR_GEM=[(x) for x in save_data['LS_CG']]
	settings.SFX_VOLUME=save_data['S_VOL']
	settings.MUSIC_VOLUME=save_data['M_VOL']
	st.crd_seen=save_data['CRD_W']

##lv6 func
def rmv_bees():
	for vbw in scene.entities[:]:
		if isinstance(vbw,npc.Bee):
			vbw.purge()
def reset_mines():
	for rsm in LC.LDM_POS[:]:
		objects.LandMine(pos=rsm)
	LC.LDM_POS.clear()