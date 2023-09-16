# python hotkey_service.py install
# import servicemanager
# import sys
# import time
from pynput import keyboard
import win32api, win32gui
import pyautogui

import win32serviceutil
import ctypes
import time

OutputDebugString = ctypes.windll.kernel32.OutputDebugStringW

class HotkeyFramework(win32serviceutil.ServiceFramework):
    _svc_name_ = 'MyHotKeyService'
    _svc_display_name_ = 'My Hotkey Service'
    is_running = False
    keymap_position = {'q' : ('m', 0.2, 0.2), 'w' : ('m', 0.5, 0.2), 'e' : ('m', 0.8, 0.2),
                       'a' : ('m', 0.2, 0.5), 's' : ('m', 0.5, 0.5), 'd' : ('m', 0.8, 0.5),
                       'z' : ('m', 0.2, 0.8), 'x' : ('m', 0.5, 0.8), 'c' : ('m', 0.8, 0.8),
                       '1' : ('s', 1, 0), '2' : ('s', 2, 0)}

    def SvcStop(self):
        OutputDebugString("__SvcStop__")
        self.is_running = False
        self.h.stop()

    def SvcDoRun(self):
        OutputDebugString("__SvcStart__")
        self.is_running = True
        def factory(key):
            def on_activate():
                screen_size = pyautogui.size()
                pos = self.keymap_position[key]
                if pos[0] == 'm':
                    x, y = (pos[1] * screen_size[0], pos[2] * screen_size[1])
                    win32api.SetCursorPos((int(x), int(y)))
                    pyautogui.click(int(x), int(y))
                elif pos[0] == 's':
                    # move forground window to monitor 2
                    handle = win32gui.GetForegroundWindow()
                    monitors = win32api.EnumDisplayMonitors()
                    if len(monitors) >= int(key):
                        win32gui.MoveWindow(handle, 
                                            monitors[int(key) - 1][2][0],
                                            monitors[int(key) - 1][2][1],
                                            monitors[int(key) - 1][2][2],
                                            monitors[int(key) - 1][2][3],
                                            True)
            return on_activate
        proc_position = {}
        for key in self.keymap_position.keys():
            proc_position[f"<ctrl>+<alt>+{key}"] = factory(key)
        OutputDebugString("__SvcPrepare&Start__")
        self.h = keyboard.GlobalHotKeys(proc_position)
        self.h.start()
        self.h.join()
        OutputDebugString("__SvcStoped__")

if '__main__' == __name__:
    OutputDebugString("__SvcMainStart__")
    win32serviceutil.HandleCommandLine(HotkeyFramework)