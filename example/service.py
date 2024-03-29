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
        self.main()

    def main(self):
        logging.info(' ** Hello PyWin32 World ** ')
        # Simulate a main loop
        while self.stop_requested == False:
            if keyboard.read_key() == "p":
                logging.info("You pressed p")
        return

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(HelloWorldSvc)