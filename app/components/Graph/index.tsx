import * as React from 'react';
import { Button } from 'antd';

import EphysGraph from './Graph';
import { ProcessedTraceData, ZoomRange } from '../../types';

import './graph-viewer.css';

const Graph: React.FunctionComponent<{
  title: string;
  yLabel: string;
  xLabel: string;
  data: ProcessedTraceData['responseData'] | ProcessedTraceData['stimulusData'];
  sweeps: ProcessedTraceData['sweeps'];
  selectedSweep: string | null;
  zoomRange?: ZoomRange;
  onZoom?: (zoomRange: ZoomRange) => void;
  onSeriesHighlight?: (seriesName: string) => void;
}> = ({
  title,
  data,
  sweeps,
  yLabel,
  xLabel,
  zoomRange,
  onZoom,
  selectedSweep,
  onSeriesHighlight, // TODO implement this if we want hover select
}) => {
  const graphDiv = React.useRef<HTMLDivElement>(null);
  const [graph, setGraph] = React.useState<EphysGraph>();

  React.useEffect(() => {
    if (!!graphDiv.current) {
      setGraph(
        new EphysGraph(graphDiv.current, {
          data,
          sweeps,
          yLabel,
          xLabel,
          onZoom,
          defaultSweep: selectedSweep,
        })
      );
    }
    return () => {
      graph && graph.destroy();
    };
  }, [graphDiv]);

  // set selected sweep
  React.useEffect(() => {
    if (graph) {
      if (selectedSweep) {
        graph.setSweepSelection(selectedSweep);
      } else {
        graph.clearSweepSelection();
      }
    }
  }, [selectedSweep]);

  // reset zoom
  React.useEffect(() => {
    if (!!graph && zoomRange) {
      graph.zoomX(zoomRange.x);
    }
  }, [zoomRange, graph]);

  return (
    <div className="graph-viewer">
      <h2 className="header">{title}</h2>
      <div className="toolbar">
        <Button
          size="small"
          onClick={() => {
            graph && graph.resetZoom();
          }}
        >
          Reset Zoom
        </Button>
      </div>
      <div className="wrapper">
        <div className="graph" ref={graphDiv} />
      </div>
    </div>
  );
};

export default Graph;
