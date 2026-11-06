# 課業學習筆記站

一個以 AGENTS.md 為規則、JSON 為內容、共用模板產生頁面的學習筆記網站。新增筆記不用重寫 HTML。

- 網站：https://Xiangyu911117.github.io/study-notes-lab/
- 專案：https://github.com/Xiangyu911117/study-notes-lab
- AI 協作規則：[AGENTS.md](AGENTS.md)

## 本機使用
需要 Python 3.9 或以上，不需安裝第三方套件。
```sh
python scripts/build.py
python scripts/check.py
python -m http.server 8000 --directory docs
```
瀏覽 http://localhost:8000 。直接開啟 docs/index.html 也能閱讀，但瀏覽器對檔案網址的儲存行為可能不同。

## 如何請 AI 新增一篇筆記
把以下任務交給能讀取此 Repository 的 AI：
> 請先閱讀 AGENTS.md 與現有 content JSON，新增一篇「如何整理閱讀筆記」，slug 使用 reading-notes，分類為學習方法。遵守固定欄位與六章結構，提供示例、檢核答案與實際查閱的來源；不要修改共用版型。建置並檢查連結，最後說明更動檔案與驗收結果。

依規則新增 content JSON，再執行建置與檢查，首頁卡片、文章、前後篇連結會自動更新。不要只改 docs。

## 功能與限制
首頁可依分類與關鍵字篩選；文章提供章節導覽、答案展開與本機勾選記錄。勾選使用 localStorage，不上傳、不跨裝置同步；不提供帳戶或即時 AI 對話。關閉 JavaScript 仍可閱讀全部文章，但搜尋、篩選與保存不運作。

## 發布
在 GitHub Settings → Pages 設定 Deploy from a branch，main /docs。來源與 docs 一起提交。每次修改後執行 build.py、check.py，確認公開網站實際更新。

## AI 協助說明
使用者提出課程作業要求，AI 協助專案選題、AGENTS.md 規則、內容整理、程式、版面、測試與文件。文章屬概念整理或自訂流程，沒有宣稱由使用者獨立撰寫或完成未執行的實驗。外部來源在各篇末尾標示。
