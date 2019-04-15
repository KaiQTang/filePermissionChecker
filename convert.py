import os
import glob
import subprocess
import platform
import csv
import pandas as pd

if (platform.system() == 'Windows'):
	print("Platform is Windows...")
	command = 'icacls '
else:
	command = ''
result = {}

print("Gathering information...")
for filename in glob.iglob('./**/*', recursive=True):
	file = os.path.abspath(filename)
	privCheck = command + '"' +file + '"'
	try:
		priv = str(subprocess.check_output(privCheck), 'utf-8')
		priv = priv[len(file):-1].replace(' ', '').splitlines()[:-2]
		priv.sort()
		result[file] = ";".join(priv)
	except:
		print("Error while processing file "+str(file))
		pass

print("Generating CSV file...")
(pd.DataFrame.from_dict(data=result, orient='index')
   .to_csv('dict_file.csv', header=False))
