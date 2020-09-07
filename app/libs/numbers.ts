export const roundAccurately = (number: number, decimalPlaces: number) =>
  Number(
    Math.round(Number(`${number}e${decimalPlaces}`)) + `e-${decimalPlaces}`,
  );
