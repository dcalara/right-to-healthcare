//Globe demo

var options = { zoom: 1.0, position: [47.19537,8.524404] };
var globe1 = new WE.map('globe_1', options); 

WE.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
    attribution: '© OpenStreetMap contributors'
  }).addTo(globe1);