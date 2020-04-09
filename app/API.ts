import { apiBase } from './config';
import csv from 'csvtojson';

export default class API {
  base: string;
  constructor() {
    this.base = apiBase;
  }

  countries() {
    console.log('countries!', `${this.base}/countries`);
    return fetch(`${this.base}/countries`).then(response => response.json());
  }

  country(countryCode: string) {
    return fetch(`${this.base}/countries/${countryCode}`).then(response =>
      response.json(),
    );
  }

  simulation() {
    return fetch(`${this.base}/simulation`, { method: 'POST' })
      .then(response => response.text())
      .then(string => csv().fromString(string));
  }
}
