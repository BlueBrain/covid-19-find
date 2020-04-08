import * as React from 'react';
import API from './API';

const context = React.createContext(null);
const { Provider } = context;

export const APIContext = context;

const APIProvider: React.FC<{
  api: API;
}> = ({ api, children }) => {
  return <Provider value={api}>{children}</Provider>;
};

export default APIProvider;
