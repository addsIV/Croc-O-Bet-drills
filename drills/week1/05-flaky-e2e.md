# 題 05：E2E 本機 5 次全過，CI 10 次掛 3 次

## 背景

這週導入 Playwright，測試在 `e2e/game.spec.ts`，設定在 `playwright.config.ts`，CI 在 `.github/workflows/e2e.yml`。
寫測試的同事在 M3 MacBook 上連跑 5 次全綠。PR 開出來後 CI 掛了，re-run 又過了，再 re-run 又掛。
同事的提議：「CI 機器比較慢，我把 `retries` 設 2，`timeout` 拉到 60 秒就好了。」

## 證據 A：CI 連續 10 次 re-run 的結果

| Run | 結果 | 失敗的測試 | 錯誤訊息 |
|---|---|---|---|
| 1 | ✅ | | |
| 2 | ❌ | place a bet, press a tooth and cash out | `expect(locator).toBeEnabled()` failed. Locator: getByRole('button', { name: /CASH OUT/ }). Expected: enabled. Received: disabled. Timeout 5000ms |
| 3 | ✅ | | |
| 4 | ✅ | | |
| 5 | ❌ | place a bet, press a tooth and cash out | `expect(locator).toBeEnabled()` failed. Locator: getByRole('button', { name: /CASH OUT/ }). Error: element(s) not found. Found button "NEW GAME" instead. Timeout 5000ms |
| 6 | ✅ | | |
| 7 | ✅ | | |
| 8 | ❌ | place a bet, press a tooth and cash out | `expect(locator).toBeEnabled()` failed. Received: disabled. Timeout 5000ms |
| 9 | ✅ | | |
| 10 | ✅ | | |

第二個測試 `balance is deducted when betting` 10 次全過。

## 證據 B：Run 2 失敗時的 trace 截圖描述

- BET NOW 已經變成 CASH OUT，但按鈕是灰的。
- 鱷魚區域是**空白的**，沒有底圖也沒有牙齒。
- Network 面板顯示 `croc_no_tooth01.png` 5.4 MB 還在 pending。

## 證據 C：Run 5 失敗時的 trace 截圖描述

- 鱷魚有畫出來，牙齒 4 的位置變暗，鱷魚嘴上有紅色 X 的 overlay。
- 按鈕顯示 NEW GAME。
- 歷史側欄多了一筆紅色 LOSS。

## 證據 D：CI runner 規格與本機差異

```
CI:    ubuntu-latest, 2 vCPU, 7 GB RAM, 磁碟冷啟動，每次都重新 build 與下載 Chromium
本機:  M3, 8 核, 圖片已在瀏覽器快取, preview server 一直開著 (reuseExistingServer)
```

## 你的任務

照模板在 `drills/week1/answers/05.md` 作答。
特別要回答：
1. Run 2 和 Run 5 的錯誤訊息不一樣，它們是同一個根因還是兩個？分別是什麼？
2. 兩個根因裡，哪一個不管機器多快都會隨機出現？出現機率大概多少？怎麼算的？
3. 「retries 2 加 timeout 60 秒」能解決哪個、不能解決哪個？長期會付出什麼代價？
4. 修法：測試該怎麼寫才確定？如果要動到產品程式碼，動在哪裡最合理？這和博弈產品本來就有的 provably fair 機制有沒有關係？
5. `workers: 4` 跑在 2 vCPU 上合不合理？它會讓哪一類問題更嚴重？
