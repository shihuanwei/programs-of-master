import pandas as pd
import numpy as np
  
#原始数据
x= pd.Series([3,1,2,2,1,3])
y= pd.Series([1,2,3,2,1,1])
r = x.corr(y,method="kendall") 