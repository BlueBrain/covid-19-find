import React from 'react';
import ReactDOM from 'react-dom';

import Analytics from 'analytics';
import googleTagManager from '@analytics/google-tag-manager';

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

// TODO: move GTM code to env var at build-time
const gtmCode = 'GTM-5J49535';

if (gtmCode) {
  const analytics = Analytics({
    app: 'awesome-app',
    plugins: [
      googleTagManager({
        containerId: gtmCode,
      }),
    ],
  });

  analytics.page();
}
