// function to test country coloring -- temporary
function getColor(num) {
    console.log(num);
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
   

});