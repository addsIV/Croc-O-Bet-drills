import { API_BASE } from '../src/config';
import { HistoryItem } from '../types';

/**
 * 回報一局結果給後端做對帳。fire-and-forget，失敗不影響遊戲。
 */
export function reportRound(item: HistoryItem): void {
  fetch(`${API_BASE}/api/round`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(item),
    keepalive: true,
  }).catch(() => {
    /* 對帳失敗交給後端 reconcile job */
  });
}
