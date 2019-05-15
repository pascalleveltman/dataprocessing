// Pascalle Veltman, 11025646

function load() {

  console.log('Yes, you can!');

  // import json data files
  var requests = [d3.json("teenpregnancy.json"), d3.json("teensarea.json"), d3.json("gdp.json")];

  // call sort function with given data files
  Promise.all(requests).then(function(response) {

      var data = sort_data(response);
      console.log(data);
      scatter_plot(data);

  });

};

function sort_data(data){

    // create empty json file for sorted data
    var sorted_data = {
      "2012" : [],
      "2013" : [],
      "2014" : [],
      "2015" : []
    };

    // sorting the pregnancies per country
    Object.values(data[0]).forEach(function (d){

        // store values per year
        d.forEach(function (e){

            // check if year is saved in data set
            var year = e.Time;
            if (parseInt(year) > 2011 && parseInt(year) < 2016){

                var place = {};
                place.country = e.Country;
                place.pregnancies = e.Datapoint;

                sorted_data[e.Time].push(place);
             }

        });

    });

    // sorting the areas per country
    Object.values(data[1]).forEach(function(d){

        // store values per year
        d.forEach(function (e){

            // check if year is saved in data set
            var year = e.Time;
            if (parseInt(year) > 2011 && parseInt(year) < 2016){

                sorted_data[year].forEach(function (f){

                    if (f.country == e.Country){
                        f["areas"] = e.Datapoint;

                    }

                })

            }

        })

    });

    // sorting the areas per country
    Object.values(data[2]).forEach(function(d){

        // store values per year
        d.forEach(function (e){

            // check if year is saved in data set
            var year = e.Year;
            if (parseInt(year) > 2011 && parseInt(year) < 2016){

                sorted_data[year].forEach(function (f){

                    if (f.country == e.Country){
                        f["gdp"] = e.Datapoint;
                    }

                })

            }

         })

      });

    // remove incomplete data arrays from data set
    Object.values(sorted_data).forEach(function(d){

        d.forEach(function(e){

            if (Object.keys(e).length != 4){

                d.splice( d.indexOf(e), 1 );

            }

        })
    });

    return sorted_data;

}

function scatter_plot(data){

    // select a year to plot data
    var plot_year = document.getElementById("myBtn").value;
    var plot_data = data[plot_year];
    console.log(plot_data);

    // set width and height for svg
    var margin = {top: 100, right: 100, bottom: 100, left: 100};
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

    // set the scale for the x axis
    var x_scale = d3.scaleLinear()
        .domain([0, d3.max(plot_data, function(d) {
          return d.pregnancies;
        })])
        .range([0, svg_width])
        .nice();

    // set the scale for the y axis
    var y_scale = d3.scaleLinear()
         .domain([0, d3.max(plot_data, function(d) {
            return d.areas;
         })])
         .range([svg_height, 0])
         .nice();

   // set the colour for scale of gdp
   var gdp_scale = d3.scaleLinear()
        .domain([d3.min(plot_data, function(d) {
           return d.gdp;
        }), d3.max(plot_data, function(d) {
           return d.gdp;
        })])
        .range([51, 255]);

    var gdp_colorscale = d3.scaleQuantize()
        .domain([d3.min(plot_data, function(d) {
           return d.gdp;
        }), d3.max(plot_data, function(d) {
           return d.gdp;
        })])
        .range(["rgb(0, 255, 0)", "rgb(0, 51, 0)"]);

    var gdp_legend = d3.legendColor(gdp_colorscale);

    // draw data points
    svg.selectAll("circle")
       .data(plot_data)
       .enter()
       .append("circle")
       .attr("cx", function(d) {
         return x_scale(d.pregnancies);
        })
       .attr("cy", function(d) {
         return svg_height - y_scale(d.areas);
        })
       .attr("fill", function(d) {
            return "rgb(0, " + gdp_scale(d.gdp) + ", 0)";
        })
       .attr("r", 6);

    // name country next to data point
    svg.selectAll("text")
       .data(plot_data)
       .enter()
       .append("text")
       .text(function(d) {
         return d.country;
        })
       .attr("x", function(d) {
         return x_scale(d.pregnancies)
        })
       .attr("y", function(d) {
         return svg_height - y_scale(d.areas)
        })
       .attr("font-family", "sans-serif")
       .attr("font-size", "10px")
       .attr("fill", "black");

    svg.append("g")
  		.attr("transform", "translate(" + 620 + "," + 20 + ")")
  		.call(gdp_legend);

    // // create bars from data
    // var positions = [200, 250, 300, 255, 153, 51];
    // svg.selectAll("rect")
    //          .data(positions)
    //          .enter()
    //          .append("rect")
    //          .attr("x", function(d) {
    //                return positions[d]
    //          })
    //          .attr("y", 10)
    //          .attr("width", 20)
    //          .attr("height", 20)
    //          .attr("fill", "rgb(0, " + function(d) {
    //                 return colours[d+3]
    //               } + ", 0)");

    // text for the x axis
    svg.append("text")
      .attr("transform", "translate(" + svg_width/2 + "," + (svg_height + margin.top - margin.bottom/2) + ")")
      .text("Pregnancies");

    // text for the y axis
    svg.append("text")
  		.attr("transform", "rotate(-90)")
  		.attr("x", - 250)
  		.attr("y", - 50)
  		.text("Areas");

    // draw x axis
    var x_axis = d3.axisBottom(x_scale);

    // draw y axis
    var y_axis = d3.axisLeft(y_scale);

    svg.append("g")
        .attr("transform", "translate(0," + svg_height + ")")
        .call(x_axis);

    svg.append("g")
        .call(y_axis);

}
