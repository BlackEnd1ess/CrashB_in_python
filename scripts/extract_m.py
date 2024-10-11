## This Code works only with CrashEdit Tool. This Tool must run in maximized Window and In order for the tool to work, the first frame or item must be at the top where you can click on it so that each 
## frame is processed individually. There are several factors to consider: screen resolution and font size/zoom on the desktop. In this case for me it would be 1920x1080 and text size at 100%, it should 
## work without any problems. While the tool is working you should not move the mouse or press a key, the process ends after the loop is finished.

import pygetwindow as gw
import time,pyautogui

win=gw.getWindowsWithTitle('CrashEdit')
NAME='FOLDER_NAME'
outf='D:\\evp\\'+NAME+'\\frame'
t=time
cnt=33

print('tool is starting in 3 sec')
t.sleep(3)
def run_tool(n):
	pyautogui.moveTo(95,107+(n*18))
	pyautogui.click()
	t.sleep(.3)
	pyautogui.moveTo(670,110)
	pyautogui.click()
	t.sleep(.2)
	pyautogui.write(outf+str(n))
	t.sleep(.1)
	pyautogui.press('enter')

if win:
	t_window=win[0]
	t_window.activate()
	for ext in range(cnt):
		run_tool(ext)
		t.sleep(.1)
input('fin')
