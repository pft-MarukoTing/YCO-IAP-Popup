# YCO IAP Popup — Pro Plan with More Monthly Credit Options

YouCam Online Editor 首頁的 IAP 訂閱彈窗 prototype（依 PM 文件 p.27），含 RWD。

- 背景：yce.perfectcorp.com 首頁的靜態快照（圖片與 CSS 直接引用官網），header 為登入後樣式
- 觸發：header 的 **Subscribe**（手機版為橘色皇冠）

## 規格對照（p.27）

| # | 項目 | 實作 |
|---|---|---|
| 1 | Monthly / Yearly tab | Yearly 標籤顯示所有方案中最高折扣：`1 − 年費 ÷ (月費 × 12)` |
| 2 | Plus / Pro 選項 | Radio card，可鍵盤操作 |
| 3 | 月均價 | Yearly：年費 ÷ 12，劃線為月訂價；Monthly：月訂價 |
| 4 | 年訂閱總價 · 每月點數 | Plus 固定 100；Pro 跟著 slider |
| 5 | Pro 點數 slider | 300 / 800 / 1,500 / 2,500 / 5,000 / 10,000，月均價、年總價、點數同步更新 |
| 6 | Check list | Pro 與 Plus 各一組，第一列點數跟著方案 |
| 7 | View Full Feature Comparison | 開 Pricing Page — Subscription tab |
| 8 | Buy Credits | 開 Pricing Page — Pay as you go tab |

價格與 tier 取自 pricing page prototype（`discount=off`，USD）。設定都在 `src/iap-popup.html` 的 script 開頭（`PLUS`、`TIERS`、`LINKS`）。

## RWD

- `≥ 900px` 桌機：兩欄（方案 | What's included）
- `600–899px` 平板：單欄置中，CTA 固定底部
- `< 600px` 手機：bottom sheet，可拖曳把手下滑關閉

## 檔案

- `index.html`：建置結果（直接開這個）
- `src/iap-popup.html`：彈窗元件（CSS + HTML + JS）
- `src/yce-home-snapshot.html`：官網首頁快照
- `src/build.py`：組合成 `index.html` → `python3 src/build.py`
- `assets/`：官網 icon 字型的本地副本（官網 CDN 不允許跨網域載入字型）

## 本機預覽

```bash
python3 -m http.server 8765
```

開啟 http://localhost:8765/
