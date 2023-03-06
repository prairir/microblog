import os
import subprocess
import sys
import unittest

class LoginFeatureTests(unittest.TestCase):
	def setUp(self):
		cwd = os.getcwd()
		pathToSetupScript = cwd + "\setup_test.ps1"
		p=subprocess.Popen(['powershell.exe', "-File", pathToSetupScript],  stdout=sys.stdout)
		p.wait()
		p.kill()
	
	def tearDown(self):
		cwd = os.getcwd()
		pathToTeardownScript = cwd + "\\tear_down_test.ps1"
		t=subprocess.Popen(['powershell.exe', "-File", pathToTeardownScript],  stdout=sys.stdout)
		t.wait()
		t.kill()

	def test_selenium(self):
		self.assertFalse(False)
		

if __name__ == '__main__':
    unittest.main(verbosity=2)