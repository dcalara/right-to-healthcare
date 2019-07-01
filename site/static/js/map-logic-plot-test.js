function getRoutes(dataset) {
  // Gets the routes for API calls based on the selector values in document
  switch(dataset) {
    case "electricity":
      return "EG-ELC-ACCS-ZS";
      break;
    case "staffed_birth":
      return "SH-STA-BRTC-ZS";
      break;
    case "birth_rate":
      return "SP-DYN-CBRT-IN";
      break;
    case "broadband":
      return "IT-NET-BBND-P2";
      break;
    case "corruption":
      return "CORRUP-HOM";
      break;
    case "death_rate":
      return "SP-DYN-CDRT-IN";
      break;
    case "econ_freedom":
      return "747";
      break;
    case "female_out_school":
      return "SE-PRM-UNER-FE";
      break;
    case "fertility_rate":
      return "SP-DYN-TFRT-IN";
      break;
    case "health_expenditure_GDP":
      return "SH-XPD-CHEX-GD-ZS"
      break;
    case "hexlth_expenditure_person":
      return "SH-XPD-CHEX-PP-CD"
      break;
    case "healthcare_coverage":
      return "HLTH-INS";
      break;
    case "hospital_beds":
      return "SH-MED-BEDS-ZS";
      break;
    case "human_rights_score":
      return "HRP-SCORE";
      break;
    case "infant_mortality_rate":
      return "SP-DYN-IMRT-IN";
      break;
    case "life_expectancy":
      return "SP-DYN-LE00-IN";
      break;
    case "life_expectancy_male":
      return "SP-DYN-LE00-MA-IN";
      break;
    case "female_literacy_adult":
      return "SE-ADT-LITR-FE-ZS";
      break;
    case "female_literacy_youth":
      return "SE-ADT-1524-LT-FE-ZS";
      break;
    case "medical_doctors":
      return "MEDS-PERPOP";
      break;
    case "migration":
      return "SM-POP-NETM";
      break;
    case "last_grade_female":
      return "SE-PRM-PRSL-FE-ZS";
      break;
    case "last-grade_male":
      return "SE-PRM-PRSL-MA-ZS";
      break;
    default:
      return "HRP-SCORE";
      break;
  }
 
}

// function to test country coloring -- temporary
function getColor(num) {
    // console.log(num);
    const r = Math.min(Math.max(0,20*num),255);
    const g = Math.min(Math.max(0,255-20*num),255);
    const b = Math.min(Math.max(0,255 - num*num),255);
    return `rgba(${r},${g},${b},1)`
}

const projection = d3.geoEqualEarth().rotate([-10, 0])

// Code source:  http://bl.ocks.org/micahstubbs/8e15870eb432a21f0bc4d3d527b2d14f
// Modified 

const margin = {top: 0, right: 0, bottom: 0, left: 0},
            width = 960 - margin.left - margin.right,
            height = 500 - margin.top - margin.bottom;

const svgMap = d3.select("#map")
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .append('g')
            .attr('class', 'map');

let path = d3.geoPath().projection(projection);

d3.json("../static/data/countries.json").then(  function(data) { 
 
  svgMap.append("g")
      .attr("class", "countries")
    .selectAll("path")
      .data(data.features)
    .enter().append("path")
      .attr("d", path)
      .style("fill", function(d) { return getColor(d.properties.name.length) })
      .style('stroke', 'white')
      .style('stroke-width', 1.5)
      .style("opacity",0.8)

  let viridisColor = d3.scaleSequential().domain([-1.0,1.0])
      .interpolator(d3.interpolateViridis)

  let cb = colorbarV(viridisColor, 25, 150);

  svgMap.append("g")
      .attr("id","colorbar")
      .attr("transform",`translate(${width * 0.935},${height * 0.69})`)
      .call(cb);

  svgMap.append("text")
      .attr("text-anchor","middle")
      .attr("transform",`translate(${width * 0.94},${height * 0.6})`)
      .attr("id","colorbar-label")
      .attr("stroke","black")
      .html("Pearson");

      svgMap.append("text")
      .attr("text-anchor","middle")
      .attr("transform",`translate(${width * 0.94},${height * 0.63})`)
      .attr("id","colorbar-label2")
      .attr("stroke","black")
      .html("Correlation");

    svgMap.append("text")
      .attr("text-anchor","middle")
      .attr("transform",`translate(${width * 0.94},${height * 0.66})`)
      .attr("id","colorbar-label3")
      .attr("stroke","black")
      .html("Coefficient");
  
  // Event handlers to get selections and make back end call
  d3.select("#selDataset1").on("change", function () {
    var var1 = d3.select("#selDataset1").node().value;
    console.log(`Var 1: ${var1}`);
    var r1 = getRoutes(var1);
    console.log(`r1: ${r1}`);
    var var2 = d3.select("#selDataset2").node().value;
    console.log(`Var 2: ${var2}`);
    var r2 = getRoutes(var2);
    console.log(`r2: ${r2}`);
    var route = "/corr/" + r1 + "/" + r2;
    console.log(`Route: ${route}`);
    d3.json(route).then( function (corrData) {
    
      d3.selectAll(".countries").selectAll("path")
        .style("fill", d => d3.interpolateViridis((1 + corrData[d.properties.iso_a3]) / 2));
        
    });
  });

  d3.select("#selDataset2").on("change", function () {
    var var2 = d3.select("#selDataset2").node().value;
    var r2 = getRoutes(var2);
    var var1 = d3.select("#selDataset1").node().value;
    var r1 = getRoutes(var1);
    var route = "/corr/" + r1 + "/" + r2;
    console.log(`Route: ${route}`);
    console.log(d3.json(route)); 
    d3.json(route).then( function (corrData) {
    
      d3.selectAll(".countries").selectAll("path")
        .style("fill",d => d3.interpolateViridis((1 + corrData[d.properties.iso_a3]) / 2));
        
    });
  });

  d3.selectAll(".countries")
        .selectAll("path")
        .on("click", function (d, i) {

    let var1 = d3.select("#selDataset1").node().value;
    let code1 = getRoutes(var1);
    let var2 = d3.select("#selDataset2").node().value;
    let code2 = getRoutes(var2);
    let isoa3 = d.properties.iso_a3;
    let countryName = d.properties.name;
    let queryUrl =  "/ts_a3/" + isoa3 + "/" + code1 + "/" + code2;
    // queryUrl = "http://your-right-to-health-staging.herokuapp.com/ts_a3/AUS/EG-ELC-ACCS-ZS/CORRUPTION";
    console.log(queryUrl);
    d3.json(queryUrl).then(function(dataset) {
        let trace1 = {
            x: dataset.year1,
            y: dataset.value1,
            mode: 'lines+markers',
            name: `${var1}`,
            line: {shape: 'linear'},
            type: 'scatter'
            };

        let trace2 = {
            x: dataset.year2,
            y: dataset.value2,
            mode: 'lines+markers',
            name: `${var2}`,
            line: {shape: 'linear'},
            type: 'scatter',
            yaxis: 'y2'
            };
        let data = [trace1, trace2];
        let layout = {
            colorway: ['#0B0','#007'],
            title: `Trends in ${var1} and ${var2} in ${countryName}`,
            xaxis: { title: "Year" },
            yaxis: { 
              title: `${var1}`,
              titlefont: {color: 'rgb(0, 191, 0)'},
              tickfont: {color: 'rgb(0, 191, 0)'}
            },
            yaxis2: {
              title: `${var2}`,
              titlefont: {color: 'rgb(0, 0, 128)'},
              tickfont: {color: 'rgb(0, 0, 128)'},
              overlaying: 'y',
              side: 'right',
              showgrid: false
            }
          };
            
        Plotly.newPlot("line-graph", data, layout);
                
    }); // end of d3.json then
  });  // end of "on click" event for countries

}); // end of d3.json for correlations