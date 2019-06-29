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
    default:
      return "HRP-SCORE";
      break;
  }}

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
    var route = "http://your-right-to-health-staging.herokuapp.com/corr/" + r1 + "/" + r2;
    console.log(`Route: ${route}`);
    console.log(d3.json(route)); 
    d3.json(route).then(function(data1){
      svgMap.selectAll(".countries").selectAll(path)
      .style("fill", function(d) {return getColor(data1[d.properties.iso_a3])})
    });
  })

  d3.select("#selDataset2").on("change", function () {
    var var2 = d3.select("#selDataset2").node().value;
    var r2 = getRoutes(var2);
    var var1 = d3.select("#selDataset1").node().value;
    var r1 = getRoutes(var1);
    var route = "http://your-right-to-health-staging.herokuapp.com/corr/" + r1 + "/" + r2;
    console.log(`Route: ${route}`);
    console.log(d3.json(route)); 
    d3.json(route).then(function(data2){
      svgMap.selectAll(".countries").selectAll(path)
      .style("fill", function(d) {return getColor(data2[d.properties.iso_a3])})
    });
  }) 

});