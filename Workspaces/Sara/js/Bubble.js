  let bubble_data = {
    type:"scatter",
    x: otu_ids,
    y: sample_values,
    mode: 'markers',
    marker: {
              color: otu_ids, 
              size: sample_values.map(d => d)
            },
    hovertext: otu_labels
  }

  let bubble_layout = {
    title: "OTU_IDs in Sample",
    xaxis: {
      title: {
        text: 'OTU ID',
      }
    }
  };

  Plotly.newPlot("bubble", [bubble_data], bubble_layout);

}

function init() {
  // Grab a reference to the dropdown select element
  let selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}