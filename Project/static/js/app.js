function buildPlot() {
  /* data route */
  const url = "/api";
  d3.json(url).then(function(response) {

    console.log(response);

    const data = response;

    const layout = {
      scope: "usa",
      title: "Pet Pals",
      showlegend: false,
      height: 600,
            // width: 980,
      geo: {
        scope: "usa",
        projection: {
          type: "albers usa"
        },
        showland: true,
        landcolor: "rgb(217, 217, 217)",
        subunitwidth: 1,
        countrywidth: 1,
        subunitcolor: "rgb(255,255,255)",
        countrycolor: "rgb(255,255,255)"
      }
    };

    Plotly.newPlot("plot", data, layout);
  });
}

//Create a bubble chart that displays each sample.      var trace2 = {        x:importedData.samples[0].otu_ids,        y: importedData.samples[0].sample_values,        mode: "markers",        marker: {          size: importedData.samples[0].sample_values,          color: importedData.samples[0].otu_ids,        }      }
var bubbledata = [trace2];
Plotly.newPlot("bubble", bubbledata); });

buildPlot();
