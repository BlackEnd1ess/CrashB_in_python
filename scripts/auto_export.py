## This Tool works with CBExporter by warenhuis on Git. To export a Model you need item 0-4 or 5 and a frame Data. This Tool can only proceed a Single Frame and this is
## very time consumpting. To save more time, this Tool will make it 3x faster. The most Time consumpting Process is rename und delete the old Files and switching Directories.
## If the tool somehow loses control or reacts too quickly/slowly, you can adjust the time there and simply close the process with escape. That's why I wouldn't run the tool 
## directly on the desktop or in a folder that contains important files, as these could be accidentally marked or overwritten. It's best to run this tool in an empty folder 
## and set it to the maximum window size, then nothing will happen.

import time,pyautogui,os,shutil
import pygetwindow as gw

MAIN_S='D:\\evp\\_stored_\\'
MAIN_P='D:\\evp\\'
MODEL='my_model'

pv=pyautogui
t=time

frames=11
wait=3

def start(idx):
	os.system('cd '+MAIN_P+' && start CB2Export.exe')
	t.sleep(5.5)
	if os.path.isdir(MAIN_P+MODEL):
		write_inp(idx)

def write_inp(idx):
	pyautogui.write(MODEL,interval=.1)#folder name
	pv.press('enter')#confirm folder
	t.sleep(.5)
	pv.press('enter')#confirm version
	t.sleep(1)
	pv.press('enter')#export call
	t.sleep(1)
	pyautogui.write(str(idx),interval=.1)#write index as name
	t.sleep(.3)
	pv.press('enter')#export name ok
	t.sleep(.5)
	pv.press('enter')#confirm .ply
	t.sleep(wait)
	pv.press('enter')
	pv.press('escape')#confirm .tga
	t.sleep(.3)
	delete_frame(idx)

def delete_frame(idx):
	fi=os.listdir(MAIN_P+MODEL)
	for file in fi:
		fp=os.path.join(MAIN_P+MODEL,file)
		if os.path.isfile(fp):
			if file == 'frame':
				os.remove(fp)
	check_next_frame(idx)

def check_next_frame(idx):
	files=os.listdir(MAIN_P+MODEL)
	for file in files:
		file_path=os.path.join(MAIN_P+MODEL,file)
		if os.path.isfile(file_path):
			if file == 'frame'+str(idx+1):
				npa=os.path.join(MAIN_P+MODEL,'frame')
				os.rename(file_path,npa)

def mv_ex_models():
	f=os.listdir(MAIN_P+MODEL)
	for file in f:
		file_p=os.path.join(MAIN_P+MODEL,file)
		if os.path.isfile(file_p):
			if '.ply' in file or file == '0.tga':
				sp=os.path.join(MAIN_P+MODEL,file)
				dp=os.path.join(MAIN_S,file)
				shutil.move(sp,dp)

for vn in range(frames):
	start(vn)
	print(f'extractions phase... current model Frame: {vn}')
	t.sleep(1)

mv_ex_models()
input('tool successfully executed')
