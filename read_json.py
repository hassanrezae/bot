#!/usr/bin/env python
# coding: utf-8

# In[149]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import os, sys, datetime
import json
from IPython.display import Javascript


# In[181]:


mpl.rcParams['agg.path.chunksize'] = 10000 


# In[182]:


def read_data(username):
    # profile info
    file_name = "/home/vahid/data/output/"+ username+ "_getProfileOverTimeData.json"
    try:
        with open(file_name) as f:
            data_profile = json.load(f)
    except:
        data_profile = -1

    # posts info
    file_name = "/home/vahid/data/output/"+ username+ "_postsData.json"
    try:
        with open(file_name) as f:
            data_posts = json.load(f)
    except:
        data_posts = -1

    # posts list
    file_name = "/home/vahid/data/output/"+ username+ "_profileData.json"
    try:
        with open(file_name) as f:
            data_post_list = json.load(f)
    except:
        data_post_list = -1
    
    return (data_profile, data_posts, data_post_list)


# In[196]:


def save_list_of_post(username, data_post_list):
    # save list of posts into file
    if data_post_list != -1 :
        _path = "/home/vahid/data/post_list/"
        os.mkdir(_path+ username)
        with open(_path+username+'/post_lists.txt','w') as f:
          f.write('\n'.join(data_post_list['postLists']))


# In[191]:


def create_date(data_posts):
    # daily date
    if data_posts != -1:
        start = datetime.datetime.fromisoformat(list(data_posts.keys())[0].split(' ')[0])
        end = datetime.datetime.fromisoformat(list(data_posts.keys())[-1].split(' ')[0])

        date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
        date_generated = [datetime.datetime.isoformat(d).split('T')[0] for d in date_generated]

        return date_generated
    else:
        return -1


# In[192]:


def create_dir_fig(username):
    _path = "/home/vahid/Documents/reports/insta/"+ username
    os.mkdir(_path)
    return _path


# In[193]:


def create_save_fig(date_generated, data_posts, _path):
    # counting post per day
    if data_posts != -1 :
        count_list = list()
        for i in range(len(date_generated)):
            temp_dic = {k:v for k, v in data_posts.items() if k.startswith(date_generated[i])}
            count_list.append(len(temp_dic))
        # plotting
        fig, ax = plt.subplots(figsize=(20, 12), dpi=200)
        ax.tick_params(axis="x", labelrotation=30)
        ax.plot(date_generated, count_list, '-b*')
        ax.set_xticks(date_generated[::2])
        ax.set_ylabel("number of posts")
        ax.set_title("Post/day of "+ username)

        plt.savefig(_path+ "/counting_posts.png")
        plt.close()

        # ----------------------------------------------

        # max like and comment per day
        like_list = list()
        name_max_like = list()
        comment_list = list()
        name_max_comment = list()
        for i in range(len(date_generated)):
            temp_dict = {k:v for k,v in data_posts.items() if k.startswith(date_generated[i])}
            if len(temp_dict) > 0:
                #_min = min(temp_dict.keys(), key=lambda x:temp_dict[x][0]['like'])
                _max = max(temp_dict.keys(), key=lambda x:int(temp_dict[x][0]['like']))
                #like_list.append((int(temp_dict[_min][0]['like'])+int(temp_dict[_max][0]['like']))/count_list[i])
                like_list.append(int(temp_dict[_max][0]['like']))
                name_max_like.append(temp_dict[_max][0]['name'])

                #_min = min(temp_dict.keys(), key=lambda x:temp_dict[x][0]['comment'])
                _max = max(temp_dict.keys(), key=lambda x:int(temp_dict[x][0]['comment']))
                #comment_list.append((int(temp_dict[_min][0]['comment'])+int(temp_dict[_max][0]['comment']))/count_list[i])
                comment_list.append(int(temp_dict[_max][0]['comment']))
                name_max_comment.append(temp_dict[_max][0]['name'])
            else:
                like_list.append(0)
                name_max_like.append(0)
                comment_list.append(0)
                name_max_comment.append(0)
        
        # finding name of most liked and most commented
        # plotting
        # max like/day
        fig, ax = plt.subplots(figsize=(20,12), dpi=200)
        ax.tick_params(axis="x", labelrotation=30)
        ax.plot(date_generated, like_list, '-g*')
        ax.set_xticks(date_generated[::2])
        ax.set_xticklabels(date_generated[::2])
        ax.set_title("max number of like/day of "+ username)
        ax.set_ylabel("max like")
        
        new_like = list()
        new_date = list()
        new_name = list()
        index_sort = np.array(like_list).argsort()
        index_sort = index_sort[::-1]
        for i in index_sort:
            new_like.append(like_list[i])
            new_date.append(date_generated[i])
            new_name.append(name_max_like[i])

        for x, y, z in zip(new_date[0:10], new_like[0:10], new_name[0:10]):
            label = str(z)
            plt.annotate(label, (x,y), 
                         textcoords="offset points", 
                         xytext=(0,10), ha='center',
                         rotation=90) 

        plt.savefig(_path+ "/max_like.png")
        plt.close()

        fig, ax = plt.subplots(figsize=(20,12), dpi=200)
        ax.tick_params(axis="x", labelrotation=30)
        ax.plot(date_generated, comment_list, '-c*')
        ax.set_xticks(date_generated[::2])
        ax.set_xticklabels(date_generated[::2])
        ax.set_title("max number of comment/day of "+ username)
        ax.set_ylabel("max comment")
        
        new_comment = list()
        new_date = list()
        new_name = list()
        index_sort = np.array(comment_list).argsort()
        index_sort = index_sort[::-1]
        for i in index_sort:
            new_comment.append(comment_list[i])
            new_date.append(date_generated[i])
            new_name.append(name_max_comment[i])

        for x, y, z in zip(new_date[0:10], new_comment[0:10], new_name[0:10]):
            label = str(z)
            plt.annotate(label, (x,y), 
                         textcoords="offset points", 
                         xytext=(0,10), ha='center',
                         rotation=90) 


        plt.savefig(_path+ "/max_comment.png")
        plt.close()


# In[197]:


all_usernames = pd.read_csv("/home/vahid/data/username1.txt").values.reshape(-1).tolist()


# In[198]:


for username in all_usernames:
    username = str(username)
    data_profile, data_posts, data_post_list = read_data(username)
    save_list_of_post(username, data_post_list)
    _path = create_dir_fig(username)
    date_generated = create_date(data_posts)
    create_save_fig(date_generated, data_posts, _path)


