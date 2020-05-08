const apiURL = process.env.API_URL || '/api';

export const apiBase =
  process.env.NODE_ENV === 'production' ? apiURL : 'http://localhost:5000/api';
