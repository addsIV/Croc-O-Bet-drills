# 題 03：PR preview 看得到介面，鱷魚永遠不出現

## 背景

團隊剛導入 PR preview：每開一個 PR，`.github/workflows/preview.yml` 會把 build 結果發佈到 GitHub Pages 的 `pr-<編號>/` 子目錄，然後在 PR 留言貼網址給設計師和 QA 看。
PR #7 是設計師要求的鱷魚陰影調整。工程師本機 `npm run dev` 看起來完全正確，截圖貼在 PR 裡。

設計師打開 preview 網址後回報：「左邊面板、倍率、歷史都在，中間鱷魚那塊是空的，什麼都沒有。」

## 證據 A：設計師那邊的 Console

```
GET https://kevin.github.io/index.css                       404
GET https://kevin.github.io/croc_no_tooth01.png             404
GET https://kevin.github.io/teeth_refined/tooth_00.png      404
GET https://kevin.github.io/teeth_refined/tooth_01.png      404
... (共 21 個 404)
Failed to load /croc_no_tooth01.png
cdn.tailwindcss.com should not be used in production. To use Tailwind CSS in production, install it as a PostCSS plugin or use the Tailwind CLI
```

## 證據 B：工程師本機 `npm run dev` 的 Console

```
GET http://localhost:3000/index.css                          404
cdn.tailwindcss.com should not be used in production. To use Tailwind CSS in production, install it as a PostCSS plugin or use the Tailwind CLI
```

工程師說：「本機也有 404 和 tailwind 警告啊，一直都這樣，不影響。」

## 證據 C：preview 的 `index.html` 原始碼節錄

```html
<link rel="stylesheet" href="/index.css">
...
<script type="module" crossorigin src="/Croc-O-Bet-drills/pr-7/assets/index-BI3Cyjsf.js"></script>
```

## 證據 D：GitHub Actions 的 build log

```
Run npm run build -- --base=/Croc-O-Bet-drills/pr-7/
vite v6.4.1 building for production...
/index.css doesn't exist at build time, it will remain unchanged to be resolved at runtime
✓ 1709 modules transformed.
dist/index.html                  1.60 kB
dist/assets/index-BI3Cyjsf.js  222.67 kB
```

## 你的任務

照模板在 `drills/week1/answers/03.md` 作答。
特別要回答：
1. 證據 A 裡哪些 404 是這次的問題，哪些是本來就有的雜訊？怎麼分辨？
2. 為什麼 js 的路徑有被改對，圖片的路徑沒有？Vite 是怎麼決定要不要幫你加 base 的？
3. 修法至少要給兩種，說明哪一種適合這個專案。注意 `public/` 底下有 13 MB 的 PNG，其中一張 5.4 MB。
4. 這種「本機對、部署錯」的問題，要加什麼到 CI 才能在 PR 階段就抓到，而不是靠設計師回報？
