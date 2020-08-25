import * as React from 'react';
import * as queryString from 'query-string';

export type QueryParams = {
  [key: string]: any;
};

export type Parser = {
  [key: string]: {
    parse: (entry: any) => any;
    stringify: (entry: any) => string;
  };
};

export default function useQueryString(parsers?: Parser) {
  const parseURLParams = (params: string) => {
    const parsedParams = queryString.parse(params);
    return Object.keys(parsedParams).reduce((memo, key) => {
      if (parsers && parsers[key]) {
        memo[key] = parsers[key].parse(memo[key]);
      }
      return memo;
    }, parsedParams);
  };

  const stringifyURLParams = (newParams: any) => {
    const convertedParams = Object.keys(newParams).reduce((memo, key) => {
      if (parsers && parsers[key]) {
        memo[key] = parsers[key].stringify(memo[key]);
      }
      return memo;
    }, newParams);
    return queryString.stringify(convertedParams, {
      skipNull: true,
    });
  };

  const [queryParams, setQueryParams] = React.useState(
    parseURLParams(location.search) || {},
  );

  const setQueryString = (newQueryParams: QueryParams) => {
    history.pushState(
      null,
      null,
      `${location.pathname}?${stringifyURLParams(newQueryParams)}`,
    );
    const myEvent = new Event('popstate');
    window.dispatchEvent(myEvent);
  };

  const listenToPopstate = () => {
    setQueryParams(parseURLParams(location.search) || {});
  };

  React.useEffect(() => {
    window.addEventListener('popstate', listenToPopstate);
    return () => {
      window.removeEventListener('popstate', listenToPopstate);
    };
  });

  return [queryParams, setQueryString] as [
    QueryParams,
    (newQueryParams: QueryParams) => void,
  ];
}
