import * as React from 'react';
import API from '../API';
import { APIContext } from '../APIProvider';

export default function useNexusContext(): API {
  const nexus = React.useContext<API>(APIContext);
  return nexus;
}
