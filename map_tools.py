import crate,item,objects
from ursina import *

c=crate
o=objects
I=item

## multible crate spawn
def bounce_twin(POS,CNT):
	for cbt in range(CNT):
		pO=.32*cbt
		c.place_crate(ID=3,p=(POS[0]+pO,POS[1],POS[2]))
		c.place_crate(ID=3,p=(POS[0]+pO,POS[1]+1.6,POS[2]))

def steel_bridge(POS,CNT):
	for cst in range(CNT):
		pO=.32*cst
		c.place_crate(ID=0,p=(POS[0]-pO,POS[1],POS[2]))

def crate_row(ID,POS,CNT,WAY):# WAY: 0=right,1=front,2=up
	for cro in range(CNT):
		pO=.32*cro
		if WAY == 0:
			c.place_crate(ID=ID,p=(POS[0]+pO,POS[1],POS[2]))
		elif WAY == 1:
			c.place_crate(ID=ID,p=(POS[0],POS[1],POS[2]+pO))
		else:
			c.place_crate(ID=ID,p=(POS[0],POS[1]+pO,POS[2]))

def crate_wall(ID,POS,CNT):
	for cwX in range(CNT):
		for cwY in range(CNT):
			pO=.32*cwX
			pA=.32*cwY
			c.place_crate(ID=ID,p=(POS[0]+pO,POS[1]+pA,POS[2]))

def crate_stair(ID,POS,CNT,WAY):# WAY: 0=up,1=down
	for cs in range(CNT):
		pO=.32*cs
		c_way={0:POS[1]+pO,1:POS[1]-pO}
		c.place_crate(ID=ID,p=(POS[0]+pO,c_way[WAY],POS[2]))

def crate_block(ID,POS,CNT):
	for cbX in range(CNT):
		for cbZ in range(CNT):
			for cbY in range(CNT):
				pO=.32*cbX
				pA=.32*cbY
				pE=.32*cbZ
				c.place_crate(ID=ID,p=(POS[0]+pO,POS[1]+pA,POS[2]+pE))

def crate_plane(ID,POS,CNT):
	for cwX in range(CNT):
		for cwZ in range(CNT):
			pO=.32*cwX
			pA=.32*cwZ
			c.place_crate(ID=ID,p=(POS[0]+pO,POS[1],POS[2]+pA))


## multible wumpa spawn
def wumpa_row(POS,CNT,WAY):
	for wr in range(CNT):#WAY: 0=right,1=front,2=up
		if WAY == 0:
			I.WumpaFruit(pos=(POS[0]+wr/3,POS[1],POS[2]))
		elif WAY == 1:
			I.WumpaFruit(pos=(POS[0],POS[1],POS[2]+wr/3))
		else:
			I.WumpaFruit(pos=(POS[0],POS[1]+wr/3,POS[2]))

def wumpa_double_row(POS,CNT):
	for wr in range(CNT):
		I.WumpaFruit(pos=(POS[0]+wr/3,POS[1],POS[2]))
		I.WumpaFruit(pos=(POS[0]+wr/3,POS[1]+.3,POS[2]))

def wumpa_wall(POS,CNT):
	for wx in range(CNT):
		for wy in range(CNT):
			I.WumpaFruit(pos=(POS[0]+wx/3,POS[1]+wy/3,POS[2]))

def wumpa_plane(POS,CNT):
	for wx in range(CNT):
		for wz in range(CNT):
			I.WumpaFruit(pos=(POS[0]+wx/3,POS[1],POS[2]+wz/3))

def wumpa_block(POS,CNT):
	for wx in range(CNT):
		for wy in range(CNT):
			for wz in range(CNT):
				I.WumpaFruit(pos=(POS[0]+wx/3,POS[1]+wy/3,POS[2]+wz/3))