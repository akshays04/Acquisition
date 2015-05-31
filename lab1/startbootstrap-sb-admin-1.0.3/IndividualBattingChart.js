var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var parseDate = d3.time.format("%d-%b-%y").parse;

var color = d3.scale.category10();

var x = d3.time.scale()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");
    
var tip = d3.tip()
.attr('class', 'd3-tip')
.offset([-10, 0])
.html(function(d) {
		return "<strong>Runs:</strong> <span style='color:red'>" + d.runs + "</span><br><strong>Opponent:</strong> <span style='color:red'>" + d.opponent + "</span><br><strong>Date:</strong> <span style='color:red'>" + d.date + "</span>";
})    

var line = d3.svg.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.runs); });

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    

svg.call(tip);

d3.json("ScatterChart.json", function(error, data) {
	data=data[0]['allRecords']
  data.forEach(function(d) {  
	  //d.date = Date.parse(dateString);
    d.date = parseDate(d.date);
    d.runs = +d.runs;
  });

  x.domain(d3.extent(data, function(d) { return d.date; }));
  y.domain(d3.extent(data, function(d) { return d.runs; }));
  
  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Runs");

  svg.append("path")
      .datum(data)
      .attr("class", "line")
      .attr("d", line);
  
  svg.selectAll("dot")
  .data(data)
  .enter().append("circle")
  .attr("class", "dot")
  .attr("r", 3.5)
  .attr("fill",function(d){if(d.win=="True")return "green";else return "red";})
  .attr("cx", function(d) { return x(d.date); })
  .attr("cy", function(d) { return y(d.runs); })
  .on('mouseover', tip.show)
  .on('mouseout', tip.hide);
})

svg.append("text")
        .attr("x", (width / 2))             
        .attr("y", 0 - (margin.top / 3))
        .attr("text-anchor", "middle")  
        .style("font-size", "16px") 
        .style("text-decoration", "underline")  
        .text("Rohit Sharma Batting Stats")
;
