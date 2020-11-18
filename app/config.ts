import colors from './colors';

const apiURL = process.env.API_URL || '/api';

// Where to look for the API
export const apiBase =
  process.env.NODE_ENV === 'production' ? apiURL : 'http://localhost:5000/api';

// How many scenarios are supported in the UI
export const MAX_SCENARIOS_COUNT = 4;

// How many phases are supported per scenario
export const MAX_PHASE_COUNT = 3;

// The types of patterns assigned to each scenario by index
// https://www.npmjs.com/package/patternomaly
export const GRAPH_PATTERNS_LIST = [
  'line-vertical',
  'line',
  'dash',
  'diagonal',
];

// Labels for Scenarios
export const DEFAULT_SCENARIO_LABELS = [
  'No testing',
  'High contact groups first',
  'Symptomatic first',
  'Open public testing',
];

export const COLORS_BY_SCENARIO_INDEX = [
  colors.pomegranate,
  colors.blueGray,
  colors.turqouise,
  colors.aubergine,
];

export const UNSELECTED_COLOR_ALPHA = 0.2;
export const SELECTED_COLOR_ALPHA = 0.5;
