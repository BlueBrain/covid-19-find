export function toLetters(num: number): string {
  const mod = num % 26;
  let pow = (num / 26) | 0;
  const out = mod ? String.fromCharCode(64 + mod) : (--pow, 'Z');
  return pow ? toLetters(pow) + out : out;
}

export function truncate(input: string, maxLength: number) {
  if (input.length > maxLength) {
    return input.substring(0, maxLength) + '...';
  }
  return input;
}
