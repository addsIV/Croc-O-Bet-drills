# 題 02：本機正常、staging 正常、production 打錯 API

## 背景

這次新增了「每局結束回報後端對帳」的功能，程式碼在 `services/api.ts`，設定集中在 `src/config.ts`。
部署流程在 `.github/workflows/deploy.yml`：build 一次產出 artifact，先部署 staging，通過後再部署 production。
Production 的 API 網址是機密，放在 GitHub 的 `production` environment secrets 裡，名字叫 `PROD_API_BASE`。

工程師在本機測過沒問題，staging 的後端也收到對帳資料。上線 production 後，後端說一筆都沒收到。

## 證據 A：三個環境的 Network 面板，各玩一局之後

本機 `npm run dev`：

```
POST http://localhost:8787/api/round        200   (本機有起 mock server)
```

Staging：

```
POST https://api-staging.croc-o-bet.example.com/api/round   200
```

Production：

```
POST http://localhost:8787/api/round        (failed) net::ERR_CONNECTION_REFUSED
```

## 證據 B：工程師的說法

> 「我有在 workflow 裡設 `VITE_API_BASE: ${{ secrets.PROD_API_BASE }}` 啊，而且我去 GitHub 的 environment 看 secret 是有值的。是不是 secret 沒權限？」

## 證據 C：GitHub Actions 的 production job log 節錄

```
Run aws s3 sync dist/ s3://croc-o-bet-prod --delete
  env:
    AWS_ACCESS_KEY_ID: ***
    AWS_SECRET_ACCESS_KEY: ***
    VITE_API_BASE: ***
upload: dist/index.html to s3://croc-o-bet-prod/index.html
upload: dist/assets/index-BI3Cyjsf.js to s3://croc-o-bet-prod/assets/index-BI3Cyjsf.js
```

## 證據 D：有人在 production 的 bundle 裡搜了一下

```
$ curl -s https://play.croc-o-bet.example.com/assets/index-BI3Cyjsf.js | grep -o 'localhost:8787' | head -1
localhost:8787
```

## 你的任務

照模板在 `drills/week1/answers/02.md` 作答。
特別要回答：
1. 為什麼 staging 對、production 錯，兩者的 build 差在哪裡？
2. 證據 C 顯示 secret 有被注入（有 `***`），為什麼還是沒用？
3. 這套流程「build 一次、部署多次」的想法本身對不對？如果對，應該怎麼改才能同時保住這個想法？
4. 本機能跑是因為什麼？這個設計在 production 出事時是幫了忙還是害了事？
