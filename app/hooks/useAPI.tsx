import * as React from 'react';
import API from '../API';
import { APIContext } from '../APIProvider';

export default function useAPIContext(): API {
  const api = React.useContext<API>(APIContext);
  return api;
}
