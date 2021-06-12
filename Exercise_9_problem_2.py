#!/usr/bin/env python
# coding: utf-8

# ## Problem 2: Points to map
#
# In this problem we continue to learn how to turn latitude and longitude coordinates in to geometries.
#

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
# YOUR CODE HERE 1 to read data
#read the csv file
data = pd.read_csv("data/some_posts.csv")
geometry = []
for idx, row in data.iterrows():
    point = Point(row['lon'], row['lat'])
    geometry.append(point)
data['geometry'] = geometry
# CODE FOR TESTING YOUR SOLUTION

# Check the result
print("Number of rows:", len(data))

# CODE FOR TESTING YOUR SOLUTION

# Check the result
print(data['geometry'].head())

# YOUR CODE HERE 2
from pyproj import CRS

# Convert DataFrame into a GeoDataFrame

geo = gpd.GeoDataFrame(data,
                       geometry='geometry',
                       crs=CRS.from_epsg(4326).to_wkt())

# CODE FOR TESTING YOUR SOLUTION

# Check the geodataframe head
print("Number of rows:", len(geo))
print(geo.head())

# CODE FOR TESTING YOUR SOLUTION

# Check that the output file exists
import os
#save geo to 'Kruger_posts.shp'
fp = 'Kruger_posts.shp'
outpath = os.path.join(fp)
geo.to_file(outpath)

assert os.path.isfile(fp), "output shapefile does not exist"

# **Finally:**
# - **Create a simple map of the points** using the `plot()` -funtion.

# YOUR CODE HERE 3
import matplotlib.pyplot as plt

geo.plot()
plt.show()

# Well done! Now you can move on to Exercise_9_problem_3.


def func5():
    return data


def func6():
    return geo
