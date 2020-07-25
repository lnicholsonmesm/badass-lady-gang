var labels = ["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"]
var parents = ["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve"]
var data = [{
      type: "treemap",
      labels: labels,
      parents: parents,
      values:  [10, 14, 12, 10, 2, 6, 6, 1, 4],
      textinfo: "label+value+percent parent+percent entry",
      domain: {"x": [0, 1]},
      outsidetextfont: {"size": 12, "color": "#377eb8"},
      marker: {"line": {"width": 2}},
      pathbar: {"visible": false
    }}]
var layout = {
  plot_bgcolor:"blue",
  paper_bgcolor:"#2B3E50",
  font: {
    color: '#fff'}
  }

Plotly.newPlot('treemap', data, layout)