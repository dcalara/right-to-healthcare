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
    }
}

console.log("hello");
d3.select("#selDataset1").on("change", function () {
    console.log("clicked");
    var1 = d3.select("#selDataset1").node().value;
    let code = getRoutes(var1);
    queryUrl =  "http://your-right-to-health-staging.herokuapp.com/ts_a3/USA/" + code;
    // queryUrl = "http://your-right-to-health-staging.herokuapp.com/ts_a3/AUS/EG-ELC-ACCS-ZS/CORRUPTION";
    console.log(queryUrl);
    d3.json(queryUrl).then(function(dataset) {
        var trace1 = {
            x: dataset.year1,
            y: dataset.value1,
            mode: 'lines+markers',
            name: 'linear',
            line: {shape: 'linear'},
            // type: 'scatter'
          };

          colors = ["rgba(67,67,67,1)"];
          var lineSize = [2];
          var label = ["Corruption index"];
          var data = [trace1];
          
          Plotly.newPlot("line-graph", data);
    });   

    
});
    