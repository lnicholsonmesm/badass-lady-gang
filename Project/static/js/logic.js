//do we need geojson
//Oregon Counties:

// var oregon_counties_url = "https://opendata.arcgis.com/datasets/e3320c8931b144aaa71eebec059ac5cd_0.geojson"
// var census_url = "https://tigerweb.geo.census.gov/arcgis/rest/services/Census2010/Tracts_Blocks/MapServer?f=jsapi

// function createMap(data)



var myMap = L.map("map", {
        center: [45.52, -122.67],
        zoom: 13,
        //layers: [population, internet, etc]
      });
      
      // Adding a tile layer (the background map image) to our map
      // We use the addTo method to add objects to our map
L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
  tileSize: 500,
  maxZoom: 18,
  zoomOffset: -1,
  id: "mapbox/streets-v11",
  accessToken: "pk.eyJ1IjoiaGVsZW5udW5leiIsImEiOiJja2N4czI2bXQwMnk3MnRsaWZqY2dveTV6In0.D1qMGnVSfZ9nc_FK_ClCeg"
}).addTo(myMap);
      
