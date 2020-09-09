export const replaceAtIndexWithoutMutation: <T>(
  orginalArray: T[],
  replaceElement: T,
  indexToReplace: number,
) => T[] = (orginalArray, replaceElement, indexToReplace) =>
  orginalArray.reduce(
    (memo, element, index) => [
      ...memo,
      index === indexToReplace ? replaceElement : element,
    ],
    [],
  );

export const removeAtIndexWithoutMutation: <T>(
  orginalArray: T[],
  indexToRemove: number,
) => T[] = (orginalArray, indexToRemove) =>
  orginalArray.reduce(
    (memo, element, index) =>
      index === indexToRemove ? memo : [...memo, element],
    [],
  );
