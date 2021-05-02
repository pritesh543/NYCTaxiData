#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os
import mysql.connector
import sys

args = sys.argv
year = args[1]
month = args[2]

# db connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="kty3<2og2xq5J",
  database="nyc_database"
)

# fetching trip data

#df_taxi_data = pd.read_csv('green_tripdata_2019-01.csv')
mycursor = mydb.cursor()
q_taxi_data = """ SELECT PULocationID, DOLocationID, passenger_count FROM nyc_taxi_data WHERE YEAR(lpep_pickup_datetime)='{year}' AND MONTH(lpep_pickup_datetime)='{month}' """.format(year=year, month=month)
mycursor.execute(q_taxi_data)

# fetching zone lookup data
myresult = mycursor.fetchall()
df_taxi_data = pd.DataFrame(myresult, columns=["PULocationID", "DOLocationID", "passenger_count"])
#df_taxi_data.insert(0, "Month", year+"-"+month)
#df_taxi_data.head()

#df_taxi_zones = pd.read_csv("taxi+_zone_lookup.csv")
q_zone_lookup = """ select LocationID, Zone FROM taxi_zone_lookup """
mycursor.execute(q_zone_lookup)
myresult_taxi = mycursor.fetchall()
df_taxi_zones = pd.DataFrame(myresult_taxi, columns=["LocationID", "Zone"])
#df_taxi_zones.head()

df_taxi_data = df_taxi_data[df_taxi_data['PULocationID'].notna()]
df_taxi_data = df_taxi_data[df_taxi_data['DOLocationID'].notna()]
df_dest = df_taxi_data[["DOLocationID", "PULocationID", "passenger_count"]].groupby(["DOLocationID","PULocationID"]).agg("sum").reset_index()
#df_dest[(df_dest["DOLocationID"]==49) & (df_dest["PULocationID"]==97)]

# pickup zone mapping
df_pickup_zones = pd.merge(df_dest, df_taxi_zones, left_on=["PULocationID"], right_on=["LocationID"], how="left").drop(columns=['LocationID'])
df_pickup_zones = df_pickup_zones.rename(columns = {'Zone':'Pickup_Zone'})

# destination zone mapping
df_dest_zones = pd.merge(df_pickup_zones, df_taxi_zones, left_on=["DOLocationID"], right_on=["LocationID"], how="left").drop(columns=['LocationID','DOLocationID','PULocationID'])
df_dest_zones = df_dest_zones.rename(columns = {'Zone':'Destination_Zone'})

# top 10 
df_dest_zones.sort_values(['Pickup_Zone','passenger_count'], ascending=[True, False], inplace=True)
df_final = df_dest_zones.groupby("Pickup_Zone").head(10).reset_index(drop=True)
#df_final.head()

# ranking 
df_final['Rank'] = df_final.groupby('Pickup_Zone')['passenger_count'].rank(ascending=False).astype(int)
del df_final["passenger_count"]
df_final.insert(0, "Month", year+"-"+month)
#df_final.head(20)

# inserting the popular trip in the database
q_popular_trip = """ INSERT INTO nyc_popular_trips (trip_month,trip_pickup_zone,trip_destination_zone,trip_rank) 
values('%s', '%s', '%s', %d) """
for row in df_final[:5].itertuples():
    #print(q_popular_trip % (str(row.Month), str(row.Pickup_Zone), str(row.Destination_Zone), row.Rank))
    mycursor.execute(q_popular_trip % (row.Month, row.Pickup_Zone, row.Destination_Zone, row.Rank))
mydb.commit()

#process completed
