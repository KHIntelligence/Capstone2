
# coding: utf-8

# # Coursera Captsone
# This will mainly be used for the coursera capstone project. with longLat data.

# In[1]:


import pandas as pd
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from pandas.io.json import json_normalize


# In[2]:


#Scrape website 

#set URL to Search, get HTML of page
url = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M"
html = urlopen(url)

#pass html into beautifulSoup and create beautifulsoup object named soup
soup = BeautifulSoup(html, 'lxml')

#check if the text looks good by print(text)
text = soup.get_text()

#find all within page you have scraped
table = soup.find("table", class_="wikitable sortable")


#print(table.prettify)


# In[3]:


#The dataframe will consist of three columns: PostalCode, Borough, and Neighborhood

df = pd.read_html(str(table))[0]
df.columns = df.iloc[0]
df.drop(df.index[0], inplace=True)
df.head(10)


# In[4]:


#Only process the cells that have an assigned borough. Ignore cells with a borough that is Not assigned.
df2 = df[df.Borough != "Not assigned"]

df2.head(10)


# If a cell has a borough but a Not assigned neighborhood, then the neighborhood will be the same as the borough. So for the 9th cell in the table on the Wikipedia page, the value of the Borough and the Neighborhood columns will be Queen's Park.

# In[5]:


#Replace a neighbourhood that is "not assigned with the value of the borough column
df2.Neighbourhood[df2.Neighbourhood == 'Not assigned'] = df.Borough
df2.head()


# More than one neighborhood can exist in one postal code area. For example, in the table on the Wikipedia page, you will notice that M5A is listed twice and has two neighborhoods: Harbourfront and Regent Park. These two rows will be combined into one row with the neighborhoods separated with a comma as shown in row 11 in the above table.

# In[6]:


#Group based on Postcode and borough
df3 = df2.groupby(["Postcode", "Borough"])['Neighbourhood'].apply(list)
df4 = df3.to_frame().reset_index()

#Convert list to string to remove brackets
df4['Neighbourhood'] = [', '.join(map(str, l)) for l in df4['Neighbourhood']]
df4.head(10)


# Clean your Notebook and add Markdown cells to explain your work and any assumptions you are making.
# In the last cell of your notebook, use the .shape method to print the number of rows of your dataframe.

# In[7]:


df4.shape


# ## Next step - Importing Geocode data

# In[12]:


#Wasnt happy with the integrity of data using the Geocode import- using CSV instead
pc_data = pd.read_csv('Geospatial_Coordinates.csv')
pc_data.head()


# In[19]:


pd_full = pd.merge(df4, pc_data, left_on='Postcode', right_on='Postal Code')
pdfinal = pd_full.drop(['Postal Code'], axis=1)
pdfinal.head(10)

