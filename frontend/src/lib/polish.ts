/**
 * Conjugates a quantitative noun based on its count.
 */
export function conjugateNumeric(
  count: number,
  singular: string,
  double: string,
  plural: string,
) {
  const countString = count.toString();
  if (count === 1) {
    return `${countString} ${singular}`;
  }
  const remainder = count % 10;
  if (count >= 12 && count <= 14) {
    // Exception for numbers 12, 13 and 14, which are conjugated differently
    return `${countString} ${plural}`;
  }
  const useSuffixB = remainder <= 1 || remainder >= 5;
  return `${countString} ${useSuffixB ? plural : double}`;
}
