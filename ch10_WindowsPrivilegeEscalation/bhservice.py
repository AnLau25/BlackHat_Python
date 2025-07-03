# Techiniche based on taking advantage of high-privilege processes currently running
# Ussing windows manament instrumentation to monitor the creation of new processes
# With this, we can figure out from what files in the process being created
# Then we interject the file-creation processes and inject the sripting code
# This way, the script will be included in the process and executed

import os
import servicemanager
import shutil
import subprocess
import sys

import win32event
import win32service
import win32serviceutil

SRCDIR = 'C:\\Users\\User\\Documents\\Prog\\BlackHat_Python\\ch10_WindowsPrivilegeEscalation'
TGTDIR = 'C:\\Users\\User\\Documents\\Prog\\BlackHat_Python\\TestFolder'

class BHServerSvc(win32serviceutil.ServiceFramework): # Service skeleton
    _svc_name_ = 'BlackHatService'
    _svc_display_name_ = 'BlackHatService'
    _svc_decription_ = ("Executes VBScripts on reg intervals." + "K podría malir sal? ᕕ( ᐛ )ᕗ")
    
    def __init__(self, args): # Create event; set running location and a time out
        self.vbs = os.path.join(TGTDIR, 'bhservice_task.vbs')
        self.timeout = 1000 * 60
        
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        
    def SvcStop(self): # Set service status and stop service
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
    
    def SvcDoRun(self): # Start service and main where the task will run
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.main()
    
    def main(self):
        while True: # one loop per min
            ret_code = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            
            if ret_code == win32event.WAIT_OBJECT_0: # loops until stop signal received
                servicemanager.LogInfoMsg("Service is stopping")
                break
            
            # In the meantime, grab the script, copy it to target, the delete it
            src = os.path.join(SRCDIR, 'bhservice_task.vbs')
            shutil.copy(src, self.vbs)
            subprocess.call("cscript.exe %s" % self.vbs, shell=False)
            os.unlink()

if __name__=='__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle()
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(BHServerSvc)