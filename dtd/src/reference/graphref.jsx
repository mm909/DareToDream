
import React, { useContext, useEffect } from 'react'

import { FlightDataContext } from '../modules/contexts/flightdata'

function Introduction() {
  const { flightDataReport } = useContext(FlightDataContext);

  // Formating Data
  const sample_data = flightDataReport['airport_visits']
  const dataArray = Object.entries(sample_data).map(([key, value]) => ({key, value}));

  useEffect(() => {

    const margin = {top: 20, right: 20, bottom: 20, left: 40};
    const box = {width: 1500, height: 500};
    const width = box.width - margin.left - margin.right;
    const height = box.height - margin.top - margin.bottom;

    // Clear the svg
    d3.select("#sample").select('svg').remove();

    // Create the svg and size it
    let svg = d3.select("#sample").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)

    // Create the graph element
    let g = svg.append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    let x = d3.scaleBand()
      .rangeRound([0, width])
      .padding(0.1)
      .domain(dataArray.map(function(d) { return d.key; }));

    let y = d3.scaleLinear()
      .rangeRound([height, 0])
      .domain([0, d3.max(dataArray, function(d) { return d.value; })]);

    g.append('g')
      .attr('transform', 'translate(0,' + height + ')')
      .call(d3.axisBottom(x));

    g.append('g')
      .call(d3.axisLeft(y));

    g.selectAll('.bar')
      .data(dataArray)
      .enter().append('rect')
        .attr('class', 'bar')
        .attr('x', function(d) { return x(d.key); })
        .attr('y', function(d) { return y(d.value); })
        .attr('width', x.bandwidth())
        .attr('height', function(d) { return height - y(d.value); });

  }, [])

  return (
    <>
      <h1>Introduction</h1>
      <div id="sample"></div>
    </>
  )
}

export default Introduction
