// set the date format when click the LoanByYear or LoanByMonth
let dateFormat = d3.timeFormat("%Y-%m");
// set the variable to store the years
let yearsRange = [];
// store the click map event
let clickedMapId;

/*
 * show the state name when click the state path
 * recover the attribute during 2s
 */
function mapClick() {
  let mapPath = d3.selectAll("div.loan-map > svg > g > path");

  mapPath.on('click', function(event) {
    /*
     * change the attribute when click
     */
    let [cordX, cordY] = d3.mouse(this);
    let currentPath = d3.select(d3.event.target);
    let currentColor = currentPath.style("fill");

    currentPath.style("fill", "#ff005a");

    if (clickedMapId === event.id) {
      return;
    } else {
      clickedMapId = event.id;
      /*
       * recover the attribute
       */
      d3.select("div.loan-map > svg")
        .append("text")
        .attr("class", "state-name")
        .attr("x", cordX)
        .attr("y", cordY)
        .transition()
        .duration(200)
        .style("fill", "#12012d")
        .text(event.properties.NAME10)

    }



    currentPath.transition()
      .duration(1000)
      .style("fill", currentColor);

    d3.selectAll("text.state-name")
      .transition()
      .duration(500)
      .delay(500)
      .remove();
  });
}


// display the detailed information about the specified circle
function interactive() {
  $("circle").click(function(event) {
    // set the change state
    $(this).attr("r", RADIUS * 2)
      .css("fill", "#00ffff");
    // get the states infomation about the click circle
    let stateName = event.target.__data__.value.state;

    let stateMessage;

    if (event.target.__data__.key === "2005") {
      stateMessage = `<p>The information about the borrower states was missing in the 2005</p>`
    } else {
      if (stateName.includes("")) {
        stateMessage = `<p>There is missing information about the borrower state, in the ${event.target.__data__.key}</p>
          <p>The users in the ${stateName.length - 1} states borrowed money by the Prosper</p>`
      } else {
        stateMessage = `<p>The users in the ${stateName.length} states borrowed money by the Prosper</p>`
      }
    }

    let message = `<p>In the ${event.target.__data__.key}, the amount of loan was \$${event.target.__data__.value.loan.toLocaleString("USD")}</p>`
    let divDoc = $("div.loan-doc");
    divDoc.html("")
      .append(message + stateMessage);

    d3.selectAll("p").attr("class", "report");

    // change the map color when click the point
    $("div.loan-map>svg>g>path").each((index, path) => {
      if (stateName.includes(path.__data__.properties.STUSPS10)) {
        d3.select(path).style("fill", "#00ffff");
      } else {
        d3.select(path).style("fill", PATHCOLOR);
      }
    });
    // recover the circle attribute
    let circle = d3.selectAll("circle")
      .transition()
      .delay(500)
      .attr("r", RADIUS)
      .style("fill", "red");
  });

}


// highlight the bar when mouse over
function barHighLight() {
  let yearSvg = d3.select("div.center-block.col-lg-6 > svg");
  yearSvg.selectAll(".bar")
    .on('mouseover', function(event) {
      // get the information about the bar
      if (event) {
        mapReport(event)
      }

      d3.select(this)
        .attr("class", "bar bar-target")
      // .transition()
      // .duration(300)
      // .attr("class", "bar");
    })
    .on('mouseout', function(event) {
      // event.preventDefault();
      /* Act on the event */
      d3.select(this)
        .attr("class", "bar");
    });

}


// highlight the map and report the data information according the data
function mapReport(fixdata) {
  let statesName = fixdata.value["state"]; // get array about the state
  let mapSvg = $("div.loan-map > svg > g > path");
  let report = $("div.loan-doc");
  let message,
    optionMessage;

  // create the message about the bar
  message = `<h3>In the ${d3.timeFormat("%Y %B")(fixdata.value["date"])},
            the loan amount was \$${fixdata.value["totalloan"].toLocaleString("USD")}.</h3>`;
  if (fixdata.value["state"].includes("") && fixdata.value["state"].length === 1) {
    optionMessage = `<h3>The information about the borrower states was missing.</h3>`
  } else if (fixdata.value["state"].length > 1) {
    if (fixdata.value["state"].includes("")) {
      optionMessage = `<h3>There was missing information about the borrower state</h3>
        <h3>The users in the ${fixdata.value["state"].length - 1} states borrowed money by the Prosper</h3>`
    } else {
      optionMessage = `<h3>The users in the ${fixdata.value["state"].length} states borrowed money by the Prosper</h3>`
    }
  }

  // show the message
  report.html("")
    .append(message + optionMessage);
  // add the control class
  d3.selectAll("h3").attr("class", "report");

  mapSvg.each((index, path) => {
    if (fixdata.value["state"].includes(path.__data__.properties.STUSPS10)) {
      d3.select(path)
        .style("fill", "#00ff00");
    } else {
      d3.select(path).style("fill", "grey");
    }
  });
}


function updateYear(loanYear, year) {
  // set the variable about layout and the variable about the information
  let yearSvg = d3.select("div.center-block.col-lg-6 > svg"),
    mapSvg = d3.select("div.loan-map").selectAll("path");
  let yearFormat = d3.timeFormat("%Y"),
    monthFormat = d3.timeFormat("%m"),
    svgHeight = yearSvg.attr("height"),
    svgWidth = yearSvg.attr("width"),
    years = new Set();
    months = new Set();

  yearSvg.selectAll("circle")
    .transition()
    .duration(100)
    .ease(d3.easeCircleOut)
    .attr("fill", "black")
    .remove();

  yearSvg.selectAll("path")
    .transition()
    .duration(100)
    .ease(d3.easePolyOut)
    .attr("fill", "white")
    .remove();

  d3.selectAll("g.axis-y")
    .transition()
    .duration(100)
    .ease(d3.easeCubicOut)
    .attr("display", "none")
    .remove();

  d3.selectAll("g.axis-x")
    .transition()
    .duration(100)
    .ease(d3.easeCubicOut)
    .attr("display", "none")
    .remove();

  d3.selectAll(".bar")
    .transition()
    .duration(100)
    .ease(d3.easeCubicOut)
    .attr("fill", "#97b1db")
    .remove();

  // filter the dataset about year selected
  let filterLoan = loanYear.filter(d => {
    return yearFormat(d.value["date"]) === year;
  });

  // sort the dataset by date
  filterLoan.sort(function(a, b) {
    a = new Date(a.value.date);
    b = new Date(b.value.date);
    return a > b ? 1 : a < b ? -1 : 0;
  });
  // get the max loan value and create the scale and the axis
  let maxLoan = d3.max(filterLoan, d => d.value["totalloan"]);

  let xScale = d3.scaleBand()
    .range([PADDING.left, svgWidth - PADDING.right])
    .round(true)
    .padding(0.5);

  let yScale = d3.scaleLinear()
    .rangeRound([svgHeight - PADDING.bottom, PADDING.top]);

  // change title
  d3.select("h2.loan-title")
    .text(`Loan Amount In The ${year}`);

  // make sure that the axis must be remove
  if ((! d3.selectAll("g.axis-y").empty()) || (d3.selectAll("g.axis-x").empty())) {
    d3.selectAll("g.axis-y").remove();
    d3.selectAll("g.axis-x").remove();
  }

  yScale.domain([0, maxLoan]);

  xScale.domain(filterLoan.map(d => d.value["date"]));

  let yAxis = d3.axisLeft(yScale)
    .ticks(yearsRange.length)
    .tickFormat(d => "$" + d.toLocaleString("USD"));

  let xAxis = d3.axisBottom(xScale)
    .tickFormat(dateFormat);

  let gY = yearSvg.append("g")
    .attr("class", "axis-y")
    .transition()
    .duration(500)
    .ease(d3.easeCubicIn)
    .attr("transform", `translate(${PADDING.left} , 0)`)
    .call(yAxis);


  let gX = yearSvg.append("g")
    .attr("class", "axis-x")
    .transition()
    .duration(500)
    .ease(d3.easeCubicIn)
    .attr("transform", `translate(0 , ${svgHeight - PADDING.bottom})`)
    .call(xAxis);

  yearSvg.selectAll(".bar").remove();
  // debugger;
  yearSvg.selectAll(".bar")
    .data(filterLoan)
    .enter().append("rect")
    .attr("class", "bar")
    .transition()
    .duration(1000)
    .ease(d3.easeCubicIn)
    .attr("x", d => xScale(d.value["date"]))
    .attr("y", d => yScale(d.value["totalloan"]))
    .attr("width", xScale.bandwidth())
    .attr("height", d => {
      return (svgHeight - PADDING.bottom - yScale(d.value["totalloan"]));
    });
  // call function about highlight bar
  barHighLight()

}


// show loan information about year
function dataActive(data) {
  let yearFormat = d3.timeFormat("%Y"),
    yearSvg = d3.select("div.center-block.col-lg-6 > svg"),
    monthFormat = d3.timeFormat("%m"),
    svgHeight = yearSvg.attr("height"),
    svgWidth = yearSvg.attr("width"),
    years = new Set();
    months = new Set();
  let mapSvg = d3.select("div.loan-map").selectAll("path");
  mapSvg.attr("class", "map");
  d3.select("text.legend-y")
    .text("Loan")
  // aggerate the data by dateFormat
    let loanYear = d3.nest()
      .key(d => {
        years.add(yearFormat(d["date"]));
        return dateFormat(d["date"]);
      })
      .rollup(leaves => {
        let totalLoan = d3.sum(leaves, (d) => d["loan"]);
        let statesName = d3.set();
        let date = new Date(dateFormat(leaves[0].date));
        leaves.forEach(d => statesName.add(d["state"]));
        return {
          "totalloan": totalLoan,
          "state": statesName.values(),
          "date": date,
        };
      })
      .entries(data)

    years.forEach(d => yearsRange.push(d));


    // firstly show the data information in 2013
    updateYear(loanYear, "2013");

    /*
     * add a element select in order to adding interactive about year, which
     * is used by the jquery
     */
    let selectOption = `<select class="year-select form-control col-lg-6"><option value="year"
    selected="selected">year</option>`;
    let addOption = ``;
    yearsRange.sort().forEach(d => {
      addOption = addOption + `<option value="${d}">${d}</option>`;
      return addOption;
    });

    if ($("select.year-select").index() === -1) {
      $("div.center-block > svg").before(selectOption + addOption + `</select>`);
    }

    // display the year selected information
    $(document).on("change", "select.year-select", function() {
      /* body... */
      if ($(this).val() !== "year") {
        updateYear(loanYear, $(this).val());
      }
    });
    mapClick();
  }

/**
* create the interacive when click loanbyyear
*/
function interactiveYear() {
    /**
   * click the loanbyyear botton to trigger the event
   */
  d3.csv("data/dataset.csv", d => {
    d["date"] = new Date(d["LoanOriginationDate"]);
    d["loan"] = +d["LoanOriginalAmount"];
    d["status"] = d["LoanStatus"];
    d["state"] = d["BorrowerState"];
    return d;
  }, dataActive)
}


