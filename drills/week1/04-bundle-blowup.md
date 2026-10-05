# 題 04：一個小 PR 讓 bundle 大了五倍

## 背景

CI 在 `.github/workflows/ci.yml` 有 bundle 預算檢查，上限 300 kB，用 `scripts/check-bundle-size.mjs` 算 `dist/assets/*.js` 總和。
初階同事開了 PR #12，描述如下：

> **feat: 歷史紀錄加狀態徽章**
> 新增 `StatusBadge` 元件顯示 WIN / LOSS，icon 用名稱指定，之後 CMS 要換圖示不用改程式碼。
> 改動：新增 `components/StatusBadge.tsx`（30 行），`HistorySidebar.tsx` 加 5 行。
> 本機看過正常，截圖如附件。

CI 紅了。同事說：「我只加了 35 行，而且 icon 只用了兩個，為什麼會變這麼大？是不是 CI 的 budget 設太緊？我把它調到 1200 可以嗎？」

## 證據 A：CI log

```
Run npm run build
vite v6.4.1 building for production...
✓ 1715 modules transformed.
dist/index.html                    1.58 kB │ gzip:   0.74 kB
dist/assets/index-BTlHy7LZ.js  1,091.91 kB │ gzip: 230.38 kB
(!) Some chunks are larger than 500 kB after minification. Consider:
- Use build.rollupOptions.output.manualChunks to improve chunking
- Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.

Run node scripts/check-bundle-size.mjs
index-BTlHy7LZ.js                          1066.3 kB
TOTAL                                      1066.3 kB  (budget 300 kB)
❌ bundle over budget by 766.3 kB
Error: Process completed with exit code 1.
```

## 證據 B：main 分支最近一次 build

```
dist/assets/index-BI3Cyjsf.js    222.67 kB │ gzip:  68.99 kB
```

## 證據 C：`npm ls lucide-react`

```
croc-o-bet@0.0.0
└── lucide-react@0.562.0
```

沒有新增任何依賴，`package.json` 沒動。

## 證據 D：同事附的 PR diff 節錄

```ts
import * as Icons from 'lucide-react';
...
const Icon = (Icons as Record<string, React.ComponentType<{ size?: number }>>)[icon] ?? Icons.Circle;
```

## 你的任務

照模板在 `drills/week1/answers/04.md` 作答。
特別要回答：
1. 35 行程式碼為什麼能讓 bundle 多 870 kB？打包工具在做什麼決定，這段程式碼讓它無法做哪個決定？
2. 「icon 用名稱指定，CMS 可以換」這個需求本身合理嗎？如果合理，怎麼實作才不會讓 bundle 爆掉？給出至少兩種做法與取捨。
3. 你會怎麼回覆同事「把 budget 調到 1200」的提議？要有理由，不是只說不行。
4. 以 code reviewer 的身分，寫出你會在 PR 上留的評論（兩到四句，給初階同事看的語氣）。
5. 除了預算檢查，CI 還能加什麼讓這類問題更早被看到、更容易定位？
