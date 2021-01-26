import { ClientSimulationRequest } from '../types/simulation';
import { download, readSingleFile } from './download';
import { leftToRightCompose } from './func';
import { compress, decompress } from 'compressed-json';

export const save = (state: ClientSimulationRequest) => {
  const fileName = 'FIND-Covid-Scenarios.json';
  const mediaType = 'application/json';
  const data = JSON.stringify(state);
  download(fileName, mediaType, data);
};

export const load = async (e: Event) => {
  const { contents, name } = await readSingleFile(e);
  return {
    name,
    contents: JSON.parse(contents as string) as ClientSimulationRequest,
  };
};

export const decodeClientState = (stateString: string) =>
  leftToRightCompose<ClientSimulationRequest, string>([
    atob,
    decompress.fromString,
  ])(stateString);

export const encodeClientState = (state: ClientSimulationRequest) =>
  leftToRightCompose<string, ClientSimulationRequest>([
    compress.toString,
    btoa,
  ])(state);
