import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import bq_helper
import cartopy
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
from bq_helper import BigQueryHelper

def gsodquery(year,stations, db):
    var2 = 'bigquery-public-data.noaa_gsod.gsod'+str(year)
    query = f"""
            SELECT 
                stn AS Station_number, 
                year AS Year, 
                mo AS Month, 
                AVG(temp) as Mean_temp
            FROM 
                {var2} 
            WHERE 
                Stn in {stations}
            GROUP BY
                stn, 
                year, 
                mo
        """
    return db.query_to_pandas_safe(query, max_gb_scanned=10)

def mapplot():
    
    shapename = 'admin_1_states_provinces_lakes'
    states_shp = shpreader.natural_earth(resolution='50m',category='cultural', name=shapename)
    fig = plt.figure(figsize = (10,10))
    ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.LambertConformal())
    #ax.set_extent([-119, -64, 22, 49], ccrs.Geodetic()) #only plot US map
    ax.set_extent([-121, -72, 21, 50], ccrs.Geodetic()) #only plot US map

    #ax.outline_patch.set_visible(False) #need to find solution to this, depreciated


    for astate in shpreader.Reader(states_shp).records():
        #try:
            # use the name of this state to get pop_density
        geo = [astate.geometry]

            #if astate.attributes['name'] == 'Alaska':
             #   geo = list(map(lambda x: shapely.affinity.scale(x, xfact=0.3, yfact=0.45), [astate.geometry]))
             #   geo = list(map(lambda x: shapely.affinity.translate(x,xoff=40, yoff=-35), geo))
            #if astate.attributes['name'] == 'Hawaii':
             #   geo = list(map(lambda x: shapely.affinity.translate(x,xoff=53, yoff=6), geo))
        #except:
         #   continue

        #`astate.geometry` is the polygon to plot
        ax.add_geometries(geo, ccrs.PlateCarree(),
                          color = 'white', edgecolor='black')
    