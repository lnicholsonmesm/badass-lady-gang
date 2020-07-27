function optionChanged(val) {
    var Region = val;
    console.log(Region);
    drawChart(Region);
};
function drawChart(Region) {
    var url = `/treemap/${Region}`;
    console.log(url);
    d3.json(url).then((response) => {
        console.log(response);
        data = response;
        // race = data.map(row => row.values);
        // y = data.map(row => row)
        //internet_per_capita = data.map(row => row.race_something);
        //add a filter for each race?
        console.log(data[0]);
        var trace1 = [{
            x: data[0]["labels"],
            y: data[0]["values"],
            type: 'bar',
            orientation: "h"
        }]
        var barData = [trace1];
        var layout = {
            title: "Distribution of Internet access by Race",
            margin: {
                l: 100,
                r: 100,
                t: 100,
                b: 100
            }
        };
        Plotly.newPlot('map-id', barData, layout);
    });
}