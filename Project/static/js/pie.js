function optionChanged(val) {
    var region = val;
    drawChart(region);
    console.log(drawChart(region));
};
//google.charts.load('current', { 'packages': ['corechart'] });
//google.charts.setOnLoadCallback(drawChart);
function drawChart(region) {
    d3.json(`/treemap/${region}`).then((response) => {
        console.log(response);
        var data = response;
        var layout = {
            height: 400,
            width: 500
        };
        Plotly.newPlot('treemap', data, layout);
    });
}
drawChart("northwest");
/*
    var data = {
        white: response.map(d =>d.w)
        asian: response.map(d =>d.a)
        values: response.map(d => d.w),
        labels: response.map,
        type: 'pie'}
  var layout = {
    height: 400,
    width: 500
  };
  Plotly.newPlot('treemap', data, layout);


function drawChart(Region) {
    var urlString = `/treemap/${Region}`;
    console.log(urlString);
    var jsonData = $.ajax({
        url: urlString, //concatenate so we have the url
        dataType: "json",
        async: false
    }).responseText;
    // Create our data table out of JSON data loaded from server.
    var data = new google.visualization.DataTable(jsonData);
    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.PieChart(document.getElementById('treemap'));
    chart.draw(data, { width: 400, height: 240 });
}
drawChart();
*/