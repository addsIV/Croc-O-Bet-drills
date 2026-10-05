
export type GameStatus = 'BETTING' | 'PLAYING' | 'BITTEN' | 'CASHED_OUT';

export interface HistoryItem {
  id: string;
  time: string;
  bet: number;
  multiplier: number;
  win: number;
  status: 'WIN' | 'LOSS';
}

export interface GameState {
  balance: number;
  betAmount: number;
  trapCount: number;
  status: GameStatus;
  clickedTeeth: number[];
  trapPositions: number[];
  currentMultiplier: number;
  history: HistoryItem[];
}
