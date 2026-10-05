# 題 01：上線後一半使用者看到舊版

## 背景

專案部署在 Cloudflare Pages，流程是 PR merge 到 main 就自動 `vite build` 然後上傳 `dist/`。
兩週前同事在 PR #41 把建置設定改了一版，PR 描述寫：「固定產物檔名，方便 CDN 預熱腳本和 QA 回報 bug 時對照檔名，另外補上快取 header 讓 Lighthouse 的 cache policy 項目過關。」那次上線後 Lighthouse 分數確實從 71 升到 93，大家很開心。

今天上線 v1.3.0，改了下注面板的文案和多頭倍率顯示。上線 40 分鐘後客服開始收到回報。

## 證據 A：客服工單摘要

| 工單 | 內容 |
|---|---|
| #1182 | 「你們不是說今天有新版？我看到的還是舊的，Potential Win 那排還是舊字」 |
| #1183 | 「同上，但我手機開無痕就是新的」 |
| #1187 | 「點左下角那個筆的圖示，整頁變白，F12 看到紅字」 |
| #1190 | 「我 Ctrl+Shift+R 以後就好了，但我朋友一直是舊的」 |

## 證據 B：工程師自己重現時的 Network 面板（一般重新整理，非強制）

```
Name                          Status   Type      Size            Time
/                             200      document  (disk cache)    2 ms
assets/index.js               200      script    (disk cache)    1 ms
croc_no_tooth01.png           200      png       (disk cache)    3 ms
assets/CrocodileAssembler.js  200      script    5.6 kB          187 ms
```

`/` 的 Response Headers：

```
cache-control: public, max-age=31536000, immutable
content-type: text/html; charset=utf-8
cf-cache-status: HIT
age: 1203844
```

## 證據 C：#1187 使用者的 Console 錯誤

```
Uncaught TypeError: Cannot read properties of undefined (reading 'teeth')
    at CrocodileAssembler.js:1:2211
```

## 證據 D：部署紀錄

```
[deploy] v1.3.0  dist/index.html 1.6 kB  dist/assets/index.js 218.5 kB  dist/assets/CrocodileAssembler.js 5.6 kB
[deploy] v1.2.4  dist/index.html 1.6 kB  dist/assets/index.js 217.9 kB  dist/assets/CrocodileAssembler.js 5.4 kB
[deploy] purge cache: skipped (no CDN token configured)
```

## 你的任務

照 README 的模板在 `drills/week1/answers/01.md` 作答。
特別要回答：為什麼 #1183 無痕是新的、#1190 強制重整就好，而其他人一直是舊的？為什麼 #1187 會白屏而不是單純看到舊版？
修法要考慮：改完之後「下一次」上線會不會還有一批人卡在舊版？
