import * as React from 'react';
import * as queryString from 'query-string';

export type Parser = {
  [key: string]: {
    parse: (entry: string) => any;
    stringify: (entry: any) => string;
  };
};

export default function useQueryString<T extends object>(
  defaultObject: T,
  parsers?: Parser,
) {
  const parseURLParams = (params: string): T | null => {
    const parsedParams = queryString.parse(params);
    if (!Object.keys(parsedParams).length) {
      return null;
    }
    return Object.keys(parsedParams).reduce<T>((memo, key) => {
      const parsedMemo = { ...memo };
      if (parsers && parsers[key]) {
        parsedMemo[key] = parsers[key].parse(memo[key]);
      }
      return parsedMemo;
    }, parsedParams as T);
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

  const setQueryString = (newQueryParams: T) => {
    history.pushState(
      null,
      null,
      `${location.pathname}?${stringifyURLParams(newQueryParams)}`,
    );
    const myEvent = new Event('popstate');
    window.dispatchEvent(myEvent);
  };

  const [queryParams, setQueryParams] = React.useState<T>(
    parseURLParams(location.search) || defaultObject,
  );

  const listenToPopstate = () => {
    setQueryParams(parseURLParams(location.search) || defaultObject);
  };

  React.useEffect(() => {
    window.addEventListener('popstate', listenToPopstate);
    return () => {
      window.removeEventListener('popstate', listenToPopstate);
    };
  });

  return [queryParams, setQueryString] as [T, (newParams: T) => void];
}
