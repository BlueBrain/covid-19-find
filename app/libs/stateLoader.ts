import { ClientSimulationRequest } from '../types/simulation';
import { download, readSingleFile } from './download';

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
