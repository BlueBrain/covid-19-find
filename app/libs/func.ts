export function leftToRightCompose<T, I>(functionsArray: Function[]) {
  return (initialValue: I) => {
    return functionsArray.reduce((memo, func) => {
      return func(memo);
    }, initialValue) as T;
  };
}
