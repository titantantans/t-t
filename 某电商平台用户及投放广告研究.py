# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 01:04:51 2020

@author: user
"""

import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import pyecharts as pe
import matplotlib.pyplot as plt
import matplotlib.style as psl
psl.use('ggplot')
import os
os.chdir('D:\\数据分析\\某电商平台研究')
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']

df=pd.read_excel('D:/数据分析/某电商平台研究/advertisement_user.xlsx')
df1=pd.read_excel('D:/数据分析/某电商平台研究/product_price.xlsx')

#将年龄层次字段与其代表的年龄层次匹配字段一一匹配好
df['年龄层次匹配']='未知'
df['年龄层次匹配'][df['年龄层次']==0]='18岁及以下'
df['年龄层次匹配'][df['年龄层次']==1]='19-25岁'
df['年龄层次匹配'][df['年龄层次']==2]='26-30岁'
df['年龄层次匹配'][df['年龄层次']==3]='31-35岁'
df['年龄层次匹配'][df['年龄层次']==4]='36-40岁'
df['年龄层次匹配'][df['年龄层次']==5]='41-50岁'
df['年龄层次匹配'][df['年龄层次']==6]='51岁及以上'

#将城市层次消费档次性别字段中的空值填充为'未知'
#在此可以构建一个函数
def drop_data_na(df,col):
    '''
    输入一dataframe及其要填充得字段名
    '''
    df[col].fillna('未知',inplace=True)
drop_data_na(df,'城市层级')
drop_data_na(df,'消费档次')
drop_data_na(df,'性别')

#研究'年龄层次匹配','城市层级','消费档次','性别'四个字段的用户画像

#获取数据
a=['年龄层次匹配','城市层级','消费档次','性别']
attr=[]
y=[]
for i in a:
    attri=df[i].value_counts().index.tolist()
    yi=df[i].value_counts().values.tolist()
    attr.append(attri)
    y.append(yi)
    
#在一个页面显示4张饼图
pie=pe.Pie('某平台用户年龄层次、城市层级、消费档次、性别画像研究环形图',title_pos='center',height=600,width=1000)
pie.add('年龄层次',attr[0],y[0],radius=[25,35],center=[30,30],is_legend_show=False,is_label_show=True)
pie.add('城市层级',attr[1],y[1],radius=[25,35],center=[75,30],is_legend_show=False,is_label_show=True)
pie.add('消费档次',attr[2],y[2],radius=[25,35],center=[30,75],is_legend_show=False,is_label_show=True)
pie.add('性别情况',attr[3],y[3],radius=[25,35],center=[75,75],is_legend_show=False,is_label_show=True)
pie.render('某平台用户画像研究环形图.html')

#将df跟df1用商品类别id连接一起
data=pd.merge(df,df1,how='left',on='商品类别id')

#将时间戳-Bigint转化成时间序列
data['时间']=pd.to_datetime(data['时间戳-Bigint']+28800,unit='s',origin='unix')
#制作气泡图
#研究广告投放上的规律
dt=data[['时间','广告id','年龄层次','商品价格','年龄层次匹配']]
dt.dropna(inplace=True)
dt.set_index('时间',inplace=True)
dd=dt.groupby([dt.index.hour,dt['年龄层次匹配']]).agg({
        '广告id':'count',
        '商品价格':'mean',
        '年龄层次':'min'})
#重新设置一下index
lst_hour=[]
lst_age=[]
for i in dd.index:
    lst_hour.append(i[0])
    lst_age.append(i[1])
dd['年龄']=lst_age
dd['时间点']=lst_hour
dd.reset_index(drop=True,inplace=True)
#画图
plt.figure(figsize=(12,8))
plt.scatter(x=dd['时间点'],#x轴为广告投放时间点
            y=dd['广告id'],#y轴为广告的频率
            s=dd['商品价格'].values*0.05,#气泡越大价格越贵
            c=dd['年龄层次'].values,#颜色越深年龄越大
            cmap='Blues',
            marker='o',
            alpha=0.8,
            linewidths=0.3,
            edgecolors='Black')
plt.xlabel('时间(小时)')
plt.xticks(list(range(0,25)))
plt.ylabel('广告频率')
plt.colorbar()
plt.savefig('广告投放时间、频率、价格及投放人群年龄段关系图.png')













