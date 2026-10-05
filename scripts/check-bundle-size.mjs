// 簡單的 bundle 預算檢查：dist/assets 底下所有 js 加總不得超過預算
import { readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const BUDGET_KB = Number(process.env.BUNDLE_BUDGET_KB ?? 300);
const dir = 'dist/assets';
let total = 0;
for (const f of readdirSync(dir)) {
  if (!f.endsWith('.js')) continue;
  const kb = statSync(join(dir, f)).size / 1024;
  total += kb;
  console.log(`${f.padEnd(40)} ${kb.toFixed(1).padStart(8)} kB`);
}
console.log(`${'TOTAL'.padEnd(40)} ${total.toFixed(1).padStart(8)} kB  (budget ${BUDGET_KB} kB)`);
if (total > BUDGET_KB) {
  console.error(`❌ bundle over budget by ${(total - BUDGET_KB).toFixed(1)} kB`);
  process.exit(1);
}
