import React from "react";
import { useD3 } from "./hooks/useD3";
import * as d3 from "d3";

const Pagerank = ({ nodes }) => {
  const ref = useD3(
    (svg) => {
      const height = 600
      const width = 600

      svg.selectAll("*").remove();
      const simulation = d3
        .forceSimulation(nodes)
        .force("x", d3.forceX().x((d) => d.x))
        .force("y", d3.forceY().y((d) => d.y))
        .force("charge", d3.forceManyBody().strength(100))
        .force("center", d3.forceCenter(width/2, height/2))
        .force("collide", d3.forceCollide().radius((d) => d.rank * 1500))

      const node = svg
        .append("g")
        .attr("stroke", "#fff")
        .attr("stroke-width", 1.5)
        .selectAll("circle")
        .data(nodes)
        .join("circle")
        .attr("r", function (d) { return d.rank * 500 })
        .attr("class", "node")
        .attr("fill", "#ff7701")
        .call(drag(simulation))

      var label = svg
        .selectAll(null)
        .data(nodes)
        .enter()
        .append("text")
        .text(function (d) { return d.name })
        .style("text-anchor", "middle")
        .style("fill", "#1b1c1d")
        .style("font-family", "Arial")
        .attr("font-weight", "700")
        .style("font-size", "10px")

      simulation.on("tick", () => {
        node.attr("cx", (d) => d.x).attr("cy", (d) => d.y)
        label
          .attr("x", function (d) { return d.x })
          .attr("y", function (d) { return d.y - d.rank * 500 - 5 })
      })
    }, [nodes.length]
  );

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
  return (
    <svg
      ref={ref}
      style={{
        height: 600,
        width: 600,
        marginLeft: "4%",
        marginTop: "0px",
        backgroundColor: "#F9F9F9",
        borderRadius: "3px"
      }}
    ></svg>
  )
}

export default Pagerank;