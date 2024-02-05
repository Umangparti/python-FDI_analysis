#!/usr/bin/env python
# coding: utf-8

# # Project-4 FDI Analysis

# In[1]:


# Submitted by: Umang Parti
# Submitted to: Unified Mentor


# In[2]:


# importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import FileLink


# In[3]:


# importing data
fdi_df = pd.read_csv(r"C:\Users\umang\Desktop\unified mentor\project - 4\FDI data.csv")
print(fdi_df.head())


# # Exploratory Analysis

# In[4]:


print(fdi_df.shape)


# In[5]:


fdi_df.info()


# In[6]:


fdi_df.isnull().sum()


# In[7]:


# check duplicated data 
fdi_df.duplicated().sum()


# - We have 63 sectors and 17 years of data
# - Only 1 column containing sectors in Object Others are Float
# - Our data neither has any null values nor duplicate records

# # Descriptive Analysis

# In[8]:


print(fdi_df.describe().T)


# - We notice that Mean FDI rose significantly from 37 in 2000-01 to 690 in 2016-17
# - We Maximum FDI is 8684 in the year 2016-17
# - The Median Value ie 50th percentile is less than Mean value for all years dipicting that data is Negatively skewed.

# # Sector-Wise Analysis of Total FDI

# In[9]:


# copying the columns in new table
fdi_df_total= fdi_df.copy()


# In[10]:


# selecting the columns
fdi_columns = fdi_df.columns[1:]
fdi_columns


# In[11]:


# create a new column of total and average
fdi_df_total['Total'] = fdi_df_total[fdi_columns].sum(axis=1)
fdi_df_total['Average'] = fdi_df_total[fdi_columns].mean(axis=1)
print(fdi_df_total)


# In[12]:


# plotting bar graph
plt.figure(figsize=(12, 6))
plt.bar(fdi_df_total['Sector'], fdi_df_total['Total'], color='blue')
plt.title('Total FDI Across Sectors',fontsize=18)
plt.xlabel('Sectors')
plt.ylabel('Total FDI Amount')
plt.xticks(rotation=90, ha='right')
plt.savefig('my_chart.png')
plt.show()


# In[13]:


FileLink(r'my_chart.png')


# In[14]:


# plotting bar graph
plt.figure(figsize=(12, 6))
plt.bar(fdi_df_total['Sector'], fdi_df_total['Average'], color='blue')
plt.title('Average FDI Across Sectors',fontsize=18)
plt.xlabel('Sectors')
plt.ylabel('Average FDI Amount')
plt.xticks(rotation=90, ha='right')
plt.savefig('my_chart2.png')
plt.show()


# In[15]:


FileLink(r'my_chart2.png')


# In[16]:


fdi_df_total = fdi_df_total.sort_values(by='Total', ascending=False)
fdi_df_total


# In[17]:


# Plotting a pie chart of top 15 sectors
plt.figure(figsize=(16,16))
plt.pie(fdi_df_total['Total'].head(15), labels=fdi_df_total['Sector'].head(15),
        autopct='%1.1f%%', startangle=140)
plt.title('Distribution of FDI Across Top 15 Sectors',fontsize=24)
plt.savefig('my_chart3.png')
plt.show()


# In[18]:


FileLink(r'my_chart3.png')


# In[19]:


fdi_df_trans = fdi_df.set_index('Sector').T


# In[20]:


# Box Plot
plt.figure(figsize=(12, 6))
sns.boxplot(data=fdi_df_trans)
plt.title('Sector-wise FDI Comparison Across Years')
plt.xlabel('Sectors')
plt.ylabel('FDI Amount')
plt.xticks(rotation=90, ha='right')
plt.savefig('my_chart4.png')
plt.show()


# In[21]:


FileLink(r'my_chart4.png')


# - We notice that Service Sector has highest Total FDI as well as Average FDI 
# - Through the bar graph we also notice that approx 15 Sectors are the top performing ones, In order to analyse them we create a pie chart.
# - We notice that among those top 15 Sectors Service Sector contributes around 23% of FDI followed by Computer, Construction, Telecom, Automobile, Drugs, Trading, and Chemicals
# - We use boxplot to compare among the sectors

# # Sector-Wise Growth Rate

# In[22]:


fdi_df_trans_growth = fdi_df_trans.pct_change() * 100


# In[23]:


plt.figure(figsize=(20, 16))
for sector in fdi_df_trans_growth.columns:
    plt.plot(fdi_df_trans_growth.index, fdi_df_trans_growth[sector], label=sector)
plt.title('Sector-wise Growth Rates Over Years',fontsize=20)
plt.xlabel('Financial Year')
plt.ylabel('Growth Rate (%)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='best', borderaxespad=0.)
plt.savefig('my_chart5.png')
plt.show()


# In[24]:


FileLink(r'my_chart5.png')


# In[25]:


# Calculate standard deviation or coefficient of variation for each sector
sector_std = fdi_df.std(axis=1)
sector_cv = fdi_df.std(axis=1) * 100  / fdi_df.mean(axis=1)
print(sector_cv, sector_cv.max(), sector_cv.mean())


# In[26]:


# Define a threshold for consistency
consistency_threshold_1 = 200
consistency_threshold_2 = 100


# In[27]:


# Identify sectors with consistently high or low FDI values
high_fdi_sectors_index = sector_cv[sector_cv > consistency_threshold_1].index
consistent_fdi_sectors_index = sector_cv[(sector_cv > consistency_threshold_2) & (sector_cv < consistency_threshold_1)].index
low_fdi_sectors_index = sector_cv[sector_cv < consistency_threshold_2].index
high_fdi_sectors_index,consistent_fdi_sectors_index,low_fdi_sectors_index


# In[28]:


high_fdi_sectors = fdi_df_trans.iloc[:, high_fdi_sectors_index]
print("high FDI sectors: ", high_fdi_sectors.columns.tolist())


# In[29]:


consistent_fdi_sectors = fdi_df_trans.iloc[:, high_fdi_sectors_index]
print("Consistent FDI Sectors: ", consistent_fdi_sectors.columns.tolist())


# In[30]:


low_fdi_sectors = fdi_df_trans.iloc[:, low_fdi_sectors_index]
print("Low FDI Sectors:", low_fdi_sectors.columns.tolist())


# - After plotting the graph it wasn't much clear about which sector grew by how much
# - So, we create a threshold to find consistent, High and Low FDI performing Sectors
# - high FDI sectors: 'COAL PRODUCTION', 'PORTS', 'MATHEMATICAL,SURVEYING AND DRAWING INSTRUMENTS', 'PHOTOGRAPHIC RAW FILM AND PAPER', 'DYE-STUFFS', 'SUGAR', 'FOOD PROCESSING INDUSTRIES', 'GLUE AND GELATIN', 'DEFENCE INDUSTRIES', 'RETAIL TRADING', 'AGRICULTURE SERVICES'
# - Consistent FDI Sectors: 'COAL PRODUCTION', 'PORTS', 'MATHEMATICAL,SURVEYING AND DRAWING INSTRUMENTS', 'PHOTOGRAPHIC RAW FILM AND PAPER', 'DYE-STUFFS', 'SUGAR', 'FOOD PROCESSING INDUSTRIES', 'GLUE AND GELATIN', 'DEFENCE INDUSTRIES', 'RETAIL TRADING', 'AGRICULTURE SERVICES'
# - Low FDI Sectors:'METALLURGICAL INDUSTRIES', 'POWER', 'ELECTRONICS', 'AUTOMOBILE INDUSTRY', 'INDUSTRIAL MACHINERY', 'MACHINE TOOLS', 'COMMERCIAL, OFFICE & HOUSEHOLD EQUIPMENTS', 'TEXTILES (INCLUDING DYED,PRINTED)', 'CONSULTANCY SERVICES', 'SERVICES SECTOR (Fin.,Banking,Insurance,Non Fin/Business,Outsourcing,R&D,Courier,Tech. Testing and Analysis, Other)', 'MISCELLANEOUS INDUSTRIES'

# # Comparative Analysis

# In[31]:


fdi_df_compare=fdi_df_total.head(9)
fdi_df_compare=fdi_df_compare.drop(columns=['Total','Average'])
fdi_df_compare=fdi_df_compare.set_index('Sector').T
fdi_df_compare


# In[32]:


# Subplots
plt.figure(figsize=(16, 8))
plt.subplots_adjust(wspace=0.5,hspace=0.5)
plt.suptitle('Comparative Analysis of top 9 Sectors',fontsize=20)

plt.subplot(3, 3, 1)
plt.plot(fdi_df_compare.index, fdi_df_compare['SERVICES SECTOR (Fin.,Banking,Insurance,Non Fin/Business,Outsourcing,R&D,Courier,Tech. Testing and Analysis, Other)'], label='SERVICES SECTOR (Fin.,Banking,Insurance,Non Fin/Business,Outsourcing,R&D,Courier,Tech. Testing and Analysis, Other)')
plt.title('Service Sector Performance Over Years')
plt.xlabel('Financial Years')
plt.ylabel('FDI Amount')
plt.gca().axes.get_xaxis().set_ticks([])
plt.gca().axes.get_xaxis().set_ticklabels([])

plt.subplot(3, 3, 2)
plt.plot(fdi_df_compare.index, fdi_df_compare['COMPUTER SOFTWARE & HARDWARE'], label='COMPUTER SOFTWARE & HARDWARE')
plt.title('Computer Sector Performance Over Years')
plt.xlabel('Financial Years')
plt.ylabel('FDI Amount')
plt.gca().axes.get_xaxis().set_ticks([])
plt.gca().axes.get_xaxis().set_ticklabels([])

plt.subplot(3, 3, 3)
plt.plot(fdi_df_compare.index, fdi_df_compare['CONSTRUCTION DEVELOPMENT: Townships, housing, built-up infrastructure and construction-development projects'], label='CONSTRUCTION DEVELOPMENT: Townships, housing, built-up infrastructure and construction-development projects')
plt.title('Construction Sector Performance Over Years')
plt.xlabel('Financial Years')
plt.ylabel('FDI Amount')
plt.gca().axes.get_xaxis().set_ticks([])
plt.gca().axes.get_xaxis().set_ticklabels([])

plt.subplot(3, 3, 4)
plt.plot(fdi_df_compare.index, fdi_df_compare['TELECOMMUNICATIONS'], label='TELECOMMUNICATIONS')
plt.title('Telecom Sector Performance Over Years')
plt.xlabel('Financial Years')
plt.ylabel('FDI Amount')
plt.gca().axes.get_xaxis().set_ticks([])
plt.gca().axes.get_xaxis().set_ticklabels([])

plt.subplot(3, 3, 5)
plt.plot(fdi_df_compare.index, fdi_df_compare['AUTOMOBILE INDUSTRY'], label='AUTOMOBILE INDUSTRY')
plt.title('Automobile Sector Performance Over Years')
plt.xlabel('Financial Years')
plt.ylabel('FDI Amount')
plt.gca().axes.get_xaxis().set_ticks([])
plt.gca().axes.get_xaxis().set_ticklabels([])

plt.subplot(3, 3, 6)
plt.plot(fdi_df_compare.index, fdi_df_compare['DRUGS & PHARMACEUTICALS'], label='DRUGS & PHARMACEUTICALS')
plt.title('Pharma Sector Performance Over Years')
plt.xlabel('Financial Years')
plt.ylabel('FDI Amount')
plt.gca().axes.get_xaxis().set_ticks([])
plt.gca().axes.get_xaxis().set_ticklabels([])

plt.subplot(3, 3, 7)
plt.plot(fdi_df_compare.index, fdi_df_compare['TRADING'], label='TRADING')
plt.title('Trading Sector Performance Over Years')
plt.xlabel('Financial Years')
plt.ylabel('FDI Amount')
plt.gca().axes.get_xaxis().set_ticks([])
plt.gca().axes.get_xaxis().set_ticklabels([])

plt.subplot(3, 3, 8)
plt.plot(fdi_df_compare.index, fdi_df_compare['CHEMICALS (OTHER THAN FERTILIZERS)'], label='CHEMICALS (OTHER THAN FERTILIZERS)')
plt.title('Chemical Sector Performance Over Years')
plt.xlabel('Financial Years')
plt.ylabel('FDI Amount')
plt.gca().axes.get_xaxis().set_ticks([])
plt.gca().axes.get_xaxis().set_ticklabels([])

plt.subplot(3, 3, 9)
plt.plot(fdi_df_compare.index, fdi_df_compare['POWER'], label='POWER')
plt.title('Power Sector Performance Over Years')
plt.xlabel('Financial Years')
plt.ylabel('FDI Amount')
plt.gca().axes.get_xaxis().set_ticks([])
plt.gca().axes.get_xaxis().set_ticklabels([])

plt.savefig('my_chart6.png')
plt.show()


# In[33]:


FileLink(r'my_chart6.png')


# - We notice that some sectors like Power were already at a rise during 2000s but fell and then grew in 2007
# - Sectors like Service, Construction, and Pharma saw a high sudden increase during years 2007-09
# - Sectors like Telecom, Computer, and Automobile grew slowly and gradually
# - Sector like Trading grew much later.
# - We also observe that in 2017 sectors like Telecom, Service, Chemical and Power are rising 
# - While Sectors like Trading, Automobile, Computer, and Construction are falling

# # Year- Wise (Time Series) Analysis

# In[34]:


fdi_trans_columns = fdi_df_trans.columns[0:]


# In[35]:


fdi_df_trans['Total']=fdi_df_trans[fdi_trans_columns].sum(axis=1)
fdi_df_trans=fdi_df_trans.drop(columns=fdi_trans_columns)
fdi_df_trans


# In[36]:


# Total FDI and its change over time
fdi_df_trans.plot(figsize=(10, 6))
plt.title('FDI Over Time for all Sectors')
plt.xlabel('Year')
plt.ylabel('FDI Amount')
plt.savefig('my_chart7.png')
plt.show()


# In[37]:


FileLink(r'my_chart7.png')


# - We notice that overall FDI of India in total for all sectors has risen with a great amount from 2000-01 to 2016-17
# - We notice that it rose most significantly in 2007-2009
# - Though it fell during 2010-11 and increased during 2011-12 fell again in 2013-14. But is constantly rising since then which is a positive growth sign.

# In[38]:


# Thank You

