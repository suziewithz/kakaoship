
function oneOnOneBarChart(id, oData){

      sB = {};
      data = [{"couple": "couple", "name": [], "times": []}];
      oData.forEach(function(d){
        data[0].name.push(d.name);
        data[0].times.push(d.children[0].note);
      })

      data.forEach(function(d){
        d.N = d.times[0] +d.times[1];
      })
        var margin = {top: 100, right: 20, bottom: 10, left: 20},
            width = 800 - margin.left - margin.right,
            height = 150 - margin.top - margin.bottom;

        var y = d3.scale.ordinal()
            .rangeRoundBands([0, height], .3);

        var x = d3.scale.linear()
            .rangeRound([0, width]);

        var color = d3.scale.ordinal()
            .range(["#f6a580", "#92c6db"]);

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("top");

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left")

        var svg = d3.select(id).append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .call(responsivefy)
            .attr("id", "d3-plot")
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

          color.domain([data[0].name[0], data[0].name[1]]);

      data.forEach(function(d) {
        // calc percentages
        d[d.name[0]] = +d.times[0]*100/d.N;
        d[d.name[1]] = +d.times[1]*100/d.N;

        //중간 바
        var x0 = 0;

        var idx = 0;
        d.boxes = color.domain().map(function(name) { return {name: name, x0: x0, x1: x0 += +d[name], N: +d.N, n: +d.times[idx++]}; });
      });
    console.log(data);
      var min_val = d3.min(data, function(d) {
              return 0;
              });

      var max_val = d3.max(data, function(d) {
              return 100;
              });

      x.domain([min_val, max_val]).nice();
      y.domain(data.map(function(d) { return d.couple; }));


      var divideLineX = [];
      //x좌표
      svg.append("g")
          .attr("class", "x axis")
          .call(xAxis);

     //바 준비
      var vakken = svg.selectAll(".couple")
          .data(data)
        .enter().append("g")
          .attr("class", "bar")
          .attr("transform", function(d) { return "translate(0," + y(d.couple) + ")"; });

          //서버바 생성 
      var bars = vakken.selectAll("rect")
          .data(function(d) { return d.boxes; })
        .enter().append("g").attr("class", "subbar");

      bars.append("rect")
          .attr("height", y.rangeBand())
          .attr("x", function(d) { return x(d.x0); })
          .attr("width", function(d) { divideLineX.push(x(d.x1) - x(d.x0)); return x(d.x1) - x(d.x0); })
          .style("fill", function(d) { return color(d.name); });


      //바 안의 텍스트
      bars.append("text")
          .attr("x", function(d) { return x(d.x0); })
          .attr("y", y.rangeBand()/2)
          .attr("dy", "0.5em")
          .attr("dx", "0.5em")
          .style("font" ,"10px sans-serif")
          .style("text-anchor", "begin")
          .style("float", function(d, i){ return i==0? "left":"right"})
          .text(function(d) { return d.N !== 0 && (d.x1-d.x0)>3 ? d.n : "" });

     //중간 라
      svg.append("g")
          .attr("class", "y axis")
      .append("line")
          .attr("x1", function(d, i){ return divideLineX[i]; })
          .attr("x2", function(d, i){ return divideLineX[i]; })
          .attr("y2", height);

      var startp = svg.append("g").attr("class", "legendbox").attr("id", "mylegendbox");
      // this is not nice, we should calculate the bounding box and use that
      var legend_tabs = [0, 120, 200, 375, 450];
      var legend = startp.selectAll(".legend")
          .data(color.domain().slice())
        .enter().append("g")
          .attr("class", "legend")
          .attr("transform", function(d, i) { return "translate(" + legend_tabs[i] + ",-45)"; });

      legend.append("rect")
          .attr("x", 0)
          .attr("width", 18)
          .attr("height", 18)
          .style("fill", color);

      legend.append("text")
          .attr("x", 22)
          .attr("y", 9)
          .attr("dy", ".35em")
          .style("text-anchor", "begin")
          .style("font" ,"10px sans-serif")
          .text(function(d) { return d; });

      d3.selectAll(".axis path")
          .style("fill", "none")
          .style("stroke", "#000")
          .style("shape-rendering", "crispEdges")

      d3.selectAll(".axis line")
          .style("fill", "none")
          .style("stroke", "#000")
          .style("shape-rendering", "crispEdges")

      var movesize = width/2 - startp.node().getBBox().width/2;
      d3.selectAll(".legendbox").attr("transform", "translate(" + movesize  + ",0)");
}


