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
engine = create_engine(db_uri, echo = True)

#________*_________*_________*_________*_________*_________*_________*_________*

df = pd.read_csv("data/S2802.csv", na_values = ["-"])
df = df.astype({"fips_id": "object"})
dt = df.dtypes[1:20]
print(f'data types of top 20 columns: {dt}')

#________*_________*_________*_________*_________*_________*_________*_________*
#Get LatLon
latlon = pd.read_csv("data/fips_latlon.csv")

#Merge on fips_code
newdf = df.merge(latlon, how="inner", left_on=["id","fips_id"], right_on=["GEO_ID","StateTractCode"])

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
newdf.to_sql("s2802", con=engine, if_exists="replace", index_label=None)

#To SQL fcc
fcc_df.to_sql("fcc", con=engine, if_exists="replace", index_label=None)


#Test
engine.execute("SELECT * FROM s2802 LIMIT 2").fetchall()
engine.execute("SELECT * FROM fcc LIMIT 2").fetchall()