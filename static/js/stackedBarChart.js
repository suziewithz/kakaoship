function dashResponsivefy(svg) {
  // get container + svg aspect ratio
    var container = d3.select(svg.node().parentNode),
        width = parseInt(svg.style("width")),
        height = parseInt(svg.style("height")),
        aspect = width / height;

    // add viewBox and preserveAspectRatio properties,
    // and call resize so that svg resizes on inital page load
    svg.attr("viewBox", "0 0 " + width + " " + height)
        .attr("perserveAspectRatio", "xMinYMid")
        .call(resize);

    // to register multiple listeners for same event type, 
    // you need to add namespace, i.e., 'click.foo'
    // necessary if you call invoke this function for multiple svgs
    // api docs: https://github.com/mbostock/d3/wiki/Selections#on
    d3.select(window).on("resize." + container.attr("id"), resize);

    // get width of container and resize svg to fit it
    function resize() {
        var targetWidth = parseInt(container.style("width"));
        svg.attr("width", targetWidth);
        svg.attr("height", Math.round(targetWidth / aspect));
    }
}

function oneOnOneBarChart(histoGramId, fData){
    var barColor = 'steelblue';
    var data={};
    var i = 0;

    for(key in fData[0].freq) {
        switch (i){
            case 0:
                data[key] = "#f6a580";
                break;
            case 1:
                data[key] =  "#92c6db";
                break;
        }
        i++;
    }

    function segColor(c){
     return data[c]; 
    }
    
    // compute total for each state.
    fData.forEach(function(d){
        d.total = 0;
        for(var i in d.freq){
            d.total += d.freq[i]; 
        }
    });
    
    // function to handle histogram.
    function histoGram(fD){
        var hG={},    hGDim = {t: 60, r: 0, b: 30, l: 0};
        hGDim.w = 500 - hGDim.l - hGDim.r, 
        hGDim.h = 300 - hGDim.t - hGDim.b;
            
        //create svg for histogram.
        var hGsvg = d3.select(histoGramId).append("svg")
            .attr("width", hGDim.w + hGDim.l + hGDim.r)
            .attr("height", hGDim.h + hGDim.t + hGDim.b)
            .call(dashResponsivefy)
            .append("g")
            .attr("transform", "translate(" + hGDim.l + "," + hGDim.t + ")");
            

        // create function for x-axis mapping.
        var x = d3.scale.ordinal().rangeRoundBands([0, hGDim.w], 0.1)
                .domain(fD.map(function(d) { return d[0]; }));

        // Add x-axis to the histogram svg.
        hGsvg.append("g").attr("class", "x axis")
            .attr("transform", "translate(0," + hGDim.h + ")")
            .call(d3.svg.axis().scale(x).orient("bottom"));

        // Create function for y-axis map.
        var y = d3.scale.linear().range([hGDim.h, 0])
                .domain([0, d3.max(fD, function(d) { return d[1]; })]);

        // Create bars for histogram to contain rectangles and freq labels.
        var bars = hGsvg.selectAll(".bar").data(fD).enter()
                .append("g").attr("class", "bar");
        
        //create the rectangles.
        bars.append("rect")
            .attr("x", function(d) { return x(d[0]); })
            .attr("y", function(d) { return y(d[1]); })
            .attr("width", x.rangeBand())
            .attr("height", function(d) { return hGDim.h - y(d[1]); })
            .attr('fill',barColor)
            .on("mouseover",mouseover)// mouseover is defined below.
            .on("mouseout",mouseout);// mouseout is defined below.
            
        //Create the frequency labels above the rectangles.
        bars.append("text").text(function(d){ return d3.format(",")(d[1])})
            .attr("x", function(d) { return x(d[0])+x.rangeBand()/2; })
            .attr("y", function(d) { return y(d[1])-5; })
            .attr("text-anchor", "middle");
        
        function mouseover(d){  // utility function to be called on mouseover.
            // filter for selected state.
            var st = fData.filter(function(s){ return s.State == d[0];})[0],
                nD = d3.keys(st.freq).map(function(s){ return {type:s, freq:st.freq[s]};});
               
            // call update functions of pie-chart and legend.    
            sB.update(nD);
        }
        
        function mouseout(d){    // utility function to be called on mouseout.
            // reset the pie-chart and legend.    
            sB.update(tF);
            
        }
        
        // create function to update the bars. This will be used by pie-chart.
        hG.update = function(nD, color){
            // update the domain of the y-axis map to reflect change in frequencies.
            y.domain([0, d3.max(nD, function(d) { return d[1]; })]);
            
            // Attach the new data to the bars.
            var bars = hGsvg.selectAll(".bar").data(nD);
            
            // transition the height and color of rectangles.
            bars.select("rect").transition().duration(500)
                .attr("y", function(d) {return y(d[1]); })
                .attr("height", function(d) { return hGDim.h - y(d[1]); })
                .attr("fill", color);

            // transition the frequency labels location and change value.
            bars.select("text").transition().duration(500)
                .text(function(d){ return d3.format(",")(d[1])})
                .attr("y", function(d) {return y(d[1])-5; });            
        }        
        return hG;
    }

    function stackedBarChart(oData){

      sB = {};
      data = [{"couple": "couple", "name": [], "times": []}];
      oData.forEach(function(d){
        data[0].name.push(d.type);
        data[0].times.push(d.freq);
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

        var svg = d3.select("#figure").append("svg")
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


        sB.update = function(nD, color){
            // update the domain of the y-axis map to reflect change in frequencies.
            // y.domain([0, d3.max(nD, function(d) { return d[1]; })]);
            
            // Attach the new data to the bars.
            var bars = svg.selectAll(".bar").data(nD);
            
            // transition the height and color of rectangles.
            bars.select("rect").transition().duration(500)
                .attr("y", function(d) {return x(d[1]); })
                .attr("height", function(d) { return hGDim.h - y(d[1]); })
                .attr("fill", color);

            // transition the frequency labels location and change value.
            bars.select("text").transition().duration(500)
                .text(function(d){ return d3.format(",")(d[1])})
                .attr("y", function(d) {return y(d[1])-5; });            
        }      


        return sB;
    }

    var tF = Object.keys(data).map(function(d){ 
        return {type:d, freq: d3.sum(fData.map(function(t){ return t.freq[d];}))}; 
    });    
    
    // calculate total frequency by state for all segment.
    var sF = fData.map(function(d){return [d.State,d.total];});

    var hG = histoGram(sF) // create the histogram.
        sB = stackedBarChart(tF) // create the pie-chart.

}



