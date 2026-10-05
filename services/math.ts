
import { HOUSE_EDGE, TOTAL_TEETH } from '../constants';

/**
 * Combination formula nCr
 */
function combinations(n: number, r: number): number {
  if (r < 0 || r > n) return 0;
  if (r === 0 || r === n) return 1;
  if (r > n / 2) r = n - r;
  
  let res = 1;
  for (let i = 1; i <= r; i++) {
    res = res * (n - i + 1) / i;
  }
  return res;
}

/**
 * Mines multiplier formula:
 * (Combinations(Total, Clicked) / Combinations(Total - Traps, Clicked)) * (1 - HouseEdge)
 */
export function calculateMultiplier(traps: number, clicked: number): number {
  if (clicked === 0) return 1.0;
  const safeSpots = TOTAL_TEETH - traps;
  if (clicked > safeSpots) return 0;
  
  const totalWays = combinations(TOTAL_TEETH, clicked);
  const safeWays = combinations(safeSpots, clicked);
  
  const rawMultiplier = totalWays / safeWays;
  return Number((rawMultiplier * (1 - HOUSE_EDGE)).toFixed(4));
}

export function generateTraps(count: number): number[] {
  const positions: number[] = [];
  while (positions.length < count) {
    const pos = Math.floor(Math.random() * TOTAL_TEETH);
    if (!positions.includes(pos)) {
      positions.push(pos);
    }
  }
  return positions;
}
