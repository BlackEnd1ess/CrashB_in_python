import player,crate,item,_core,environment,animation,objects,settings,status,ui,level
from ursina import *

cc=_core
def information_output():
	ppos=cc.playerInstance[0]
	print(f'player_position::{ppos.position}')
	print(f'is_landed::{ppos.landed}')
	print(f'is_jumping::{ppos.jumping}')