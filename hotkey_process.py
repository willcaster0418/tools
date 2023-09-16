import win32api
import pyautogui
import win32gui
from pynput import keyboard
class HotkeyProcess:
    def __init__(self):
        self.keymap_position = {'q' : ('m', 0.2, 0.2), 'w' : ('m', 0.5, 0.2), 'e' : ('m', 0.8, 0.2),
                                'a' : ('m', 0.2, 0.5), 's' : ('m', 0.5, 0.5), 'd' : ('m', 0.8, 0.5),
                                'z' : ('m', 0.2, 0.8), 'x' : ('m', 0.5, 0.8), 'c' : ('m', 0.8, 0.8),
                                '1' : ('s', 1, 0), '2' : ('s', 2, 0),
                                't' : ('v',   0, -10), 'g' : ('v',  0, 10),
                                'f' : ('v', -10,   0), 'h' : ('v', 10,  0), 'r' : ('c', 0, 0), 'y' : ('l', 0, 0)}
        self.proc_position = {}
        for key in self.keymap_position.keys():
            self.proc_position[f"<ctrl>+<alt>+{key}"] = self.factory(key)

    def __call__(self):
        self.proc()

    def __str__(self):
        return f"HotkeyProcess({self.keymap},{self.proc})"

    def factory(self, key):
        def on_activate():
            screen_size = pyautogui.size()
            pos = self.keymap_position[key]
            if pos[0] == 'm':
                x, y = (pos[1] * screen_size[0], pos[2] * screen_size[1])
                win32api.SetCursorPos((int(x), int(y)))
                # pyautogui.click(int(x), int(y))
            elif pos[0] == 'v':
                x, y = win32api.GetCursorPos()
                win32api.SetCursorPos((x + pos[1], y + pos[2]))
            elif pos[0] == 'l':
                x, y = win32api.GetCursorPos()
                pyautogui.click(int(x), int(y), button='right')
            elif pos[0] == 'c':
                x, y = win32api.GetCursorPos()
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

HotkeyInstance = HotkeyProcess()
# print(proc_position)
with keyboard.GlobalHotKeys(HotkeyInstance.proc_position) as h:
    h.join()