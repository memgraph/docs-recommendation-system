import React from "react";
import { useD3 } from "./hooks/useD3";
import * as d3 from "d3";

const Graph = ({ nodesData, linksData }) => {

  const nodes = nodesData
  const links = linksData

  const ref = useD3(
    (svg) => {
      const height = 550
      const width = 600

      svg.selectAll("*").remove();
      const simulation = d3
        .forceSimulation(nodes)
        .force("link", d3.forceLink(links).distance(100).id((d) => d.id))
        .force("charge", d3.forceManyBody().strength(-200))
        .force("center", d3.forceCenter(width/2, height/2))

      const link = svg
        .append("g")
        .attr("stroke", "#999")
        .attr("stroke-opacity", 0.6)
        .selectAll("line")
        .data(links)
        .join("line")
        .attr("stroke-width", 1)

      const node = svg
        .append("g")
        .attr("stroke", "#fff")
        .attr("stroke-width", 1.5)
        .selectAll("circle")
        .data(nodes)
        .join("circle")
        .attr("r", function (node) { return 30 - 5*node.depth })
        .attr("class", "node")
        .attr("fill", function (node) {
          if (node.depth === 0) return "#fb6e00"
          else if (node.depth === 1) return "orange"
          return "#f5e042"
        })
        .call(drag(simulation))

      var label = svg
        .selectAll(null)
        .data(nodes)
        .enter()
        .append("text")
        .text(function (d) { return d.id })
        .style("text-anchor", "middle")
        .style("fill", "black")
        .style("font-family", "Arial")
        .attr("font-weight", "550")
        .style("font-size", "12px")

      simulation.on("tick", () => {
        link
          .attr("x1", (d) => d.source.x)
          .attr("y1", (d) => d.source.y)
          .attr("x2", (d) => d.target.x)
          .attr("y2", (d) => d.target.y)

        node.attr("cx", (d) => d.x).attr("cy", (d) => d.y)
        label
          .attr("x", function (d) { return d.x })
          .attr("y", function (d) { return d.y - (30 - d.depth*5) - 3 })
      });
    }, [nodes.length]
  );

  const refEmpty = useD3((svg) => {
    svg.selectAll("*").remove()
    const height = 550
    const width = 600

    var g = svg.append("g").attr("transform", function (d, i) { return "translate(0,0)" })
    g.append("text")
      .attr("x", width/2)
      .attr("y", height/2)
      .attr("fill", "#ff7701")
      .attr("font-weight", "50")
      .text("No data available")
      .style("text-anchor", "middle")
      .style("font-family", "Arial")
      .style("font-size", "20px")
  })

  const drag = (simulation) => {
    function dragstarted(event) {
      if (!event.active) simulation.alphaTarget(0.3).restart()
      event.subject.fx = event.subject.x
      event.subject.fy = event.subject.y
    }

    function dragged(event) {
      event.subject.fx = event.x
      event.subject.fy = event.y
    }

    function dragended(event) {
      if (!event.active) simulation.alphaTarget(0)
      event.subject.fx = null
      event.subject.fy = null
    }

    return d3.drag().on("start", dragstarted).on("drag", dragged).on("end", dragended)
  }
  
  if (nodes.length !== 0) {
    return (
      <svg ref={ref}
           style={{
             height: 550,
             width: 600,
             marginTop: "0px",
             marginLeft: "4%",
             backgroundColor: "#F9F9F9",
             borderRadius: "3px"
            }}>
        </svg>
    )
  } else {
    return (
      <svg ref={refEmpty}
           style={{
             height: 550,
             width: 600,
             marginTop: "0px",
             marginLeft: "4%",
             backgroundColor: "#F9F9F9",
             borderRadius: "3px"
            }}>
      </svg>
    )
  }
}

export default Graph;