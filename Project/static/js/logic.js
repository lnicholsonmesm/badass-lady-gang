//Get data from Flask App API call
function optionChanged(val) {
  var subjectID = val;
  console.log(subjectID);
  //plotGraph(subjectID);
};


var selector = d3.select("#region").node().value;
console.log(selector);
d3.selectAll("#region").on("change", console.log(selector));
var test = d3.select("#navbarDropdown").node().value;
d3.selectAll("#navbarDropdown").on("change", console.log(test));


d3.json("/<region>/happy").then((response) => {
  console.log(response);
  //Define base map centered in Portland
  var myMap = L.map("map-id", {
    center: [45.52, -122.67],
    zoom: 7,
  });

  //Add Tile Layer from Mapbox
  L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
    attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
    tileSize: 512,
    maxZoom: 18,
    zoomOffset: -1,
    id: "mapbox/streets-v11",
    accessToken: API_KEY
  }).addTo(myMap);

  //Get Maxvalue for intensity using response and correct column "household"
  householdData = response.map(track => track.has_computer_and_broadband)
  maxValue = Math.max(has_computer_and_broadband)

  //Function to get intensity based on number of housholds
  //var max = 3000
  function getIntensity(rawValue, maxValue) {
    var intensity = rawValue / maxValue
    return intensity
  }
  //getIntensity(200,max)

  //Get an array of the parametres that the heat layer requires: latitude, longitude, householdcount
  var getHeatInfo = response.map(track => { return [track.latitude, track.longitude, getIntensity(track.has_computer_and_broadband, maxValue)] })
  //Add Heat Layer to map using the getHeatInfo array
  var heat = L.heatLayer([
    //[45.52, -122.67, 500], lat, lng, intensity
    getHeatInfo], { radius: 35 }).addTo(myMap);
  //give it a gradient
})





      // var tractData = "https://raw.githubusercontent.com/loganpowell/census-geojson/master/GeoJSON/500k/2010/41/tract.json";
      // // var geoData1 = "https://opendata.arcgis.com/datasets/e3320c8931b144aaa71eebec059ac5cd_0.geojson"
      // //  //var geoData2 = "https://raw.githubusercontent.com/loganpowell/census-geojson/master/GeoJSON/500k/2018/41/tract.json";
      // //  //Get data
      // d3.json(tractData, function(data) {
      //         //console.log (data)
      //         L.geoJSON(data).addTo(myMap)
      // //         //createFeatures(data.features);
      //     });


  //intensity = households
  //find the max intesity, set it to 1




  //call the route in the url




  // var circle = L.circle([45.52, -122.67],{
  //         color: 'red',
  //         fillColor: '#f03',
  //         fillOpacity: 0.5,
  //         radius: 5000
  //     }).addTo(myMap);

  // async function getData(){
  //         const response = await fetch('/api');
  //         const data = await response.json()
  //         for (item of data){
  //                 const marker = L.marker([item.lat, item.lon]).addTo(myMap);
  //                 const txt = `This is the information ${item.lat}; population is ${item.population}`;
  //                 marker.bindPopup(txt)
  //         }
  //         console.log(data)
  // }

  //heatmap #housholds that have internet access


  // To include the plugin, just use leaflet-heat.js from the dist folder:
  // <script src="leaflet-heat.js"></script>



  // function buildPlot() {
  //   /* data route */
  //   const url = "/api/pals";
  //   d3.json(url).then(function(response) {
  //     console.log(response);
  //     const data = response;
  //     const layout = {
  //       scope: "usa",
  //       title: "Pet Pals",
  //       showlegend: false,
  //       height: 600,
  //             // width: 980,
  //       geo: {
  //         scope: "usa",
  //         projection: {
  //           type: "albers usa"
  //         },
  //         showland: true,
  //         landcolor: "rgb(217, 217, 217)",
  //         subunitwidth: 1,
  //         countrywidth: 1,
  //         subunitcolor: "rgb(255,255,255)",
  //         countrycolor: "rgb(255,255,255)"
  //       }
  //     };
  //     Plotly.newPlot("plot", data, layout);
  //   });
  // }
  // buildPlot();