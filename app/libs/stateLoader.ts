import { ClientSimulationRequest } from '../types/simulation';
import { download, readSingleFile } from './download';
import { leftToRightCompose } from './func';

export const save = (state: ClientSimulationRequest) => {
  const fileName = 'FIND-Covid-Scenarios.json';
  const mediaType = 'application/json';
  const data = JSON.stringify(state);
  download(fileName, mediaType, data);
};

export const load = async (e: Event) => {
  const file = (await readSingleFile(e)) as string;
  return JSON.parse(file) as ClientSimulationRequest;
};

export const decodeClientState = (stateString: string) =>
  leftToRightCompose<ClientSimulationRequest, string>([
    decodeURIComponent,
    atob,
    JSON.parse,
  ])(stateString);

export const encodeClientState = (state: ClientSimulationRequest) =>
  leftToRightCompose<string, ClientSimulationRequest>([
    JSON.stringify,
    btoa,
    encodeURIComponent,
  ])(state);
