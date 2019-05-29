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
  var margin = {top: 50, right: 100, bottom: 100, left: 100};
  var svg_width = 900 - margin.right - margin.left;
  var svg_height = 600 - margin.top - margin.bottom;

  // create svg element
  var svg = d3.select("#bars")
              .append("svg")
                .attr("width", svg_width + margin.right + margin.left)
                .attr("height", svg_height + margin.top + margin.bottom)
                .attr("id", "bar_chart")
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

  // set click dummy to see if a pie chart has to be removed
  var click = 0;

  // create bar chart
  svg.selectAll("rect")
      .data(keys)
      .enter()
      .append("rect")
      .attr("x", function(d, i) {
            return x_scale(d) + 9
      })
      .attr("y", function(d, i) {
          return y_scale(datasettest[d]["Totaal huwelijkssluitingen"])
      })
      .attr("width", 15)
      .style("height", function(d) {
          return svg_height - y_scale(datasettest[d]["Totaal huwelijkssluitingen"])
      })
      .attr("fill", "pink")
      .attr("id", function(d,i){ return "_" + i; } )
      .on("mouseover", function(d, i) {
                                        mouse_over_bar(x_scale(d) + 9,
                                                  y_scale(datasettest[d]["Totaal huwelijkssluitingen"]),
                                                  svg_height - y_scale(datasettest[d]["Totaal huwelijkssluitingen"]),
                                                  i,
                                                  datasettest[d]["Totaal huwelijkssluitingen"])
                                })
      .on("mouseout", function(d, i) {
                                        mouse_out_bar(x_scale(d) + 9,
                                                  y_scale(datasettest[d]["Totaal huwelijkssluitingen"]),
                                                  svg_height - y_scale(datasettest[d]["Totaal huwelijkssluitingen"]),
                                                  i)
                                })
      .on("click", function(d) {
        if (click == 0){
          click = 1;
        }
        else {
          click = 2;
        }
        piechart_plot(datasettest[d], d, click);
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

  // title of the bar chart
  svg.append("text")
    .attr("class", "title_axis")
    .attr("transform", "translate(" + 200 + "," + -30 + ")")
    .text("Aantal huwelijksluitingen in Nederland per jaar");

  // text for the x axis
  svg.append("text")
    .attr("class", "title_axis")
    .attr("transform", "translate(" + (svg_width - margin.left)/2 + "," + (svg_height + margin.bottom - margin.top) + ")")
    .text("Tijd (in jaren)");

  // text for the y axis
  svg.append("text")
    .attr("class", "title_axis")
    .attr("transform", "rotate(-90)")
    .attr("x", - (svg_height/2 + 40))
    .attr("y", - (margin.left/2 + 15))
    .text("Totaal aantal huwelijksluitingen");

}

function mouse_over_bar(x, y, h, i, value){

  // change size and color of bar
  d3.select("#_" + i)
    .attr("fill", "rgb(219,112,147)")
    .attr("x", x - 2)
    .attr("y", y - 4)
    .attr("width", 19)
    .style("height", h + 4);

  // show value of bar in text
  d3.select("#bar_chart")
     .append('text')
       .attr("id", "_t")
       .attr("class", "mouse")
       .attr("x", x + 105)
       .attr("y", y + 45)
       .text(value)
}

function mouse_out_bar(x, y, h, i){

  // change size and color of bar
  d3.select("#_" + i)
    .attr("fill", "pink")
    .attr("x", x)
    .attr("y", y)
    .attr("width", 15)
    .style("height", h);

  // remove text
  d3.select("#_t").remove();

}

function piechart_plot(data, year, click){

  // remove previous pie chart if necessary
  if (click == 2){
    d3.select("#pie_chart").remove();
  }

  // define array of data for pie chart
  var pie_data = [data["Tussen man en vrouw"], data["Tussen mannen"], data["Tussen vrouwen"]];

  // set size piechart
  var margin = {top: 10, right: 10, bottom: 10, left: 10};
  var pie_width = 300 - margin.right - margin.left;
  var pie_height = 300 - margin.top - margin.bottom;
  var radius = pie_height/2;

  // create svg element for pie chart
  var svg = d3.select("#piechart")
              .append("svg")
                .attr("width", pie_width + margin.right + margin.left)
                .attr("height", pie_height + margin.top + margin.bottom)
                .attr("id", "pie_chart")
              .append("g")
                .attr("transform", "translate(" + pie_width/2 + "," + pie_height/2 + ")");

  // generate the arcs
  var arc = d3.arc()
              .innerRadius(80)
              .outerRadius(radius - 10);

  // generate the arcs
  var arc_over = d3.arc()
              .innerRadius(70)
              .outerRadius(radius);

  // generate pie data with arcs
  var arcs = d3.pie()(pie_data);

  var label_arc = d3.arc()
                    .innerRadius(radius - 30)
                    .outerRadius(radius - 30)

  // Define the div for the tooltip
  var tooltip = d3.select("#piechart").append("div")
      .attr("class", "tooltip");

  // create pie chart
  var paths = svg.selectAll("arcs")
                  .data(arcs)
                  .enter()

  // add the slices and mouse on/off
  paths.append("path")
        .attr("d", arc)
        .attr("fill", function(d){
          if (arcs.indexOf(d) == 0){
            return "rgb(255,228,225)";
          }
          else if (arcs.indexOf(d) == 1){
            return "pink"
          }
          else {
            return "rgb(219,112,147)"
          }
        })
        .on("mouseover", function(d){

        	d3.select(this)
            .transition()
               .duration(300)
               .attr("d", arc_over)

          paths.append('text')
               .attr("id", "_m")
               .attr("class", "mouse")
               .attr("transform", function(d) {
                    return "translate(" + arc.centroid(d) + ")"; })
               .text(function(d){
                     return d.data
                   })})

        .on("mouseout", function(d) {
        	d3.select(this).transition()
             .duration(300)
             .attr("d", arc)

          d3.select("#_m").remove()});

  // add legend
  svg.append('g')
  .attr('class', 'legend')
    .selectAll('text')
    .data(pie_data)
      .enter()
        .append('text')
          .text(function(d) {
            if (pie_data.indexOf(d) == 0){
            return "Tussen man en vrouw"
            }
            else if (pie_data.indexOf(d) == 1){
              return "Tussen mannen"
            }
            else {
            return "Tussen vrouwen"
          }}
          )
          .attr('fill', function(d) {
            if (pie_data.indexOf(d) == 0){
            return "rgb(255,228,225)"
            }
            else if (pie_data.indexOf(d) == 1){
              return "pink"
            }
            else {
            return "rgb(219,112,147)"
          }})
          .attr('y', function(d, i) { return 20 * (i + 1); })
          .attr('x', function(d, i) { return 20 * (i + 1); })
          .attr("transform", "translate(" + - 20 + "," + 0 + ")")

  // show year inside donut chart
  svg.append("text")
           .attr("class", "pie_year")
           .attr("transform", "translate(" + - 20 + "," + 0 + ")")
           .text(year);

}
