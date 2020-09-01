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
