import pandas as pd
import numpy as np

x = pd.DataFrame([[1,np.nan,2, 1],[1,np.nan,np.nan, 2]])
print(x.transpose())
print(x.transpose().corr())
print(x.where(x == np.nan, 0.5))
print(x)