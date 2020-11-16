const apiURL = process.env.API_URL || '/api';

// Where to look for the API
export const apiBase =
  process.env.NODE_ENV === 'production' ? apiURL : 'http://localhost:5000/api';

// How many scenarios are supported in the UI
export const MAX_SCENARIOS_COUNT = 3;

// How many phases are supported per scenario
export const MAX_PHASE_COUNT = 3;

export const GRAPH_PATTERNS_LIST = [
  'line-vertical',
  'line',
  'dash',
  'diagonal',
];
