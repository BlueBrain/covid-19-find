import React from 'react';
import ReactDOM from 'react-dom';

import API from './API';
import APIProvider from './APIProvider';

import App from './App';

const api = new API();

ReactDOM.render(
  <APIProvider api={api}>
    <App />
  </APIProvider>,
  document.getElementById('app'),
);
