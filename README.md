# MateriaRadar · 原料海巡雷達 公開更新通道

提供 **0.3.20** 完整版安裝檔、可攜版、完整資料庫及版本核對資訊。
使用者下載與程式內「檢查最新版本」均不需 GitHub 登入、存取權杖或 Python。

- [最新完整安裝版與所有下載](https://github.com/applehitmyhead-svg/MateriaRadar-Updates/releases/latest)
- [最新版本資訊 latest.json](https://github.com/applehitmyhead-svg/MateriaRadar-Updates/releases/latest/download/latest.json)
- [0.3.20 Windows x64 完整版安裝檔](https://github.com/applehitmyhead-svg/MateriaRadar-Updates/releases/download/v0.3.20/MateriaRadar-0.3.20-windows-x64-setup.exe)

第一次請下載安裝此通道提供的新版。之後在設定按「檢查最新版本」，
程式會檢查公開版本資訊，有更新即下載、核對 SHA-256、顯示進度並開啟安裝。
目前版本相符時顯示「已是最新版本」。升級沿用使用者資料庫、設定與 Excel 輸出。

## 完整版內容

Windows x64 安裝檔包含完整歷史資料與修訂，以及同一資料快照產生的七本產業明細及價格總表。
Excel 副本位於安裝目錄的 Excel 資料夾。另提供資料庫快照與 manifest，可獨立核對及匯入。
各商品的報價日期按原始來源保留；版本資訊中的資料取得時間不代表全部商品同日報價。

## 開源通道工具

tools/generate_manifest.py 僅使用 Python 標準函式庫，依已通過驗證的發行檔案
產生 latest.json，核對 SHA256SUMS、建置 ID、版本與安裝檔。
通道工具及 schema 依本庫 MIT LICENSE 開放；安裝檔、第三方依賴及報價資料沿用各自授權與來源條件。

~~~text
python tools/generate_manifest.py --release-dir path/to/verified-release
~~~

同一產品版本重新封裝時，以不同建置 ID 和 UTC 建立時間識別，避免重複安裝或降版。
重新發佈可使用 --tag v0.3.20-build.YYYYMMDD.BUILD_ID；產品版本仍為 0.3.20。

維護者先上傳安裝檔、資料庫與驗證資訊到草稿 Release，
核對檔案後再上傳相符的 latest.json 並發佈。不要手動修改校驗碼或將不同建置的檔案混用。
終端用戶無需授權；維護者上傳仍使用自己的 GitHub 登入，授權不隨安裝檔散布。
