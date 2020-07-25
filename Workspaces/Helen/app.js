 //var geoData = "https://raw.githubusercontent.com/loganpowell/census-geojson/master/GeoJSON/500k/2010/41/tract.json";
 var geoData1 = "https://opendata.arcgis.com/datasets/e3320c8931b144aaa71eebec059ac5cd_0.geojson"
 //var geoData2 = "https://raw.githubusercontent.com/loganpowell/census-geojson/master/GeoJSON/500k/2018/41/tract.json";

// Get data
d3.json(geoData1, function(data) {
        //console.log (data)
        L.geoJSON(data).addTo(myMap)
        //createFeatures(data.features);
    });

    var myMap = L.map("map", {
        center: [45.52, -122.67],
        zoom: 7,
        //layers: [census]
      });

L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
        attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
        tileSize: 512,
        maxZoom: 18,
        zoomOffset: -1,
        id: "mapbox/streets-v11",
        accessToken: API_KEY
}).addTo(myMap);


var circle = L.circle([45.52, -122.67],{
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.5,
        radius: 5000
    }).addTo(myMap);


async function getData(){
        const response = await fetch('/Internet_Data');
        const data = await response.json()
        for (item of data){
                const marker = L.marker([item.lat, item.lon]).addTo(myMap);
                const txt = `This is the information ${item.lat}; population is ${item.population}`;
                marker.bindPopup(txt)
        }
        console.log(data)
}

