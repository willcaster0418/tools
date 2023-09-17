# put in system env
# C:\Users\tosang\anaconda3
# C:\Users\tosang\anaconda3\Scripts
# sc delete HelloWorld-Service

import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time
import logging
import keyboard
logging.basicConfig(
    filename = 'c:\\Temp\\hello-service.log',
    level = logging.DEBUG, 
    format = '[helloworld-service] %(levelname)-7.7s %(message)s'
)
from collections import namedtuple

KeyboardEvent = namedtuple('KeyboardEvent', ['event_type', 'key_code',
                                             'scan_code', 'alt_pressed',
                                             'time'])

handlers = []
is_running = True
def listen():
    global is_running, handlers
    """
    Calls `handlers` for each keyboard event received. This is a blocking call.
    """
    # Adapted from http://www.hackerthreads.org/Topic-42395
    from ctypes import windll, CFUNCTYPE, POINTER, c_int, c_uint, c_void_p, byref
    import win32con, win32api, win32gui, atexit

    event_types = {win32con.WM_KEYDOWN: 'key down',
                   win32con.WM_KEYUP: 'key up',
                   0x104: 'key down', # WM_SYSKEYDOWN, used for Alt key.
                   0x105: 'key up', # WM_SYSKEYUP, used for Alt key.
                  }

    def low_level_handler(nCode, wParam, lParam):
        """
        Processes a low level Windows keyboard event.
        """
        event = KeyboardEvent(event_types[wParam], lParam[0], lParam[1],
                              lParam[2] == 32, lParam[3])
        for handler in handlers:
            handler(event)

        # Be a good neighbor and call the next hook.
        return windll.user32.CallNextHookEx(hook_id, nCode, wParam, lParam)
       
    # Our low level handler signature.
    CMPFUNC = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
    # add argtypes for 64-bit Python compatibility (per @BaiJiFeiLong)
    windll.user32.SetWindowsHookExW.argtypes = (
        c_int,
        c_void_p, 
        c_void_p,
        c_uint
    )
    # Convert the Python handler into C pointer.
    pointer = CMPFUNC(low_level_handler)

    print(win32api.GetModuleHandle(None))
    # Hook both key up and key down events for common keys (non-system).
    hook_id = windll.user32.SetWindowsHookExA(win32con.WH_KEYBOARD_LL, pointer,
                                             c_void_p(win32api.GetModuleHandle(None)), 0)

    # Register to remove the hook when the interpreter exits. Unfortunately a
    # try/finally block doesn't seem to work here.
    atexit.register(windll.user32.UnhookWindowsHookEx, hook_id)

    while is_running:
        msg = win32gui.GetMessage(None, 0, 0)
        win32gui.TranslateMessage(byref(msg))
        win32gui.DispatchMessage(byref(msg))

class HelloWorldSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "HelloWorld-Service"
    _svc_display_name_ = "HelloWorld Service"
    
    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.stop_event = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)
        self.stop_requested = False

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        logging.info('Stopping service ...')
        self.stop_requested = True

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_,'')
        )
        def print_event(e):
            global is_running
            logging.info(e)

        handlers.append(print_event)
        listen()

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(HelloWorldSvc)