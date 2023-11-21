import scipy.stats
import pandas as pd

# read excel
excel_file_path = 'E:\Reserch\PaperAndReading\Shenhua\模拟设置数据.xlsx'
sheet_name = 'analysis'
df = pd.read_excel(excel_file_path, sheet_name=sheet_name, header=None)
# 从DataFrame中提取B4到F4行的数据并存储为数组x
row_data_x = df.iloc[19, 1:5]  # 第四行的索引是3，列范围从B到F是1到6
row_data_y = df.iloc[24, 1:5]

x = row_data_x.values.tolist()
y = row_data_y.values.tolist()

print (x)
print (y)
# print pearson correlation coefficient
print(scipy.stats.pearsonr(x, y)[0])
# print speaman correlation coefficient
print(scipy.stats.spearmanr(x, y)[0])




#import pandas as pd
#import numpy as np
#  
##原始数据
#X1=pd.Series([1, 2, 3, 4, 5, 6])
#Y1=pd.Series([0.3, 0.9, 2.7, 2, 3.5, 5])
#  
##处理数据删除Nan
#x1=X1.dropna()
#y1=Y1.dropna()
#n=x1.count()
#x1.index=np.arange(n)
#y1.index=np.arange(n)
#  
##分部计算
#d=(x1.sort_values().index-y1.sort_values().index)**2
#dd=d.to_series().sum()
#  
#p=1-n*dd/(n*(n**2-1))
#  
##s.corr()函数计算
#r=x1.corr(y1,method='spearman')
#print(r,p) 