function optionChanged(val) {
    var region = val;
    drawCharts(region);
    buildCharts(region);
    barCharts(region)
};

// PIE CHART
function drawCharts(region) {
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
    })};

//BAR CHART

// google.charts.load('current', {packages: ['corechart', 'bar']});
// google.charts.setOnLoadCallback(barChart);

function barCharts(region) {
    d3.json(`/bar/${region}`).then((response) => {
            /////////////////////////////////////////////////////////
            console.log(response);
        var trace1 = response;
        var barData = [trace1];
        var layout = {
            plot_bgcolor: "blue",
            paper_bgcolor: "#2B3E50",
            font: { color: '#fff' },
            title: "Distribution of Internet access by Race",
            margin: {
                l: 100,
                r: 100,
                t: 100,
                b: 100
                },
            };
        Plotly.newPlot('bubble', barData, layout);
        })
    };
//     var jsonData = $.ajax({
//         url: "/bar/<region>/",
//         dataType: "json",
//         async: false
//         }).responseText;
          
//     // Create our data table out of JSON data loaded from server.
//     var data = new google.visualization.DataTable(jsonData);

//     // var options = {
//     //     title: 'Population of Largest U.S. Cities',
//     //     chartArea: {width: '70%'},
//     //     hAxis: {
//     //       title: 'Internet Access',
//     //       minValue: 0,
//     //       textStyle: {
//     //         bold: true,
//     //         fontSize: 12,
//     //         color: '#4d4d4d'
//     //       },
//     //       titleTextStyle: {
//     //         bold: true,
//     //         fontSize: 18,
//     //         color: '#4d4d4d'
//     //       }
//     //     },
//     //     vAxis: {
//     //       title: 'Per Household',
//     //       textStyle: {
//     //         fontSize: 14,
//     //         bold: true,
//     //         color: '#848484'
//     //       },
//     //       titleTextStyle: {
//     //         fontSize: 14,
//     //         bold: true,
//     //         color: '#848484'
//     //       }
//     //     }
//     //   };
//       var chart = new google.visualization.BarChart(document.getElementById('bubble'));
//       chart.draw(data);
    // }


// //drawChart("northwest");


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
