/*

let labelA = ["Lessthan$20,000!!_dialupOnly", "$20,000to$74,999!!_dialupOnly", "75Kplus_dialupOnly"]
let labelB = ["Lessthan$20,000!!_WithBroadband", "$20,000to$74,999!!_WithBroadband", "75Kplus_WithBroadband"]
let labelC = ["Lessthan$20,000WithoutInternet", "$20,000to$74,999WithoutInternet", "75KplusWithoutInternet"]
let labelHist = ["< $20,000", "$20,000-$74,999", "$75K+"]
let eastDialup = [207, 571, 236]
let eastBroadband = [15642, 71161, 56347]
let eastNoInternet = [11281, 18382, 4932]

let northwestDialup = [104722, 428149, 472923]
let northwestBroadband = [104722, 428149, 472923]
let northwestNoInternet = [59134, 84234, 21815]

let southwestDialup = [461, 1219, 271]
let southwestBroadband = [27957, 97953, 60838]
let southwestNoInternet = [19146, 24153, 4399]

//https://badass-lady-gang.herokuapp.com/

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
        name: 'No Internet',
        data: eastNoInternet,
    }, {
        name: 'Has Broadband',
        data: eastBroadband,
    }, {
        name: 'Dial-up Only',
        data: eastDialup,
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


$(window).resize(function () {
    chart.setSize(window.innerWidth)
});
*/