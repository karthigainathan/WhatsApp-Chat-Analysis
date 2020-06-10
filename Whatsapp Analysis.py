# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:53:49 2020

@author: karth
"""

#---------importing packages---------------
import re
import pandas as pd
import matplotlib.pyplot as plt
import emoji
import numpy as np


#---------reading file---------------
file = open(r"C:\\Users\\karth\\Desktop\\WhatsApp Chat.txt",mode='r',encoding="utf8")
chat = file.read()
file.close()
print(chat)

#---------using regualr expression to find match and sequence from data---------------
# Get date
date_regex=re.compile(r'(\d+/\d+/\d+)')#Match a digit: [0-9]
date=date_regex.findall(chat)
print(date)

# Get time
time_regex=re.compile(r'(\d{1,2}:\d{2} am|pm)') #(\d{1,2}) - captures upto two digits(ie; one or two digits).
time=time_regex.findall(chat)

# Get Users
user_regex=re.compile(r'-(.*?):')
user=user_regex.findall(chat)
  
#\   Used to drop the special meaning of character following it (discussed below)
#[]  Represent a character class
#^   Matches the beginning
#$   Matches the end
#.   Matches any character except newline
#?   Matches zero or one occurrence.
#|   Means OR (Matches with any of the characters separated by it.
#*   Any number of occurrences (including 0 occurrences)
#+   One or more occurrences
#{}  Indicate number of occurrences of a preceding RE to match.
#()  Enclose a group of REs

# Get Message
message_regex=re.compile(r'([^:]+):?$')
me_regex=re.compile(r"(\n)(?<=)(\d+/\d+/\d+)(.*)")
mess=me_regex.findall(chat)
message = [''.join(message_regex.findall(''.join(msg))).strip() for msg in mess]

# Zip date,time,user,message together
data=[]
for w,x,y,z in zip(date,time,user,message):
    data.append([str(w),str(x),str(y),str(z)])
print(data)

# Create DataFrame from joined zip data from above list
df=pd.DataFrame(data,columns=("Date","Time","User","Message"))
print(df)


#-----------------Data Cleaning-------------------------

# Let's clean our Message
df['Message']=df['Message'].str.replace('\'(.*?): ','')

#Date

df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
#df['Date'] = pd.to_datetime(df['Date'])

# Get Day, Month, year from Date
df['Day']=df['Date'].dt.day
df['Month']=df['Date'].dt.month
df['Year']=df['Date'].dt.year

# Message words
df['Words'] = df['Message'].str.strip().str.split('[\W_]+')

# Word length
df['Word Length'] = df['Words'].apply(len)-2

# Get Media shared in the Message
df['Media']=df['Message'].str.contains('<Media omitted>')

# Save the DataFrame to a csv file
df.to_csv("whatsapps.csv")

#Returns the first 5 rows of the dataframe
print(df.head())
#The shape attribute of pandas. DataFrame stores the number of rows and columns as a tuple (number of rows, number of columns)
print(df.shape[0]) 
#To display number of columns
print(df.columns)


#---------------------------------------------------------------------

#Summary by no. of msg by dates
dates=df.groupby('Date')['Date'].count()
print(dates)

#Summary by no. of msg by user 
#message=df.groupby('User')['Message'].count()
#print(message)


#Summary by no. of msg by month
month =df.groupby(['Month'])['Month'].count()
print(month)


#Summary by no. of msg by day
Day=df.groupby('Day')['Day'].count()
print(Day)

#Summary by Message word length and User
char_wordlength=df.groupby(['User'])['Word Length'].sum()
print(char_wordlength)

#counting total no. media
media=df.groupby(['Media'])['Media'].sum()
print(media)


#---------------Plotting Visuals---------------------------

# Total No.of messages by user
plt.style.use('ggplot')
users=df.groupby('User')['Message'].count().nlargest(5)
print(users)
def bar_chart(users):
    ax = users.plot(kind='bar', color = ['limegreen','darkorange','gold', 'yellow', 'red'], fontsize=12)
    ax.seb_ackground_color = 'black'
    ax.set_title("Total No.of messages by user\n", fontsize=16, fontweight='bold')
    ax.set_xlabel("Names", fontsize=10,fontweight='bold')
    ax.set_ylabel("No.of Messages", fontsize=10,fontweight='bold')
    ax.set_facecolor('snow')
    #ax.legend("User Names")
    plt.show('users')
    #plt.savefig('whatsapp.png')
bar_chart(users)


# No. of Messages by Month
message=df.groupby('Month')['Message'].count()
plt.style.use('ggplot')
message=df.groupby('Month')['Message'].count()
def line_chart(message):
    ax = message.plot(kind='line', color = ['deeppink'], fontsize=12)
    ax.seb_ackground_color = 'black'
    ax.set_title("No. of Messages by Month\n", fontsize=16, fontweight='bold')
    ax.set_xlabel("Month", fontsize=10,fontweight='bold')
    ax.set_ylabel("No.of Messages", fontsize=10,fontweight='bold')
    ax.set_facecolor('snow')
    #ax.legend("User Names")
    plt.show('message')
    #plt.savefig('whatsapp.png')
line_chart(message)


#count emoji
#message=df.groupby('User')['Message'].count().nlargest(5)
def extract_emojis(message):
    emojis=[]
    for string in df['Message']:
        my_str = str(string)
        for each in my_str:
            if each in emoji.UNICODE_EMOJI:
                emojis.append(each)
    return emojis

emoji_dict={}
for keys in message.keys():
    print(keys)
    emoji_dict[keys] = extract_emojis(keys)
    emoji_df = pd.DataFrame(emoji_dict[keys])
    print(emoji_df[0].value_counts()[:10])
    

#count of media per user
media_df=df[df['Media']==True]
media_per_user_group=media_df.groupby(['User'])['Media'].count().nlargest(4)
print(media_per_user_group)
def media_shared_pie(media_per_user_group):
    fig, ax = plt.subplots()
    explode=[]
    for i in np.arange(len(media_per_user_group)):
        explode.append(0)
    ax = media_per_user_group.plot(kind='pie', colors = ['limegreen','darkorange','gold','red'], explode=explode, fontsize=10, autopct='%1.1f%%', startangle=180)
    ax.axis('equal')  
    ax.set_title(" No. of Media shared by Users\n", fontsize=18)
    plt.show()
media_shared_pie(media_per_user_group)


#count of text msg per user
media_df=df[df['Media']==False]
media_per_user_group=media_df.groupby(['User'])['Media'].count().nlargest(4)
print(media_per_user_group)
def media_shared_pie(media_per_user_group):
    fig, ax = plt.subplots()
    explode=[]
    for i in np.arange(len(media_per_user_group)):
        explode.append(0)
    ax = media_per_user_group.plot(kind='pie', colors = ['limegreen','darkorange','gold','red'], explode=explode, fontsize=10, autopct= '%1.1f%%', startangle=180)
    ax.axis('equal')  
    ax.set_title("No. of Text Message by Users\n", fontsize=18)
    plt.show()
media_shared_pie(media_per_user_group)

 
#count of media per user
plt.style.use('ggplot')
media_per_user_group=media_df.groupby(['User'])['Media'].count().nlargest(4)
print(media_per_user_group)

def bar_chart(users):
    ax = media_per_user_group.plot(kind='barh', color = ['limegreen','darkorange','gold', 'yellow', 'red'], fontsize=12)
    ax.seb_ackground_color = 'black'
    ax.set_title("No. of Media shared by Users\n", fontsize=16, fontweight='bold')
    ax.set_xlabel("Names", fontsize=10,fontweight='bold')
    ax.set_ylabel("No.of Messages", fontsize=10,fontweight='bold')
    ax.set_facecolor('snow')
    #ax.legend("User Names")
    plt.show('media_per_user_group')
    #plt.savefig('whatsapp.png')
bar_chart(media_per_user_group)




