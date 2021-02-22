import scrapper as gs
import numpy as np
import pandas as pd
import os

path = os.getcwd() + '/chromedriver.exe'

'''Configuration'''
configFile = open('config.txt', 'r')
config = configFile.readlines()
job = config[0].rstrip()
csv_file = config[1].rstrip()

df = gs.get_jobs(job, 1000, False, path, 15)
df.to_csv(csv_file, index=False)
