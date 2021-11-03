'''
Author: your name
Date: 2021-05-24 21:21:23
LastEditTime: 2021-11-03 17:19:40
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /webXray/education_process.py
'''

import pandas as pd 

# xl = pd.ExcelFile('education.xlsx')

# df_denmark = xl.parse("Denmark")  # sheet name

# dk_education_list = df_denmark['Education'].map("https://www.{}".format)

# dk_education_list.to_csv('page_lists/dk_education_list.txt',index = None)

# # 印度

# df_india = xl.parse("India")
# it_education_list = df_india['Education'].map("https://www.{}".format)
# it_education_list.to_csv('page_lists/it_education_list.txt',index = None)

# 美国
# df_America = xl.parse('America')
# us_education_list = df_America['Education'].map("https://www.{}".format)
# us_education_list.to_csv('page_lists/us_education_list.txt',index = None)

import json
import os
id_to_owner = {}
id_to_parent = {}
domain_owners = {}

domain_list = []
id = []
name = []
platform = []
country_list = []
notes = []
uses = []

is_tracker_domain = []
for item in json.load(open(os.path.dirname(os.path.abspath(__file__))+'/webxray/resources/domain_owners/domain_owners.json', 'r', encoding='utf-8')):
    if item['id'] == '-': continue

    # id_to_owner[item['id']] = item['name']
    # id_to_parent[item['id']] = item['parent_id']
    # platform = item['platforms']
    # country = item['country']
    for domain in item['domains']:
        domain_owners[domain] = item['id']
        domain_list.append(domain)
        id.append(item['id'])
        name.append(item['name'])
        platform.append(item['platforms'])
        country_list.append(item['country'])
        notes.append(item['notes'])
        uses.append(item['uses'])
        if "marketing" in item['uses']:
            is_tracker_domain.append("is_tracker")
        else:
            is_tracker_domain.append("no_tracker")
        print(domain,item['id'],item['name'],item['country'],item['notes'],item['uses'])

df = pd.DataFrame({"domain":domain_list, "id":id, "name":name,
"country":country_list,"notes":notes,"uses":uses,"is_tracker_domain":is_tracker_domain})
df.to_csv("trackers_extracted_from_webxray.csv",index = None)
# print(df.head())

# df_domain_1 = pd.read_csv("trackers_domain.csv")

# df_domain_2 = pd.read_csv("trackers_extracted_from_webxray.csv")

# print(df_domain_1['domain'].head())

# df_domain_1_list = df_domain_1['domain'].to_list()


# print(df_domain_2['domain'].head())

# df_domain_2_list = df_domain_2['domain'].to_list()
# print(len(df_domain_1_list))
# print(len(df_domain_2_list))

# print(len(list(set(df_domain_1_list).intersection(set(df_domain_2_list)))))