import crate,item,objects
c=crate
o=objects
I=item

## multible crate spawn
def bounce_twin(POS,CNT,trs=1.65):
	for cbt in range(CNT):
		pO=.32*cbt
		c.place_crate(ID=3,p=(POS[0]+pO,POS[1],POS[2]))
		c.place_crate(ID=3,p=(POS[0]+pO,POS[1]+trs,POS[2]))
	del POS,CNT,trs

def steel_bridge(POS,CNT):
	for cst in range(CNT):
		c.place_crate(ID=0,p=(POS[0]-.32*cst,POS[1],POS[2]))
	del POS,CNT

def crate_row(ID,POS,CNT,WAY,l=None,m=None):# WAY: 0=right,1=front,2=up
	for cro in range(CNT):
		pO=.32*cro
		if WAY == 0:
			if ID == 13:
				c.place_crate(ID=ID,p=(POS[0]+pO,POS[1],POS[2]),m=m,l=l)
			else:
				c.place_crate(ID=ID,p=(POS[0]+pO,POS[1],POS[2]))
		elif WAY == 1:
			if ID == 13:
				c.place_crate(ID=ID,p=(POS[0],POS[1],POS[2]+pO),m=m,l=l)
			else:
				c.place_crate(ID=ID,p=(POS[0],POS[1],POS[2]+pO))
		else:
			if ID == 13:
				c.place_crate(ID=ID,p=(POS[0],POS[1]+pO,POS[2]),m=m,l=l)
			else:
				c.place_crate(ID=ID,p=(POS[0],POS[1]+pO,POS[2]))
	del ID,POS,CNT,WAY,l,m,cro,pO

def crate_wall(ID,POS,CNT):#[x,y]
	for cwX in range(CNT[0]):
		for cwY in range(CNT[1]):
			c.place_crate(ID=ID,p=(POS[0]+.32*cwX,POS[1]+.32*cwY,POS[2]))
	del ID,POS,CNT,cwX,cwY

def crate_stair(ID,POS,CNT,WAY):# WAY: 0=up,1=down
	for cs in range(CNT):
		pO=.32*cs
		c_way={0:POS[1]+pO,1:POS[1]-pO}
		c.place_crate(ID=ID,p=(POS[0]+pO,c_way[WAY],POS[2]))
	del ID,POS,CNT,WAY,cs,pO

def crate_block(ID,POS,CNT):#[x,y,z]
	for cbX in range(CNT[0]):
		for cbZ in range(CNT[1]):
			for cbY in range(CNT[2]):
				pO=.32*cbX
				pA=.32*cbY
				pE=.32*cbZ
				c.place_crate(ID=ID,p=(POS[0]+pO,POS[1]+pA,POS[2]+pE))
	del ID,POS,CNT,cbX,cbZ,cbY,pO,pA,pE

def crate_plane(ID,POS,CNT):#[x,z]
	for cwX in range(CNT[0]):
		for cwZ in range(CNT[1]):
			c.place_crate(ID=ID,p=(POS[0]+.32*cwX,POS[1],POS[2]+.32*cwZ))
	del ID,POS,CNT,cwX,cwZ

## multible wumpa spawn
def wumpa_row(POS,CNT,WAY):#WAY: 0=right,1=front,2=up
	for wr in range(CNT):
		if WAY == 0:
			I.place_wumpa((POS[0]+wr/3,POS[1],POS[2]),cnt=1)
		elif WAY == 1:
			I.place_wumpa((POS[0],POS[1],POS[2]+wr/3),cnt=1)
		else:
			I.place_wumpa((POS[0],POS[1]+wr/3,POS[2]),cnt=1)
	del wr,POS,CNT,WAY

def wumpa_double_row(POS,CNT):
	for wr in range(CNT):
		I.place_wumpa((POS[0]+wr/3,POS[1],POS[2]),cnt=1)
		I.place_wumpa((POS[0]+wr/3,POS[1]+.3,POS[2]),cnt=1)
	del POS,CNT,wr

def wumpa_wall(POS,CNT):#[x,y]
	for wx in range(CNT[0]):
		for wy in range(CNT[1]):
			I.place_wumpa((POS[0]+wx/3,POS[1]+wy/3,POS[2]),cnt=1)
	del POS,CNT,wx,wy

def wumpa_plane(POS,CNT):#[x,z]
	for wx in range(CNT[0]):
		for wz in range(CNT[1]):
			I.place_wumpa((POS[0]+wx/3,POS[1],POS[2]+wz/3),cnt=1)
	del POS,CNT,wx,wz

def wumpa_block(POS,CNT):#[x,y,z]
	for wx in range(CNT[0]):
		for wy in range(CNT[1]):
			for wz in range(CNT[2]):
				I.place_wumpa((POS[0]+wx/3,POS[1]+wy/3,POS[2]+wz/3),cnt=1)
	del POS,CNT,wx,wy