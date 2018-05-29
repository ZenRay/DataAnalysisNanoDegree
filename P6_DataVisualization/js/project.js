let MARGIN = {
    top: 30,
    left: 0
  },
  PADDING = {
    top: 20,
    right: 70,
    bottom: 20,
    left: 70,
  },
  WIDTH = 650 - MARGIN.left,
  HEIGHT = 600 - MARGIN.top,
  RADIUS = 5,
  MULTIPLIER = 1000,
  PATHCOLOR = "grey";


// set the layout
let div = d3.select("div.loan");

let title = div.append("h2")
  .attr("class", "loan-title col-lg-12")
  .text("Loan In The Years Between 2005 And 2014");
let divSvg = div.append("div")
  .attr("class", "loan-plot")
  .attr("class", "center-block col-lg-6")
  .append("svg")
  .attr("width", WIDTH + MARGIN.left)
  .attr("height", HEIGHT + MARGIN.top);

let divSelect = div.append("div")
  .attr("class", "col-lg-6 report-map");

let divDoc = divSelect.append("div")
  .attr("class", "loan-doc")
  .style("padding-left", PADDING.left)
  .select("div.loan-doc");

// let divSelect = div.append("div");

let divMap = divSelect.append("div")
  .attr("class", "loan-map")
  .style("padding-left", PADDING.left)
  .append("svg")
  .attr("width", WIDTH + MARGIN.left)
  .attr("height", (HEIGHT + MARGIN.top) * 2 / 3);


// aggregation about loan data in every year
function yearLoan(leaves) {
  let state = d3.set();

  let yearTotal = d3.sum(leaves, d => d["loan"]);

  leaves.forEach(d => state.add(d["BorrowerState"]));

  return {
    "loan": yearTotal,
    "state": state.values(),
  };
}
/*
* create the function to draw map
*/
function drawMap(geo_data) {
  // use the statetopo.json with state name to plot map
  let projection = d3.geoAlbersUsa()
    .scale(600)
    .translate([WIDTH / 3 , HEIGHT / 3]);
  let path = d3.geoPath().projection(projection);

  divMap.style("display", "flex")
    .append("g")
    .selectAll("path")
    .data(topojson.feature(geo_data, geo_data.objects.state).features)
    .enter()
    .append("path")
    .attr("class", "map")
    .attr("d", path)
    .attr("stroke-width", 0.5)
    // .attr("fill", "grey")
    .attr("stroke", "white");

  // hidding the map
  divMap.style("display", "none");
  mapClick()

}

function loan(data) {
  // set the aggregate date format
  let yearFormat = d3.timeFormat("%Y");

  let yearNest = d3.nest()
    .key(d => yearFormat(d["date"]))
    .sortKeys(d3.asceding)
    .rollup(yearLoan)
    .entries(data);

  // plot the svg
  let loanRange = d3.extent(yearNest, d => d.value["loan"]);

  let dateRange = d3.extent(data, d => d["date"]);

  // set the value scale
  let yScale = d3.scaleLinear()
    .range([HEIGHT, PADDING.top])
    .domain([0, loanRange[1] / MULTIPLIER])
    .nice();

  let xScale = d3.scaleTime()
    .range([PADDING.left, WIDTH - PADDING.right])
    .domain([d3.timeYear(dateRange[0]), d3.timeYear(dateRange[1])]);
  // set the axis
  let xAxis = d3.axisBottom(xScale)
    .ticks(d3.timeYear);
  let yAxis = d3.axisLeft(yScale)
    .ticks(7);

  let gY = divSvg.append("g")
    .attr("class", "axis-y");
  let gX = divSvg.append("g")
    .attr("class", "axis-x");

  gY.attr("transform", "translate(" + PADDING.left + ",0)")
    .call(yAxis);

  gX.attr("transform", "translate(0" + "," + HEIGHT + ")")
    .call(xAxis);

  // add axis legend
  divSvg.append("text")
    .attr("class", "legend-y")
    .attr("x", PADDING.bottom)
    .attr("y", 15)
    .attr("font-size", "15")
    .text(`Loan (multiply ${MULTIPLIER} unit: $)`);

  divSvg.append("text")
    .attr("class", "legend-x")
    .attr("x", WIDTH - PADDING.right)
    .attr("y", HEIGHT)
    .attr("font-size", "15")
    .text("DATE");

  let circle = divSvg.selectAll("circle")
    .data(yearNest)
    .enter()
    .append("circle")
    .transition()
    .duration(1000)
    .attr("cx", d => xScale(new Date(d.key)))
    .attr("cy", d => yScale(d.value["loan"] / MULTIPLIER))
    .attr("r", RADIUS);
  // plot the line
  let lineFunction = d3.line()
    .x(d => xScale(new Date(d.date)))
    .y(d => yScale(d.loan / MULTIPLIER));
  let lineData = [];
  yearNest.sort((a, b) => a.key > b.key).forEach(d => {
    let temData = {};
    temData.date = d.key;
    temData.loan = d.value.loan;
    lineData.push(temData);
  });

  divSvg.append("path")
    .datum(lineData)
    .attr("fill", "none")
    .attr("stroke", "steelblue")
    .attr("stroke-linjoin", "round")
    .attr("stroke-linecap", "round")
    .attr("stroke-width", 1.5)
    .attr("d", lineFunction)
    .transition();

  // display the trending information
  let message = `<h2>Rough Information</h2>
                  <h3 class="report">1)Before 2013, the loan amount growed as the year increased</h3>
                  <h3 class="report">2)But the loan amount declined extremely after 2013</h3>
                  <h3 class="report">3)In 2005, the loan amount was $78,687</h3>
                  <h3 class="report"style="color:red">4)Get information in detail by clicking the point</h3>`;
  // append the message by jquery
  $("div.loan-doc").append(message);
  // draw map

  d3.json("data/statetopo.json", drawMap)

  interactive()

}

/*
* make a closure about showing loan information about every year when click the
* LoanByYear and the loan function
*/

// function allFunc(data) {
//   // call the function loan
//   loan(data)

//   // call the function about dataActive when click the loanByYear
//   $("#navbar > ul > li:nth-child(1) > a").click((event) => {
//     dataActive(data)
//   });
// }
d3.csv("data/dataset.csv", d => {
  // debugger;
  d["date"] = new Date(d["LoanOriginationDate"]);
  d["loan"] = +d["LoanOriginalAmount"];
  d["state"] = d["BorrowerState"];
  return d;
}, loan)