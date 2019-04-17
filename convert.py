import os
import glob
import subprocess
import platform
import csv
import pandas as pd
import sys

result = {}
if (platform.system() == 'Windows'):
	print("Platform is Windows...")
	command = 'icacls '
	print("Gathering information...")
	for filename in glob.iglob('./**/*', recursive=True):
		file = os.path.abspath(filename)
		privCheck = command + '"' + file + '"'
		try:
			priv = str(subprocess.check_output(privCheck), 'utf-8')
			priv = priv[len(file):-1].replace(' ', '').splitlines()[:-2]
			priv.sort()
			result[file] = ";".join(priv)
		except:
			print("Error while processing file " + str(file))
			print("Error Message : " + str(sys.exc_info()[0]))
			pass
else:
	print("Platform is Linux...")
	print("Gathering information...")
	for filename in glob.iglob('./**/*', recursive=True):
		file = os.path.abspath(filename)
		try:
			priv = str(subprocess.check_output(['ls', '-al', file]), 'utf-8')
			priv = priv.split("\n")
			if (priv[0][0] == 't'):
				priv = priv[1]
			else:
				priv = priv[0]
			priv = priv.split(" ")[0]
			result[file] = priv
		except:
			print("Error while processing file " + str(file))
			print("Error Message : " + str(sys.exc_info()[0]))
			pass


print("Generating CSV file...")
(pd.DataFrame.from_dict(data=result, orient='index')
   .to_csv('dict_file.csv', header=False))

