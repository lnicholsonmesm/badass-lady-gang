//var oregon_counties_url = "https://opendata.arcgis.com/datasets/e3320c8931b144aaa71eebec059ac5cd_0.geojson"


// var boundaries_url = "https://raw.githubusercontent.com/loganpowell/census-geojson/master/GeoJSON/500k/2018/41/tract.json"

//function createMap(DB_data)

//var data1

var myMap = L.map("map", {
        center: [45.52, -122.67],
        zoom: 13,
        //layers: [population, internet, etc]
      });
      
      // Adding a tile layer (the background map image) to our map
      // We use the addTo method to add objects to our map
L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
        attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
        tileSize: 512,
        maxZoom: 18,
        zoomOffset: -1,
        id: "mapbox/streets-v11",
        accessToken: API_KEY
}).addTo(myMap);
      
var geoData = "https://raw.githubusercontent.com/loganpowell/census-geojson/master/GeoJSON/500k/2010/41/tract.json"


var geojson;

// Grab data with d3
d3.json(geoData, function(data) {

  // Create a new choropleth layer
  geojson = L.choropleth(data, {

    // Define what  property in the features to use
    valueProperty: "MHI2016",

    // Set color scale
    scale: ["#ffffb2", "#b10026"],

    // Number of breaks in step range
    steps: 10,

    // q for quartile, e for equidistant, k for k-means
    mode: "q",
    style: {
      // Border color
      color: "#fff",
      weight: 1,
      fillOpacity: 0.8
    },
});

});


//Plot2 - Treechart - Aranza

//Plot3 - Infographic -

//Plot4 - Scatter Plot - 

