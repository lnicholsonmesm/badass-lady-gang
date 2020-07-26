# SQLAlchemy
from sqlalchemy import create_engine

# Imports the methods needed to abstract classes into tables
from sqlalchemy.ext.declarative import declarative_base

# Allow us to declare column types
from sqlalchemy import Table, Column, Integer, String, Float, MetaData

#pandas for data manipulation and export
import pandas as pd

#________*_________*_________*_________*_________*_________*_________*_________*
db_uri = "sqlite:///db.sqlite"
#engine = create_engine(db_uri, echo = True)
engine = create_engine(db_uri, echo = False)

#________*_________*_________*_________*_________*_________*_________*_________*

census = pd.read_csv("data/S2802.csv", na_values = ["-"])
census = census.astype({"fips_id": "object"})
census["county_name"] = [x.replace(" ", "") for x in census["county_name"]]
census["state"] = [x.replace(" ", "") for x in census["state"]]
dt = census.dtypes[1:10] 
print(f'data types of top 10 columns: {dt}')

#________*_________*_________*_________*_________*_________*_________*_________*
#Get LatLon
latlon = pd.read_csv("data/fips_latlon.csv")

#________*_________*_________*_________*_________*_________*_________*_________*
#Get Region
region = pd.read_csv("data/region.csv")
dt = region.dtypes
print(f'region data types are: {dt}')
#________*_________*_________*_________*_________*_________*_________*_________*
#Merge Region on County
df_reg = census.merge(region, how="inner", left_on="county_name", right_on="CountyName")

#Merge Coordinates on fips_code
census_df = df_reg.merge(latlon, how="inner", left_on=["id","fips_id"], right_on=["GEO_ID","StateTractCode"])
print(census_df)
#________*_________*_________*_________*_________*_________*_________*_________*
#Get FCC
fcc = pd.read_csv("data/fcc_data.csv") #, na_values = ["-"]
fcc = fcc.astype({"tract": "object"})

#subset columns
fcc_df = fcc[["dbaname","hocofinal","stateabbr","blockcode", "tract", "techcode","consumer","maxaddown","maxadup"]]
fcc_df
dt = fcc_df.dtypes
print(f"fcc dtypes: {dt}")

#________*_________*_________*_________*_________*_________*_________*_________*
# To SQL census
census_df.to_sql("census", con=engine, if_exists="replace", index_label=None)

#To SQL fcc
fcc_df.to_sql("fcc", con=engine, if_exists="replace", index_label=None)

#Test
print(engine.execute("SELECT * FROM census LIMIT 2").fetchall())
print(engine.execute("SELECT * FROM fcc LIMIT 2").fetchall())