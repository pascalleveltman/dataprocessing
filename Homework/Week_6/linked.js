// Pascalle Veltman, 11025646

window.onload = function () {

  // import json data files
  var requests = [d3.json("Huwelijken_json.json")];

  // call plot function with given data file
  Promise.all(requests).then(function(response) {

      console.log(response);
      barchart_plot(response);

  });

};

function barchart_plot(input){

  // define keys to make it possible to loop over data
  let datasettest = input[0];
  let keys = Object.keys(datasettest);

  // set width and height for svg
  var margin = {top: 200, right: 100, bottom: 100, left: 100};
  var svg_width = 900 - margin.right - margin.left;
  var svg_height = 700 - margin.top - margin.bottom;

  // create SVG element
  var svg = d3.select("body")
              .append("svg")
              .attr("width", svg_width + margin.right + margin.left)
              .attr("height", svg_height + margin.top + margin.bottom)
              .append("g")
              .attr("transform",
                    "translate(" + margin.left + "," + margin.top + ")");

  // create x scale function where nothing changes
  var x_scale = d3.scaleBand()
                  .domain(keys)
                  .rangeRound([0, svg_width])
                  .paddingInner(0.2);

  // set the scale for the x axis
  var y_scale = d3.scaleLinear()
      .domain([0, d3.max(keys, function(d) {
        return datasettest[d]["Totaal huwelijkssluitingen"];
      })])
      .range([svg_height, 0])
      .nice();

  // add grid lines
  svg.append('g')
    .attr('class', 'grid')
    .call(d3.axisLeft()
        .scale(y_scale)
        .tickSize(-svg_width, 0, 0)
        .tickFormat(''))

  // create bar chart
  svg.selectAll("rect")
      .data(keys)
      .enter()
      .append("rect")
      .attr("x", function(d, i) {
            return x_scale(d) + 9
      })
      .attr("y", function(d, i) {
          return y_scale(datasettest[d]["Totaal huwelijkssluitingen"]);
      })
      .attr("width", 15)
      .style("height", function(d) {
          return svg_height - y_scale(datasettest[d]["Totaal huwelijkssluitingen"]);
      })
      .attr("fill", "pink")
      .on("click", function(d) {
        piechart_plot(datasettest[d]);
        console.log("Click!")
      });

  // draw x axis
  svg.append("g")
      .attr("transform", "translate(0," + svg_height + ")")
      .attr("class", "axis")
      .call(d3.axisBottom(x_scale));

  // draw y axis
  svg.append("g")
      .attr("class", "axis")
      .call(d3.axisLeft(y_scale));


}

function piechart_plot(data){

  // define array of data for pie chart
  pie_data = [data["Tussen man en vrouw"], data["Tussen mannen"], data["Tussen vrouwen"]];
  console.log(pie_data);

  // choose radius
  var pie_width = 200;
  var pie_height = 200;
  var radius = 0.4 * pie_width;

  var svg = d3.select("body")
              .append("svg")
              .attr("width", pie_width)
              .attr("height", pie_height)

  var g = svg.append("g")
             .attr("transform", "translate(" + pie_width / 2 + "," + pie_height / 2 + ")");

  // generate pie
  var pie = d3.pie();

  // Generate the arcs
  var arc = d3.arc()
              .innerRadius(0)
              .outerRadius(radius);

  //Generate groups
  var arcs = g.selectAll("arc")
                .data(pie_data)
                .enter()
                .append("g");

  //Draw arc paths
    arcs.append("path")
        .attr("fill", "pink")
        .attr("d", arc);
}
