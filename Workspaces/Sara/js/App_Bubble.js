

  async function buildCharts(sample) {

    
    // Build a Bubble Chart using the sample data
    let bubble_data = {
      type:"scatter",
      x: "Race",
      y: sample_values,
      mode: 'markers',
      marker: {
                color: County, 
                size: sample_values.map(d => d)
              },
      hovertext: otu_labels
    }
  
    let bubble_layout = {
      title: "Counties",
      xaxis: {
        title: {
          text: 'County',
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