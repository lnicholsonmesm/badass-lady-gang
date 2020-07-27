function optionChanged(val) {
    var region = val;
    drawChart(region);
    buildCharts(region);
};
//google.charts.load('current', { 'packages': ['corechart'] });
//google.charts.setOnLoadCallback(drawChart);
function drawChart(region) {
    d3.json(`/treemap/${region}`).then((response) => {
        //console.log(response);
        var data = response;
        var layout = {
            //plot_bgcolor: "blue",
            paper_bgcolor: "#2B3E50",
            height: 400,
            width: 500
        };
        Plotly.newPlot('treemap', data, layout);

        /////////////////////////////////////////////////////////
        data = response;
        // race = data.map(row => row.values);
        // y = data.map(row => row)
        //internet_per_capita = data.map(row => row.race_something);
        //add a filter for each race?
        console.log(data[0]["values"]);
        var trace1 = {
            x: data[0]["labels"],
            y: data[0]["values"],
            type: 'bar',
            //orientation: "v"
        };
        var barData = [trace1];
        var layout = {
            //plot_bgcolor: "blue",
            paper_bgcolor: "#2B3E50",
            font: { color: '#fff' },
            title: "Distribution of Internet access by Race",
            margin: {
                l: 100,
                r: 100,
                t: 100,
                b: 100
            },
            font: { color: '#fff' },
        };
        Plotly.newPlot('bubble', barData, layout);
    });
}

drawChart("northwest");


async function buildCharts(region) {
    // Use `d3.json` to fetch the sample data for the plots
    d3.json(`/fcc/${region}`).then((response) => {
        //const url = `/fcc/${region}`;
        // let data = await d3.json(url);
        let data = response;
        console.log(data);
        let Internet_Providers = data.dbaname;
        let Service_Count = data.service_count;
        let Max_Download_Speed = data.maxaddown;
        console.log(Internet_Providers);
        // Build a Bubble Chart using the sample data
        let bubble_data = {
            type: "scatter",
            x: Internet_Providers,//providers names
            y: Max_Download_Speed,
            //y: Service_Count, // provider counts
            mode: 'markers',
            marker: {
                color: Max_Download_Speed,
                size: Max_Download_Speed.map(d => d / 10)
            },
            hovertext: Internet_Providers //provider name
        }

        let bubble_layout = {
            title: "What kind of Internet is accessible in each Region?",
            xaxis: {
                title: {
                    text: 'Providers'
                },
                font: {
                    size: 18,
                    color: '#fff'
                },
                showlegend: true,
                plot_bgcolor: "transparent",
                paper_bgcolor: "#2B3E50"
            }
        }
        Plotly.newPlot("map-id", [bubble_data], bubble_layout);
    });
}
buildCharts('northwest');
