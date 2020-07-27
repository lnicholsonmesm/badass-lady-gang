

async function buildCharts(region) {

  // Use `d3.json` to fetch the sample data for the plots
  const url = "/fcc/<region>" + region;
  let data = await d3.json(url);

  let Internet_Providers = data.dbaname;
  let Service_Count = data.consumer;
  let Max_Download_Speed = data.maxaddown;

  // Build a Bubble Chart using the sample data
  let bubble_data = {
    type: "scatter",
    x: Internet_Providers,//providers names
    y: Max_Download_Speed, // provider counts
    mode: 'markers',
    marker: {
      color: Internet_Providers,
      size: 5 //Service_Count / 1000 //.map(d => d / 1000)
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
  };

  Plotly.newPlot("bubble", [bubble_data], bubble_layout);

}

function init() {
  // Grab a reference to the dropdown select element
  let selector = d3.select("#navbarDropdown");

  // Use the list of sample names to populate the select options
  d3.json("/").then((regionNames) => {
    regionNames.forEach((region) => {
      selector
        .append("option")
        .text(region)
        .property("value", region);
    });

    // Use the first sample from the list to build the initial plots
    const firstRegion = regionNames[0];
    buildCharts(firstRegion);
    buildMetadata(firstRegion);
  });
}

function optionChanged(newRegion) {
  // Fetch new data each time a new sample is selected
  buildCharts(newRegion);
  buildMetadata(newRegion);
}
init();