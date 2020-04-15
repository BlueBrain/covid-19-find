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
  };

  React.useEffect(() => {
    setQueryParams(queryString.parse(location.search) || {});
  }, [location.search]);

  return [queryParams, setQueryString] as [
    QueryParams,
    (newQueryParams: QueryParams) => void,
  ];
}
