import matplotlib.pyplot as plt
import seaborn as sns
import database
import numpy as np
import folium
from folium import plugins
from folium.plugins import HeatMap
import pandas as pd



def crimecode_data_bar(crimecodes):
   plt.rcParams["figure.autolayout"] = True
   fig, ax = plt.subplots(1,1)
   #hide the axes
   fig.patch.set_visible(False)
   ax.axis('tight')
   ax.axis('off')
   table = ax.table(cellText=crimecodes.values, colLabels=crimecodes.columns, loc='center')
   table.auto_set_font_size(False)
   table.set_fontsize(10)


def least_crime_committing_bar(least_crimes):
   figure = least_crimes.plot(x = 'Race', y = 'number_of_crimes', kind = 'bar')
   return figure

def types_of_crimes_count(count_of_crimes):
   df_number_of_crimes = count_of_crimes
   cp = sns.countplot(data = df_number_of_crimes, y = "Description", hue = "CountOfCrimes", width = 30)
   return cp 

def crimes_by_location_graph():
   crime_location_data = [['1500 RUSSELL ST',39.2741,-76.6276, 1],
   ['200 E PRATT ST',39.2866,-76.6121, 0.9989],
   ['2400 FREDERICK AVE',39.284,-76.6549,0.9959],
   ['2400 LIBERTY HEIGHTS AVE',39.3186,-76.654, 0.9700],
   ['0 LIGHT ST', 39.288,-76.6137, 0.9789],
   ['6300 EASTERN AVE', 39.2876,-76.5399, 0.8859],
   ['3500 BOSTON ST', 39.277,-76.5674, 0.7759],
   ['300 LIGHT ST', 39.2851,-76.6131, 0.6709],
   ['3200 TIOGA PKWY', 39.3182,-76.6584, 0.6059],
   ['300 E MADISON ST',39.2999,-76.5851, 0.5000],
   ['0 MARKET PL', 39.2883,-76.6067, 0.4459],
   ['400 E BALTIMORE ST', 39.2898,-76.6101, 0.4409],
   ['600 E PRATT ST', 39.2868,-76.6077, 0.3359],
   ['1800 ORLEANS ST', 39.2953,-76.5913, 0.3309],
   ['1600 PENNSYLVANIA AVE', 39.3034,-76.6346, 0.2259],
   ['1200 W PRATT ST', 39.2855,-76.6376, 0.2229],
   ['2400 W BELVEDERE AVE', 39.2856,-76.6367, 0.2159],
   ['600 E 33RD ST', 39.3282,-76.6084, 0.2139],
   ['2400 N CHARLES ST',39.3164,-76.6168, 0.1100],
   ['200 W CHASE ST', 39.3014,-76.6197, 0.1100]]
                        

   df_for_map = pd.DataFrame(crime_location_data, columns=['locations', 'latitude', 'longitude', 'brightness'])

   #plotting a heatmap displaying the 20 locations with high crime rate 
   #this heat has a reducing gadient effect depending upon the level of crime rate
   data_for_map = [[row['latitude'],row['longitude'], row['brightness']] for index, row in df_for_map.iterrows()]
   baltimore_map = folium.Map(location=[39.3121, -76.6198], zoom_start=11)
   HeatMap(data_for_map).add_to(baltimore_map)
   return baltimore_map
   
def more_details_by_loc_graph(more_details_crime_loc):
   x = more_details_crime_loc['times']
   y = more_details_crime_loc['Description']
   plt.rcParams['figure.figsize'] = (15, 30)
   plt.title('1500 RUSSELL ST')
   plt.legend = 'none'
   plt.stackplot(x,y)

def inside_outside_scatterplot(df):
   sns.set_theme(style = "white", palette = "muted")

   df_crime_by_loc = df

   ax = sns.swarmplot(data = df_crime_by_loc, x = "YearOfCrime", y = "Inside_Outside",
                     hue = "Description").set(title = "Crimes occurred in '1500 RUSSELL ST'")

   return ax

def male_female_heatmap(df):
   sns.set_theme()

   df_criminals_by_age = df

   trimmed_df = df_criminals_by_age.pivot("Location", "Age", "Criminals_Age")

   #Draw a heatmap with the numeric values in each cell
   f, ax = plt.subplots(figsize = (9,6))
   hm = sns.heatmap(trimmed_df, linewidths = .5, ax = ax, annot = True).set(title = "Criminals Age and Location")

   return hm
