# YCO IAP Popup — Pro Plan with More Monthly Credit Options

YouCam Online Editor 首頁的 IAP 訂閱彈窗 prototype（依 PM 文件 p.27），含 RWD。

- 背景：yce.perfectcorp.com 首頁的靜態快照（圖片與 CSS 直接引用官網），header 為登入後樣式
- 觸發：頁面載入時直接打開；關閉後可按 header 的 **Subscribe**（手機版為橘色皇冠）再打開

## 規格對照（p.27）

| # | 項目 | 實作 |
|---|---|---|
| 1 | Monthly / Yearly tab | Yearly 標籤顯示 Pro 方案的最高折扣（目前 60% off）：`1 − 年費 ÷ (月費 × 12)` |
| 2 | Plus / Pro 選項 | Radio card，可鍵盤操作 |
| 3 | 月均價 | Yearly：年費 ÷ 12，劃線為月訂價；Monthly：月訂價 |
| 4 | 年訂閱總價 · 每月點數 | Plus 固定 100；Pro 跟著 slider |
| 5 | Pro 點數 slider | 300 / 800 / 1,500 / 2,500 / 5,000 / 10,000，月均價、年總價、點數同步更新。UI 同 pricing page（藍色軌道＋刻度點、點數 tooltip、開啟時的手指滑動提示） |
| 6 | Check list | Plus 4 項、Pro 7 項（依「Plus/Pro 方案敘述」），Pro 第一列點數跟著 slider |
| 7 | View Full Feature Comparison | 新分頁開 pricing page prototype 的 Subscription tab，並自動捲到 Compare All Plans（`?tab=sub#compare`） |
| 8 | Buy Credits | 新分頁開 pricing page prototype 的 Pay As You Go tab（`?tab=payg`） |

價格依 PM 文件「Pro Plan with more credit pack - Pricing」（YCO Proposal 2，USD），Pro Yearly 預設 300 credits/month（$95.99）：

| | Plus | Pro 300 | 800 | 1,500 | 2,500 | 5,000 | 10,000 |
|---|---|---|---|---|---|---|---|
| Monthly | $9.99 | $19.99 | $34.99 | $59.99 | $89.99 | $164.99 | $319.99 |
| Yearly | $39.99 | $95.99 | $249.99 | $429.99 | $649.99 | $1,199.99 | $2,399.99 |
| Yearly/12 | $3.33 | $7.99 | $20.83 | $35.83 | $54.17 | $99.99 | $199.99 |

方案敘述 Monthly / Yearly 相同；Pro 第一列點數跟著 slider。設定都在 `src/iap-popup.html` 的 script 開頭（`PLUS`、`TIERS`、`LINKS`）。

## 連結

頁面上所有連結都不連正式網站：一律在新分頁開 pricing page prototype（https://pricing-page-optimization.vercel.app/?discount=off）。首頁快照裡指向 perfectcorp.com / youcamapps.com 的連結在 `src/build.py` 建置時統一改寫。

## RWD

- `≥ 900px` 桌機：兩欄（方案 | What's included）
- `600–899px` 平板：單欄置中，CTA 固定底部
- `< 600px` 手機：bottom sheet，可拖曳把手下滑關閉

## 檔案

- `index.html`：建置結果（直接開這個；桌機橘色 Pro + 填色選取，手機 What's included 在下方；Yearly 標籤在 Monthly 時桃紅底、選 Yearly 後淡桃紅底 + 桃紅字，方案卡折扣桃紅底白字）
- `c.html`、`d.html`：舊版本連結，自動轉到 `index.html`
- 節慶主題（預設隱藏，一般網址只會看到 Default；網址加 `?review=1` 才會出現切換器）：右下角切換 Default / Christmas / Year End / Halloween / Black Friday / Golden Week（`?review=1&holiday=christmas` 可直接開某個主題）。目前完成 Christmas、Year End、Halloween、Black Friday（同一套版面，只換主題變數）：桌機右欄換成節慶插畫底 + 倒數 + Flash Sales / UP TO 50% off + 白卡清單；平板、手機在標題下方放橫幅（參考 Figma YCO_Content（Product Pages）舊版節慶 popup）。素材在 `assets/christmas/`、`assets/year-end/`、`assets/halloween/`、`assets/black-friday/`
- `src/iap-popup.html`：彈窗元件（CSS + HTML + JS）
- `src/yce-home-snapshot.html`：官網首頁快照
- `src/build.py`：組合成 `index.html` → `python3 src/build.py`
- `assets/`：官網 icon 字型的本地副本（官網 CDN 不允許跨網域載入字型），以及 slider 用的 `handle-blue.svg`、`coin.svg`、`finger-pointer.svg`（來自 pricing-page-optimization）

## 本機預覽

```bash
python3 -m http.server 8765
```

開啟 http://localhost:8765/
