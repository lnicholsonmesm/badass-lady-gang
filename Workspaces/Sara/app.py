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

missingcol = pd.read_csv("data/missingcol.csv")
missingcol
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
#Get FCC
fcc = pd.read_csv("data/fcc_data.csv") #, na_values = ["-"]
fcc = fcc.astype({"tract": "object"})

#subset columns
fcc_subset = fcc[["dbaname","hocofinal","stateabbr","blockcode", "tract", "techcode","consumer","maxaddown","maxadup"]]

#fcc_df
region_subset = census_df[["CountyName", "Region", "Latitude", "Longitude", "fips_id"]]
fcc_df = fcc_subset.merge(region_subset, how="left", left_on="tract", right_on="fips_id")
fcc_df

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


# import necessary libraries
import sqlalchemy
from sqlalchemy import create_engine
from flask import Flask, render_template, jsonify, request, redirect

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///db.sqlite")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/fcc/<region>")
def fcc(region):
    query = "SELECT * FROM fcc" #Where Region = '{region}' -- need to add to df
    results = engine.execute(race_query).fetchall()
    dictionary = {"data": results}
    return jsonify(dictionary)
  

#load race query
from race_query import race_query, race_columns

@app.route("/treemap/<region>/")
def treemap(region):
    census = []
    results = engine.execute(race_query).fetchall()
    df = pd.DataFrame(results)
    df.columns = race_columns
    data_frame = df.groupby("Region").sum()
    '''
    # E_Computer_Broadband_Households
    # E_Computer_NoInternet_Households
    #NoComputer_Households
    [
        ["Race", None,0],

        ["White","Race",0],
        ["With Computer, White", "White", 0]
        ["No Computer, White", "White", 0]
        ["With Internet", "With Computer, White", 0]

        ["American Indian or Alaska Native","Race",0],
        ["With Computer, Indigenous", "American Indian or Alaska Native", 0]
        ["No Computer, Indigenous", "American Indian or Alaska Native", 0]
        ["With Internet", "With Computer, Indigenous", 0]

        ["Asian","Race",0],
        ["With Computer, Asian", "Asian", 0]
        ["No Computer, Asian", "Asian", 0]
        ["With Internet", "With Computer, Asian", 0]

        
        ["Native Hawaiian/Other Pacific Islander", "Race", 0],
        ["Other", "Race", 0],
        ["Two or more Races", "Race", 0]
    ]
    '''
    #{"latitude": row[0]}
    #census.append(mydict)
        #if upper(enter_race_or_ethnicity) == "RACE" then:
        #where = "race"
    #OnlyWhite = []
    #census = {
    #    ""
    #}
    #mapdata =jsonify(census)
    #return mapdata


@app.route("/map/<region>")
def map(region):
    census = []
    mapquery = f"select Latitude, Longitude, Region, county_name, fips_id, PE_Computer_Broadband_Household, E_Computer_Broadband_Household FROM census"
    # where Region = '{region}"
    results = engine.execute(mapquery)
    
    for row in results:
        mydict = {
            "latitude": row[0], 
            "longitude": row[1],
            "region": row[2],
            "county": row[3],
            "tract": row[4],
            "pct_has_computer_and_broadband": row[5],
            "has_computer_and_broadband": row[6]
            } #{"latitude": row[0]}
        census.append(mydict)
       
    return jsonify(census)
    #return redirect("/", code=302)

@app.route("/region2")
def map2():
    query = "SELECT Latitude, Longitude, Region, county_name, fips_id, PE_Computer_Broadband_Household, E_Computer_Broadband_Household FROM census"
    results = engine.execute(query)
    mapdata = []
    for row in results:
        datadict = {
            "latitude": row[0],
            "longitude": row[1],
            "region": row[2],
            "county": row[3],
            "fips_id": row[4],
            "pct_ComputerAndBroadband": row[5],
            "ComputerAndBroadband": row[6]
        }
        mapdata.append(datadict)
    return jsonify(mapdata)

if __name__ == "__main__":
    app.run()



# # Remove tracking modifications
# # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# Pet = create_classes(db)

# # create route that renders index.html template
# @app.route("/")
# def home():
#     session = Session(engine)
#     return render_template("index.html")


# # Query the database and send the jsonified results
# """
# @app.route("/send", methods=["GET", "POST"])
# def send():
#     if request.method == "POST":
#         name = request.form["petName"]
#         lat = request.form["petLat"]
#         lon = request.form["petLon"]

#         pet = Pet(name=name, lat=lat, lon=lon)
#         db.session.add(pet)
#         db.session.commit()
#         return redirect("/", code=302)

#     return render_template("form.html")
#     """


# @app.route("/api") ----- can we merge into a single app.route?
# def pals():
#     results = db.session.query(Pet.name, Pet.lat, Pet.lon).all()

#     hover_text = [result[0] for result in results]
#     lat = [result[1] for result in results]
#     lon = [result[2] for result in results]

#     pet_data = [{
#         "type": "scattergeo",
#         "locationmode": "USA-states",
#         "lat": lat,
#         "lon": lon,
#         "text": hover_text,
#         "hoverinfo": "text",
#         "marker": {
#             "size": 50,
#             "line": {
#                 "color": "rgb(8,8,8)",
#                 "width": 1
#             },
#         }
#     }]

#     return jsonify(pet_data)

'''

    White = []
    AmIndAlasNat = []
    Black = []
    Asian = []
    HawaiianPacific = []
    OneRaceOther = []
    TwoPlusRaces = []
    CompInt = []
    for array in results:
        for x in range(len(array))
        w= row[0]
        n= row[1]
        b= row[2]
        a= row[3]
        h= row[4]
        o= row[5]
        t= row[6]
        _ci = row[7]
        wci = row[8]
        nci = row[9]
        bci = row[10]
        aci = row[11]
        hci = row[12]
        oci = row[13]
        tci = row[14]
        _cni= row[15]
        wcni = row[16]
        ncni = row[17]
        bcni = row[18]
        acni = row[19]
        hcni = row[20]
        ocni = row[21]
        tcni = row[22]
        hl_any = row[23]
        w_not_hl = row[24]
        hl_any_ci = row[25]
        w_not_hl_ci = row[26]
        ncw = row[27]
        ncn = row[28]
        ncb = row[29]
        nca = row[30]
        nc_hl_any = row[31]
        nc_w_not_hl = row[32]
'''

if __name__ == "__main__":
    app.run()
