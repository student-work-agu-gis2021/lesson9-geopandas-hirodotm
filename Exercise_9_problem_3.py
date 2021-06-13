#!/usr/bin/env python
# coding: utf-8

# ## Problem 3: How long distance individuals have travelled? 
# 
# In this problem the aim is to calculate the "distance" in meters that the individuals have travelled according the social media posts (Euclidean distances between points). In this problem, we will need the `userid` -column an the points created in the previous problem. You will need the shapefile `Kruger_posts.shp` generated in Problem 2 as input file.
# 

# YOUR CODE HERE 1 to read data
import geopandas as gpd
from pyproj import CRS
import os

#read the shapely file
input_fp = os.path.join("Kruger_posts.shp")
data=gpd.read_file(input_fp)

# - Check the crs of the input data. If this information is missing, set it as epsg:4326 (WGS84).
# - Reproject the data from WGS84 to `EPSG:32735` -projection which stands for UTM Zone 35S (UTM zone for South Africa) to transform the data into metric system. (don't create a new variable, update the existing variable `data`!)"

# YOUR CODE HERE 2 to set crs
#set crs
data=data.to_crs(epsg=32735)
# CODE FOR TESTING YOUR SOLUTION

# Check the data
print(data.head())

# CODE FOR TESTING YOUR SOLUTION

# Check that the crs is correct after re-projecting (should be epsg:32735)
print(data.crs)


#  - Group the data by userid

#  YOUR CODE HERE 3 to group 
#grouping
grouped=data.groupby('userid')

# CODE FOR TESTING YOUR SOLUTION

#Check the number of groups:
assert len(grouped.groups) == data["userid"].nunique(), "Number of groups should match number of unique users!"


# **Create LineString objects for each user connecting the points from oldest to latest:**
# 

# YOUR CODE HERE 4 to set movements
import pandas as pd
from shapely.geometry import LineString, Point
#set movements
movements=pd.DataFrame()
movements['geometry']=None
data=data.sort_values(['userid','timestamp'])
geometry=[]
t=data['userid'].min(axis=0)
p=[]
u=[]
u.append(t)
for idx,row in data.iterrows():
  p.append(row['geometry'])
  if t!=row['userid']:
    if len(p)>1:
      geometry.append(LineString(p))
    if len(p)<=1:
      geometry.append(Point(p[0]))
    t=row['userid']
    u.append(t)
    p=[]
datat=data[data['userid']==t]
for idx,row in datat.iterrows():
  p.append(row['geometry'])
if len(p)>1:
  geometry.append(LineString(p))
if len(p)<=1:
  geometry.append(Point(p[0]))
movements['userid']=u
movements['geometry']=geometry
movements = gpd.GeoDataFrame(movements,geometry='geometry',crs=CRS.from_epsg(32735).to_wkt())

# CODE FOR TESTING YOUR SOLUTION

#Check the result
print(type(movements))
print(movements.crs)
print(movements["geometry"].head())


# **Finally:**
# - Check once more the crs definition of your dataframe (should be epsg:32735, define the correct crs if this information is missing)
# - Calculate the lenghts of the lines into a new column called ``distance`` in ``movements`` GeoDataFrame.

# YOUR CODE HERE 5 to calculate distance
#calculate distance
movements['distance']=None
dist=[]
for idx,row in movements.iterrows():
  if type(row['geometry'])==LineString:
    dist.append(row['geometry'].length)
  if type(row['geometry'])==Point:
    dist.append(0)
movements['distance']=dist

# CODE FOR TESTING YOUR SOLUTION

#Check the output
print(movements.head())


# You should now be able to print answers to the following questions: 
# 
#  - What was the shortest distance travelled in meters?
#  - What was the mean distance travelled in meters?
#  - What was the maximum distance travelled in meters?

# YOUR CODE HERE 6 to find max, min,mean of the distance.
#sarch some dustance
datat=movements[movements['distance']>0]
min=datat['distance'].min(axis=0)
max=datat['distance'].max(axis=0)
mean=datat['distance'].mean(axis=0)


# - Finally, save the movements of into a Shapefile called ``some_movements.shp``

# YOUR CODE HERE 7 to save as Shapefile
fp = 'some_movements.shp'
outpath = os.path.join(fp)
movements.to_file(outpath)
# CODE FOR TESTING YOUR SOLUTION



#Check if output file exists
assert os.path.isfile(fp), "Output file does not exits."


# That's all for this week!
#check length
def func7():
    return data

#check type
def func8():
    return grouped 

#check crs
def func9():
    return movements

#check movements['distance']
def func10():
    return movements
