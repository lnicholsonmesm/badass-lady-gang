function optionChanged(val) {
    var region = val;
    bubbleCharts(region);
    pieCharts(region);
    barCharts(region);
    makeHighchart(region);
    //mapCharts(region);
};
//##############################################################################
// BUBBLE PLOT
async function bubbleCharts(region) {
    d3.json(`/fcc/${region}`).then((response) => {
        let data = response;
        console.log(data);
        let Internet_Providers = data.dbaname;
        let Service_Count = data.service_count;
        let Max_Download_Speed = data.maxaddown;
        //console.log(Internet_Providers);
        // Build a Bubble Chart using the data
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
            height: 600,
            width: 800,
            title: "Internet Speeds and Providers Available",
            font: {
                //size: 18,
                color: 'rgb(255,255,255)'
            },
            yaxis: {
                title: {
                    text: 'Max download speed (mbps)'
                },
                font: {
                    size: 10,
                    //color: 'rgb(255,255,255)'
                },
                showlegend: true,
                plot_bgcolor: "transparent",
                paper_bgcolor: "#2B3E50"
            },
            xaxis: {
                tickangle: 45,
                automargin: true,
                title: {
                    //text: 'Providers'
                },
                font: {
                    size: 10,
                    //color: '#ffffff'
                },
                showlegend: true,
            },
            plot_bgcolor: "transparent",
            paper_bgcolor: "#2B3E50"
        }
        Plotly.newPlot("bubble-plot", [bubble_data], bubble_layout);
    });
}
//##############################################################################
//##############################################################################
// PIE CHART
function pieCharts(region) {
    d3.json(`/pie/${region}`).then((response) => {
        console.log(`pie response is: ${response}`);
        var data = response;
        var layout = {
            //plot_bgcolor: "blue",
            title: "Internet Customer Racial Distribution",
            paper_bgcolor: "#2B3E50",
            height: 525,
            width: 475,
            font: {
                size: 14,
                color: '#fff'
            },
            margin: {
                l: 100,
                r: 100,
                t: 100,
                b: 100
            },
        };
        Plotly.newPlot('pie-chart', data, layout);
    })
};

//##############################################################################
//##############################################################################
//BAR CHART
function barCharts(region) {
    d3.json(`/bar/${region}`).then((response) => {
        /////////////////////////////////////////////////////////
        console.log(response);
        var trace1 = response;
        var barData = [trace1];
        var layout = {
            //height: 425,
            //width: 500,
            plot_bgcolor: "transparent",
            paper_bgcolor: "#2B3E50",
            font: {
                size: 14,
                color: '#fff'
            },
            title: "Internet Access by Race",
            margin: {
                l: 50,
                r: 50,
                t: 100,
                b: 100
            },
        };
        Plotly.newPlot('bar-chart', barData, layout);
    })
};
//##############################################################################
//##############################################################################
//MAPPLOT
function mapCharts(region) {
    //d3.json(`/map/${region}`).then((response) => {
    d3.json(`/fcc/${region}`).then((response) => {
        let data = response;
        console.log(data);
        let Internet_Providers = data.dbaname;
        let Service_Count = data.service_count;
        let Max_Download_Speed = data.maxaddown;
        console.log(Internet_Providers);
        // Build a Bubble Chart using the data
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
            yaxis: {
                title: {
                    text: 'Max download speed (mbps)'
                },
                font: {
                    //size: 8,
                    color: "transparent"
                },
                showlegend: false,
                plot_bgcolor: "transparent",
                paper_bgcolor: "transparent"
            },
            xaxis: {
                title: {
                    //text: 'Providers'
                },
                font: {
                    //size: 8,
                    color: "transparent"
                },
                showlegend: true,
                plot_bgcolor: "transparent",
                paper_bgcolor: "transparent"
            }
        }
        Plotly.newPlot("map-id", [bubble_data], bubble_layout);
    });
}
let labelA = ["Lessthan$20,000!!_dialupOnly", "$20,000to$74,999!!_dialupOnly", "75Kplus_dialupOnly"]
let labelB = ["Lessthan$20,000!!_WithBroadband", "$20,000to$74,999!!_WithBroadband", "75Kplus_WithBroadband"]
let labelC = ["Lessthan$20,000WithoutInternet", "$20,000to$74,999WithoutInternet", "75KplusWithoutInternet"]
let labelHist = ["< $20,000", "$20,000-$74,999", "$75K+"]
let eastDialup = [207, 571, 236]
let eastBroadband = [15642, 71161, 56347]
let eastNoInternet = [11281, 18382, 4932]

let northwestDialup = [1114, 3278, 1310]
let northwestBroadband = [104722, 428149, 472923]
let northwestNoInternet = [59134, 84234, 21815]

let southwestDialup = [461, 1219, 271]
let southwestBroadband = [27957, 97953, 60838]
let southwestNoInternet = [19146, 24153, 4399]
let NoInternet = "";
let Broadband = "";
let Dialup = "";
//https://badass-lady-gang.herokuapp.com/

function makeHighchart(region) {
    if (region == "northwest") {
        NoInternet = northwestNoInternet;
        Broadband = northwestBroadband;
        Dialup = northwestDialup;
    }
    else if (region == "southwest") {
        NoInternet = southwestNoInternet;
        Broadband = southwestBroadband;
        Dialup = southwestDialup;
    }
    else if (region == "east") {
        NoInternet = eastNoInternet;
        Broadband = eastBroadband;
        Dialup = eastDialup;
    }
    var chart = Highcharts.chart({


        chart: {
            type: 'column',
            renderTo: 'histogram',
            plotBackgroundColor: null,
            backgroundColor: null,
            style: { color: '#ffffff' }
        },
        title: {
            text: 'Income',
            style: {
                color: '#ffffff'
            }
        },
        xAxis: {
            categories: labelHist,
            title: { text: 'Income', style: { color: '#ffffff' } },
            labels: { style: { color: '#ffffff' } },
            alignTicks: false
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Count',
                align: 'middle',
                style: { color: '#ffffff' }
            },
            labels: {
                overflow: 'justify',
                style: { color: '#ffffff' }
            }
        },
        plotOptions: {
            column: {
                dataLabels: {
                    enabled: true,
                }
            }
        },
        legend: {
            itemStyle: { color: "#ffffff" }
        },
        series: [{
            name: 'Dial-up Only',
            data: Dialup,
        }, {
            name: 'No Internet',
            data: NoInternet,
        }, {
            name: 'Has Broadband',
            data: Broadband,


        }],
        responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    legend: {
                        align: 'center',
                        verticalAlign: 'bottom',
                        layout: 'horizontal'
                    },
                    yAxis: {
                        labels: {
                            align: 'left',
                            x: 0,
                            y: -5
                        },
                        title: {
                            text: null
                        }
                    },
                    subtitle: {
                        text: null
                    },
                    credits: {
                        enabled: false
                    }
                }
            }]
        }
    });
};

$(window).resize(function () {
    chart.setSize(window.innerWidth)
});
//##############################################################################
//##############################################################################
// INITIALIZE FUNCTIONS
//##############################################################################
//##############################################################################
bubbleCharts("northwest");
pieCharts("northwest");
barCharts("northwest");
//mapCharts("northwest");
makeHighchart("northwest");