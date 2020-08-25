import * as React from 'react';
import TrendArrow from './TrendArrow';

import './trend-indicator';

const DEFAULT_TREND_DIFF = 3;

export enum TREND {
  UP = 'UP',
  STABLE = 'STABLE',
  DOWN = 'DOWN',
}

export const calcPercentageChange = (previous: number, present: number) => {
  const difference = present - previous;
  return (difference / previous) * 100;
};

export const calcIndicatorRotationDeg = (x: number) => {
  return (-90 / Math.PI) * 2 * Math.atan(x / 50);
};

const TrendIndicator: React.FC<{
  previous: number;
  present: number;
  upIsGood?: boolean;
}> = ({ previous, present, upIsGood = true }) => {
  const percentageChange = calcPercentageChange(previous, present);
  const trendStatus =
    percentageChange > DEFAULT_TREND_DIFF
      ? TREND.UP
      : percentageChange < -DEFAULT_TREND_DIFF
      ? TREND.DOWN
      : TREND.STABLE;

  const indicatorRotationDeg = calcIndicatorRotationDeg(percentageChange);

  return (
    <span
      className={`trend-indicator ${trendStatus.toLocaleLowerCase()} ${
        upIsGood ? 'good' : 'bad'
      }`}
    >
      {trendStatus === TREND.DOWN ? '-' : trendStatus === TREND.UP ? '+' : ''}
      {percentageChange.toFixed(0)}%{' '}
      <TrendArrow rotation={indicatorRotationDeg} />
    </span>
  );
};

export default TrendIndicator;
