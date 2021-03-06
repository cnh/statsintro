import numpy as np
import os
import pandas as pd
from statsmodels.formula.api import glm
from statsmodels.genmod.families import Binomial

# Get the data
dataDir = r'..\Data\data_bayes'
fileName = 'challenger_data.csv'
inFile = os.path.join(dataDir, fileName)
challenger_data = np.genfromtxt(inFile, skip_header=1, usecols=[1, 2],
                                missing_values='NA', delimiter=',')
# Eliminate NaNs
challenger_data = challenger_data[~np.isnan(challenger_data[:, 1])]

# Create a dataframe, with suitable columns for the fit
df = pd.DataFrame()
df['temp'] = np.unique(challenger_data[:,0])
df['failed'] = 0
df['ok'] = 0
df['total'] = 0
df.index = df.temp.values

# Count the number of starts and failures
for ii in range(challenger_data.shape[0]):
    curTemp = challenger_data[ii,0]
    curVal  = challenger_data[ii,1]
    df.loc[curTemp,'total'] += 1
    if curVal == 1:
        df.loc[curTemp, 'failed'] += 1
    else:
        df.loc[curTemp, 'ok'] += 1

# fit the model

# --- >>> START stats <<< ---
model = glm('ok + failed ~ temp', data=df, family=Binomial()).fit()
# --- >>> STOP stats <<< ---

print(model.summary())
