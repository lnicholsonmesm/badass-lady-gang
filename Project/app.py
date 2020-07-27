# SQLAlchemy
from sqlalchemy import create_engine

# Imports the methods needed to abstract classes into tables
from sqlalchemy.ext.declarative import declarative_base

# Allow us to declare column types
from sqlalchemy import Table, Column, Integer, String, Float, MetaData

#pandas for data manipulation and export
import pandas as pd
import numpy as np

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
#print(f"fcc dtypes: {dt}")

#________*_________*_________*_________*_________*_________*_________*_________*
# To SQL census
census_df.to_sql("census", con=engine, if_exists="replace", index_label=None)

#To SQL fcc
fcc_df.to_sql("fcc_version1", con=engine, if_exists="replace", index_label=None)

#this one is not really needed:
fcc_by_tract = pd.read_csv("data/fcc_bytract.csv")
fcc_by_tract.to_sql("fcc_tracts",  con=engine, if_exists="replace", index_label=None)
#________*_________*_________*_________*_________*_________*_________*_________*
#________*_________*_________*_________*_________*_________*_________*_________*
filtered_fcc = pd.read_csv("data/fcc_groupedbyregion_andcompany_andspeed.csv")

filtered_fcc.to_sql("fcc", con=engine, if_exists="replace", index_label=None)



#________*_________*_________*_________*_________*_________*_________*_________*#________*_________*_________*_________*_________*_________*_________*_________*
#Test
#print(engine.execute("SELECT * FROM census LIMIT 2").fetchall())
#print(engine.execute("SELECT * FROM fcc LIMIT 2").fetchall())


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
    #return render_template("indextest.html")

@app.route("/<region>")
def region(region):
    return render_template("index.html", region = region)

@app.route("/<region>/happy")
def apitest(region):
    census = []
    mapquery = f"select Latitude, Longitude, Region, county_name, fips_id, PE_Computer_Broadband_Household, E_Computer_Broadband_Household FROM census where Region = '{region}'"
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


@app.route("/fcc/<string:region>")
def fcc(region):
    query = "SELECT * FROM FCC" 
    #f"SELECT dbaname, maxaddown, Region FROM fcc WHERE Region = '{region}'"# GROUP BY dbaname, Region" #, COUNT(consumer) as service_count   and consumer = 1 
    #print(query)
    results = engine.execute(query) #.fetchall()
    #fcc_df_qry = pd.DataFrame(results)
    #print(fcc_df_qry[11])
    
    fcc = []
    dbaname = []
    service_count = []
    maxaddown = []
    maxadupload = []
    region = []
    for result in results:
        #print(result[11])
       # if result[11]==region:
            #print(result)
        dbaname.append(result[1])
        maxaddown.append(result[2])
        maxadupload.append(result[3])
        region.append(result[5])
       # service_count.append(result[7] if result[7] == 1 else 0)
        service_count.append(result[6])

    fcc_dictionary = {
        "dbaname": dbaname,
        'maxaddown': maxaddown,
        'maxadupload': maxadupload,
        'region': region,
        "service_count": service_count,
                        }        
    #"dbaname","hocofinal","stateabbr","blockcode", "tract", "techcode",
    #"consumer","maxaddown","maxadup"]]
    return jsonify(fcc_dictionary)


##def region(sample):
    # Filter the data based on the sample number and
    # only keep rows with values above 1
   # sample_data = df.loc[df[sample] > 1, ["hocofinal", "consumer", "maxaddown"]
    # Sort by sample
  #  sample_data.sort_values(by=sample, ascending=False, inplace=True)
    # Format the data to send as json
    
  #  return jsonify(data)
    # query = f"SELECT * FROM census Where Region = '{region}'"
    # results = engine.execute(query).fetchall()
    # dictionary = {"data": results}
    # return jsonify(dictionary)

    #return render_template("laura.html")

# @app.route("/northerncoast/")
# def apitesting():
#     return render_template("northerncoast.html")



  

# #load race query
from race_query import race_query, race_columns, pie_query

@app.route("/treemap/<string:region>/")
def treemap(region='northwest'):
    
    #print(race_query.format(region))
    results = engine.execute(pie_query.format(region))
    white = []
    native = []
    black = []
    asian = []
    hawaiian = []
    other = []
    two_plus = []
    labels = ['white','native','black','asian','hawaiian','other','two_plus']
    for row in results:
        white.append(row[0])
        native.append(row[1])
        black.append(row[2])
        asian.append(row[3])
        hawaiian.append(row[4])
        other.append(row[5])
        two_plus.append(row[6]) #,
            #"_ci" : row[7],
            # "wci" : row[8],
            # "nci" : row[9],
            # "bci" : row[10],
            # "aci" : row[11],
            # "hci" : row[12],
            # "oci" : row[13],
            # "tci" : row[14],
            # "_cni": row[15],
            # "wcni" : row[16],
            # "ncni" : row[17],
            # "bcni" : row[18],
            # "acni" : row[19],
            # "hcni" : row[20],
            # "ocni" : row[21],
            # "tcni" : row[22],
            # "hl_any" : row[23],
            # "w_not_hl" : row[24],
            # "hl_any_ci" : row[25],
            # "w_not_hl_ci" : row[26],
            # "ncw" : row[27],
            # "ncn" : row[28],
            # "ncb" : row[29],
            # "nca" : row[30],
            # "nc_hl_any" : row[31],
            # "nc_w_not_hl" : row[32],

    pie_data = [{
        "labels": labels,
        "values": [sum(white), sum(native), sum(black), sum(asian), sum(hawaiian), sum(other),sum(two_plus)],
        "type": "pie"
    }]
    return jsonify(pie_data)

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


# @app.route("/map/<region>")
# def map(region):
#     census = []
#     mapquery = f"select Latitude, Longitude, Region, county_name, fips_id, PE_Computer_Broadband_Household, E_Computer_Broadband_Household FROM census"
#     # where Region = '{region}"
#     results = engine.execute(mapquery)
    
#     for row in results:
#         mydict = {
#             "latitude": row[0], 
#             "longitude": row[1],
#             "region": row[2],
#             "county": row[3],
#             "tract": row[4],
#             "pct_has_computer_and_broadband": row[5],
#             "has_computer_and_broadband": row[6]
#             } #{"latitude": row[0]}
#         census.append(mydict)
       
#     return jsonify(census)
#     #return redirect("/", code=302)

# @app.route("/region2")
# def map2():
#     query = "SELECT Latitude, Longitude, Region, county_name, fips_id, PE_Computer_Broadband_Household, E_Computer_Broadband_Household FROM census"
#     results = engine.execute(query)
#     mapdata = []
#     for row in results:
#         datadict = {
#             "latitude": row[0],
#             "longitude": row[1],
#             "region": row[2],
#             "county": row[3],
#             "fips_id": row[4],
#             "pct_ComputerAndBroadband": row[5],
#             "ComputerAndBroadband": row[6]
#         }
#         mapdata.append(datadict)
#     return jsonify(mapdata)



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

if __name__ == "__main__":
    app.run(debug=True)
