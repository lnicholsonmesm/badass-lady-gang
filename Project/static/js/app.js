// var labels = ["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"]
// var parents = ["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve"]
// var data = [{
//       type: "treemap",
//       labels: labels,
//       parents: parents,
//       values:  [10, 14, 12, 10, 2, 6, 6, 1, 4],
//       textinfo: "label+value+percent parent+percent entry",
//       domain: {"x": [0, 1]},
//       outsidetextfont: {"size": 12, "color": "#377eb8"},
//       marker: {"line": {"width": 2}},
//       pathbar: {"visible": false
//     }}]
// var layout = {
//   plot_bgcolor:"blue",
//   paper_bgcolor:"#2B3E50",
//   font: {
//     color: '#fff'}
//   }

// Plotly.newPlot('treemap', data, layout)

google.charts.load('current', {'packages':['treemap']});
      google.charts.setOnLoadCallback(drawChart);
      function drawChart() {
        var jsonData = $.ajax({
            url: "/treemap/<region>/",
            dataType: "json",
            async: false
            }).responseText;
              
        // Create our data table out of JSON data loaded from server.
        var data = new google.visualization.DataTable(jsonData);
        
        tree = new google.visualization.TreeMap(document.getElementById('treemap'));

        tree.draw(data, {
          minColor: '#f00',
          midColor: '#ddd',
          maxColor: '#0d0',
          headerHeight: 15,
          fontColor: 'black',
          showScale: true
        });

      }