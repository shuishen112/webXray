'''
Author: Zhan
Date: 2021-05-18 20:16:37
LastEditTime: 2021-05-25 16:16:42
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /webXray/clustering.py
'''



import pandas as pd 
import numpy as np 
import json

def split_col(data, columns):
    '''拆分成列

    :param data: 原始数据
    :param columns: 拆分的列名
    :type data: pandas.core.frame.DataFrame
    :type columns: list
    '''
    for c in columns:
        new_col = data.pop(c)
        max_len = max(list(map(lambda x:len(x) if isinstance(x, list) else 1, new_col.values)))  # 最大长度
        new_col = new_col.apply(lambda x: x+[None]*(max_len - len(x)) if isinstance(x, list) else [x]+[None]*(max_len - 1))  # 补空值，None可换成np.nan
        new_col = np.array(new_col.tolist()).T  # 转置
        for i, j in enumerate(new_col):
            data[c + str(i)] = j


def split_row(data, column):
    '''拆分成行

    :param data: 原始数据
    :param column: 拆分的列名
    :type data: pandas.core.frame.DataFrame
    :type column: str
    '''
    row_len = list(map(len, data[column].values))
    rows = []
    for i in data.columns:
        if i == column:
            row = np.concatenate(data[i].values)
        else:
            row = np.repeat(data[i].values, row_len)
        rows.append(row)
    return pd.DataFrame(np.dstack(tuple(rows))[0], columns=data.columns)


file_name = 'in_top_1000'

df = pd.read_csv("reports/{}/3p_domains.csv".format(file_name)).dropna()
df = df.drop('owner_lineage',axis = 1)

# 需要将数据中的list string 转换为list
def convert_list_to_string(row):
    s = row.replace('\'','"')
    return json.loads(s)
df['owner_uses_list'] = df['owner_uses'].apply(convert_list_to_string)
df['owner_platforms_list'] = df['owner_platforms'].apply(convert_list_to_string)

# data = df[['owner_uses_list','owner_platforms_list']].dropna()
print(len(df))
df = split_row(df,column='owner_uses_list')
df = split_row(df,column = 'owner_platforms_list')

# preprocessing the dataset

country_dump = pd.get_dummies(df['owner_country'])
owner_uses_dump = pd.get_dummies(df['owner_uses_list'])
owner_platforms_dump = pd.get_dummies(df['owner_platforms_list'])



domain_set = pd.concat([df['percent_total'],country_dump,owner_uses_dump,owner_platforms_dump],axis = 1)
print(domain_set.head())

# normalization
from sklearn import preprocessing
values = domain_set.values
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(values)
cluster_scaled = pd.DataFrame(x_scaled, columns = domain_set.columns)

print(cluster_scaled.head())

# reduce the dimension of features 

from sklearn.decomposition import PCA
pca = PCA(2)
print(cluster_scaled.shape)
pca_data = pca.fit_transform(cluster_scaled)
print(pca_data.shape)

from sklearn.cluster import KMeans
import numpy as np 


# clustering

num_clusters = 9

kmeans = KMeans(num_clusters)
kfit = kmeans.fit(pca_data)
identified_clusters = kfit.predict(pca_data)


u_labels = np.unique(identified_clusters)


# data_view

view_list = ['percent_total','owner','owner_country','owner_uses_list','owner_platforms_list']
clustered_data_scaled = df.copy()[view_list]
print(clustered_data_scaled.columns)
clustered_data_scaled['Cluster'] = identified_clusters

# 获得中心
centroids = kmeans.cluster_centers_
cen_x = [i[0] for i in centroids]
cen_y = [i[1] for i in centroids]

# add to df 
clustered_data_scaled['cen_x'] = clustered_data_scaled.Cluster.map(lambda x: cen_x[x])
clustered_data_scaled['cen_y'] = clustered_data_scaled.Cluster.map(lambda y: cen_y[y])
print(centroids.shape)


colors = ['#DF2020', '#81DF20', '#2095DF']



df_sort = clustered_data_scaled.sort_values(by = 'Cluster')

for i in u_labels:
    print(df_sort[df_sort['Cluster'] == i])



# plot the pictures
import matplotlib.pyplot as plt 
import numpy as np 

# plt.scatter(cen_x,cen_y,marker='^',s = 70)
for i in u_labels:
    plt.scatter(pca_data[identified_clusters == i, 0],pca_data[identified_clusters == i, 1],label = i,alpha=0.6,s = 10)

# # plot lines
# for idx,val in clustered_data_scaled.iterrows():
#     x = [pca_data[idx][0], val.cen_x]
#     y = [pca_data[idx][1], val.cen_y]
#     plt.plot(x,y,label = idx)

# 输出文件
del df_sort['cen_x']
del df_sort['cen_y']
df_sort.to_csv('reports/{}/cluster_{}.csv'.format(file_name,file_name.split('_')[0]))

# plt.legend()
plt.savefig(file_name + '_clustering')
plt.show()