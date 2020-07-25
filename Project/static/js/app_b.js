var trace1 = {
  x: [1, 2, 3, 4],
  y: [10, 11, 12, 13],
  mode: 'markers',
  marker: {
    size: [40, 60, 80, 100]
  }
};

var data = [trace1];

var layout = {
  title: 'Marker Size',
  font: {
    size: 18,
    color: '#fff'},
  showlegend: true,
  plot_bgcolor:"transparent",
  paper_bgcolor:"#2B3E50"
};

Plotly.newPlot('bubble', data, layout);