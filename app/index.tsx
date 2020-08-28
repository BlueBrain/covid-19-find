import React from 'react';
import ReactDOM from 'react-dom';

import API from './API';
import APIProvider from './APIProvider';
import App from './App';
import enableAnalytics from './libs/analytics';
import MainLayout from './layouts/MainLayout';

const api = new API();

enableAnalytics();

ReactDOM.render(
  <MainLayout>
    <APIProvider api={api}>
      <App />
    </APIProvider>
  </MainLayout>,
  document.getElementById('app'),
);
