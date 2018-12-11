import subprocess
import sys
import time

p = subprocess.Popen(['python', 'queryCX.py'], stdout=subprocess.PIPE)
time.sleep(30)
p.terminate()

