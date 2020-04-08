import * as d3 from 'd3';
import { flatten } from 'lodash';

import { ProcessedTraceData, ZoomRange } from '../../types';

export type FormattedSweepsData = {
  sweepKey: string;
  data: {
    x: number;
    y: number;
  }[];
  color: string;
}[];

export type MakeGraphOptions = {
  yLabel: string;
  xLabel: string;
  data: ProcessedTraceData['responseData'] | ProcessedTraceData['stimulusData'];
  sweeps: ProcessedTraceData['sweeps'];
  onZoom?: (ranges: ZoomRange) => void;
  defaultSweep?: string | null;
};

class EphysGraph {
  svg: any;
  lines: {
    line: any;
    dataAccess: d3.Line<[number, number]>;
  }[];
  xScale: number[] & d3.ScaleLinear<number, number>;
  yScale: number[] & d3.ScaleLinear<number, number>;
  xAxis: any;
  yAxis: any;
  onZoom?: (zoomRange: ZoomRange) => void;
  xExtent: [undefined, undefined] | [number, number] = [undefined, undefined];
  brush: d3.BrushBehavior<unknown>;
  // TODO what timeout type to use?
  idleTimeout: any | null;
  constructor(graphDiv: HTMLDivElement, options: MakeGraphOptions) {
    const { data, sweeps, yLabel, xLabel, onZoom, defaultSweep } = options;
    this.onZoom = onZoom;

    if (!data.length) {
      throw new Error('No Data');
    }

    // set the dimensions and margins of the graph
    const margin = { top: 10, right: 30, bottom: 30, left: 60 };
    const width = graphDiv.clientWidth - margin.left - margin.right;
    const height = graphDiv.clientHeight - margin.top - margin.bottom;

    // append the svg object to the body of the page
    this.svg = d3
      .select(graphDiv)
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const xData = data.map(series => series[0]);
    const yData = flatten(
      data.map(series => {
        const [head, ...tail] = series;
        return tail;
      })
    );

    const xExtent = (this.xExtent = d3.extent(xData));

    const xScale = (this.xScale = d3
      .scaleLinear()
      // @ts-ignore // TODO: Type problem from D3?
      .domain(xExtent)
      .range([0, width]));

    const xAxis = (this.xAxis = this.svg
      .append('g')
      .attr('transform', `translate(0, ${height})`)
      .call(d3.axisBottom(xScale))).attr('class', 'x-axis axis');

    const xAxisLabel = this.svg
      .append('text')
      .attr('class', 'label')
      .attr('transform', `translate(${margin.left}, ${height + margin.bottom})`)
      .text(xLabel);

    const yScale = (this.yScale = d3
      .scaleLinear()
      // @ts-ignore  // TODO: Type problem from D3?
      .domain(d3.extent(yData))
      .range([height, 0]));

    const yAxis = (this.yAxis = this.svg
      .append('g')
      .call(
        d3
          .axisLeft(yScale)
          .ticks(5)
          // @ts-ignore // TODO: Type problem from d3?
          .tickFormat((d: number) => {
            return d;
          })
          .scale(yScale)
      )
      .attr('class', 'y-axis axis')
      .append('text')
      .attr('class', 'label')
      .attr('transform', `rotate(-90)  translate(${-margin.top}, -50)`)
      .text(yLabel));

    // Add a clipPath: everything out of this area won't be drawn.
    const clip = this.svg
      .append('defs')
      .append('svg:clipPath')
      .attr('id', 'clip')
      .append('svg:rect')
      .attr('width', width)
      .attr('height', height)
      .attr('x', 0)
      .attr('y', 0);

    // Add brushing
    const brush = (this.brush = d3
      .brushX() // Add the brush feature using the d3.brush function
      .extent([
        [0, 0],
        [width, height],
      ]) // initialise the bruszh area: start at 0,0 and finishes at width,height: it means I select the whole graph area
      .on('end', this.updateChart.bind(this))); // Each time the brush selection changes, trigger the 'updateChart' function

    const makeLines = (sweepKey: string, color: string, index: number) => {
      // Create the line variable: where both the line and the brush take place
      const line = this.svg.append('g').attr('clip-path', 'url(#clip)');

      // How to access data in this line?
      const dataAccess = d3
        .line()
        .x(d => {
          return xScale(d[0]);
        })
        .y(d => {
          return yScale(d[index + 1]);
        });

      // Add the line
      line
        .append('path')
        .data([data])
        .attr('class', `line key-${sweepKey}`) // I add the class line to be able to modify this line later on.
        .attr('fill', 'none')
        .attr('stroke', () => {
          return color;
        })
        .attr('stroke-width', 1.5)
        .attr('d', dataAccess);

      return { line, dataAccess };
    };

    const lines = sweeps.map((sweep, index) => {
      const line = makeLines(sweep.sweepKey, sweep.color, index);
      if (index === 0) {
        // Add the brushing
        line.line
          .append('g')
          .attr('class', 'brush')
          .call(brush);
      }
      return line;
    });
    this.lines = lines;

    // If user double click, reinitialize the chart
    this.svg.on('dblclick', () => {
      this.resetZoom();
    });

    // Draw for the first time to initialize.
    const redraw = () => {
      const width = graphDiv.clientWidth - margin.left - margin.right;
      const height = graphDiv.clientHeight - margin.top - margin.bottom;

      this.animateGraphChanges();
    };

    // Redraw based on the new size whenever the browser window is resized.
    window.addEventListener('resize', redraw);

    if (defaultSweep) {
      this.setSweepSelection(defaultSweep);
    }
  }

  updateChart() {
    const xScale = this.xScale;
    const lines = this.lines;
    // What are the selected boundaries?
    const extent = d3.event.selection;

    // If no selection, back to initial coordinate. Otherwise, update X axis domain
    if (!extent) {
      if (!this.idleTimeout) {
        return (this.idleTimeout = setTimeout(() => {
          this.idleTimeout = null;
        }, 350)); // This allows to wait a little bit
      }
      this.resetZoom();
    } else {
      const invertedScale = [
        xScale.invert(extent[0]),
        xScale.invert(extent[1]),
      ];
      xScale.domain(invertedScale);
      this.onZoom &&
        this.onZoom({
          x: [invertedScale[0] || 0, invertedScale[1] || 0],
          y: [0, 0],
        });

      lines.forEach(({ line }) => {
        line.select('.brush').call(this.brush.move, null); // This remove the grey brush area as soon as the selection has been done
      });
      this.animateGraphChanges();
    }
  }

  animateGraphChanges() {
    // Update axis and line position
    this.xAxis
      .transition()
      .duration(1000)
      .call(d3.axisBottom(this.xScale));

    this.lines.forEach(({ line, dataAccess }) => {
      line
        .select('.line')
        .transition()
        .duration(1000)
        .attr('d', dataAccess);
    });
  }

  zoomX(xRange: number[]) {
    this.xScale.domain(xRange);
    this.animateGraphChanges();
  }

  resetZoom() {
    // @ts-ignore TODO: why is this necessary
    this.xScale.domain(this.xExtent);
    this.onZoom &&
      this.onZoom({
        x: [this.xExtent[0] || 0, this.xExtent[1] || 0],
        y: [0, 0],
      });
    this.animateGraphChanges();
  }

  setSweepSelection(sweepKey: string) {
    this.svg
      .selectAll(`.line:not(.key-${sweepKey})`)
      .transition()
      .duration(300)
      .ease(d3.easeLinear)
      .style('opacity', 20 / 100);

    this.svg
      .select(`.key-${sweepKey}`)
      .transition()
      .duration(300)
      .ease(d3.easeLinear)
      .style('opacity', 100);
  }

  clearSweepSelection() {
    this.svg
      .selectAll(`.line`)
      .transition()
      .duration(300)
      .ease(d3.easeLinear)
      .style('opacity', 100);
  }

  destroy() {
    this.svg.remove();
    this.idleTimeout = null;
  }
}

export default EphysGraph;
