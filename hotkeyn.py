from pynput import keyboard

def on_activate_h():
    print('<ctrl>+<alt>+h pressed')

def on_activate_i():
    print('<ctrl>+<alt>+i pressed')

keymap_position = {'q' : (0.2, 0.2), 'w' : (0.5, 0.2), 'e' : (0.8, 0.2),
                   'a' : (0.2, 0.5), 's' : (0.5, 0.5), 'd' : (0.8, 0.5),
                   'z' : (0.2, 0.8), 'x' : (0.5, 0.8), 'c' : (0.8, 0.8),
                   '<up>' : (0.5, 0.5), '<ESC>' : (-1, -1)}
proc_position = {}
import win32api
import pyautogui

def factory(key):
    global keymap_position
    def on_activate():
        screen_size = pyautogui.size()
        pos = keymap_position[key]
        x, y = (pos[0] * screen_size[0], pos[1] * screen_size[1])
        win32api.SetCursorPos((int(x), int(y)))
        pyautogui.click(int(x), int(y))

    return on_activate

for key in keymap_position.keys():
    proc_position[f"<ctrl>+<alt>+{key}"] = factory(key)

# print(proc_position)
with keyboard.GlobalHotKeys(proc_position) as h:
    h.join()