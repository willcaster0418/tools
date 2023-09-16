from pynput import keyboard
keymap_position = {'q' : ('m', 0.2, 0.2), 'w' : ('m', 0.5, 0.2), 'e' : ('m', 0.8, 0.2),
                   'a' : ('m', 0.2, 0.5), 's' : ('m', 0.5, 0.5), 'd' : ('m', 0.8, 0.5),
                   'z' : ('m', 0.2, 0.8), 'x' : ('m', 0.5, 0.8), 'c' : ('m', 0.8, 0.8),
                   '1' : ('s', 1, 0), '2' : ('s', 2, 0)}
proc_position = {}
import win32api
import pyautogui
import win32gui
def factory(key):
    global keymap_position
    def on_activate():
        screen_size = pyautogui.size()
        pos = keymap_position[key]
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

for key in keymap_position.keys():
    proc_position[f"<ctrl>+<alt>+{key}"] = factory(key)

# print(proc_position)
with keyboard.GlobalHotKeys(proc_position) as h:
    while True:
        #h.join()
        h.run()
        print("h.run()")
        break
    h.stop()