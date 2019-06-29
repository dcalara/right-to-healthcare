//Globe demo
function rgbToHex (rgb) { 
  // For color conversion
  var hex = Number(rgb).toString(16);
  if (hex == "NaN") {
      hex = "0"
      }
  if (hex.length < 2) {
       hex = "0" + hex;
  }
  return hex;
};

function fullColorHex (r,g,b) {   
  var red = rgbToHex(r);
  var green = rgbToHex(g);
  var blue = rgbToHex(b);
  return red+green+blue;
};

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
    default:
      return "HRP-SCORE";
      break;
  }

}

function getGlobePolyColor(inputNum, minNum, maxNum) {

    inputNum = +inputNum;
    minNum = +minNum;
    maxNum = +maxNum;
    const num = (inputNum - minNum) / (maxNum - minNum);

    const r = Math.round(Math.min(Math.max(0,255*num), 255));
    const g = Math.round(Math.min(Math.max(0,255 * (1-num)), 255));
    const b = Math.round(Math.min(Math.max(0,255 - num*num), 255));

    return "#" + fullColorHex(r,g,b)

}

let options = { zoom: 1.0, position: [47.19537,8.524404] };
let globe1 = new WE.map('globe_1', options); 

WE.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
    attribution: '© OpenStreetMap contributors'
  }).addTo(globe1);

d3.select("#selDataset1").on("change", function () {

  //  d3.select("#globe_1").html("");

 //   let options = { zoom: 1.0, position: [47.19537,8.524404] };
 //   let globe1 = new WE.map('globe_1', options); 
  
    WE.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
        attribution: '© OpenStreetMap contributors'
    }).addTo(globe1);

    let dataset1 = d3.select("#selDataset1").node().value;
    
    let req_route = getRoutes(dataset1);
    console.log(req_route);
    d3.json("../static/data/countries.json").then(  function(data) { 

        const req_url = "/ts_all/" + req_route + "/2000";

        return d3.json(req_url).then( function (isodict) {
            // Get max and min values in object returned from server (isodict)
            // which is a set of iso_a3,value pairs 
            let minVal = 0.0;
            let maxVal = 0.0;
            firstKey = true;

            Object.keys(isodict).forEach( function (key) {
                if(firstKey) {
                    minVal = isodict[key];
                    maxVal = isodict[key];
                    firstKey = false;
                }
                else {
                    if (isodict[key] > maxVal) {
                      maxVal = isodict[key];
                    }
                    if (isodict[key] < minVal) {
                      minval = isodict[key];
                    }
                }
            });

            // Loop through every country provided and generate a polygon string object
            data.features.forEach( function (feature) {
                let innerColor = getGlobePolyColor(isodict[feature.properties.iso_a3], minVal, maxVal);
                let coordList = feature.geometry.coordinates;
                // Fix the coordinates list to switch from [lon lat] to [lat lon]
                let fixedList = [];
                coordList[0].forEach( function(lonlat) {
                    latlon = lonlat.reverse();
                    fixedList.push(latlon);
                });

                tempPoly = WE.polygon(fixedList, {
                    color: innerColor,
                    opacity: 1,
                    fillColor: innerColor,
                    fillOpacity: 0.5,
                    editable: false,
                    weight: 2
                });   // WE polygon
                tempPoly.addTo(globe1); 

            }); // forEach loop -- each country

        }); // d3.json.then async for data

    }); // d3.json.then async for map

}); // event listener


