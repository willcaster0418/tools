# python serv.py install
import win32serviceutil
import servicemanager
import ctypes
import sys
import time

OutputDebugString = ctypes.windll.kernel32.OutputDebugStringW

class MyServiceFramework(win32serviceutil.ServiceFramework):
    _svc_name_ = 'MyPythonService'
    _svc_display_name_ = 'My Python Service'
    is_running = False

    def SvcStop(self):
        OutputDebugString("MyServiceFramework __SvcStop__")
        self.is_running = False

    def SvcDoRun(self):
        self.is_running = True
        while self.is_running:
            OutputDebugString("MyServiceFramework __loop__")
            time.sleep(1)

if '__main__' == __name__:
    win32serviceutil.HandleCommandLine(MyServiceFramework)
