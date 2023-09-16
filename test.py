import win32api
import pyautogui
pos = [0.5, 0.5]
screen_size = pyautogui.size()
print(screen_size)
monitors = win32api.EnumDisplayMonitors()
print(monitors)

import win32gui
# move forground window to monitor 2
handle = win32gui.GetForegroundWindow()
win32gui.MoveWindow(handle, 1920, 0, 1920, 1080, True)