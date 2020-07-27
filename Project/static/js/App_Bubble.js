
  
  async function buildCharts(sample) {
  
    // Use `d3.json` to fetch the sample data for the plots
    const url = "/samples/" + sample;
    let data = await d3.json(url);

    
    // Build a Bubble Chart using the sample data
    let bubble_data = {
      type:"scatter",
      x: otu_ids, // Providers
      y: sample_values, //Provider counts
      mode: 'markers',
      marker: {
                color: otu_ids, 
                size: sample_values.map(d => d) // Provider speed
              },
      hovertext: otu_labels
    }
  
    let bubble_layout = {
      title: "Providers",
      xaxis: {
        title: {
          text: 'Provider',
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