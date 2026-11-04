# YCO IAP Popup — Proposal B (RWD)

YouCam Online Editor 首頁的 IAP 訂閱彈窗 prototype（老闆選定的 B 版），含 RWD。

- 背景：yce.perfectcorp.com 首頁的靜態快照（圖片與 CSS 直接引用官網），header 改為登入後樣式
- 觸發：header 的 **Subscribe**（手機版為橘色皇冠）
- 斷點
  - `≥ 900px` 桌機：兩欄 modal（方案 + What's Included）
  - `600–899px` 平板：單欄置中 modal，CTA 固定底部
  - `< 600px` 手機：bottom sheet，可拖曳把手下滑關閉
- `assets/`：官網 icon 字型的本地副本（官網 CDN 不允許跨網域載入字型）

## 本機預覽

```bash
python3 -m http.server 8765
```

開啟 http://localhost:8765/
