import os
import subprocess
import sys

#This file is for testing the setup and teardown of the docker container for testing

cwd = os.getcwd()
pathToSetupScript = cwd + "\setup_test.ps1"
pathToTeardownScript = cwd + "\\tear_down_test.ps1"

print ("path to poweshell startup script: "+pathToSetupScript)
print ("path to poweshell teardown script: "+pathToSetupScript)

#Code for unix example
# p=subprocess.Popen( pathToSetupScriptCleaned,  shell=True)
# p.wait

#Code for windows
p=subprocess.Popen(['powershell.exe', "-File", pathToSetupScript],  stdout=sys.stdout)
p.wait()
p.kill()

t=subprocess.Popen(['powershell.exe', "-File", pathToTeardownScript],  stdout=sys.stdout)
t.wait()
t.kill()