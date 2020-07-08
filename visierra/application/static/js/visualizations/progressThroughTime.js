

var svg = d3.select("#my_palette")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")"
    );



function plot_parsed_data(data, allGroups, y_range, x_range){
    var dataReady = allGroups.map(
        function(groupName){
            return {
                name: groupName,
                values: data.map(
                    function(d){
                        return {time: d["timestamp"], value: +d[groupName]}
                    }
                )
            };
        }
    );

    console.log(dataReady.length)

    var myColor = d3.scaleOrdinal()
        .domain(allGroups)
        .range(d3.schemeCategory20);

    // todo: the following domain has to be changed
    // to a variable set by the flask caller.
    var x = d3.scaleLinear()
        .domain(y_range)
        .range([0, width]);

    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    // adding the y axis
    var y = d3.scaleLinear()
        .domain(x_range)
        .range([height, 0]);

    svg.append("g")
        .call(d3.axisLeft(y));

    // adding the lines
    var line = d3.line()
        .x(function(d){
            return x(+d.time)
        })
        .y(function(d){
            return y(+d.value)
        });

    svg.selectAll("myLines")
        .data(dataReady)
        .enter()
        .append("path")
            .attr("class", function(d){return d.name})
            .attr("d", function(d){return line(d.values)})
            .attr("stroke", function(d){ return myColor(d.name)})
            .attr("stroke-width", 4)
            .style("fill", "none");

    svg.selectAll("myDots")
        .data(dataReady)
        .enter()
            .append("g")
            .style("fill", function(d){return myColor(d.name)})
            .attr("class", function(d){return d.name})
        .selectAll("myPoints")
        .data(function(d){return d.values})
        .enter()
        .append("circle")
            .attr("cx", function(d){return x(d.time)})
            .attr("cy", function(d){return y(d.value)})
            .attr("r", 5)
            .attr("stroke", "white");

    svg.selectAll("myLabels")
        .data(dataReady)
        .enter()
        .append("g")
        .append("text")
            .attr("class", function(d){return d.name})
            .datum(function(d){return {name: d.name, value: d.values[d.values.length-1]};})
            .attr("transform", function(d){return "translate("+ x(d.value.time) + "," + y(d.value.value) + ")"; })
            .attr("x", 12)
            .text(function(d){return d.name})
            .style("fill", function(d){return myColor(d.name)})
            .style("font-size", 15);

    svg.selectAll("myLegend")
        .data(dataReady)
        .enter()
            .append("g")
            .append("text")
            .attr("x", function(d, i){return 30 + i*60})
            .attr("y", 30)
            .text(function(d){return d.name})
            .style("fill", function(d){return myColor(d.name)})
            .style("font-size", 15)
        .on("click",
            function(d){
                currentOpacity = d3.selectAll("." + d.name).style("opacity");
                d3.selectAll("." + d.name).transition().style("opacity", currentOpacity == 1 ? 0 : 1);
            }

        )

}