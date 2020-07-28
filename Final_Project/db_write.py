# SQLAlchemy
from sqlalchemy import create_engine

# Allow us to declare column types
from sqlalchemy import Table, Column, Integer, String, Float, MetaData

#pandas for data manipulation and export
import pandas as pd
import numpy as np
#________*_________*_________*_________*_________*_________*_________*_________*
#connect to SQLite Database
db_uri = "sqlite:///db.sqlite"
engine = create_engine(db_uri, echo = False)
#________*_________*_________*_________*_________*_________*_________*_________*
#Get Census
census = pd.read_csv("data/S2802.csv", na_values = ["-"])
census = census.astype({"fips_id": "object"})
census["county_name"] = [x.replace(" ", "") for x in census["county_name"]]
census["state"] = [x.replace(" ", "") for x in census["state"]]

#________*_________*_________*_________*_________*_________*_________*_________*
#Get LatLon
latlon = pd.read_csv("data/fips_latlon.csv")

#________*_________*_________*_________*_________*_________*_________*_________*
#Get Region
region = pd.read_csv("data/region.csv")

missingcol = pd.read_csv("data/missingcol.csv")
pd.merge(census, region, left_on="county_name", right_on="CountyName")

#________*_________*_________*_________*_________*_________*_________*_________*
#Merge missing column, on fips_code
df_col = census.merge(missingcol, how="inner", on="fips_id")

#Merge Region on County
df_reg = df_col.merge(region, how="inner", left_on="county_name", right_on="CountyName")

#Merge Coordinates on fips_code
census_df = df_reg.merge(latlon, how="inner", left_on=["id","fips_id"], right_on=["GEO_ID","StateTractCode"])
census_df.iloc[0,10:50]
#census_df.PE_Computer_Broadband_Household
print(census_df.E_Computer_Broadband_Household)
#________*_________*_________*_________*_________*_________*_________*_________*
##Full FCC ----NOTE: NOT USED!
# Get FCC
fcc = pd.read_csv("data/fcc_data.csv") #, na_values = ["-"]
fcc = fcc.astype({"tract": "object"})

#subset columns
fcc_subset = fcc[["dbaname","hocofinal","stateabbr","blockcode", "tract", "techcode","consumer","maxaddown","maxadup"]]

#get county/region names for fcc
region_subset = census_df[["CountyName", "Region", "Latitude", "Longitude", "fips_id"]]

#Merge county/regions with fcc data
fcc_df = fcc_subset.merge(region_subset, how="left", left_on="tract", right_on="fips_id")

#this one is not really needed:
fcc_by_tract = pd.read_csv("data/fcc_bytract.csv")
fcc_by_tract.to_sql("fcc_tracts",  con=engine, if_exists="replace", index_label=None)

#________*_________*_________*_________*_________*_________*_________*_________*
filtered_fcc = pd.read_csv("data/fcc_region_broadband_bySpeed.csv")
#________*_________*_________*_________*_________*_________*_________*_________*
#TO SQL

#FCC Data "fcc" to SQL
filtered_fcc.to_sql("fcc", con=engine, if_exists="replace", index_label=None)

# To SQL census
census_df.to_sql("census", con=engine, if_exists="replace", index_label=None)

#To SQL fcc
fcc_df.to_sql("fcc_version1", con=engine, if_exists="replace", index_label=None)
#________*_________*_________*_________*_________*_________*_________*_________*
#________*_________*_________*_________*_________*_________*_________*_________*
