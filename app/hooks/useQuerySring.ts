import * as React from 'react';
import * as queryString from 'query-string';
export type QueryParams = {
  [key: string]: any;
};

export default function useQueryString() {
  const [queryParams, setQueryParams] = React.useState(
    queryString.parse(location.search) || {},
  );

  const setQueryString = (newQueryParams: QueryParams) => {
    history.pushState(
      null,
      null,
      `${location.pathname}?${queryString.stringify(newQueryParams, {
        skipNull: true,
      })}`,
    );
    let myEvent = new Event('popstate');
    window.dispatchEvent(myEvent);
  };

  const listenToPopstate = () => {
    setQueryParams(queryString.parse(location.search) || {});
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
