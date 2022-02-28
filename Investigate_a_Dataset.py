#!/usr/bin/env python
# coding: utf-8

# 
# 
# # Project: Investigate a Dataset (No-show appointments)
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# I analysed a dataset for this project and presented my results. NumPy, Pandas, and Matplotlib are
# Python libraries that I used to conduct the research.
# This Python script is used to investigate no-show appointments data for Project 2 of Udacity's
# Data Analyst Nanodegree.
# Data Wrangling was done first, then the data was cleaned in preparation for Exploratory Data
# Analysis.
# 

# # DATASET:
# This dataset is based on data from 100k Brazilian medical appointments and focuses on whether
# or not patients turn up for their appointments. Each row contains a number of characteristics
# about the patient.
# 
# variables:<br>
# • PatientId<br>
# • AppointmentID<br>
# • Gender<br>
# • ScheduledDay<br>
# • AppointmentDay<br>
# • Age<br>
# • Neighbourhood<br>
# • Scholarship<br>
# • Hipertension<br>
# • Diabetes<br>
# • Alcoholism<br>
# • Handcap<br>
# • SMS_received<br>

# ## Questions to answer :
# 1- Who in terms of age misses more appointments?  <br>
# 2- Are no-show appointments associated with a certain gender? <br>
# 3- What is the percentage of show-up and no-show rate?<br>
# 4- What is the percentage of MALE and FEMALE rate patient?  <br>
# 5- How many patients received SMS and how many patients did not receive SMS?<br>
# 6- Do SMS reminders decrease the number of absences?

# In[1]:


# Use this cell to set up import statements for all of the packages that you
#   plan to use.
import numpy as np
import pandas as pd
import matplotlib as plt
import seaborn as sns

# Remember to include a 'magic word' so that your visualizations are plotted
#   inline with the notebook. See this page for more:
#   http://ipython.readthedocs.io/en/stable/interactive/magics.html
get_ipython().run_line_magic('matplotlib', 'inline')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# 
# 
# ### General Properties

# In[2]:


# Load your data and print out a few lines. Perform operations to inspect data
#   types and look for instances of missing or possibly errant data.
df = pd.read_csv("noshowappointments.csv")
df.head()


# In[3]:


#check NAN Data
df.isnull().sum()


# In[4]:


#Data describtion
df.describe()


# In[5]:


#shape of data
df.shape


# In[6]:


#histogram all numerical data
df.hist(figsize=(20,20));


# In[7]:


fig, ax = plt.pyplot.subplots(figsize=(15,10))
sns.heatmap(df.corr(), ax=ax, annot=True);


# In[8]:


#check duplicates
sum(df.duplicated())


# In[9]:


#check if there is negative value in Age
df.Age.min()


# # Data Cleaning (Replace this with more specific notes!)
# ### Now my data is loaded, I will make the following steps:
# - there is no NAN value to change. <br>
# - check if there is a negative value of age, then drop it. <br>
# - I will create binning function to cut age column, or distribute ages to categories. <br>
# - create a new column describe which category of ages for each patient.

# In[10]:


# After discussing the structure of the data and any problems that need to be
#   cleaned, perform those cleaning steps in the second part of this section.

#get the index of negative age
df.query('Age == "-1"')


# In[11]:


#delete the negative Age
df.drop(index= 99832 , inplace= True)


# In[12]:


#check shape to make sure we delete this row
df.shape


# In[13]:


#chick min age
df.Age.min()


# In[14]:


#binning function to cut age column

def binning(data, cut_points, label=None):
    # min and max values
    mi = data.min()
    ma = data.max()
    
    #list of min and max to cut_points
    break_points = [mi] + cut_points + [ma]
    
    #Binning using cut function of pandas
    data_Bin = pd.cut(data, bins = break_points, labels = label, include_lowest = True)
    return data_Bin

#Binning age:
cut_points = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
label = ["child","teen","adult","40s", "50s", "60s", "70s", "80s", "90s", "100s", "above_100"]
df["Age_Bin"] = binning(df["Age"], cut_points, label)
print(pd.value_counts(df["Age_Bin"], sort = False))


# In[15]:


df.head()


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# 
# ### Research Question 1:
# Who in terms of age misses more appointments? 

# In[16]:


# Use this, and more code cells, to explore your data. Don't forget to add
#   Markdown cells to document your observations and findings.

df["Age_Bin"] = binning(df["Age"], cut_points, label)
df.groupby(['No-show' , 'Age_Bin']).size()


# We can calculate the number of patients who not turn up for appointments by plotting only the Age variable.

# In[17]:


# Plot the histogram
ax = df['Age'].plot(kind='hist')
ax.set_xticks(cut_points)
ax.set_xticklabels(label, rotation= 60, )

# Set histogram labels
plt.pyplot.xlabel('Age Group', fontsize= 20)
plt.pyplot.ylabel('Number of Patients', fontsize=20)
plt.pyplot.xlim([0, 120])

# use the magic word to show the bar graph
plt.pyplot.show()


# # answer:
# Patients in their childhood and 60s years did not show up for appointments in large numbers.

# ### Research Question 2 
# Are no-show appointments associated with a certain gender?

# In[18]:


# Continue to explore the data to address your additional research
#   questions. Add more headers as needed if you have more questions to
#   investigate.
df.groupby(['No-show','Gender']).size()


# In[30]:


# Set pie chart properties
labels ='No Show-Male','No Show-Female','Show-Male',  'show-Female' 
cut_points = [ 7725, 14594, 30962 , 57245]

plt.pyplot.pie(cut_points , labels = labels, autopct='%1.1f%%');


# # answer:
# 51.8% of patients are SHOWED female , but 13.2% are NO-SHOWED female  <br>
# 28% of patients are SHOWED male , but 7% are NO-SHOWED male  <br>

# # Research Question 3
# 
# (What is the percentage of show-up and no-show rate?)
# 

# In[20]:


df["No-show"].value_counts()


# In[21]:


plt.pyplot.pie([88207,22319] , labels = ["Show" , "No-Show"], autopct='%1.1f%%');


# # answer:
# 
# 79.8% of patients are SHOWED , but 20.2% are NO SHOWED 
# 

# # Research Question 4
# What is the percentage of MALE and FEMALE rate patient?
# 

# In[22]:


df['Gender'].value_counts()


# In[23]:


plt.pyplot.pie([71839,38687] , labels = ["Female" , "Male"], autopct='%1.1f%%');


# # answer:
# 65% of patients are Females , but 35% are Males 

# # Research Question 5
# How many patients received SMS and how many patients did not receive SMS?

# In[24]:


df['SMS_received'].value_counts()


# In[25]:


plt.pyplot.pie([75044,35482] , labels = ["Don't receive SMS" , "received SMS"], autopct='%1.1f%%');


# 
# # answer:
# 67.9% of patient don't receive SMS , but 32.1% are received 

# # Research Question 6
# Do SMS reminders decrease the number of absences?

# In[26]:


df.groupby(['No-show','SMS_received']).size()


# In[29]:


count= [62509,62509,62509,9784]
title_pie = ["show, Don't receive" , "show, received" , "No-show, Don't receive" , "No-show, received"]

plt.pyplot.pie(count , labels = title_pie, autopct='%1.1f%%');


# # answer:
# 31.7% of patient are No-Show & received SMS  <br>
# 31.7% of patient are Showed & Don't receive SMS  <br>
# 5% of patient are Showed & received SMS  <br>
# 31.7% of patient are No-Show & Don't receive SMS  <br>
# 
# When compared to patients who got SMS and showed up, there is a high number of patients who did not receive SMS and did not show up.

# <a id='conclusions'></a>
# ## Conclusions
# 
# #### results:
# -  79.8% of patients are SHOWED , but 20.2% are NO SHOWED.  <br>
# -  Patients in their childhood and 60s years did not show up for appointments in large numbers. <br>
# -  51.8% of patients are NO-SHOWED female , but 13.2% are SHOWED female <br>
#    28% of patients are NO-SHOWED male , but 7% are SHOWED male <br>
# -  65% of patients are Females , but 35% are Males. <br>
# -  67.9% of patient don't receive SMS , but 32.1% are received. <br>
# -  31.7% of patient are No-Show & received SMS  <br>
#    31.7% of patient are Showed & Don't receive SMS  <br>
#    5% of patient are Showed & received SMS  <br>
#    31.7% of patient are No-Show & Don't receive SMS  <br>
# 
#    When compared to patients who got SMS and showed up, there is a high number of patients who did not receive SMS and did not show up. <br>
# 
# 
# 
# ## Submitting your Project 
# 
# 

# In[58]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])


# In[ ]:




